from django.contrib import admin
from .models import (
    Cliente,
    Huesped,
    EstadoReserva,
    Reserva,
    ReservaHuesped,
    HistorialReserva,
)

admin.site.register(Cliente)
admin.site.register(Huesped)
admin.site.register(EstadoReserva)
admin.site.register(Reserva)
admin.site.register(ReservaHuesped)
admin.site.register(HistorialReserva)