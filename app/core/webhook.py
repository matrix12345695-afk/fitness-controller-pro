from aiohttp import web
from aiogram import Bot, Dispatcher
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
    Create aiohttp application.
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

    register_routes(app)

    logger.success("Webhook application initialized")

    return app


def register_routes(
    app: web.Application,
) -> None:
    """
    Register HTTP routes.
    """

    async def index(
        request: web.Request,
    ) -> web.Response:

        return web.json_response(
            {
                "status": "ok",
                "service": "Fitness Controller PRO",
            }
        )

    async def health(
        request: web.Request,
    ) -> web.Response:

        return web.json_response(
            {
                "status": "healthy",
            }
        )

    app.router.add_get(
        "/",
        index,
    )

    app.router.add_get(
        "/health",
        health,
    )

    logger.success("HTTP routes registered")
