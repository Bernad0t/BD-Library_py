from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.for_questions import menu
from keyboards.for_reports import report_menu, for_most_pop_book, for_most_pop_author, for_book_on_reader, \
    for_statistic_genre, for_fin_report

router = Router()


@router.message(F.text.lower() == "отчеты")
async def answer_report(message: Message):
    await message.answer(
        "Выберите нужный отчет",
        reply_markup=report_menu()
    )

class OrderPopBook(StatesGroup):
    date = State()


@router.message(F.text.lower() == "популярные книги")
async def answer_pop_book(message: Message, state: FSMContext):
    await message.answer(
        'Введите дату в формате "2020.1.23", отсчитывая от которой будет составляться список (топ 5 популярных книг)',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderPopBook.date)


@router.message(
    OrderPopBook.date,
)
async def chosen_pop_book(message: Message, state: FSMContext):
    result = for_most_pop_book(message.text.lower())
    if result[0] == 0:
        await message.answer(
            "Введенная дата была некорректна",
            reply_markup=menu()
        )
        return
    table = result[1]
    await message.answer(
        f"<pre>{table}</pre>",
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )
    await state.clear()


class OrderPopAuthor(StatesGroup):
    date = State()


@router.message(F.text.lower() == "популярные авторы")
async def answer_pop_author(message: Message, state: FSMContext):
    await message.answer(
        'Введите дату в формате "2020.1.23", отсчитывая от которой будет составляться список (топ 5 популярных Авторов)',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderPopAuthor.date)


@router.message(
    OrderPopAuthor.date,
)
async def chosen_date_pop_author(message: Message, state: FSMContext):
    result = for_most_pop_author(message.text.lower())
    if result[0] == 0:
        await message.answer(
            "Введенная дата была некорректна",
            reply_markup=menu()
        )
        return
    table = result[1]
    await message.answer(
        f"<pre>{table}</pre>",
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )
    await state.clear()


@router.message(F.text.lower() == "книг на человека в год")
async def answer_book_on_reader(message: Message):
    result = for_book_on_reader()
    if result[0] == 0:
        await message.answer(
            "Сударь, библиотека пустеет, за год тут не было никого",
            reply_markup=menu()
        )
        return
    table = result[1]
    await message.answer(
        f"<pre>{table}</pre>",
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )


@router.message(F.text.lower() == "статистика по жанрам")
async def answer_statistic_for_genre(message: Message):
    result = for_statistic_genre()
    if result[0] == 0:
        await message.answer(
            "Сударь, библиотека загибается: никто так и не взял ни одной книги",
            reply_markup=menu()
        )
        return
    table = result[1]
    await message.answer(
        f"<pre>{table}</pre>",
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )


@router.message(F.text.lower() == "фин. отчет")
async def answer_finance_report(message: Message):
    result = for_fin_report()
    table = result[1]
    await message.answer(
        f"<pre>{table}</pre>",
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )