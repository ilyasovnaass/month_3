from aiogram import F, Router
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот!'
    )
    print(f'Пользователь {message.from_user.full_name} написал команду start.')

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(
        '/start - команда для запуска\n' \
        '/help - список комманд'
    )

@router.message(F.text.lower() == 'группа')
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
