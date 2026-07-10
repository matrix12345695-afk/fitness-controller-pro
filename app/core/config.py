from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Fitness Controller PRO configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================================================
    # Telegram
    # ==========================================================

    bot_token: str = Field(..., alias="BOT_TOKEN")
    admin_id: int = Field(..., alias="ADMIN_ID")
    group_id: int = Field(..., alias="GROUP_ID")

    # ==========================================================
    # Database
    # ==========================================================

    database_url: str = Field(..., alias="DATABASE_URL")

    # ==========================================================
    # General
    # ==========================================================

    timezone: str = Field(
        default="Asia/Tashkent",
        alias="TIMEZONE",
    )

        default_language: str = Field(
        default="ru",
        alias="DEFAULT_LANGUAGE",
    )

    environment: str = Field(
        default="production",
        alias="ENVIRONMENT",
    )

    webhook_url: str = Field(
        default="",
        alias="WEBHOOK_URL",
    )

    webhook_path: str = Field(
        default="/webhook",
        alias="WEBHOOK_PATH",
    )

    webhook_secret: str = Field(
        default="fitness-controller-pro",
        alias="WEBHOOK_SECRET",
    )

    port: int = Field(
        default=10000,
        alias="PORT",
    )

    port: int = Field(
        default=10000,
        alias="PORT",
    )

    # ==========================================================
    # Survey
    # ==========================================================

    survey_start_hour: int = Field(
        default=20,
        alias="SURVEY_START_HOUR",
    )

    survey_start_minute: int = Field(
        default=0,
        alias="SURVEY_START_MINUTE",
    )

    reminder_1_hour: int = Field(
        default=21,
        alias="REMINDER_1_HOUR",
    )

    reminder_1_minute: int = Field(
        default=0,
        alias="REMINDER_1_MINUTE",
    )

    reminder_2_hour: int = Field(
        default=22,
        alias="REMINDER_2_HOUR",
    )

    reminder_2_minute: int = Field(
        default=0,
        alias="REMINDER_2_MINUTE",
    )

    survey_close_hour: int = Field(
        default=23,
        alias="SURVEY_CLOSE_HOUR",
    )

    survey_close_minute: int = Field(
        default=0,
        alias="SURVEY_CLOSE_MINUTE",
    )

    summary_hour: int = Field(
        default=23,
        alias="SUMMARY_HOUR",
    )

    summary_minute: int = Field(
        default=1,
        alias="SUMMARY_MINUTE",
    )

    # ==========================================================
    # Logging
    # ==========================================================

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached application settings.
    """
    return Settings()


settings = get_settings()
