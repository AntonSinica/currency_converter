import requests
import tkinter as tk
from tkinter import ttk


def get_rates():
    try:
        # Отправляем GET-запрос к API с таймаутом 5 секунд
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)

        # Проверяем статус ответа HTTP
        response.raise_for_status()

        # Преобразуем ответ в формат JSON
        data = response.json()

        # Извлекаем курсы USD и EUR
        usd_rate = data["Valute"]["USD"]["Value"]
        eur_rate = data["Valute"]["EUR"]["Value"]

        # Возвращаем курсы
        return usd_rate, eur_rate
    except:
        # Если произошла ошибка, возвращаем None для обоих курсов
        return None, None


def convert():
    # Получаем курсы валют
    usd_rate, eur_rate = get_rates()

    # Проверяем, удалось ли получить курсы
    if usd_rate is None:
        label_result.config(text="Нет данных с сервера!")
        return

    try:
        # Получаем введённое значение в рублях
        rub = float(entry_rub.get())

        # Конвертируем рубли в доллары и евро
        usd = rub / usd_rate
        eur = rub / eur_rate

        # Формируем текст результата
        result_text = f"{usd:.2f} USD\n{eur:.2f} EUR"

        # Обновляем метку с результатом
        label_result.config(text=result_text)
    except ValueError:
        # Если введено некорректное значение, показываем сообщение об ошибке
        label_result.config(text="Введите число!")


window = tk.Tk()
window.title("Конвертер валют")
window.geometry("400x200")

# Поле для ввода рублей
label_rub = tk.Label(window, text="Рубли:")
label_rub.pack()
entry_rub = tk.Entry(window)
entry_rub.pack()

# Кнопка конвертации
btn_convert = tk.Button(window, text="Конвертировать")
btn_convert.pack(pady=10)
btn_convert.config(command=convert)

# Поле для результата
label_result = tk.Label(window, text="Результат:")
label_result.pack()

window.mainloop()
