from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.for_questions import menu, librery_menu, work_withReader, add_reader, delete_reader,\
operation_with_book_reader, get_book_reader, answer_get_id_book_status_0, extend_book_reader, reception_book_reader,\
refund_cost_question, mistakes_reader_kb, generate_letter, seek_reader_for_mistakes, for_set_date_now, generate_receipt,\
act_reader_with_receipt

router = Router()  # [1]

@router.message(F.text.lower() == "библиотека")
async def answer_librery(message: Message):
    await message.answer(
        "Вы в библиотеке",
        reply_markup=librery_menu()
    )


class OrderDate(StatesGroup):
    date = State()


@router.message(F.text.lower() == "установить дату сейчас")
async def answer_set_date_now(message: Message, state: FSMContext):
    await message.answer(
        'Введите дату в формате "2020.1.1"',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderDate.date)

@router.message(
    OrderDate.date,
)
async def chosen_id_reader_get(message: Message, state: FSMContext):
    await state.update_data(date=(message.text.lower()))
    user_data = await state.get_data()
    status = for_set_date_now(user_data['date'])
    if status == 0:
        await message.answer(
            'Дата упешно изменена!',
            reply_markup=menu()
        )
    else:
        await message.answer(
            'Ваша дата некорректна',
            reply_markup=librery_menu()
        )
    await state.clear()

@router.message(F.text.lower() == "работа с читателями")
async def answer_work_with_reader(message: Message):
    await message.answer(
        "работа с читателем",
        reply_markup=work_withReader()
    )


class OrderInsertReader(StatesGroup):
    name = State()


@router.message(F.text.lower() == "оформить")
async def answer_insert_reader(message: Message, state: FSMContext):
    await message.answer(
        "Введите ФИО читатетля, которого хотите оформить",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderInsertReader.name)


@router.message(
    OrderInsertReader.name,
)
async def answer_insert_reader_bd(message: Message, state: FSMContext):
    add_reader(message.text)
    await message.answer(
        "Успех!",
        reply_markup=work_withReader()
    )
    await state.clear()

@router.message(F.text.lower() == "отчислить")
async def answer_delete_reader(message: Message):
    delete_reader()
    await message.answer(
        "Удаление закончено",
        reply_markup=work_withReader()
    )

@router.message(F.text.lower() == "операции с книгой")
async def answer_operation_with_book(message: Message):
    await message.answer(
        "Операции с книгами",
        reply_markup=operation_with_book_reader()
    )

class OrderIssuance(StatesGroup):
    choosing_reader_id = State()
    choosing_book_id = State()

