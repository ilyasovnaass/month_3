import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)

BOT_TOKEN = '8736066912:AAFXWMViw14z9LlzgKIZeWL0_CiClAvPQr4'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users_data = {}

class Registration(StatesGroup):
    name = State()
    age = State()



@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}'
    )


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Доступные команды:\n'
        '/start - команда для запуска\n' \
        '/help - список комманд\n'
        '/register - команда для регистрации\n'
        '/profile - команда для проверки вашего профиля\n'
    )


@dp.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer(
        'Введите ваше имя:'
    )

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(Registration.age)
    await message.answer(
        'Введите ваш возраст:'
    )

@dp.message(Registration.age)
async def get_age(message: Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer(
            'Пожалуйста, введите возраст цифрами:'
        )
        return
    
    age = int(age)

    if age == 0:
        await message.answer(
            'Возраст должен быть больше нуля! Попробуйте снова:'
        )
        return

    await state.update_data(age = age)

    data = await state.get_data()
    name = data['name']

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить',
            callback_data='confirm_reg')
        ],
        [InlineKeyboardButton(
            text='Начать заново',
            callback_data='restart_reg'
        )]
        ]
    )

    await message.answer(
        f'Имя - {name}\n'
        f'Возраст - {age}',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == 'confirm_reg')
async def confirm_registration(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()
    user_id = callback.from_user.id
    users_data[user_id] = {
        'name': data['name'],
        'age': data['age']
    }

    await callback.message.answer(
        'Регистрация завершена!'
    )

    await state.clear()

    await callback.answer()

@dp.callback_query(F.data == 'restart_reg')
async def restart_registration(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.set_state(Registration.name)
    await state.set_data({})
    await callback.message.answer(
        'Начнем заново!\n'
        'Введите ваше имя:'
    )
    await callback.answer()


@dp.message(Command('profile'))
async def profile(message: Message):
    user_id = message.from_user.id

    if user_id in users_data:
        name = users_data[user_id]['name']
        age = users_data[user_id]['age']

        await message.answer(
            f'Имя - {name}\n'
            f'Возраст - {age}'
        )
    else:
        await message.answer(
            'Вы незарегистрированы.\n'
        )
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

