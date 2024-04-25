from aiogram import types
from BaseData.src.queries.orm import most_popular_book, most_popular_author, book_on_reader_year, statistic_for_genre,\
finance_result_for_year
from prettytable import PrettyTable
from datetime import datetime


def report_menu():
    kb = [
        [
            types.KeyboardButton(text="Популярные книги"),
            types.KeyboardButton(text="Популярные авторы"),
            types.KeyboardButton(text="Фин. отчет"),
        ],
        [
            types.KeyboardButton(text="Статистика по жанрам"),
            types.KeyboardButton(text="Книг на человека в год"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def for_most_pop_book(date):
    result_search = most_popular_book(datetime.strptime(date, "%Y.%m.%d"))
    table = PrettyTable()
    table.field_names = ["id", "Название", "Взяли раз"]
    for result in result_search:
        row = [result[0], result[1], result[2]]
        table.add_row(row)
    return [len(result_search), table]


def for_most_pop_author(date):
    result_search = most_popular_author(datetime.strptime(date, "%Y.%m.%d"))
    table = PrettyTable()
    table.field_names = ["id", "ФИО", "Прочитан раз"]
    for result in result_search:
        row = [result[0], result[1], result[2]]
        table.add_row(row)
    return [len(result_search), table]


def for_book_on_reader():
    result_search = book_on_reader_year()
    table = PrettyTable()
    table.field_names = ["ФИО", "Взятые книги за год"]
    for result in result_search:
        row = [result[0], result[1]]
        table.add_row(row)
    return [len(result_search), table]


def for_statistic_genre():
    result_search = statistic_for_genre()
    table = PrettyTable()
    table.field_names = ["Жанр", "Взятые книг с таким жанром"]
    for result in result_search:
        row = [result[0], result[1]]
        table.add_row(row)
    return [len(result_search), table]


def for_fin_report():
    result = finance_result_for_year()
    table = PrettyTable()
    table.field_names = ["Количество книг", "Общая стоимость книг на хранении", "Сумма штрафов"]
    row = [result[0], result[1], result[2]]
    table.add_row(row)
    return [len(result), table]