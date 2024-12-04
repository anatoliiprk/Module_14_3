from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weigth = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.row(button1, button2)
kb.add(button3)

kb2 = InlineKeyboardMarkup()
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы рассчета', callback_data='formulas')
kb2.row(button4, button5)

kb3 = InlineKeyboardMarkup()
button6 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
button9 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
kb3.row(button6, button7, button8, button9)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Этот бот рассчитывает вашу норму калорий.')

@dp.callback_query_handler(text='calories')
async def set_gender(call):
    await call.message.answer('Введите свой пол (м/ж)')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weigth(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weigth.set()

@dp.message_handler(state = UserState.weigth)
async def send_calories(message, state):
    await state.update_data(weigth=message.text)
    data = await state.get_data()
    a = int(data['age'])
    g = int(data['growth'])
    w = int(data['weigth'])
    calories = 0
    if data['gender'] == 'м':
        calories = 10 * w + 6.25 * g - 5 * a + 5
    else:
        calories = 10 * w + 6.25 * g - 5 * a - 161
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1,5):
        await message.answer(f'Название: Продукт{i} | Описание: описание {i} | Цена: {i * 100}')
        with open(f'files/{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

