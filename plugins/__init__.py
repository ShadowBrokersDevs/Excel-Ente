from django.apps import AppConfig

default_app_config = "plugins.apps.PluginsConfig"


class PluginsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins"


class MailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins.mail"


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins.telegram_bot"
