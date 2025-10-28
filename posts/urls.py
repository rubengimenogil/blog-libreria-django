from django.urls import path
from . import views

# Rutas específicas de la app `posts`.
# Separar rutas por app mantiene el proyecto ordenado y fácil de mantener.
urlpatterns = [
    # Home: lista de entradas del blog
    path('', views.post_list, name='post_list'),

    # Comprobación de salud del runtime (sin tocar BD)
    path('healthz/', views.healthz, name='healthz'),

    # Comprobación de salud de la base de datos (hace SELECT 1)
    path('db-healthz/', views.db_healthz, name='db_healthz'),
]
