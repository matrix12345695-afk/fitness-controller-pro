from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    Message,
)

from app.core.config import settings
from app.core.database import SessionLocal
from app.services.registration import RegistrationService

from app.keyboards.admin import users_keyboard
from app.keyboards.reply import (
    admin_menu,
    main_menu_ru,
    main_menu_uz,
)

from app.repositories.profiles import ProfileRepository
from app.services.admin import AdminService
from app.keyboards.dashboard import dashboard_keyboard
from app.keyboards.remind import remind_confirm_keyboard
from app.core.bot import bot
from app.keyboards.excel import excel_keyboard

from aiogram.types import FSInputFile
from app.services.excel_export import ExcelExportService

from loguru import logger

from pathlib import Path

router = Router()


# ==========================================================
# ADMIN PANEL
# ==========================================================

@router.message(
    F.text.in_(
        [
            "👨‍💼 Админ",
            "👨‍💼 Admin",
        ]
    )
)
async def admin_panel(
    message: Message,
):
    """
    Open admin panel.
    """

    if message.from_user.id not in settings.admin_ids:

        await message.answer(
            "⛔ У вас нет доступа."
        )

        return

    await message.answer(
        (
            "👨‍💼 <b>Панель администратора</b>\n\n"
            "Добро пожаловать!\n\n"
            "Выберите раздел."
        ),
        reply_markup=admin_menu(),
        parse_mode="HTML",
    )

# ==========================================================
# EXIT ADMIN PANEL
# ==========================================================

@router.message(
    F.text == "⬅️ Назад",
)
async def exit_admin_panel(
    message: Message,
):
    """
    Exit admin panel and return to main menu.
    """

    async with SessionLocal() as session:

        registration = RegistrationService(
            session,
        )

        user = await registration.get_user(
            message.from_user.id,
        )

    if (
        user
        and getattr(user, "language", None)
        and user.language.value == "uz"
    ):

        await message.answer(
            "🏠 Asosiy menyu",
            reply_markup=main_menu_uz(
                message.from_user.id,
            ),
        )

    else:

        await message.answer(
            "🏠 Главное меню",
            reply_markup=main_menu_ru(
                message.from_user.id,
            ),
        )


# ==========================================================
# USERS LIST
# ==========================================================

@router.message(
    F.text == "👥 Пользователи",
)
async def users_list(
    message: Message,
):
    """
    Show all users.
    """

    if message.from_user.id not in settings.admin_ids:
        return

    async with SessionLocal() as session:

        service = AdminService(session)

        users = await service.get_users()

    if not users:

        await message.answer(
            "❌ Пользователей пока нет."
        )

        return

    await message.answer(
        "👥 <b>Список пользователей</b>\n\n"
        "Выберите пользователя:",
        reply_markup=users_keyboard(users),
        parse_mode="HTML",
    )


# ==========================================================
# USER CARD
# ==========================================================

@router.callback_query(
    F.data.startswith("user:")
)
async def user_card(
    callback: CallbackQuery,
):
    """
    Show user information.
    """

    if callback.from_user.id not in settings.admin_ids:

        await callback.answer()

        return

    user_id = int(
        callback.data.split(":")[1]
    )

    async with SessionLocal() as session:

        service = AdminService(session)

        user = await service.get_user(
            user_id,
        )

        profile = await ProfileRepository(
            session,
        ).get(
            user_id,
        )

    if user is None:

        await callback.answer(
            "Пользователь не найден.",
            show_alert=True,
        )

        return

    text = (
        f"👤 <b>{user.first_name}</b>"
    )

    if user.last_name:

        text += f" {user.last_name}"

    text += "\n\n"

    text += (
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
    )

    if user.username:

        text += (
            f"👤 Username: @{user.username}\n"
        )

    if profile:

        text += (
            f"\n📏 Рост: {profile.height} см\n"
            f"⚖️ Вес: {profile.start_weight} кг\n"
            f"👤 Пол: {profile.gender.value}\n"
            f"🎂 Дата рождения: {profile.birth_date}\n"
        )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
    )

    await callback.answer()


