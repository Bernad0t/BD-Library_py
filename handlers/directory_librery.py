from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.for_questions import menu, librery_menu
from keyboards.for_directory_librery import work_with_book_from_libr, upd_founds_keybrd, update_old_founds,\
update_new_founds, search_book_kb, search_for_name_book_answ, search_book_for_author_answ, search_book_for_author_book_answ,\
for_set_lose_book

router = Router()

@router.message(F.text.lower() == "работа с книгами")
async def answer_librery(message: Message):
    await message.answer(
        "Пространство для работы с книгами",
        reply_markup=work_with_book_from_libr()
    )

@router.message(F.text.lower() == "пополнить")  # [2]
async def cmd_update(message: Message):
    await message.answer(
        "Раздел пополнения",
        reply_markup=upd_founds_keybrd()
    )


class OrderUpdateOld(StatesGroup):
    choosing_book_id = State()
    number = State()


@router.message(F.text.lower() == "пополнить существующий фонд")  # [2]
async def cmd_update_old(message: Message, state: FSMContext):
    await message.answer(
        "Введите id книги",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateOld.choosing_book_id)


@router.message(
    OrderUpdateOld.choosing_book_id,
)
async def chosen_id_book_upd_old(message: Message, state: FSMContext):
    await state.update_data(id_book=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите количество новых экземпляров:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateOld.number)

@router.message(
    OrderUpdateOld.number,
)
async def chosen_id_number_upd_old(message: Message, state: FSMContext):
    await state.update_data(number=int(message.text.lower()))
    user_data = await state.get_data()
    status = update_old_founds(user_data['id_book'], user_data['number'])
    if status == 0:
        await message.answer(
            "Успешно пополнено!",
            reply_markup=menu()
        )
    if status == 1:
        await message.answer(
            "Такого фонда не существует",
            reply_markup=librery_menu()
        )
    await state.clear()


class OrderUpdateNew(StatesGroup):
    name = State()
    number = State()
    genre = State()
    price = State()
    name_author = State()


@router.message(F.text.lower() == "создать новый фонд")  # [2]
async def cmd_crt_new_found(message: Message, state: FSMContext):
    await message.answer(
        "Введите название книги",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateNew.name)


@router.message(
    OrderUpdateNew.name,
)
async def chosen_name_get_upd_new(message: Message, state: FSMContext):
    await state.update_data(name=(message.text))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите количество новых экземпляров:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateNew.number)


@router.message(
    OrderUpdateNew.number,
)
async def chosen_number_upd_new(message: Message, state: FSMContext):
    await state.update_data(number=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите жанр:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateNew.genre)


@router.message(
    OrderUpdateNew.genre,
)
async def chosen_genre_upd_new(message: Message, state: FSMContext):
    await state.update_data(genre=(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите цену:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateNew.price)


@router.message(
    OrderUpdateNew.price,
)
async def chosen_price_upd_new(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите автора:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderUpdateNew.name_author)


@router.message(
    OrderUpdateNew.name_author,
)
async def chosen_author_upd_new(message: Message, state: FSMContext):
    await state.update_data(name_author=(message.text))
    user_data = await state.get_data()
    status = update_new_founds(user_data['name'], user_data['number'], user_data['genre'], user_data['price'],
                               user_data['name_author'])
    if status == 0:
        await message.answer(
            "Успешно создан новый фонд!",
            reply_markup=menu()
        )
    if status == 1:
        await message.answer(
            "Такой фонд уже существует",
            reply_markup=librery_menu()
        )
    await state.clear()


@router.message(F.text.lower() == "поиск книг")
async def answer_search_book(message: Message):
    await message.answer(
        "Выберете, как искать книгу",
        reply_markup=search_book_kb()
    )


class OrderSearchBookBookName(StatesGroup):
    name = State()


@router.message(F.text.lower() == "по названию книги")  # [2]
async def answer_search_book_for_bkname(message: Message, state: FSMContext):
    await message.answer(
        "Введите название книги",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderSearchBookBookName.name)


@router.message(
    OrderSearchBookBookName.name,
)
async def answer_search_book_for_bkname_chosen(message: Message, state: FSMContext):
    result = search_for_name_book_answ(message.text)
    if result[0] == 0:
        await message.answer(
            "Такой книги нет",
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


class OrderSearchBookAuthor(StatesGroup):
    name = State()


@router.message(F.text.lower() == "по автору книги")  # [2]
async def answer_search_book_for_bkname(message: Message, state: FSMContext):
    await message.answer(
        "Введите имя автора",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderSearchBookAuthor.name)


@router.message(
    OrderSearchBookAuthor.name,
)
async def answer_search_book_for_bkauthor_chosen(message: Message, state: FSMContext):
    result = search_book_for_author_answ(message.text)
    if result[0] == 0:
        await message.answer(
            "Такого автора нет",
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


class OrderSearchBookAuthorBook(StatesGroup):
    book_name = State()
    author_name = State()


@router.message(F.text.lower() == "по автору и названию книги")  # [2]
async def answer_search_book_for_book_author(message: Message, state: FSMContext):
    await message.answer(
        "Введите имя автора",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderSearchBookAuthorBook.author_name)


@router.message(
    OrderSearchBookAuthorBook.author_name,
)  # [2]
async def search_book_for_book_author_bk_chosen(message: Message, state: FSMContext):
    await state.update_data(name_author=(message.text))
    await message.answer(
        "Введите название книги",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderSearchBookAuthorBook.book_name)


@router.message(
    OrderSearchBookAuthorBook.book_name,
)
async def search_book_for_book_author_auth_chosen(message: Message, state: FSMContext):
    await state.update_data(book_name=(message.text))
    user_data = await state.get_data()

    result = search_book_for_author_book_answ(user_data['name_author'], user_data['book_name'])
    if result[0] == 0:
        await message.answer(
            "Книги от такого автора нет",
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


@router.message(F.text.lower() == "списать")  # [2]
async def answer_set_lose_book(message: Message, state: FSMContext):
    status = for_set_lose_book()
    if status == 0:
        await message.answer(
            "Списание прошло успешно",
            reply_markup=menu()
        )
    if status == 1:
        await message.answer(
            "Книг для списывания нет",
            reply_markup=menu()
        )