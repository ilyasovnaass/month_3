from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.state import Quiz
from src.questions import QUESTIONS
from src.keyboards import reply_buttons, inline_buttons, repeat_button


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот!',
        reply_markup=reply_buttons
    )
    print(f'Пользователь {message.from_user.full_name} написал команду start.')

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(
        '/start - команда для запуска\n'
        '/help - список комманд'
        reply_markup=inline_buttons)
    

@router.message(F.text.lower() == 'группа')
async def group(message: Message):
    await message.answer(
        'Твоя группа 71-1!'
    )

@router.callback_query(F.data == 'quiz_start')
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Начинаем игру!', show_alert=True)
    await state.update_data(index=0, score=0)   # сохраняем прогресс
    await state.set_state(Quiz.waiting_answer)  # переводим в состояние
    await callback.message.answer(f'Вопрос 1: (QUESTIONS[0])')


@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data
    index = data['index']
    score = data['score']

    if message.text.lower() == QUESTIONS[index]:
        score += 1
        await message.answer('Правильно! +1')
    else:
        await message.answer('Неверно! Правильный ответ: {QUESTIONS[index]['a']}')

    index += 1
    if index >= len(QUESTIONS):
        await message.answer(f'Конец! Счет: {score}/len(QUESTIONS)')
        reply_buttons=repeat_button()
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f'Вопрос {index + 1}: {QUESTIONS[index]['q']}')

# @dp.message(F.from_user.id == 5667531193)
# async def user(message: Message):
#     await message.answer(
#         'Привет мой создатель!'
#     )

# Домашка:

@router.message(Command('about'))
async def about(message: Message):
    await message.answer(
        'Я бот-ассистент группы 71-1.\n' \
        'Я умею отвечать на комманды и реагировать на слова.'
    )

@router.message(F.text.lower() == 'пока')
async def echo(message: Message):
    await message.answer(
        f'Пока-пока!'
    )

