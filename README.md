# Blog Librería (Django) — proyecto "blog", app "posts"

Aprendizaje guiado: este README explica a fondo cómo está construido el prototipo del blog, por qué se tomaron ciertas decisiones y cómo ejecutarlo en local y en Vercel.

Índice
- Requisitos y entorno
- Ejecutar en local (paso a paso)
- Estructura del proyecto y responsabilidades
- Diseño por requisitos del ejercicio (modelo, vista, plantilla, rutas)
- Datos de ejemplo y panel de administración
- Salud y diagnósticos (runtime y BD)
- Configuración de settings y variables de entorno
- Gestión de estáticos (Django + WhiteNoise + Vercel)
- Despliegue en Vercel (vercel.json explicado)
- Tests mínimos y cómo ejecutarlos
- Endurecimiento de seguridad y notas finales

## Requisitos y entorno

- Python 3.11+
- Dependencias en `requirements.txt` (Django, psycopg, dj-database-url, python-dotenv, whitenoise)
- Variables en `.env` para entorno local:
  - `SECRET_KEY` (cualquier string para desarrollo)
  - `DEBUG=True` (en local)
  - `DATABASE_URL` (PostgreSQL de Neon; ver ejemplo en `.env`)

## Ejecutar en local (paso a paso)

```pwsh
pip install -r requirements.txt
python manage.py migrate
# (opcional) python manage.py createsuperuser
# (opcional) cargar datos de ejemplo
python manage.py loaddata posts/fixtures/sample_posts.json

python manage.py runserver
```

Verifica:
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Salud runtime: http://127.0.0.1:8000/healthz/
- Salud BD: http://127.0.0.1:8000/db-healthz/

## Estructura del proyecto y responsabilidades

```
api/
  index.py        # Entry ASGI de Django para Vercel (expone `app`)
  healthz.py      # Función ASGI mínima para `/healthz` sin tocar Django/BD
blog/
  settings.py     # Configuración (env, BD, estáticos, hosts, etc.)
  urls.py         # Incluye las rutas de la app `posts`
  asgi.py,wsgi.py # Entrypoints estándar del proyecto Django
posts/
  models.py       # Modelo `Post`
  views.py        # Vistas: índice + endpoints de salud
  urls.py         # Rutas de la app
  admin.py        # Registro de `Post` en el admin
  templates/posts/index.html  # Plantilla
  static/post/style.css       # Estilos
  fixtures/sample_posts.json  # Datos de ejemplo
  tests.py        # Tests mínimos
staticfiles/      # Salida de `collectstatic` (no se versiona)
vercel.json       # Configuración de despliegue en Vercel
```

Separación de responsabilidades (por qué):
- `api/` contiene puntos de entrada para el runtime sin acoplarse al proyecto Django (patterns comunes en Vercel).
- `blog/` es el proyecto Django (settings, enrutado global).
- `posts/` encapsula dominio y UI del blog: modelo, vistas, plantillas y assets.
- `staticfiles/` es solo salida de build para producción (no se versiona).

## Diseño por requisitos del ejercicio

1) Modelo de datos (`posts/models.py`)

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]  # más recientes primero
```

Decisiones:
- `auto_now_add=True` fija la fecha automáticamente al crear (ideal para un prototipo).
- `Meta.ordering` garantiza orden inverso por defecto a nivel ORM (coincide con el requisito del cliente).

2) Vista personalizada (`posts/views.py`)

```python
def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'posts/index.html', {'posts': posts})
```

Contratos y errores:
- Entrada: GET anónimo.
- Salida: HTML renderizado con `posts` en contexto.
- Errores típicos evitados: si la BD no existe o no hay migraciones → 500. Por eso añadimos endpoints de salud y guía de migraciones.

3) Plantilla visual (`posts/templates/posts/index.html`)
- Itera `posts` y pinta título, fecha y contenido.
- Estilos en `posts/static/post/style.css` (aplicables tras `collectstatic` en prod, servidos por `django.contrib.staticfiles` en dev).

4) Sistema de rutas (`blog/urls.py` y `posts/urls.py`)
- `blog/urls.py` incluye `path('', include('posts.urls'))` ⇒ la home es la vista de posts.
- `posts/urls.py` define `''` → `post_list`, `healthz/` y `db-healthz/`.

## Datos de ejemplo y admin

Crear usuario admin (opcional):
```pwsh
python manage.py createsuperuser
```

Cargar datos de ejemplo:
```pwsh
python manage.py loaddata posts/fixtures/sample_posts.json
```

Panel de admin: http://127.0.0.1:8000/admin/
- `posts/admin.py` registra el modelo con columnas y búsqueda útil para gestionar contenidos.

## Salud y diagnósticos

- `/healthz` (Vercel): función ASGI en `api/healthz.py`. No toca Django ni la BD → confirma que el runtime está vivo.
- `/db-healthz/` (Django): ejecuta `SELECT 1` vía `django.db.connection` → confirma conectividad real a la BD.

Por qué dos checks:
- Para distinguir problemas de runtime/routing (ASGI) de problemas de base de datos.

## Configuración de settings y variables de entorno

`blog/settings.py`:
- Carga `.env` en local con `python-dotenv`.
- `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` admiten despliegues en `*.vercel.app`.
- BD: usa `DATABASE_URL` (Neon) y la sanea (elimina `channel_binding` y fuerza `sslmode=require`) para evitar incompatibilidades en ciertos runtimes.
- Fallback local (si no hay `DATABASE_URL`): SQLite en `/tmp/db.sqlite3` para que incluso en entornos de solo lectura el proyecto arranque.
- Estáticos: `STATIC_ROOT = BASE_DIR / 'staticfiles'` y `WhiteNoise` con `CompressedManifestStaticFilesStorage`.

Variables en Vercel (Panel → Settings → Environment Variables):
- `SECRET_KEY`: seguro.
- `DEBUG=0`.
- `DATABASE_URL`: cadena de Neon.
- (Opcional) `ALLOWED_HOSTS`/`DJANGO_ALLOWED_HOSTS`: tu dominio en Vercel (sin `https://`).