# ==========================================================
# BACK
# ==========================================================

@router.callback_query(
    F.data == "admin_back",
)
async def admin_back(
    callback: CallbackQuery,
):
    """
    Back to admin panel.
    """

    if callback.from_user.id not in settings.admin_ids:

        await callback.answer()

        return

    await callback.message.edit_text(
        (
            "👨‍💼 <b>Панель администратора</b>\n\n"
            "Выберите раздел."
        ),
        parse_mode="HTML",
    )

    await callback.answer()
    
@router.message(
    F.text == "📊 Сегодня",
)
async def today_dashboard(
    message: Message,
):
    """
    Dashboard for today.
    """

    if message.from_user.id not in settings.admin_ids:
        return

    async with SessionLocal() as session:

        service = AdminService(session)

        stats = await service.dashboard_stats()

        users = await service.users_without_report_today()

    text = (
        "📊 <b>Сегодня</b>\n\n"

        f"👥 Пользователей: <b>{stats['total_users']}</b>\n"

        f"✅ Прошли: <b>{stats['completed_today']}</b>\n"

        f"❌ Не прошли: <b>{stats['not_completed_today']}</b>\n"

        f"📈 Выполнение: <b>{stats['completion_percent']}%</b>\n"
    )

    if users:

        text += "\n──────────────\n\n"

        text += "❌ <b>Не прошли:</b>\n\n"

        for user in users:

            name = user.first_name or "Без имени"

            if user.last_name:
                name += f" {user.last_name}"

            text += f"👤 {name}\n"

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=dashboard_keyboard(),
    )

@router.callback_query(
    F.data == "dashboard_remind",
)
async def dashboard_remind(
    callback: CallbackQuery,
):
    """
    Reminder confirmation.
    """

    if callback.from_user.id not in settings.admin_ids:

        await callback.answer()

        return

    async with SessionLocal() as session:

        service = AdminService(session)

        users = await service.users_without_report_today()

    if not users:

        await callback.answer(
            "🎉 Все уже прошли опрос!",
            show_alert=True,
        )

        return

    text = (
        "📢 <b>Напоминание</b>\n\n"

        f"Получателей: <b>{len(users)}</b>\n\n"

        "Сообщение будет отправлено:\n\n"
    )

    for user in users[:10]:

        name = user.first_name or "Без имени"

        if user.last_name:
            name += f" {user.last_name}"

        text += f"👤 {name}\n"

    if len(users) > 10:

        text += (
            f"\n...и ещё {len(users)-10}"
        )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=remind_confirm_keyboard(),
    )

    await callback.answer()

@router.callback_query(
    F.data == "remind_send",
)
async def remind_send(
    callback: CallbackQuery,
):
    """
    Send reminder to all users without today's report.
    """

    if callback.from_user.id not in settings.admin_ids:

        await callback.answer()

        return

    async with SessionLocal() as session:

        service = AdminService(session)

        success, failed = await service.remind_users_today(
            bot,
        )

    await callback.message.edit_text(
        (
            "✅ <b>Рассылка завершена</b>\n\n"
            f"📨 Успешно отправлено: <b>{success}</b>\n"
            f"❌ Ошибок: <b>{failed}</b>"
        ),
        parse_mode="HTML",
    )

    await callback.answer(
        "Рассылка выполнена!"
    )

@router.callback_query(
    F.data == "remind_cancel",
)
async def remind_cancel(
    callback: CallbackQuery,
):
    """
    Cancel reminder.
    """

    await callback.message.edit_text(
        "❌ Рассылка отменена."
    )

    await callback.answer()

