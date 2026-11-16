"""
Crea los grupos del personal con sus permisos y los estados de reserva.

Uso:
    python manage.py configurar_roles

Se puede ejecutar las veces que sea necesario: no duplica datos.
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from reservas.constantes import TODOS_LOS_ESTADOS
from reservas.models import EstadoReserva


# Principio de mínimo privilegio (OWASP):
# cada rol recibe solo los permisos que necesita para su trabajo.
PERMISOS_RECEPCIONISTA = [
    # Habitaciones: solo puede consultarlas
    'habitaciones.view_habitacion',

    # Reservas: consultar y gestionar (check-in, check-out, cancelar, pago)
    'reservas.view_reserva',
    'reservas.change_reserva',
    'reservas.view_estadoreserva',
    'reservas.view_historialreserva',

    # Clientes y huéspedes
    'reservas.view_cliente',
    'reservas.view_huesped',
    'reservas.add_huesped',
    'reservas.view_reservahuesped',
    'reservas.add_reservahuesped',
]

PERMISOS_ADMINISTRADOR = PERMISOS_RECEPCIONISTA + [
    # Administración de habitaciones
    'habitaciones.add_habitacion',
    'habitaciones.change_habitacion',

    # Corrección de datos
    'reservas.add_reserva',
    'reservas.change_cliente',
    'reservas.change_huesped',
]

# Nota: ningún rol tiene permisos de "delete".
# Las reservas no se borran, se cancelan, para conservar el historial.

GRUPOS = {
    'Recepcionista': PERMISOS_RECEPCIONISTA,
    'Administrador hotel': PERMISOS_ADMINISTRADOR,
}


class Command(BaseCommand):
    help = 'Crea los grupos del personal, sus permisos y los estados de reserva.'

    @transaction.atomic
    def handle(self, *args, **options):

        for nombre in TODOS_LOS_ESTADOS:
            _, creado = EstadoReserva.objects.get_or_create(nombre=nombre)
            if creado:
                self.stdout.write(f'  Estado creado: {nombre}')

        for nombre_grupo, permisos in GRUPOS.items():
            grupo, _ = Group.objects.get_or_create(name=nombre_grupo)

            objetos = []
            for permiso in permisos:
                app_label, codename = permiso.split('.')
                try:
                    objetos.append(Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    ))
                except Permission.DoesNotExist:
                    self.stderr.write(
                        f'  No existe el permiso {permiso}. '
                        '¿Ejecutaste "python manage.py migrate"?'
                    )

            grupo.permissions.set(objetos)
            self.stdout.write(
                f'  Grupo "{nombre_grupo}": {len(objetos)} permisos'
            )

        self.stdout.write(self.style.SUCCESS('Roles y estados configurados.'))
