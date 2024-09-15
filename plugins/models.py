from django.contrib.auth.models import User
from django.db import models

from users.models import Role


class PluginPermission(models.Model):
    plugin_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("plugin_name", "role", "permission_name")
