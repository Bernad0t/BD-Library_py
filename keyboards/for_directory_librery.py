from aiogram.types import ReplyKeyboardMarkup
from aiogram import types
from BaseData.src.queries.orm import search_for_name_book, update_fonds, search_for_author,insert_book,\
    search_for_author_name, lose_book
from prettytable import PrettyTable

def work_with_book_from_libr():
    kb = [
        [
            types.KeyboardButton(text="Списать"),
            types.KeyboardButton(text="Пополнить"),
        ],
        [
            types.KeyboardButton(text="Поиск книг"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def upd_founds_keybrd():
    kb = [
        [
            types.KeyboardButton(text="Создать новый фонд"),
        ],
        [
            types.KeyboardButton(text="Пополнить существующий фонд"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def update_old_founds(book_id, number):
    return update_fonds(book_id, number)


def update_new_founds(name, number, genre, price, name_author):
    return insert_book(name, number, genre, price, name_author)


def search_book_kb():
    kb = [
        [
            types.KeyboardButton(text="По автору книги"),
            types.KeyboardButton(text="По названию книги"),
            types.KeyboardButton(text="По автору и названию книги"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def search_for_name_book_answ(book_name):
    result_search = search_for_name_book(book_name)
    table = PrettyTable()
    table.field_names = ["id", "Название", "Жанр", "Количество", "Цена", "Автор"]
    for result in result_search:
        row = [result[0].id, result[0].Название, result[0].Жанр, result[0].Количество, result[0].Цена, result[1]]
        table.add_row(row)
    return [len(result_search), table]


def search_book_for_author_answ(author):
    result_search = search_for_author(author)
    table = PrettyTable()
    table.field_names = ["id", "Название", "Жанр", "Количество", "Цена", "Автор"]
    for result in result_search:
        row = [result[0].id, result[0].Название, result[0].Жанр, result[0].Количество, result[0].Цена, result[1]]
        table.add_row(row)
    return [len(result_search), table]


def search_book_for_author_book_answ(author, book):
    result_search = search_for_author_name(author, book)
    table = PrettyTable()
    table.field_names = ["id", "Название", "Жанр", "Количество", "Цена", "Автор"]
    for result in result_search:
        row = [result[0].id, result[0].Название, result[0].Жанр, result[0].Количество, result[0].Цена, result[1]]
        table.add_row(row)
    return [len(result_search), table]


def for_set_lose_book():
    return lose_book()