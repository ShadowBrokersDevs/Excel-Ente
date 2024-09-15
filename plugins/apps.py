from django.apps import AppConfig
import os
from django.utils.module_loading import import_string


class PluginsConfig(AppConfig):
    name = "plugins"
    verbose_name = "Plugins"

    def ready(self):
        plugins_dir = os.path.join(self.path, "plugins")
        for plugin in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, plugin)
            if os.path.isdir(plugin_path):
                try:
                    import_string(f"plugins.{plugin}.models")
                except ImportError:
                    print(f"No se pudo cargar el plugin: {plugin}")
                    continue
