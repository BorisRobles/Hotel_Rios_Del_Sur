from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from habitaciones.models import Habitacion


class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Huesped(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    documento = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class EstadoReserva(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):

    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    codigo_reserva = models.CharField(
        max_length=20,
        unique=True
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    estado = models.ForeignKey(
        EstadoReserva,
        on_delete=models.PROTECT
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()

    cantidad_personas = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    precio_total = models.PositiveIntegerField(default=0)

    estado_pago = models.CharField(
        max_length=15,
        choices=ESTADOS_PAGO,
        default='pendiente'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    huespedes = models.ManyToManyField(
        Huesped,
        through='ReservaHuesped',
        related_name='reservas'
    )

    def clean(self):
        super().clean()

        if self.fecha_entrada and self.fecha_salida:
            if self.fecha_salida <= self.fecha_entrada:
                raise ValidationError(
                    'La fecha de salida debe ser posterior a la entrada.'
                )

        if self.habitacion_id and self.cantidad_personas:
            if self.cantidad_personas > self.habitacion.capacidad:
                raise ValidationError(
                    'La cantidad de personas supera la capacidad.'
                )
    
    def estado_pago_mostrar(self):
        """
        Texto del pago para mostrar en pantalla.
        En una reserva cancelada no tiene sentido decir "Pendiente".
        """
        if self.estado.nombre == 'Cancelada':
            if self.estado_pago == 'pagado':
                return 'Pagado (por reembolsar)'
            return 'No aplica'

        return self.get_estado_pago_display()

    def __str__(self):
        return self.codigo_reserva


class ReservaHuesped(models.Model):
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE
    )

    huesped = models.ForeignKey(
        Huesped,
        on_delete=models.PROTECT
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reserva', 'huesped'],
                name='reserva_huesped_unico'
            )
        ]


class HistorialReserva(models.Model):

    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='historial'
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=50)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reserva.codigo_reserva} - {self.accion}'
