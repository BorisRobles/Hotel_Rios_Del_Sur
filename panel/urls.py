from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .seguridad import LoginConBloqueoView

urlpatterns = [
    # Login con bloqueo tras 3 intentos fallidos
    path(
        'acceso/',
        LoginConBloqueoView.as_view(),
        name='login'
    ),

    # Cerrar sesión 
    path(
        'salir/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'panel/',
        views.inicio_panel,
        name='inicio_panel'
    ),

    # Recepción
    path(
        'panel/reservas/',
        views.lista_reservas,
        name='lista_reservas'
    ),

    path(
        'panel/reservas/<int:pk>/',
        views.detalle_reserva,
        name='detalle_reserva'
    ),

    path(
        'panel/reservas/<int:pk>/checkin/',
        views.checkin_reserva,
        name='checkin_reserva'
    ),

    path(
        'panel/reservas/<int:pk>/checkout/',
        views.checkout_reserva,
        name='checkout_reserva'
    ),

    path(
        'panel/reservas/<int:pk>/cancelar/',
        views.cancelar_reserva,
        name='cancelar_reserva'
    ),

    path(
        'panel/reservas/<int:pk>/pago/',
        views.pagar_reserva,
        name='pagar_reserva'
    ),

    path(
        'panel/reservas/<int:pk>/huespedes/',
        views.agregar_huesped,
        name='agregar_huesped'
    ),

        path(
        'panel/disponibilidad/',
        views.disponibilidad_panel,
        name='panel_disponibilidad'
    ),

    path(
        'panel/reservar/<int:habitacion_id>/',
        views.reservar_panel,
        name='panel_reservar'
    ),

    path(
        'panel/ocupacion/',
        views.estado_habitaciones,
        name='estado_habitaciones'
    ),

    # Administración
    path(
        'panel/habitaciones/',
        views.lista_habitaciones,
        name='lista_habitaciones'
    ),

    path(
        'panel/habitaciones/nueva/',
        views.agregar_habitacion,
        name='agregar_habitacion'
    ),

    path(
        'panel/habitaciones/<int:pk>/editar/',
        views.editar_habitacion,
        name='editar_habitacion'
    ),

        path(
        'panel/personal/',
        views.lista_personal,
        name='lista_personal'
    ),

    path(
        'panel/personal/<int:pk>/estado/',
        views.cambiar_estado_recepcionista,
        name='cambiar_estado_recepcionista'
    ),
]

    