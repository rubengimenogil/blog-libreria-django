# Blog Librería (Django) — guía completa para principiantes

Este README enseña, paso a paso, cómo está construido el proyecto, cómo ejecutarlo en Windows (PowerShell), cómo desplegarlo en Vercel y cómo diagnosticar problemas. Incluye un recorrido por los archivos para que puedas leer el código con confianza.

Índice
- Requisitos rápidos
- Inicio rápido (Windows PowerShell)
- Variables de entorno (.env) — plantilla
- Estructura del proyecto y recorrido de archivos
- Endpoints disponibles (UI y salud)
- Base de datos: SQLite vs PostgreSQL (Neon)
- Ficheros estáticos (Django + WhiteNoise + Vercel)
- Despliegue en Vercel (vercel.json)
- Tests (unitarios y en CI)
- CI/CD (GitHub Actions): tests + smoke tests
- Seguridad: checklist básico y ajustes
- Solución de problemas frecuentes (troubleshooting)

---

## Requisitos rápidos

- Python 3.11+ (3.12 recomendado)
- pip para instalar dependencias (ver `requirements.txt`)
- Acceso a una BD (opcional):
  - Local: SQLite automática (sin configuración)
  - Remota: PostgreSQL (Neon) vía `DATABASE_URL`

## Inicio rápido (Windows PowerShell)

1) Instala dependencias y prepara la BD
```pwsh
pip install -r requirements.txt
python manage.py migrate
```

2) (Opcional) Crea un usuario administrador
```pwsh
python manage.py createsuperuser
```

3) (Opcional) Carga datos de ejemplo
```pwsh
python manage.py loaddata posts/fixtures/sample_posts.json
```

4) Lanza el servidor en local
```pwsh
python manage.py runserver
```

5) Verifica en el navegador
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Salud runtime: http://127.0.0.1:8000/healthz/
- Salud BD: http://127.0.0.1:8000/db-healthz/

## Variables de entorno (.env) — plantilla

Para desarrollo local crea un archivo `.env` en la raíz del repo con algo como:

```env
# Seguridad y debug (desarrollo)
SECRET_KEY=dev-secret-unsafe
DEBUG=True

# Si usas PostgreSQL (Neon), descomenta y rellena. En local puedes omitirlo para usar SQLite.
# DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require

# Django settings module (opcional si usas manage.py)
DJANGO_SETTINGS_MODULE=blog.settings

# Opcional: hosts permitidos (útil en despliegue)
# ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.vercel.app
```

Notas:
- En producción, NO subas `.env` al repositorio; usa variables de entorno del proveedor (Vercel → Project Settings → Environment Variables).
- `DATABASE_URL` con `sslmode=require` es importante para proveedores gestionados como Neon.

## Estructura del proyecto y recorrido de archivos

```
api/
  index.py        # Punto ASGI de Django para Vercel (exporta `app`)
  healthz.py      # ASGI mínimo para /healthz sin tocar Django/BD
blog/
  settings.py     # Configuración: env, BD, estáticos, seguridad, tests
  urls.py         # Rutas de alto nivel; delega en `posts`
  asgi.py         # ASGI estándar del proyecto Django
  wsgi.py         # WSGI estándar (útil fuera de Vercel)
posts/
  models.py       # Modelo Post (title, content, published_date)
  views.py        # Vista de listado + endpoints de salud
  urls.py         # Rutas de la app
  admin.py        # Panel admin para Post
  templates/posts/index.html  # Plantilla principal
  static/post/style.css       # Estilos de la home
  fixtures/sample_posts.json  # Datos de ejemplo
  tests.py        # Pruebas mínimas
staticfiles/      # Salida de collectstatic (generado en build)
vercel.json       # Configuración de despliegue en Vercel
```

Pistas de lectura para principiantes (archivos más interesantes):
- `api/index.py`: cómo Vercel carga tu app ASGI y por qué exportamos `app`.
- `api/healthz.py`: ciclo ASGI (scope/receive/send) explicado paso a paso.
- `blog/settings.py`: saneo de `DATABASE_URL`, fallback a SQLite, estáticos con WhiteNoise, y estrategia de tests.
- `posts/views.py`: de la consulta ORM al render de la plantilla.
- `posts/templates/posts/index.html`: uso de `{% load static %}` y el bucle `{% for %}…{% empty %}`.

## Endpoints disponibles (UI y salud)

- `/` — Home: lista de posts (más recientes primero)
- `/admin/` — Panel de administración
- `/healthz/` — Health runtime ligero (no toca Django/BD; útil en Vercel)
- `/db-healthz/` — Health con BD (hace `SELECT 1`)
- `/static/...` — Archivos estáticos (CSS/JS/IMG)

