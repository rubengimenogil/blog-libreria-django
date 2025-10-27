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
