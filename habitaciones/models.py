from django.db import models
from django.core.validators import MinValueValidator


class Habitacion(models.Model):

    ESTADOS = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No disponible'),
        ('mantenimiento', 'En mantenimiento'),
    ]

    numero = models.CharField(max_length=6, unique=True)

    tipo = models.CharField(max_length=30)

    capacidad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    precio_noche = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    descripcion = models.CharField(
        max_length=255,
        blank=True
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='disponible'
    )

    def __str__(self):
        return f'Habitación {self.numero} - {self.tipo}'