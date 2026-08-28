from django.urls import path

from . import views

app_name = 'vet'

urlpatterns = [
    path('', views.listado, name='listado'),
    path('nueva/', views.registrar, name='nueva'),
]