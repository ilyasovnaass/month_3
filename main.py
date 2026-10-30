# import time

# def task(name, seconds):
#     print(f'Упала задача {name} начал работу!')
#     time.sleep(seconds)
#     print(f'Задача {name} готово!')

# task('1', 4)
# task('2', 3)
# task('3', 2)


# import asyncio
# # Event Loop - менеджер


# async def task(name, second):
#     await asyncio.sleep(second)
#     print(f'Задача {name}  готово!')

# async def main():
#     await asyncio.gather(
#         task('1', 4),
#         task('2', 2),
#         task('3', 1),
#     )

# asyncio.run(main())

import asyncio
import logging


BOT_TOKEN = '8676423397:AAHVTJFVWoAYIrDPgbIcW-pEGti5lBn8i3M'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот!'
    )
    print(f'Пользователь {message.from_user.full_name} написал команду start.')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        '/start - команда для запуска\n' \
        '/help - список комманд'
    )

@dp.message(F.text.lower() == 'группа')
async def group(message: Message):
    await message.answer(
        'Твоя группа 71-1!'
    )

# @dp.message(F.from_user.id == 5667531193)
# async def user(message: Message):
#     await message.answer(
#         'Привет мой создатель!'
#     )

# Домашка:

@dp.message(Command('about'))
async def about(message: Message):
    await message.answer(
        'Я бот-ассистент группы 71-1.\n' \
        'Я умею отвечать на комманды и реагировать на слова.'
    )

@dp.message(F.text.lower() == 'пока')
async def echo(message: Message):
    await message.answer(
        f'Пока-пока!'
    )

async def main():
    await dp.start_polling(bot)     # отправляет запросы на тг-сервер

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    