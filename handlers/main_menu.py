from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from keyboards.for_questions import menu

router = Router()

@router.message(StateFilter(None))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        "Главное меню",
        reply_markup=menu()
    )