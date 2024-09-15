from django.apps import AppConfig
import os
from django.utils.module_loading import import_string
from django.db import models
import sys
from django.conf import settings


class PluginsConfig(AppConfig):
    name = "plugins"
    verbose_name = "Plugins"

    def ready(self):
        for plugin in os.listdir(self.path):
            plugin_path = os.path.join(self.path, plugin)
            if os.path.isdir(plugin_path):
                try:
                    models_module = import_string(f"plugins.{plugin}.models")
                    for name, obj in vars(models_module).items():
                        if isinstance(obj, type) and issubclass(obj, models.Model):
                            setattr(sys.modules[__name__], name, obj)
                    templates_path = os.path.join(self.path, plugin, "templates")
                    if os.path.isdir(templates_path):
                        settings.TEMPLATES[0]["DIRS"].append(templates_path)

                    print(f"Plugin cargado: {plugin}")
                except ImportError as e:
                    print(f"No se pudo cargar el plugin: {plugin}. {e}")
                    continue
