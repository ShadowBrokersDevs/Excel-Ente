from django.apps import AppConfig, apps


class PluginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins"


class BasePlugin:
    name = "Base Plugin"
    description = "Descripción base del plugin"

    @classmethod
    def is_enabled(cls, user):
        """Verifica si el plugin está habilitado para el usuario"""
        UserPluginPreference = apps.get_model("users", "UserPluginPreference")
        try:
            preference = UserPluginPreference.objects.get(user=user, plugin_name=cls.name)
            return preference.is_enabled
        except UserPluginPreference.DoesNotExist:
            return True  # Por defecto, el plugin está habilitado

    @classmethod
    def get_urls(cls):
        # Devuelve las URLs específicas del plugin
        return []

    @classmethod
    def get_models(cls):
        # Devuelve los modelos específicos del plugin
        return []
