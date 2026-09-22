# tienda/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Mascotas
    path('mascotas/', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/crear/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/editar/<int:id>/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:id>/', views.eliminar_mascota, name='eliminar_mascota'),

    # Productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Citas
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/editar/<int:id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:id>/', views.eliminar_cita, name='eliminar_cita'),
    path('citas/confirmar/<int:id>/', views.confirmar_cita, name='confirmar_cita'),
]