@router.callback_query(
    F.data == "dashboard_excel",
)
async def dashboard_excel(
    callback: CallbackQuery,
):
    """
    Excel export menu.
    """

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer()
        return

    await callback.message.edit_text(
        (
            "📥 <b>Экспорт Excel</b>\n\n"
            "Выберите период формирования отчёта."
        ),
        parse_mode="HTML",
        reply_markup=excel_keyboard(),
    )

    await callback.answer()

@router.callback_query(
    F.data == "excel_today",
)
async def excel_today(
    callback: CallbackQuery,
):
    """
    Generate Excel for today.
    """

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer()
        return

    status = await callback.message.edit_text(
        "⏳ Формирую Excel...\n\nПожалуйста, подождите."
    )

    async with SessionLocal() as session:

        exporter = ExcelExportService(
            session,
        )

        try:

            filepath = await exporter.create_report(
                "today",
            )    

            logger.info(
                "Excel report generated: {}",
                filepath,
            )

        except Exception as e:

            logger.exception(e)

            await status.edit_text(
                f"❌ Ошибка формирования Excel.\n\n<code>{e}</code>",
                parse_mode="HTML",
            )

            return

    await status.edit_text(
        "✅ Excel успешно сформирован."
    )

    document = FSInputFile(filepath)

    await callback.message.answer_document(
        document=document,
        caption="📥 Отчёт сформирован автоматически.",
    )

    try:
        Path(filepath).unlink(
            missing_ok=True,
        )
    except Exception:
        logger.exception("Cannot delete %s", filepath)

    await callback.message.answer(
        "👨‍💼 Панель администратора",
        reply_markup=admin_menu(),
    )

@router.callback_query(
    F.data == "excel_yesterday",
)
async def excel_yesterday(
    callback: CallbackQuery,
):
    """
    Generate Excel for yesterday.
    """

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer()
        return

    status = await callback.message.edit_text(
        "⏳ Формирую Excel за вчера..."
    )

    async with SessionLocal() as session:

        exporter = ExcelExportService(session)

        try:

            filepath = await exporter.create_report(
                "yesterday",
            )

        except Exception as e:

            logger.exception(e)

            await status.edit_text(
                f"❌ Ошибка.\n\n<code>{e}</code>",
                parse_mode="HTML",
            )

            return

    await status.edit_text(
        "✅ Excel сформирован."
    )

    await callback.message.answer_document(
        FSInputFile(filepath),
    )

    Path(filepath).unlink(
        missing_ok=True,
    )

    await callback.message.answer(
        "👨‍💼 Панель администратора",
        reply_markup=admin_menu(),
    )

@router.callback_query(
    F.data == "excel_week",
)
async def excel_week(
    callback: CallbackQuery,
):

    if callback.from_user.id not in settings.admin_ids:
        
        await callback.answer()
        return

    status = await callback.message.edit_text(
        "⏳ Формирую Excel за неделю..."
    )

    async with SessionLocal() as session:

        exporter = ExcelExportService(session)

        filepath = await exporter.create_report(
            "week",
        )

    await status.edit_text(
        "✅ Excel сформирован."
    )

    await callback.message.answer_document(
        FSInputFile(filepath),
    )

    Path(filepath).unlink(
        missing_ok=True,
    )

    await callback.message.answer(
        "👨‍💼 Панель администратора",
        reply_markup=admin_menu(),
    )

@router.callback_query(
    F.data == "excel_month",
)
async def excel_month(
    callback: CallbackQuery,
):

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer()
        return

    status = await callback.message.edit_text(
        "⏳ Формирую Excel за месяц..."
    )

    async with SessionLocal() as session:

        exporter = ExcelExportService(session)

        filepath = await exporter.create_report(
            "month",
        )

    await status.edit_text(
        "✅ Excel сформирован."
    )

    await callback.message.answer_document(
        FSInputFile(filepath),
    )

    Path(filepath).unlink(
        missing_ok=True,
    )

    await callback.message.answer(
        "👨‍💼 Панель администратора",
        reply_markup=admin_menu(),
    )
