from django.urls import path
from .views import (
    loader,
    preview,
    database_view,
    database_edit_view,
    rename_database_view,
    delete_database_view,
    db_info_view,
)

app_name = "data_manager"

urlpatterns = [
    path("loader/", loader, name="loader"),
    path("preview/<str:db_name>/", preview, name="preview"),
    path("database/", database_view, name="database"),
    path("database/edit/", database_edit_view, name="database_edit"),
    path("database/rename/", rename_database_view, name="rename_database"),  # Ruta para renombrar
    path("database/delete/<int:id>/", delete_database_view, name="delete_database"),  # Ruta para eliminar
    path("database/info/<int:id>/", db_info_view, name="info_database"),
]
