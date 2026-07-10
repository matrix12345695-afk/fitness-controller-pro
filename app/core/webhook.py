from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from app.core.config import settings
from app.core.logger import logger


def create_web_app(
    bot: Bot,
    dp: Dispatcher,
) -> web.Application:
    """
    Create aiohttp application for Telegram webhook.
    """

    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.webhook_secret,
    ).register(
        app,
        path=settings.webhook_path,
    )

    setup_application(
        app,
        dp,
        bot=bot,
    )

    logger.success("Webhook application created")

    return app


async def healthcheck(
    request: web.Request,
) -> web.Response:
    """
    Render health check.
    """

    return web.Response(
        text="Fitness Controller PRO is running!",
    )


def register_routes(
    app: web.Application,
) -> None:
    """
    Register HTTP routes.
    """

    app.router.add_get(
        "/",
        healthcheck,
    )

    app.router.add_get(
        "/health",
        healthcheck,
    )

    logger.success("HTTP routes registered")