## Base de datos: SQLite vs PostgreSQL (Neon)

- Desarrollo local: si no defines `DATABASE_URL`, se usa SQLite automáticamente. Sencillo y sin dependencias.
- Producción: define `DATABASE_URL` (Neon) y el proyecto la sanea para evitar parámetros problemáticos (`channel_binding`) y fuerza `sslmode=require`.
- Tests: por defecto se fuerzan en SQLite para que sean rápidos y deterministas (ver `IS_TESTING` y `USE_POSTGRES_FOR_TESTS` en `settings.py`).

Para ejecutar tests contra Postgres en CI (Neon):
- Proporciona `NEON_TEST_DATABASE_URL` como secret y `USE_POSTGRES_FOR_TESTS=1` (ya cableado en el workflow, ver más abajo).

## Ficheros estáticos (Django + WhiteNoise + Vercel)

- Desarrollo: `runserver` sirve `STATIC_URL=/static/` automáticamente.
- Producción: `python manage.py collectstatic --noinput` genera `staticfiles/` (no se versiona), y WhiteNoise los sirve con hashes y compresión.
- En `vercel.json`, hay una ruta dedicada para `/static/(.*)` hacia `staticfiles/$1`.

## Despliegue en Vercel (vercel.json)

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" },
    { "src": "api/healthz.py", "use": "@vercel/python" }
  ],
  "installCommand": "pip install -r requirements.txt",
  "buildCommand": "python manage.py collectstatic --noinput",
  "routes": [
    { "src": "/static/(.*)", "dest": "staticfiles/$1" },
    { "src": "/healthz/?", "dest": "api/healthz.py" },
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

Claves del despliegue:
- Se crean dos serverless functions: la app Django ASGI y el health ligero.
- `collectstatic` corre en build para tener `staticfiles/` listo.
- Las rutas envían `/static` a archivos, `/healthz` al health, y el resto a Django.

## Tests (unitarios y en CI)

Ejecutar localmente:
```pwsh
python manage.py test -v 2
```

Qué prueban:
- Modelo `Post`: `__str__` y orden por defecto (más recientes primero)
- Vista de índice: renderiza y respeta el orden
- Endpoints de salud: `/healthz` y `/db-healthz`

## CI/CD (GitHub Actions)

Hay dos workflows en `.github/workflows/` que se ejecutan en GitHub cuando haces push/PR, o manualmente desde la pestaña Actions.

### 1) `ci.yml` — Tests automáticos

Cuándo se ejecuta:
- En cada `push` a `main` y en cada `pull_request` hacia `main` (también manual con “Run workflow”).

Qué hace: define dos jobs independientes, uno siempre (SQLite) y otro opcional (Postgres/Neon):

- tests-sqlite (siempre)
  - Sistema: `ubuntu-latest`
  - Python: `3.12`
  - Pasos: checkout → configurar Python → cache de pip → instalar deps → ejecutar tests.
  - Variables de entorno en el paso de tests:
    - `SECRET_KEY`: clave dummy
    - `DEBUG='False'`: ejecuta como producción
    - `USE_POSTGRES_FOR_TESTS='0'`: fuerza SQLite (ver `settings.py`, sección de tests)
  - Comando: `python manage.py test --noinput -v 2`

- tests-postgres (opcional)
  - Solo corre si el secret `NEON_TEST_DATABASE_URL` está definido. El propio YAML calcula `HAS_NEON` y salta el job si está vacío.
  - Instala deps y ejecuta tests contra Postgres con:
    - `DATABASE_URL=${{ env.NEON_TEST_DATABASE_URL }}`
    - `USE_POSTGRES_FOR_TESTS='1'`
    - bandera `--keepdb` para no crear/eliminar la BD en cada ejecución (útil en Neon).
  - Requisitos previos:
    1. Crea en Neon una base/branch dedicada a tests (para no mezclar con producción).
    2. Copia la cadena de conexión y añádele `?sslmode=require` si no lo trae.
    3. En GitHub, ve a: Repo → Settings → Secrets and variables → Actions → New repository secret:
       - Nombre: `NEON_TEST_DATABASE_URL`
       - Valor: la URL completa (ej.: `postgresql://user:pass@host/db?sslmode=require`)
  - Notas prácticas:
    - Nuestro `settings.py` sanea `DATABASE_URL` removiendo `channel_binding` y forzando `sslmode=require` para evitar errores en entornos serverless.
    - Si el secret no existe, el job muestra “skipping Postgres tests” y no falla.

Cómo leer los logs:
- En la pestaña Actions → elige la ejecución → entra en cada step (“Install dependencies”, “Run Django tests…”) para ver salida completa.

Cómo desactivar/activar Postgres temporalmente:
- Basta con borrar (o no definir) el secret `NEON_TEST_DATABASE_URL`. El job quedará “skipped”.

### 2) `smoke.yml` — Smoke tests de despliegue

Objetivo: comprobar rápidamente que la web responde tras un despliegue en producción y en preview de Vercel.

Dos jobs separados:

- smoke-production (solo en push a `main`)
  - Requiere el secret `SMOKE_BASE_URL` (ej.: `https://blog-libreria-django.vercel.app`). Si no existe, se salta.
  - Qué comprueba (con reintentos):
    - Endpoints obligatorios: `/` y `/db-healthz/` deben devolver 200.
    - Endpoint opcional: `/healthz` (si existe) intentará 200; si falla, solo avisa.
    - Verifica además que desde `/` haya al menos un `<link href="...css">` y que dicho CSS responde 200 (best-effort).
  - Reintentos y tiempos:
    - Hasta 12 intentos por endpoint, con `sleep 5` entre intentos.
    - `curl` usa `--connect-timeout 5` y `--max-time 12` (evita bloqueos largos).
  - Fallo del job: si algún endpoint obligatorio no devuelve 200 tras los reintentos.

- smoke-preview-vercel (solo en `pull_request`)
  - Requiere `VERCEL_TOKEN` y `VERCEL_PROJECT_ID` como secrets (opcional `VERCEL_TEAM_ID`).
  - Pasos:
    1. Instala `jq` para parsear JSON.
    2. Resuelve la URL de preview llamando a la API de Vercel:
       - Primero busca el deployment `READY` asociado al commit (`meta-githubCommitSha`).
       - Si no lo encuentra, busca el último `READY` del proyecto (fallback).
       - Exporta `PREVIEW_BASE=https://<url>` para los siguientes pasos.
    3. Corre los mismos checks que producción (mandatory `/` y `/db-healthz/`, optional `/healthz`, y CSS enlazado).
  - Reintentos y tiempos (más paciencia por build en curso):
    - Hasta 20 intentos por endpoint, `sleep 8` entre intentos.
    - `curl` con `--max-time 5` para las sondas principales y `--max-time 12` para el HTML de la home.
  - Fallo del job: igual que producción (si fallan endpoints obligatorios tras reintentos).

Cómo crear los secrets para smoke:
- `SMOKE_BASE_URL`: la URL pública de producción (p.ej., el dominio de Vercel).
- `VERCEL_TOKEN`: crea un token en Vercel (Account → Settings → Tokens).
- `VERCEL_PROJECT_ID`: en Vercel, en Settings del proyecto → General → Project ID.
- `VERCEL_TEAM_ID` (opcional si el proyecto pertenece a un equipo): Settings del Team.
Ruta: GitHub → Repo → Settings → Secrets and variables → Actions → New repository secret.

Qué ver en los logs:
- El workflow imprime cada intento y el HTTP status recibido. Muestra un trozo del HTML (primeros ~300 bytes) para ayudar a diagnosticar redirecciones/errores.
- Si el CSS no se encuentra (no hay `<link rel="stylesheet" ...>`), solo emite un warning.

## Seguridad: checklist básico y ajustes

Comprobación automática de Django:
```pwsh
python manage.py check --deploy
```

Recomendaciones para producción:
- `DEBUG=0`, `SECRET_KEY` robusta (secreta), `ALLOWED_HOSTS` definidos.
- Cookies seguras: `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`.
- Redirección HTTPS si procede: `SECURE_SSL_REDIRECT=True` (o gestionado por el proxy/CDN).
- Considera HSTS: `SECURE_HSTS_SECONDS>0` cuando todo sea HTTPS estable.

## Solución de problemas frecuentes (troubleshooting)

- Error de migraciones (tabla no existe):
  ```pwsh
  python manage.py migrate
  ```

- Módulo no encontrado (imports): asegúrate de ejecutar comandos en la raíz del repo y con el venv activado.

- `ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured`:
  - Usa `manage.py` o exporta `DJANGO_SETTINGS_MODULE=blog.settings`.

- Fallo conectando a PostgreSQL (SSL/`channel_binding`):
  - Usa `sslmode=require` en `DATABASE_URL`. El código ya elimina `channel_binding` si viene.

  - Asegúrate de que `collectstatic` ha corrido (Vercel lo hace en build) y que la ruta `/static/(.*)` apunta a `staticfiles/`.

---

Con este recorrido, deberías poder leer y modificar el proyecto con confianza: el modelo define la estructura, la vista consulta y renderiza, las rutas exponen endpoints claros, `settings.py` orquesta entorno/BD/estáticos, y Vercel empaqueta la app en funciones ASGI con checks de salud útiles.
