# Hotel Ríos del Sur – Instalación

Pasos para instalar y ejecutar el proyecto en otro computador (Windows).

---

## Requisitos previos

- [Python 3.13](https://www.python.org/downloads/) (al instalar, marcar **"Add Python to PATH"**)
- [XAMPP](https://www.apachefriends.org/) con MySQL/MariaDB 10.5 o superior
- Visual Studio Code u otro editor

---

## 1. Descomprimir el proyecto

Descomprimir el archivo ZIP recibido en cualquier carpeta (por ejemplo, en Documentos) y abrir esa carpeta en Visual Studio Code (**File → Open Folder**).

---

## 2. Importar la base de datos

1. Abrir el **XAMPP Control Panel** y pulsar **Start** en **Apache** y **MySQL**.
2. Entrar a http://localhost/phpmyadmin.
3. Crear una base de datos vacía llamada `hotel_prueba` con cotejamiento `utf8mb4_unicode_ci`.
4. Seleccionarla, ir a la pestaña **Importar**, elegir el archivo `base_de_datos/hotel_prueba.sql` y pulsar **Importar**.

---

## 3. Crear el entorno virtual e instalar dependencias

Abrir una terminal en la carpeta del proyecto (donde está `manage.py`) y ejecutar:

```powershell
python -m venv venv
venv\Scripts\activate
pip install "Django>=5.2,<5.3" mysqlclient python-dotenv
```

> Si PowerShell muestra un error de "ejecución de scripts deshabilitada", ejecutar una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
> y volver a ejecutar `venv\Scripts\activate`.

---

## 4. Revisar el archivo `.env`

El proyecto ya incluye un archivo `.env` junto a `manage.py`. Solo hay que modificarlo si el MySQL de XAMPP tiene contraseña: en ese caso, escribirla en `DB_PASSWORD`.

```
DB_NAME=hotel_prueba
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

## 5. Ejecutar el servidor

```powershell
python manage.py runserver
```

Abrir en el navegador:

| Página | Dirección |
|---|---|
| Sitio público | http://127.0.0.1:8000/ |
| Acceso del personal | http://127.0.0.1:8000/acceso/ |
| Administración de Django | http://127.0.0.1:8000/admin/ |

---

## Volver a abrir el proyecto más adelante

1. En XAMPP, pulsar **Start** en **MySQL**.
2. En la terminal, dentro de la carpeta del proyecto:

```powershell
venv\Scripts\activate
python manage.py runserver
```
