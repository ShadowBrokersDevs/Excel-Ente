from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
import pandas as pd
import logging
import sqlite3
import os
import json
from django.conf import settings
import re
from django.utils.text import slugify
import unidecode
from .models import UserFile

# Configuración del logger
logger = logging.getLogger(__name__)


def sanitize_name(name):
    # Convertir a slug y latinizar
    name = name.strip().lower().replace(" ", "_").replace("-", "_")
    name = slugify(name, allow_unicode=True)
    name = unidecode.unidecode(name)
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    if name and name[0].isdigit():
        name = "_" + name
    return name


@login_required
def loader(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        logger.info(f"Datos del formulario: {request.POST} | Archivos: {request.FILES}")
        if form.is_valid():
            file = request.FILES.getlist("file")
            if file:
                file = file[0]
                if file.name.endswith((".csv", ".xls", ".xlsx", ".ods")):
                    db_name = file.name.rsplit(".", 1)[0]
                    db_name = sanitize_name(db_name)
                    if file.name.endswith(".csv"):
                        data = {db_name: pd.read_csv(file)}
                    elif file.name.endswith((".xls", ".xlsx")):
                        data = pd.read_excel(file, sheet_name=None)  # Return dict of DataFrame
                    elif file.name.endswith(".ods"):
                        data = pd.read_excel(file, engine="odf", sheet_name=None)  # Return dict of DataFrame

                    logger.info(f"Archivo subido: {file.name} | Nombre de base de datos: {db_name}")
                    # Guardar datos en un archivo
                    user_alias = request.user.username
                    with open(f"{settings.SESSION_FILE_PATH}/{user_alias}_{db_name}.json", "w") as f:
                        json_data = {
                            table_name: df.to_dict(orient="records") for table_name, df in data.items()
                        }
                        json.dump(json_data, f)
                    logger.info(
                        f"Datos guardados en: {settings.SESSION_FILE_PATH}/{user_alias}_{db_name}.json"
                    )
                    if db_name:
                        return redirect("data_manager:preview", db_name=db_name)
                    else:
                        form.add_error("file", "No se pudo determinar el nombre de la base de datos.")
                else:
                    form.add_error("file", "El archivo debe ser de tipo CSV, XLS, XLSX o ODS.")
            else:
                form.add_error("file", "No se ha seleccionado ningún archivo.")
        else:
            form.add_error("file", "El archivo debe ser de tipo CSV, XLS, XLSX o ODS.")
    else:
        form = FileUploadForm()
    return render(request, "data_manager/loader.html", {"form": form})


@login_required
def preview(request, db_name):
    if request.method == "POST":
        user_alias = request.user.username
        db_file = f"{user_alias}_{db_name}.sqlite3"

        # Asegurarse de que la tabla UserFile existe antes de usarla
        try:
            _, created = UserFile.objects.update_or_create(
                user=request.user.username,
                db_file=db_file,
            )
        except Exception as e:
            logger.error(f"Error al registrar el archivo: {e}")
            return render(request, "data_manager/error.html", {"error": "Error al registrar el archivo."})

        logger.info(f"Registrando: {db_file} | Creado:{created}")

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Cargar datos desde el archivo
        with open(f"{settings.SESSION_FILE_PATH}/{user_alias}_{db_name}.json", "r") as f:
            uploaded_data = json.load(f)
            logger.info(f"Datos recuperados de: {settings.SESSION_FILE_PATH}/{user_alias}_{db_name}.json")

        for table_name, records in uploaded_data.items():
            table_name = sanitize_name(table_name)
            if records:
                # Manejar columnas duplicadas
                columns = records[0].keys()
                unique_columns = {}
                new_columns = []

                for column in columns:

                    column = sanitize_name(column)

                    if column in unique_columns:
                        unique_columns[column] += 1
                        new_column_name = f"{column}_{chr(65 + unique_columns[column] - 1)}"  # A, B, C, ...
                    else:
                        unique_columns[column] = 1
                        new_column_name = column
                    new_columns.append(new_column_name)
                cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(new_columns)})')
                for record in records:
                    values = tuple(
                        record.get(column, None) for column in new_columns
                    )  # Obtener valores según los nuevos nombres
                    cursor.execute(
                        f'INSERT INTO "{table_name}" ({", ".join(new_columns)})'
                        f' VALUES ({", ".join(["?"] * len(values))})',
                        values,
                    )

        conn.commit()
        conn.close()
        logger.info(f"Base de datos guardada en: {db_file}")
        return redirect("data_manager:preview", db_name=db_name)
    else:
        with open(f"{settings.SESSION_FILE_PATH}/{db_name}.json", "r") as f:
            uploaded_data = json.load(f)

        html_dataframes = {
            table_name: pd.DataFrame(records)
            .head(15)
            .map(lambda x: x[:20] if isinstance(x, str) else x)
            .to_html(classes="dataframe", index=False)
            for table_name, records in uploaded_data.items()
        }
    return render(
        request,
        "data_manager/preview.html",
        {
            "html_dataframes": html_dataframes,
            "saved": False,
            "db_name": db_name,
        },
    )


@login_required
def database_view(request):
    user_alias = request.user.username

    # Obtener los db_file del usuario actual
    user_files = UserFile.objects.filter(user=user_alias)

    return render(
        request,
        "data_manager/database.html",
        {
            "user_files": user_files,  # Pasar la lista de archivos de usuario
        },
    )


@login_required
def database_edit_view(request):
    if request.method == "POST":
        db_name = request.POST.get("db_name")
        # Aquí puedes manejar la lógica para editar la base de datos
        # Procesar SQL desde el formulario
        return redirect("data_manager:database")


@login_required
def rename_database_view(request):
    if request.method == "POST":
        old_db_name = request.POST.get("db_name")
        new_db_name = request.POST.get("new_db_name")
        user_alias = request.user.username

        old_db_file = f"{user_alias}_{old_db_name}.sqlite3"
        new_db_file = f"{user_alias}_{new_db_name}.sqlite3"

        # Renombrar el archivo de la base de datos
        os.rename(old_db_file, new_db_file)
        UserFile.objects.filter(db_file=old_db_file).update(db_file=new_db_file)
        logger.info(f"Base de datos renombrada de {old_db_name} a {new_db_name}")
        return redirect("data_manager:database", db_name=new_db_name)
    else:
        return redirect("data_manager:database")


@login_required
def delete_database_view(request, id):
    user_alias = request.user.username
    user_file = UserFile.objects.get(id=id, user=user_alias)

    # Eliminar el archivo de la base de datos
    os.remove(f"{user_file.db_file}")
    user_file.delete()  # Eliminar la entrada de la base de datos

    logger.info(f"Base de datos eliminada: {user_file.db_file}")
    return redirect("data_manager:database")


@login_required
def db_info_view(request, id):
    user_alias = request.user.username
    user_file = UserFile.objects.get(id=id, user=user_alias)

    # Obtener información de la base de datos
    db_file_path = f"{user_file.db_file}"
    creation_time = os.path.getctime(db_file_path)
    modification_time = os.path.getmtime(db_file_path)

    # Obtener detalles de las tablas
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_details = {table[0]: table_info(cursor, table[0]) for table in tables}
    conn.close()

    return render(
        request,
        "data_manager/db_info.html",
        {
            "db_name": user_file.db_file,
            "creation_time": creation_time,
            "modification_time": modification_time,
            "table_details": table_details,
        },
    )


def table_info(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()
