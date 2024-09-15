from django.db import models


class PluginPermission(models.Model):
    plugin_name = models.CharField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    permission_name = models.CharField(max_length=100)
