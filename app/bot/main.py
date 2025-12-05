from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app.core.config import BOT_TOKEN
from app.db.crud import  add_new_user, user_exists, add_food, get_food, log_food, get_day_log_food, add_search_log, search_log_exists, search_food
from app.db.models import create_table_food, create_table_log_food, create_table_search_log, create_table_users
from api_client import FoodBotApi
from aiogram.fsm.state import State, StatesGroup
from app.parsers.pars import get_foods
from functools import lru_cache
from app.api.schemas import User
import time
class Form(StatesGroup):
    waiting_for_answer = State()

API_URL = "http://127.0.0.1:8000/"
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
api = FoodBotApi(base_url=API_URL)


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
    await api.connect()
    id = message.from_user.id
    if not await api.user_exist(id):
        await api.add_user({"id":id,"lang":"ru"})
    await api.disconnect()




@dp.message(Command("Add"))
async def start_cmd(message: Message, state: FSMContext):
    await message.answer("Напиши название продукта и гр/мл. Пример - Гречка 100")
    await state.set_state(Form.waiting_for_answer)




@lru_cache(maxsize=None)
@dp.message(Form.waiting_for_answer)
async def get_name(message: Message, state: FSMContext):

    mess = message.text.replace("-","").split()
    name = "".join(mess[:-1])
    flag = await api.search_log_exist(name)
    if flag:
        try:
            if int(mess[-1]):
                al = list(sorted(get_foods(name),key=lambda x:len(x["title"])))

                add_food(al)

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"{i['title']}", callback_data=f"{i['id']} {mess[-1]}")] for i in al[:8]] +
                        [[InlineKeyboardButton(text="Еще...", callback_data="lot")]] +
                        [[InlineKeyboardButton(text="Отмена", callback_data="stop")]])

                await api.add_search_log({"user_id":message.from_user.id,"date":int(time.time()),"mess":mess})

                await message.answer("Выбери Вариант:",reply_markup=keyboard)
                await state.clear()

        except:
            await message.answer("Попробуйте ещё раз")

    else:
        await api.connect()
        foods = (await api.search_food(name))["message"]
        al = list(sorted(foods,key=lambda x:len(x[1])))
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"{i[1]}", callback_data=f"{i[0]} {mess[-1]}")] for i in al[:15]] +
                        [[InlineKeyboardButton(text="Еще...", callback_data="lot")]] +
                        [[InlineKeyboardButton(text="Отмена", callback_data="stop")]])

        await message.answer("Выбери Вариант:", reply_markup=keyboard)
        await state.clear()
        await api.disconnect()





@dp.callback_query()
async def handler_callback(callback: CallbackQuery):
    data = callback.data
    if data == "stop":

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Действие отменено")

        return

    data = data.split()
    await api.connect()
    food = (await api.get_food(data[0]))["message"]


    for i in range(len(food)):
        if type(food[i])==float:
            food[i]*=int(data[-1])/100

    await api.log_food_ent({"id":food[0],"user_id":callback.from_user.id, "date":int(time.time()), "name":food[1], "energy":food[2], "fat":food[3], "carbohydrate":food[4], "protein":food[5],"mass":data[-1]})

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Добавлено✨')
    await api.disconnect()



@dp.message(Command("Day"))
async def start_cmd(message: Message):
    await api.connect()
    res = await api.get_day_log_food(user_id = message.from_user.id, date = 1)
    await api.disconnect()
    await message.answer(res["message"])



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