## Gestión de estáticos

- En desarrollo, `runserver` sirve `STATIC_URL=/static/` sin `collectstatic`.
- En producción (Vercel), `collectstatic` genera `staticfiles/` → servido por la ruta de vercel.json.
- `staticfiles/` no se versiona; se crea en cada build. Esto evita inconsistencias y reduce el repo.

## Despliegue en Vercel (vercel.json explicado)

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

Claves:
- Se construyen dos funciones: la ASGI de Django (`api/index.py`) y el health runtime (`api/healthz.py`).
- `collectstatic` corre en build, dejando listo `staticfiles/`.
- El ruteo sirve `/static/...` desde `staticfiles` y el resto pasa a Django.

## Tests mínimos

```pwsh
python manage.py test posts -v 2
```

Nota: durante los tests forzamos SQLite automáticamente (ver `blog/settings.py`) para evitar problemas al crear/eliminar bases de datos temporales en proveedores gestionados como Neon. Esto hace que los tests sean rápidos y deterministas.

Cubren:
- `__str__` del modelo.
- Orden por defecto más recientes primero.
- Render del índice con orden correcto.

## Endurecimiento de seguridad (cuando salgas de prototipo)

Ejecuta el chequeo:
```pwsh
python manage.py check --deploy
```

Recomendado en producción:
- `DEBUG=0` y logs adecuados.
- `SECURE_SSL_REDIRECT=True` (o manejarlo en el proxy de Vercel).
- Cookies seguras: `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`.
- Considerar `SECURE_HSTS_SECONDS>0` si todo es HTTPS.

---

Con esto deberías entender cómo se conecta cada pieza: el modelo define la estructura y el orden; la vista consulta y entrega contexto a la plantilla; las rutas exponen la UI y checks; settings orquesta entorno/BD/estáticos; y Vercel empaqueta todo en funciones serverless con ASGI.

## Documentación detallada de archivos (guía rápida)

- `api/index.py` — Punto de entrada ASGI para Vercel.
  - Inserta la raíz del repo en PYTHONPATH, fija `DJANGO_SETTINGS_MODULE` y exporta `app`.
  - Todas las rutas (excepto `/static` y `/healthz`) llegan aquí según `vercel.json`.

- `api/healthz.py` — ASGI mínimo para `/healthz` sin arrancar Django.
  - Responde `{ "ok": true }` y evita abrir conexiones a BD.

- `blog/settings.py` — Configuración central.
  - Variables de entorno con `python-dotenv` para entorno local.
  - Seguridad: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
  - Base de datos: parseo de `DATABASE_URL` con saneado (quita `channel_binding` y fuerza `sslmode=require`).
  - Estáticos: `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_STORAGE = CompressedManifestStaticFilesStorage` (hash + compresión).
  - Tests: SQLite por defecto; Postgres opcional con `USE_POSTGRES_FOR_TESTS=1`.

- `blog/urls.py` — Rutas globales.
  - `admin/` → admin de Django; `''` → incluye rutas de la app `posts`.

- `blog/wsgi.py` — Entrypoint WSGI clásico para `runserver` y compatibilidad.

- `posts/models.py` — Modelo `Post`; orden estable: más recientes primero y desempate por `-id`.

- `posts/views.py` — Vistas: `post_list`, `healthz`, `db_healthz`.

- `posts/urls.py` — Enrutado: home + endpoints de salud.

- `posts/admin.py` — Admin: columnas visibles, búsqueda y orden.

- `posts/tests.py` — Tests de dominio, vista y salud; valida que existe `<link>` al CSS.

- `posts/templates/posts/index.html` — Plantilla del listado; usa `{% static 'post/style.css' %}`.

- `posts/static/post/style.css` — Estilos base del blog. En producción se sirve con nombre hasheado.

- `vercel.json` — Despliegue en Vercel (JSON no admite comentarios; documentado aquí):
  - builds: `api/index.py` y `api/healthz.py` con `@vercel/python`.
  - install/build: `pip install -r requirements.txt` + `python manage.py collectstatic --noinput`.
  - routes: `/static/(.*)` → `staticfiles/$1`, `/healthz` → `api/healthz.py`, catch-all → `api/index.py`.

