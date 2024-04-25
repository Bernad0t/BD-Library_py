import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions, directory_librery, main_menu, reports
from config_reader import config

# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    # Альтернативный вариант регистрации роутеров по одному на строку
    dp.include_router(questions.router)
    dp.include_router(directory_librery.router)
    dp.include_router(reports.router)
    dp.include_router(main_menu.router)
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())