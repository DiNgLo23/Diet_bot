from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import TOKEN
from database import create_table_users, add_new_user, user_exists, create_table_food, create_table_log_food, add_food, get_food, log_food, get_day_log_food, create_table_search_log, add_search_log, search_log_exists, search_food
import requests
import datetime
from aiogram.fsm.state import State, StatesGroup
from pars import get_foods
import numpy as np
import time


class Form(StatesGroup):
    waiting_for_answer = State()


bot = Bot(TOKEN)
dp = Dispatcher()



####################
# CREATE DATABASES
####################
create_table_users()
create_table_food()
create_table_log_food()
create_table_search_log()





@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Привет")
    if user_exists(message.from_user.id): add_new_user(message.from_user.id, "ru")




@dp.message(Command("Add"))
async def start_cmd(message: Message, state: FSMContext):
    await message.answer("Напиши название продукта и гр/мл. Пример - Гречка 100")
    await state.set_state(Form.waiting_for_answer)




@dp.message(Command("Day"))
async def start_cmd(message: Message):
    foods = get_day_log_food(message.from_user.id,"1")
    res = foods[0][4:]
    foods.pop(0)

    for i in foods:
        i = i[4:]
        res[0] += i[0]
        res[1] += i[1]
        res[2] += i[2]
        res[3] += i[3]
        res[4] += i[4]

    name = ["Ккал - ","Жиры - ","Углеводы - ","Белки - ", "Масса - "]
    res = "".join([name[i]+str(int(res[i]))+"\n" for i in range(len(res))])

    await message.answer(res)




@dp.message(Form.waiting_for_answer)
async def get_name(message: Message, state: FSMContext):

    mess = message.text.replace("-","").split()
    name = "".join(mess[:-1])
    if search_log_exists(name):
        try:
            if int(mess[-1]):
                al = get_foods(name)
                add_food(al)

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"{i['title']}", callback_data=f"{i['id']} {mess[-1]}")] for i in al[:15]] +
                        [[InlineKeyboardButton(text="Еще...", callback_data="lot")]] +
                        [[InlineKeyboardButton(text="Отмена", callback_data="stop")]])

                add_search_log(message.from_user.id, name)

                await message.answer("Выбери Вариант:",reply_markup=keyboard)
                await state.clear()

        except:
            await message.answer("Попробуйте ещё раз")

    else:
        al = list(search_food(name))

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"{i[1]}", callback_data=f"{i[0]} {mess[-1]}")] for i in al[:15]] +
                        [[InlineKeyboardButton(text="Еще...", callback_data="lot")]] +
                        [[InlineKeyboardButton(text="Отмена", callback_data="stop")]])

        await message.answer("Выбери Вариант:", reply_markup=keyboard)
        await state.clear()





@dp.callback_query()
async def handler_callback(callback: CallbackQuery):
    data = callback.data
    if data == "stop":

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Действие отменено")

        return

    data = data.split()

    food = get_food(data[0])

    for i in range(len(food)):
        if type(food[i])==float:
            food[i]*=int(data[-1])/100

    log_food(food,data[-1],callback.from_user.id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Добавлено✨')




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



