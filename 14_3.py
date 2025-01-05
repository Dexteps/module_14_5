from aiogram import  Bot, F, Dispatcher
from aiogram.filters import  Command, CommandStart,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,FSInputFile, CallbackQuery
from crud_functions import get_all_products, is_included, add_user

TOKEN = '' # Пиши свой токен бота друган )))))
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher()

button1 = KeyboardButton(text='информация')
button2 = KeyboardButton(text = 'Рассчитать')
button3 = KeyboardButton(text='купить')
button4 = KeyboardButton(text='Регистрация')
kb = ReplyKeyboardMarkup(keyboard=[[button1, button2, button3, button4]],resize_keyboard=True)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying'),
        InlineKeyboardButton(text='Product2', callback_data='product_buying'),
        InlineKeyboardButton(text='Product3', callback_data='product_buying'),
        InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ]
)

@dp.message(F.text == 'купить')
async def get_buying_list(message: Message):
    for el in get_all_products():
        await message.answer(text=f'Название: {el[1]} | Описание: описание {el[2]} | Цена: {el[3]}')
        await message.answer_photo(photo=FSInputFile(f'{el[0]}.png'))
    await message.answer('Выберите продукт для покупки', reply_markup=buy_kb)
    

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    # Balance = 1000

@dp.message(F.text == 'Регистрация')
async def sing_up(message: Message, state: FSMContext):
    await message.answer(text= "Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)

@dp.message(StateFilter(RegistrationState.username))
async def set_username(message: Message, state: FSMContext):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await state.set_state(RegistrationState.email)

@dp.message(StateFilter(RegistrationState.email))
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await state.set_state(RegistrationState.age)

@dp.message(StateFilter(RegistrationState.age))
async def set_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    print(data)
    add_user(data['username'], data['email'], int(data['age']))
    await message.answer('Регистрация звершена!')
    await state.clear()


@dp.message(Command(commands='start'))
async def process_start(message: Message):
    await message.answer('Я бот вычесляющий норму калорий', reply_markup=kb)

@dp.message(F.text == 'информация')
async def run_info(message: Message):
    await message.answer('Я бот помогающий твоему здоровью')

@dp.message(F.text == 'Рассчитать')
async def set_message(message: Message, state: FSMContext):
    await message.answer('Введите ваш возраст: ')
    await  state.set_state(UserState.age)

@dp.message(StateFilter(UserState.age))
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите ваш рост: ')
    await state.set_state(UserState.growth)

@dp.message(StateFilter(UserState.growth))
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await state.set_state(UserState.weight)

@dp.message(StateFilter(UserState.weight))
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    print(data)
    res =  10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {str(res)}')
    await state.clear()

@dp.callback_query(F.data == 'product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer('Вы успешно преобрели продукт!')
    await call.answer()

if __name__ == '__main__':
    dp.run_polling(bot)
