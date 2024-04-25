from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup
from aiogram import types
from BaseData.src.queries.orm import create_tables, search_for_name_book, update_fonds, search_for_author, deduction_user,\
refund_cost, book_issuance, book_reception, book_extend, insert_reader, insert_book, search_for_author_name,\
most_popular_book, most_popular_author, book_on_reader_year, create_letter_to_reader, search_reader_for_id, \
    change_date_now, search_list_receipt_to_reader, actions_wth_receipt_to_reader
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
def menu() -> ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Отчеты"),
            types.KeyboardButton(text="Библиотека")
        ],
        [
            types.KeyboardButton(text="Установить дату сейчас"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard

def librery_menu() -> ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Работа с читателями"),
            types.KeyboardButton(text="Работа с книгами")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard

def work_withReader() -> ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Оформить"),
            types.KeyboardButton(text="Отчислить"),
            types.KeyboardButton(text="Операции с книгой")
        ],
        [
            types.KeyboardButton(text="Нарушения")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard

def add_reader(user_name: str):
    insert_reader(user_name)

def delete_reader():
    deduction_user()

def operation_with_book_reader():
    kb = [
        [
            types.KeyboardButton(text="Выдать"),
            types.KeyboardButton(text="Продлить"),
            types.KeyboardButton(text="Принять")
        ],
        [
            types.KeyboardButton(text="Возместить ущерб")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard

def get_book_reader(reader_id, book_id):
    return book_issuance(reader_id, book_id)

def answer_get_id_book_status_0():
    kb = [
        [
            types.KeyboardButton(text="Оформить"),
            types.KeyboardButton(text="главное меню"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def extend_book_reader(reader_id, book_id):
    return book_extend(reader_id, book_id)

def reception_book_reader(reader_id, book_id):
    return book_reception(reader_id, book_id)


def refund_cost_question(reader_id, book_id):
    return refund_cost(reader_id, book_id)


def mistakes_reader_kb():
    kb = [
        [
            types.KeyboardButton(text="Ругательное письмо"),
            types.KeyboardButton(text="Штрафная квитанция"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def seek_reader_for_mistakes(reader_id):
    return search_reader_for_id(reader_id)[0]
def generate_letter():
    result = create_letter_to_reader()
    if len(result) == 0:
        return []
    list_id = [i.Читатель_id for i in result]
    return list_id


def generate_receipt():
    return search_list_receipt_to_reader()


def act_reader_with_receipt(hisory_id):
    return actions_wth_receipt_to_reader(hisory_id)

def for_set_date_now(date):
    if len(date.split('.')) != 3:
        return 1
    change_date_now(datetime.strptime(date, "%Y.%m.%d"))
    return 0
