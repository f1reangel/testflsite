from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_panel import get_main_panel_keyboard
router = Router()


@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer(f"Привіт, {message.from_user.first_name} саме цей бот"
                         f" дозволяє зарезервувати  столик в нашому кафе."
                         f" Але для початку потрібно пройти анкетування.",
                         reply_markup=get_main_panel_keyboard())
