from aiogram import Bot
from aiogram.types import BotCommand

# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для и menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Старт бота'),
        BotCommand(command='/cancel',
                   description='Сброс'),
        BotCommand(command='/help',
                   description='Поддержка')
    ]

    await bot.set_my_commands(main_menu_commands)