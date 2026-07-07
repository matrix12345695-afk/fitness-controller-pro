from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.database import SessionLocal
from app.keyboards.inline import language_keyboard
from app.keyboards.reply import admin_menu, main_menu_ru, main_menu_uz
from app.services.registration import RegistrationService

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """
    /start command
    """

    await state.clear()

    async with SessionLocal() as session:

        service = RegistrationService(session)

        user = await service.get_user(
            message.from_user.id
        )

        if user:

            if user.role.value == "ADMIN":

                await message.answer(
                    f"👋 Добро пожаловать обратно, {message.from_user.full_name}!",
                    reply_markup=admin_menu(),
                )

                return

            if user.language.value == "ru":

                await message.answer(
                    f"👋 С возвращением, {message.from_user.full_name}!",
                    reply_markup=main_menu_ru(),
                )

            else:

                await message.answer(
                    f"👋 Xush kelibsiz, {message.from_user.full_name}!",
                    reply_markup=main_menu_uz(),
                )

            return

    text = (
        "👋 <b>Добро пожаловать в Fitness Controller PRO</b>\n\n"
        "Пожалуйста, выберите язык.\n\n"
        "🇷🇺 Русский\n"
        "🇺🇿 O'zbekcha"
    )

    await state.set_state(
        RegistrationState.language,
    )

    await message.answer(
        text=text,
        reply_markup=language_keyboard(),
    )
