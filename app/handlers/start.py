from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.config import settings
from app.core.database import SessionLocal
from app.keyboards.inline import language_keyboard
from app.keyboards.reply import (
    admin_menu,
    main_menu_ru,
    main_menu_uz,
)
from app.services.registration import RegistrationService
from app.states.registration import RegistrationState

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handle /start command.
    """

    await state.clear()

    async with SessionLocal() as session:

        registration = RegistrationService(
            session,
        )

        user = await registration.get_user(
            message.from_user.id,
        )

        if user:

            # Администратор
            if message.from_user.id in settings.admin_ids:

                await message.answer(
                    text=f"👋 Добро пожаловать обратно, <b>{message.from_user.full_name}</b>!",
                    reply_markup=admin_menu(),
                    parse_mode="HTML",
                )

                return

            # Обычный пользователь (RU)
            if user.language.value == "ru":

                await message.answer(
                    text=f"👋 С возвращением, <b>{message.from_user.full_name}</b>!",
                    reply_markup=main_menu_ru(
                        message.from_user.id,
                    ),
                    parse_mode="HTML",
                )

            # Обычный пользователь (UZ)
            else:

                await message.answer(
                    text=f"👋 Xush kelibsiz, <b>{message.from_user.full_name}</b>!",
                    reply_markup=main_menu_uz(
                        message.from_user.id,
                    ),
                    parse_mode="HTML",
                )

            return

    await state.set_state(
        RegistrationState.language,
    )

    await message.answer(
        text=(
            "👋 <b>Добро пожаловать в Fitness Controller PRO!</b>\n\n"
            "Для начала выберите язык.\n\n"
            "👋 <b>Fitness Controller PRO ga xush kelibsiz!</b>\n\n"
            "Boshlash uchun tilni tanlang."
        ),
        reply_markup=language_keyboard(),
        parse_mode="HTML",
    )
