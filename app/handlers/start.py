from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.inline import language_keyboard
from app.states.registration import RegistrationState

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Start command.
    """

    await state.clear()

    text = (
        "👋 <b>Добро пожаловать в Fitness Controller PRO!</b>\n\n"
        "Пожалуйста, выберите язык.\n\n"
        "👋 <b>Fitness Controller PRO ga xush kelibsiz!</b>\n\n"
        "Iltimos, tilni tanlang."
    )

    await state.set_state(RegistrationState.language)

    await message.answer(
        text=text,
        reply_markup=language_keyboard(),
    )
