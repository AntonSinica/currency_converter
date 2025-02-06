import tkinter as tk
from tkinter import ttk
import requests


# Класс для работы с API ЦБ РФ
class APIHandler:
    def __init__(self) -> None:
        """Инициализирует URL и таймаут для запросов к API ЦБ РФ."""
        self.url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.timeout: int = 5

    def get_rates(self) -> tuple[float | None, float | None]:
        """
        Получает курсы валют USD и EUR через API ЦБ РФ.
        Возвращает кортеж с курсами (usd_rate, eur_rate) или (None, None) в случае ошибки.
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            usd_rate = data["Valute"]["USD"]["Value"]
            eur_rate = data["Valute"]["EUR"]["Value"]
            return usd_rate, eur_rate
        except:
            return None, None


# Класс для управления историей конвертаций
class HistoryManager:
    def __init__(self, text_widget: tk.Text) -> None:
        """
        Инициализирует менеджер истории с текстовым виджетом для отображения записей.
        """
        self.text_widget: tk.Text = text_widget

    def add_record(self, rub: float, result_text: str) -> None:
        """
        Добавляет запись о конвертации в текстовое поле истории.
        """
        self.text_widget.insert(tk.END, f"{rub} RUB → {result_text}\n")
        self.text_widget.see(tk.END)

    def clear_history(self) -> None:
        """
        Очищает текстовое поле с историей конвертаций.
        """
        self.text_widget.delete(1.0, tk.END)


# Класс для логики конвертации валют
class CurrencyConverter:
    def __init__(self, api_handler: APIHandler) -> None:
        """
        Инициализирует конвертер валют с объектом APIHandler для получения курсов.
        """
        self.api_handler: APIHandler = api_handler

    def convert(self, rub: float, currency: str) -> str | None:
        """
        Конвертирует сумму в рублях в выбранную валюту.
        Возвращает строку с результатом или None в случае ошибки.
        """
        usd_rate, eur_rate = self.api_handler.get_rates()
        if usd_rate is None or eur_rate is None:
            return None

        if currency == "USD":
            rate = usd_rate
        elif currency == "EUR":
            rate = eur_rate
        elif currency == "CNY":
            rate = eur_rate / 7.5  # Примерный курс юаня
        else:
            return None

        result = rub / rate
        return f"{result:.2f} {currency}"


# Класс для графического интерфейса
class GUI:
    def __init__(self, root: tk.Tk, converter: CurrencyConverter) -> None:
        """
        Инициализирует графический интерфейс приложения.
        """
        self.root: tk.Tk = root
        self.converter: CurrencyConverter = converter

        self.root.title("Конвертер валют")
        self.root.geometry("400x400")

        # Создаем текстовое поле для истории
        self.history_text: tk.Text = tk.Text(self.root, height=5, width=40)
        self.history_manager: HistoryManager = HistoryManager(self.history_text)

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Создает и размещает все виджеты интерфейса.
        """
        # Поле для ввода рублей
        label_rub = tk.Label(self.root, text="Рубли:")
        label_rub.pack()
        self.entry_rub = tk.Entry(self.root)
        self.entry_rub.pack()
        self.entry_rub.focus()

        # Выпадающий список для выбора валюты
        currencies = ["USD", "EUR", "CNY"]
        self.selected_currency = tk.StringVar(self.root)
        self.selected_currency.set(currencies[0])
        dropdown = ttk.Combobox(
            self.root, textvariable=self.selected_currency, values=currencies, state="readonly"
        )
        dropdown.pack(pady=5)

        # Кнопка конвертации
        btn_convert = ttk.Button(self.root, text="Конвертировать", command=self.perform_conversion)
        btn_convert.pack(pady=10)

        # Поле для результата
        self.label_result = tk.Label(self.root, text="Результат:")
        self.label_result.pack()

        # Подсказка о горячих клавишах
        label_hint = tk.Label(
            self.root,
            text="Enter — конвертация\n"
                 "Ctrl + Shift + C — очистка\n"
                 "Ctrl + H — скрыть/показать историю",
            font=("Arial", 8), fg="gray"
        )
        label_hint.pack(pady=5)

        # Кнопка "Очистить"
        btn_clear = ttk.Button(self.root, text="Очистить", command=self.clear_fields)
        btn_clear.pack(pady=5)

        # Текстовое поле для истории конвертаций
        self.history_text.pack(pady=10)

        # Горячие клавиши
        self.root.bind("<Return>", lambda event: self.perform_conversion())
        self.root.bind("<Control-Shift-Key-C>", lambda event: self.clear_fields())
        self.root.bind("<Control-h>", lambda event: self.toggle_history())

    def perform_conversion(self) -> None:
        """
        Выполняет конвертацию валюты и обновляет интерфейс.
        """
        try:
            rub = float(self.entry_rub.get())
            currency = self.selected_currency.get()
            result_text = self.converter.convert(rub, currency)
            if result_text is None:
                self.label_result.config(text="Нет данных с сервера!")
            else:
                self.label_result.config(text=result_text)
                self.history_manager.add_record(rub, result_text)
        except ValueError:
            self.label_result.config(text="Введите число!")

    def clear_fields(self) -> None:
        """
        Очищает поле ввода и текстовое поле с историей.
        """
        self.entry_rub.delete(0, tk.END)
        self.history_manager.clear_history()

    def toggle_history(self) -> None:
        """
        Скрывает или показывает текстовое поле с историей конвертаций.
        """
        if self.history_text.winfo_viewable():
            self.history_text.pack_forget()
        else:
            self.history_text.pack(pady=10)


# Основная функция
if __name__ == "__main__":
    root = tk.Tk()
    api_handler = APIHandler()
    converter = CurrencyConverter(api_handler)
    app = GUI(root, converter)
    root.mainloop()