## WhiteNoise + Manifest: cómo funcionan los estáticos en producción

- Con `STATICFILES_STORAGE = whitenoise.storage.CompressedManifestStaticFilesStorage` y `DEBUG=False`:
  - `collectstatic` genera nombres con hash: `/static/post/style.abc123.css`.
  - `{% static 'post/style.css' %}` en plantilla resolverá la versión hasheada.
  - Pedir el nombre plano (`/static/post/style.css`) devolverá 404 (esperado).

Checklist para evitar 404 de CSS en Vercel:
1. Asegura `DEBUG=False` en Variables de Entorno de Vercel.
2. `vercel.json` ya ejecuta `collectstatic` en build.
3. La plantilla usa `{% static 'post/style.css' %}` (ya hecho).
4. Verifica que el `<link>` de la home apunta a `/static/.../<hash>.css` y responde 200.

## Smoke tests (producción y previews)

- El workflow `smoke.yml` comprueba:
  - `GET /` y `GET /db-healthz/` deben ser 200.
  - `GET /healthz` es opcional (ASGI ligero).
  - Extrae un `<link rel="stylesheet">` de la home y verifica que devuelve 200.
- Recomendación: cuando tengas estable el hash en producción, puedes endurecer la validación
  para exigir que el nombre del CSS contenga un hash (p.ej. `style.[a-f0-9]{8,}.css`).

## Variables de entorno (producción)

Define en Vercel → Settings → Environment Variables:
- `SECRET_KEY` — Una segura.
- `DEBUG=False`
- `DATABASE_URL` — Cadena de conexión Neon (con `sslmode=require`).

## Glosario

- ASGI: Interfaz asíncrona para servidores web Python. En Vercel usamos ASGI con Django (`api/index.py`).
- WSGI: Interfaz síncrona clásica. Se usa en `manage.py runserver` y queda para compatibilidad (`blog/wsgi.py`).
- WhiteNoise: Middleware que sirve archivos estáticos directamente desde Django.
- Manifest (StaticFilesStorage): Sistema que renombra archivos estáticos con hash para cache-busting.
- `collectstatic`: Comando que compila/copía los estáticos a `STATIC_ROOT` para servir en producción.
- Neon: Proveedor de PostgreSQL serverless; expone una `DATABASE_URL` que usamos con `dj-database-url`.
- Vercel: Plataforma serverless donde desplegamos funciones (Python) y rutas de archivos estáticos.

## FAQ

1) ¿Por qué me da 404 en `/static/post/style.css` en producción?
- Porque en producción usamos Manifest: el archivo real se llama `style.<hash>.css`.
- Solución: usa `{% static 'post/style.css' %}` en plantillas (ya hecho), `DEBUG=False` y asegúrate de correr `collectstatic` en build (ya en `vercel.json`).

2) ¿Cómo compruebo que el CSS llega bien en los smoke tests?
- El workflow extrae el primer `<link rel="stylesheet">` de la home y lo solicita; si responde 200, OK.
- Opcional: endurecer el test para exigir que el nombre contenga un hash (p.ej. `style.[a-f0-9]{8,}.css`).

3) ¿Qué pasa si no tengo `DATABASE_URL` en local?
- El proyecto hace fallback a SQLite (en `/tmp/db.sqlite3` para compatibilidad con entornos de solo lectura).

4) ¿Cómo pruebo contra Postgres en CI?
- Exporta `USE_POSTGRES_FOR_TESTS=1` y provee `DATABASE_URL` (en nuestro caso, `NEON_TEST_DATABASE_URL` como secret). El job opcional de Postgres lo recoge.

5) ¿Por qué saneamos `DATABASE_URL` y forzamos `sslmode=require`?
- Algunos runtimes tienen libpq sin channel binding; si la URL trae `channel_binding=require` puede fallar la conexión.
- Forzar `sslmode=require` es buena práctica en entornos gestionados y coincide con las recomendaciones de Neon.

## Pautas para comentar plantillas y estilo HTML/CSS

Plantillas (Django + HTML):
- Usa comentarios HTML `<!-- ... -->` y evita incluir sintaxis de Django dentro del comentario (no escribas `{% ... %}` o `{{ ... }}` en comentarios), ya que el parser de plantillas podría intentar interpretarlos.
- Carga estáticos con `{% load static %}` y genera rutas con `{% static 'ruta/archivo.ext' %}`; no hardcodees `/static/...`.
- Considera crear una plantilla base `base.html` con bloques `{% block head %}` y `{% block content %}` para reutilizar estructura.
- Mantén los comentarios informativos y no invasivos; para documentación extensa, usa este README en lugar de llenar el HTML.

CSS:
- Usa comentarios `/* ... */` en los fuentes dentro de `posts/static/...`.
- No edites la salida de `staticfiles/`; es generada por `collectstatic`.
- Tras cambios en CSS, vuelve a ejecutar `collectstatic` para regenerar el hash (en producción, lo hace el build de Vercel).
- Si introduces utilidades o convenciones (p.ej., BEM), documenta el patrón al inicio del CSS.
