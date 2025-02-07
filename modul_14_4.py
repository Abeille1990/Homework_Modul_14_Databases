from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from time import sleep
from crud_functions import *

api = '8199490075:AAEzUjpNsw1J7M-oPJ5-Vhdnx5qEjoeRr_U'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

rkb = ReplyKeyboardMarkup(resize_keyboard=True)
rkb2 = ReplyKeyboardMarkup(resize_keyboard=True)
ikb2 = InlineKeyboardMarkup(resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


rbutton = KeyboardButton(text='Что я умею?')
rkb.add(rbutton)

ibutton1 = KeyboardButton(text='Расчитать норму калорий')
ibutton2 = KeyboardButton(text='Формула расчета калорий')
ibutton3 = KeyboardButton(text='Купить витамины')
rkb2.row(ibutton1, ibutton2, ibutton3)
inline_menu = rkb2

product1 = InlineKeyboardButton(text='UNCARIA FORTE', callback_data="product1")
product2 = InlineKeyboardButton(text='ANTISWEET CONTROL', callback_data="product2")
product3 = InlineKeyboardButton(text='BRONCHOLUX INTENSIVE', callback_data="product3")
product4 = InlineKeyboardButton(text='VISION COMPLEX', callback_data="product4")
ikb2.add(product1, product2, product3, product4)
inline_product_menu = ikb2


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=rkb)


@dp.message_handler(text='Что я умею?')
async def main_menu(message):
    await message.answer("А вот что:", reply_markup=rkb2)


@dp.message_handler(text='Формула расчета калорий')
async def get_formulas(message):
    await message.answer(f'Раcчет производится по формуле Миффлина-Сан Жеора'
                         '\nА именно:'
                         '\nДля женщин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах)'
                         ' − (5 × возраст в годах) − 161'
                         '\nДля мужчин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах)'
                         ' − (5 × возраст в годах) + 5', reply_markup=rkb2)



@dp.message_handler(text='Купить витамины')
async def get_buying_list(message):
    products = get_all_products()
    for i in products:
            with open(f'files/{i[0]} бад.jpg', 'rb') as img:
                await message.answer(f"Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}")
                await message.answer_photo(img, reply_markup=rkb2)
    await message.answer("Выберите продукт для покупки:", reply_markup=ikb2)

for i in range(5):
    @dp.callback_query_handler(text=f'product{i}')
    async def send_confirm_message(call):
        await call.message.answer(f'Вы успешно приобрели продукт!')


@dp.message_handler(text='Расчитать норму калорий')
async def set_age(message):
    await message.answer("Введите свой возраст")
    # await message.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    print(data)
    await message.answer("Запускаем калькулятор, пожалуйста ожидайте")
    sleep(3)
    calories = (10 * float(data['weight'])) + (6.25 * float(data['growth'])) - (5 * float(data['age'])) - 161
    await message.answer(f'Ваша суточная норма калорий: {int(calories)}. \nПриятного аппетита=)')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