@router.message(F.text.lower() == "выдать")
async def answer_get_book_reader(message: Message, state: FSMContext):
    await message.answer(
        "Введите id читателя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderIssuance.choosing_reader_id)

@router.message(
    OrderIssuance.choosing_reader_id,
)
async def chosen_id_reader_get(message: Message, state: FSMContext):
    await state.update_data(id_reader=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите id книги:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderIssuance.choosing_book_id)

@router.message(
    OrderIssuance.choosing_book_id,
)
async def chosen_id_reader_get(message: Message, state: FSMContext):
    await state.update_data(id_book=int(message.text.lower()))
    user_data = await state.get_data()
    status = get_book_reader(user_data['id_reader'], user_data['id_book'])
    if status == 0:
        await message.answer(
            "Такого читатетля нет. Хотите получить абонимент?",
            reply_markup=answer_get_id_book_status_0()
        )
    if status == 1:
        await message.answer(
            "Такой книги нет",
            reply_markup=operation_with_book_reader()
        )
    if status == 2:
        await message.answer(
            "Этой книги нет в наличии",
            reply_markup=operation_with_book_reader()
        )
    if status == 3:
        await message.answer(
            "Этот пользователь уже взял эту книгу",
            reply_markup=menu()
        )
    if status == 4:
        await message.answer(
            "Успешно оформлено!",
            reply_markup=menu()
        )
    await state.clear()

class OrderExtend(StatesGroup):
    choosing_reader_id = State()
    choosing_book_id = State()

@router.message(F.text.lower() == "продлить")
async def answer_extend_book_reader(message: Message, state: FSMContext):
    await message.answer(
        "Введите id читателя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderExtend.choosing_reader_id)

@router.message(
    OrderExtend.choosing_reader_id,
)
async def chosen_id_reader_ext(message: Message, state: FSMContext):
    await state.update_data(id_reader=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите id книги:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderExtend.choosing_book_id)

@router.message(
    OrderExtend.choosing_book_id,
)
async def chosen_id_reader_ext(message: Message, state: FSMContext):
    await state.update_data(id_book=int(message.text.lower()))
    user_data = await state.get_data()
    status = extend_book_reader(user_data['id_reader'], user_data['id_book'])
    if status == 0:
        await message.answer(
            "Данный читатель не брал данную книгу",
            reply_markup=work_withReader()
        )
    if status == 1:
        await message.answer(
            "Вы уже вернули книгу",
            reply_markup=work_withReader()
        )
    if status == 2:
        await message.answer(
            "Вы просрочили книгу. Вам придется ее вернуть",
            reply_markup=work_withReader()
        )
    if status == 3:
        await message.answer(
            "Вы не можете продлить больше 3 раз",
            reply_markup=work_withReader()
        )
    if status == 4:
        await message.answer(
            "Успешно продлено!",
            reply_markup=menu()
        )
    await state.clear()

class OrderReception(StatesGroup):
    choosing_reader_id = State()
    choosing_book_id = State()

@router.message(F.text.lower() == "принять")
async def answer_reception_book_reader(message: Message, state: FSMContext):
    await message.answer(
        "Введите id читателя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderReception.choosing_reader_id)

@router.message(
    OrderReception.choosing_reader_id,
)
async def chosen_id_reader_reception(message: Message, state: FSMContext):
    await state.update_data(id_reader=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите id книги:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderReception.choosing_book_id)

@router.message(
    OrderReception.choosing_book_id,
)
async def chosen_id_reader_reception(message: Message, state: FSMContext):
    await state.update_data(id_book=int(message.text.lower()))
    user_data = await state.get_data()
    status = reception_book_reader(user_data['id_reader'], user_data['id_book'])
    if status == 0:
        await message.answer(
            "Данный читатель не брал данную книгу",
            reply_markup=work_withReader()
        )
    if status == 1:
        await message.answer(
            "Вам придется заплатить трехкратный штраф",
            reply_markup=menu()
        )
    if status == 2:
        await message.answer(
            "Успешно принято!",
            reply_markup=menu()
        )
    await state.clear()


class OrderPay(StatesGroup):
    choosing_reader_id = State()
    choosing_book_id = State()

@router.message(F.text.lower() == "возместить ущерб")
async def answer_get_book_reader(message: Message, state: FSMContext):
    await message.answer(
        "Введите id читателя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderPay.choosing_reader_id)

@router.message(
    OrderPay.choosing_reader_id,
)
async def chosen_id_reader_pay(message: Message, state: FSMContext):
    await state.update_data(id_reader=int(message.text.lower()))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите id книги:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderPay.choosing_book_id)

@router.message(
    OrderPay.choosing_book_id,
)
async def chosen_id_reader_pay(message: Message, state: FSMContext):
    await state.update_data(id_book=int(message.text.lower()))
    user_data = await state.get_data()
    status = refund_cost_question(user_data['id_reader'], user_data['id_book'])
    if status == 0:
        await message.answer(
            "Успешно возмещено!",
            reply_markup=menu()
        )
    if status == 1:
        await message.answer(
            "У вас просрочка более года",
            reply_markup=work_withReader()
        )
    if status == 2:
        await message.answer(
            "Этот пользователь не брал эту книгу",
            reply_markup=menu()
        )
    if status == 3:
        await message.answer(
            "Эта история уже закрыта",
            reply_markup=menu()
        )
    await state.clear()


@router.message(F.text.lower() == "нарушения")#TODO если нет таких, то выведется шо гуд, если есть такие, то выведится таблица с ними, откуда можно изъять имена(1 или неск) и для них уже сгенерируется
async def answer_mistakes(message: Message):
    await message.answer(
        "Здесь сгенерируется письмо для нарушителей",
        reply_markup=mistakes_reader_kb()
    )


class OrderLetter(StatesGroup):
    reader_id = State()

@router.message(F.text.lower() == "ругательное письмо")
async def answer_letter(message: Message, state: FSMContext):
    result = generate_letter()
    if len(result) == 0:
        await message.answer(
            "Нарушителей нет ^_^",
            reply_markup=work_withReader()
        )
        return
    await message.answer(
        f"Выберите id читателя из списка: {result}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderLetter.reader_id)


@router.message(
    OrderLetter.reader_id,
)
async def answer_letter_сhosen_id(message: Message, state: FSMContext):
    await state.update_data(id_reader=int(message.text.lower()))
    user_data = await state.get_data()
    name = seek_reader_for_mistakes(user_data['id_reader'])
    await message.answer(
        f"Уважаемый(ая) {name}, вы просрочили книгу. Верните, пожалуйста, иначе будет назначен штраф",
        reply_markup=menu()
    )
    await state.clear()


class OrderReceipt(StatesGroup):
    reader_id = State()
    save_index_hist = State()
    save_index_reader = State()

@router.message(F.text.lower() == "штрафная квитанция")
async def answer_letter(message: Message, state: FSMContext):
    result = generate_receipt()
    if len(result[0]) == 0:
        await message.answer(
            "Нарушителей нет ^_^",
            reply_markup=work_withReader()
        )
        return
    await message.answer(
        f"Выберите id читателя из списка: {result[0]}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(save_index_hist=result[1])
    await state.update_data(save_index_reader=result[0])
    await state.set_state(OrderReceipt.reader_id)


@router.message(
    OrderReceipt.reader_id,
)
async def answer_receipt_сhosen_id(message: Message, state: FSMContext):
    await state.update_data(id_reader=int(message.text.lower()))
    user_data = await state.get_data()
    if user_data['id_reader'] not in user_data['save_index_reader']:
        await message.answer(
            f"Вы выбрали id не из списка",
            reply_markup=menu()
        )
        return
    hist_id = user_data['save_index_hist'][user_data['save_index_reader'].
                            index(int(message.text.lower()))]
    list_with_name_price = act_reader_with_receipt(hist_id)
    await message.answer(
        f"Уважаемый(ая) {list_with_name_price[0]}, вы не возвращаете книгу более года. С вас взят штраф в раззмере {list_with_name_price[1]}",
        reply_markup=menu()
    )
    await state.clear()