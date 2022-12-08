# -*- coding: utf8 -*-

import logging
import os
import csv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import business_logic



class CheckStigma(StatesGroup):
    wait_stigma = State()


bot = Bot(token='5609860985:AAEkmMiUWqhAFeco7w23rXKus5YhT9ZDmRY')  # Токен  бота checkwelder

dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

btnHlp = KeyboardButton('Help')
btnDon = KeyboardButton('Donate')

help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row(btnHlp, btnDon)

greet_me = ['Хозяин', 'Иван Александрович']
boss_id = 799592984


@dp.message_handler(commands='start')
async def start_using(message: types.Message):
    if message.from_user.id == 799592984:
        await message.answer('Приветствую. Работает 09.09.22', reply_markup=help_kb)
    else:
        await message.answer('Приветствую. Чтобы узнать что я умею нажми Help', reply_markup=help_kb)
        await bot.send_message(799592984, f'Кто-то нажал старт user_id - {message.from_user.id}, \n'
                                          f'user_name - {message.from_user.username}')


@dp.message_handler()
async def help_command(message: types.Message):
    if message.text == 'Help':
        writeBtn = InlineKeyboardButton('Написать разработчику', url='telegram.me/ivanikos')
        btn_naks = InlineKeyboardButton('Проверить НАКС сварщика', callback_data='/check_naks')

        write_kb = InlineKeyboardMarkup().add(btn_naks).add(writeBtn)
        await message.answer('Пока что это все, что можно выбрать:', reply_markup=write_kb)
    elif message.text == 'Donate':
        await message.answer('Пока не работает. Жми HELP.')
    else:
        await message.answer('Не пойму чего ты хочешь, нажми кнопку Help.')


@dp.callback_query_handler(lambda c: c.data == '/check_naks')
async def callback_check_naks(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != boss_id:
        await bot.send_message(boss_id, f'Кто-то пытается использовать проверку по клейму:\n'
                                        f' его ID: {callback_query.from_user.id}, \n'
                                        f'его username: {callback_query.from_user.username}')
    await bot.send_message(callback_query.from_user.id, 'Введи клеймо сварщика:')
    await CheckStigma.wait_stigma.set()


async def naks_answer(message: types.Message, state: FSMContext):
    await state.update_data(stigma=message)
    stigma = await state.get_data()
    await message.reply('Нужно немного подождать')
    data_welder = business_logic.check_welder_att(stigma)

    try:
        await message.reply(data_welder)
        await state.finish()
    except:
        await message.reply('Извини, что-то пошло не так, попробуй ещё раз, пожалуйста.')
        await state.finish()
    await state.finish()

dp.register_callback_query_handler(callback_check_naks, state=CheckStigma.wait_stigma)
dp.register_message_handler(naks_answer, state=CheckStigma.wait_stigma)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)