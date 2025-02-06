import tkinter as tk
from tkinter import ttk
import requests

# Функция для получения курсов валют
def get_rates():
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
        response.raise_for_status()
        data = response.json()
        usd_rate = data["Valute"]["USD"]["Value"]
        eur_rate = data["Valute"]["EUR"]["Value"]
        return usd_rate, eur_rate
    except:
        return None, None

# Функция для конвертации рублей в выбранную валюту
def convert():
    currency = selected_currency.get()
    usd_rate, eur_rate = get_rates()
    if usd_rate is None:
        label_result.config(text="Нет данных с сервера!")
        return
    try:
        rub = float(entry_rub.get())
        if currency == "USD":
            rate = usd_rate
        elif currency == "EUR":
            rate = eur_rate
        elif currency == "CNY":
            rate = eur_rate / 7.5  # Примерный курс юаня
        result = rub / rate
        result_text = f"{result:.2f} {currency}"
        label_result.config(text=result_text)
        # Добавляем запись в историю
        history_text.insert(tk.END, f"{rub} RUB → {result_text}\n")
        history_text.see(tk.END)
    except ValueError:
        label_result.config(text="Введите число!")

# Функция для очистки полей
def clear_fields():
    entry_rub.delete(0, tk.END)  # Очищаем поле ввода
    history_text.delete(1.0, tk.END)  # Очищаем текстовое поле с историей

# Функция для скрытия/показа истории
def toggle_history():
    if history_text.winfo_viewable():  # Если текстовое поле видимо
        history_text.pack_forget()  # Скрываем его
    else:
        history_text.pack(pady=10)  # Показываем его

# Создание окна
window = tk.Tk()
window.title("Конвертер валют")
window.geometry("400x400")

# Поле для ввода рублей
label_rub = tk.Label(window, text="Рубли:")
label_rub.pack()
entry_rub = tk.Entry(window)
entry_rub.pack()

# Установка фокуса на поле ввода
entry_rub.focus()

# Выпадающий список для выбора валюты
currencies = ["USD", "EUR", "CNY"]
selected_currency = tk.StringVar(window)
selected_currency.set(currencies[0])
dropdown = ttk.Combobox(window, textvariable=selected_currency, values=currencies, state="readonly")
dropdown.pack(pady=5)

# Кнопка конвертации
btn_convert = ttk.Button(window, text="Конвертировать", command=convert)
btn_convert.pack(pady=10)

# Поле для результата
label_result = tk.Label(window, text="Результат:")
label_result.pack()

# Кнопка "Очистить"
btn_clear = ttk.Button(window, text="Очистить", command=clear_fields)
btn_clear.pack(pady=5)

# Подсказка о горячих клавишах (разделенная на несколько строк)
label_hint = tk.Label(
    window,
    text="Enter — конвертация\n"
         "Ctrl + Shift + C — очистка\n"
         "Ctrl + H — скрыть/показать историю",
    font=("Arial", 8), fg="gray"
)
label_hint.pack(pady=5)

# Текстовое поле для истории конвертаций (сразу после подсказки)
history_text = tk.Text(window, height=5, width=40)
history_text.pack(pady=10)

# Привязка клавиши Enter к функции convert()
window.bind("<Return>", lambda event: convert())

# Привязка сочетания клавиш Ctrl + Shift + C (латиница и кириллица)
window.bind("<Control-Shift-Key-C>", lambda event: clear_fields())  # Физическая клавиша "C"

# Привязка сочетания клавиш Ctrl + H (латиница и кириллица)
window.bind("<Control-h>", lambda event: toggle_history())  # Физическая клавиша "H"

# Запуск главного цикла
window.mainloop()
