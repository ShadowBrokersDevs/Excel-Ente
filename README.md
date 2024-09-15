# Proyecto de Utilidad de Negocio para Análisis de Datos

## Importancia
Esta utilidad es crucial para que el equipo de negocio realice análisis de datos de manera eficiente y con lenguaje natural. Facilita la importación y manipulación de datos, permitiendo a los usuarios sin conocimientos técnicos realizar consultas complejas y obtener insights valiosos.

## Características
- **Carga de Archivos**: Soporta múltiples formatos (CSV, XLSX, ODS).
- **Transformaciones de Datos**: Permite realizar operaciones SQL y transformaciones con Pandas.
- **Integración con IA**: Facilita interacciones mediante un chat que utiliza la estructura de datos como contexto.
- **Persistencia de Datos**: Guarda el estado de trabajo del usuario para sesiones futuras.

## Instalación
1. Clona el repositorio.
2. Instala las dependencias requeridas.
3. Configura la base de datos.


```bash
# Clona el repositorio
git clone https://github.com/ShadowBrokersDevs/Excel-Ente.git

# Instala paquetes necesarios
sudo apt-get install libmemcached-dev

# Navega al directorio del proyecto
cd Excel-Ente

# Crea un entorno virtual e instala
poetry install

# Realiza las migraciones
poetry run python manage.py migrate

# Recopila los archivos estáticos
poetry run python manage.py collectstatic

# Inicia el servidor de desarrollo
poetry run python manage.py runserver
```

## Ejecutar tests

Para ejecutar los tests, usa el siguiente comando:

```bash
python manage.py test
```

Para obtener un informe de cobertura, instala `coverage` y ejecuta:

```bash
coverage run manage.py test
coverage report
```

## Uso
- Accede a la aplicación y carga tus archivos.
- Realiza consultas y transformaciones de datos.
- Interactúa con la IA para obtener análisis automatizados.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cambios.
