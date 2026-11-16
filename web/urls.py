from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path(
        'disponibilidad/',
        views.buscar_disponibilidad,
        name='buscar_disponibilidad'
    ),

    path(
        'reservar/<int:habitacion_id>/',
        views.reservar_habitacion,
        name='reservar_habitacion'
    ),

    path(
        'reserva-confirmada/<str:codigo>/',
        views.reserva_confirmada,
        name='reserva_confirmada'
    ),

    
    path(
        'mi-reserva/',
        views.mi_reserva,
        name='mi_reserva'
    ),

    path(
        'mi-reserva/cancelar/',
        views.cancelar_mi_reserva,
        name='cancelar_mi_reserva'
    ),
]