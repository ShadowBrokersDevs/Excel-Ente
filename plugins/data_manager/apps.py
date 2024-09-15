from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DataTable, DataUpload  # Asegúrate de importar tus modelos


class ImportFileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "import_file"

    def ready(self):
        # Aquí puedes realizar inicializaciones, como registrar señales o cargar modelos
        pass  # Reemplaza esto con tu lógica


class DataManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins.data_manager"

    def ready(self):
        # Registrar señales para el modelo DataUpload
        post_save.connect(data_upload_post_save, sender=DataUpload)


@receiver(post_save, sender=DataTable)
def data_table_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Nuevo objeto creado: {instance}")


@receiver(post_save, sender=DataUpload)
def data_upload_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Nuevo archivo subido: {instance.file.name} por el usuario: {instance.user.username}")
