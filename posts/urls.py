from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('healthz/', views.healthz, name='healthz'),
    path('db-healthz/', views.db_healthz, name='db_healthz'),
]
