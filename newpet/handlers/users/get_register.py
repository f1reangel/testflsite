from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import asyncpg
storage = MemoryStorage()
router = Router()
user_dict: dict[int, dict[str, str | int | bool]] = {}

async def create_db_pool():
    # Змініть параметри підключення відповідно до вашої конфігурації
    pool = await asyncpg.create_pool(
        user='postgres',
        password='88461978',
        database='postgres',
        host='localhost'
    )
    return pool

db_pool = None


async def init_db():
    global db_pool
    db_pool = await create_db_pool()


class FSMReservation(StatesGroup):
    fill_name = State()
    fill_phone_number = State()
    fill_date = State()
    fill_time = State()
    fill_guests_count = State()
    select_table = State()
    fill_news_subscription = State()


@router.message(F.text == "Почати анкетування✍", StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Ця анкета потрібна для ідентифікації користувачів\n\n'
             'Щоб перейти до заповнення анкети - '
             'відправте команду /startForm'
    )


@router.message(Command("startForm"), StateFilter(default_state))
async def process_start_command(message: Message,state:FSMContext):
    await message.answer(
        text='Будь ласка, введіть ваше ім\'я'
    )
    await state.set_state(FSMReservation.fill_name)


@router.message(StateFilter(FSMReservation.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f'Дякую {message.text}!\n А тепер введіть ваш номер телефону')
    await state.set_state(FSMReservation.fill_phone_number)


@router.message(StateFilter(FSMReservation.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='Те, що ви відправили не схоже на ім\'я\n\n'
             'Будь ласка, введіть ваше ім\'я\n\n'
             'Якщо ви хочете перервати резервацію - '
             'відправте команду /cancel'
    )


@router.message(StateFilter(FSMReservation.fill_phone_number), F.text.isdigit())
async def process_phone_number_sent(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer(text='Дякую!\n\nТепер введіть дату в форматі ДД.ММ.')
    await state.set_state(FSMReservation.fill_date)


@router.message(StateFilter(FSMReservation.fill_phone_number))
async def warning_not_phone_number(message: Message):
    await message.answer(
        text='Номер телефону має складатися лише з цифр\n\n'
             'Спробуйте ще раз\n\nЯкщо ви хочете перервати '
             'резервацію - надішліть команду /cancel'
    )


@router.message(StateFilter(FSMReservation.fill_date), lambda x: x.text.count('.') == 1)
async def process_date_sent(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer(text='Дякую!\n\nТепер введіть час у форматі ГГ:ХХ')
    await state.set_state(FSMReservation.fill_time)


@router.message(StateFilter(FSMReservation.fill_date))
async def warning_not_date(message: Message):
    await message.answer(
        text='Дата має бути у форматі ДД.ММ\n\n'
             'Спробуйте ще раз\n\nЯкщо ви хочете перервати '
             'резервацію - надішліть команду /cancel'
    )


@router.message(StateFilter(FSMReservation.fill_time), lambda x: x.text.count(':') == 1)
async def process_time_sent(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer(text='Дякую!\n\nВведіть кількість гостей')
    await state.set_state(FSMReservation.fill_guests_count)

@router.message(StateFilter(FSMReservation.fill_time))
async def warning_not_time(message: Message):
    await message.answer(
        text='Час має бути у форматі ГГ:ХХ\n\n'
             'Спробуйте ще раз\n\nЯкщо ви хочете перервати '
             'резервацію - надішліть команду /cancel'
    )


@router.message(StateFilter(FSMReservation.fill_guests_count), F.text.isdigit())
async def process_guests_count_sent(message: Message, state: FSMContext):
    await state.update_data(guests_count=message.text)
    table1_button = InlineKeyboardButton(text='Столик 1', callback_data='table1')
    table2_button = InlineKeyboardButton(text='Столик 2', callback_data='table2')
    table3_button = InlineKeyboardButton(text='Столик 3', callback_data='table3')
    keyboard = [
        [table1_button, table2_button],
        [table3_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(text='Виберіть столик', reply_markup=markup)
    await state.set_state(FSMReservation.select_table)


@router.message(StateFilter(FSMReservation.fill_guests_count))
async def warning_not_guests_count(message: Message):
    await message.answer(
        text='Кількість гостей має бути числом\n\n'
             'Спробуйте ще раз\n\nЯкщо ви хочете перервати '
             'резервацію - надішліть команду /cancel'
    )


@router.callback_query(StateFilter(FSMReservation.select_table),
                       F.data.in_(['table1', 'table2', 'table3']))
async def process_table_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(table=callback.data)
    yes_news_button = InlineKeyboardButton(text='Так', callback_data='yes_news')
    no_news_button = InlineKeyboardButton(text='Ні', callback_data='no_news')
    keyboard = [[yes_news_button, no_news_button]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text(
        text='Дякую!\n\nХочете підписатися на розсилку новин?',
        reply_markup=markup
    )
    await state.set_state(FSMReservation.fill_news_subscription)


@router.message(StateFilter(FSMReservation.select_table))
async def warning_not_table_selected(message: Message):
    await message.answer(
        text='Будь ласка, виберіть столик за допомогою кнопок\n\n'
             'Якщо ви хочете перервати резервацію - '
             'відправте команду /cancel'
    )


@router.callback_query(StateFilter(FSMReservation.fill_news_subscription),
                       F.data.in_(['yes_news', 'no_news']))
async def process_news_subscription(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    news_subscription = data['news_subscription'] = callback.data == 'yes_news'
    reservation_data = {
        'name': data['name'],
        'phone_number': data['phone_number'],
        'reservation_date': data['date'],
        'reservation_time': data['time'],
        'guests_count': data['guests_count'],
        'table_number': int(data['table'][-1]),  # Отримати номер столика з callback_data
        'news_subscription': news_subscription
    }
    async with db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO reservations (name, phone_number, reservation_date, reservation_time, guests_count, table_number, news_subscription) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7)",
            *reservation_data.values()  # Unpack the values from the dictionary
        )
    await state.clear()
    await callback.message.edit_text(
        text='Дякую! Ваша резервація успішно створена!\n\n'
             'Ви вийшли з процесу резервації'
    )
    await callback.message.answer(
        text='Щоб подивитися деталі вашої резервації - '
             'надішліть команду /showreservation'
    )

@router.message(StateFilter(FSMReservation.fill_news_subscription))
async def warning_not_news_subscription(message: Message):
    await message.answer(
        text='Будь ласка, скористайтесь кнопками!\n\n'
             'Якщо ви хочете перервати резервацію - '
             'відправте команду /cancel'
    )


@router.message(Command(commands='showreservation'), StateFilter(default_state))
async def process_showreservation_command(message: Message):
    if message.from_user.id in user_dict:
        data = user_dict[message.from_user.id]
        await message.answer(
            text=f"Деталі вашої резервації:\n\n"
                 f"Ім'я: {data['name']}\n"
                 f"Номер телефону: {data['phone_number']}\n"
                 f"Дата: {data['date']}\n"
                 f"Час: {data['time']}\n"
                 f"Кількість гостей: {data['guests_count']}\n"
                 f"Столик: {data['table']}\n"
                 f"Підписка на новини: {'Так' if data['news_subscription'] else 'Ні'}"
        )
    else:
        await message.answer(
            text='Ви ще не робили резервацію. Щоб почати - '
                 'надішліть команду "Зробити резервацію"'
        )

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Скасовувати нічого.\n\n'
             'Щоб почати резервацію - '
             'надішліть команду "Зробити резервацію"'
    )

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Ви вийшли з процесу резервації\n\n'
             'Щоб почати знову - '
             'надішліть команду "Зробити резервацію"'
    )
    await state.clear()


@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Я вас не розумію')