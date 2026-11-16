import unicodedata
import uuid

from itertools import combinations
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from habitaciones.models import Habitacion
from .constantes import (
    CANCELADA,
    EN_CURSO,
    ESTADOS_POR_LLEGAR,
    ESTADOS_QUE_OCUPAN,
    FINALIZADA,
    MAX_NOCHES,
)
from .models import (
    Cliente,
    Huesped,
    EstadoReserva,
    HistorialReserva,
    Reserva,
    ReservaHuesped,
)

def _normalizar_texto(texto):
    """'  Méndez ' -> 'mendez' (sin tildes, mayúsculas ni espacios extra)."""
    sin_tildes = unicodedata.normalize('NFKD', texto or '')
    sin_tildes = ''.join(c for c in sin_tildes if not unicodedata.combining(c))
    return ' '.join(sin_tildes.split()).casefold()

def crear_reserva(
    habitacion_id,
    fecha_entrada,
    fecha_salida,
    cantidad_personas,
    datos_cliente,
    usuario=None
):
    """
    Crea una reserva confirmada, evitando reservas
    superpuestas para una misma habitación.
    """

    with transaction.atomic():

        # Bloqueamos la habitación mientras se crea
        # la reserva para evitar conflictos simultáneos.
        habitacion = Habitacion.objects.select_for_update().get(
            pk=habitacion_id
        )

        # Validar estado de la habitación
        if habitacion.estado != 'disponible':
            raise ValidationError(
                'Esta habitación no está habilitada para reservas.'
            )

        # Validar fechas
        if fecha_entrada < timezone.localdate():
            raise ValidationError(
                'La fecha de entrada no puede ser anterior a hoy.'
            )

        if fecha_salida <= fecha_entrada:
            raise ValidationError(
                'La fecha de salida debe ser posterior a la entrada.'
            )

        if (fecha_salida - fecha_entrada).days > MAX_NOCHES:
            raise ValidationError(
                f'No se puede reservar más de {MAX_NOCHES} noches seguidas.'
            )

        # Validar cantidad de personas
        if cantidad_personas < 1:
            raise ValidationError(
                'La cantidad de personas debe ser mayor que cero.'
            )

        if cantidad_personas > habitacion.capacidad:
            raise ValidationError(
                'La habitación no tiene capacidad suficiente.'
            )

        # Comprobar reservas que se superponen
        existe_reserva = Reserva.objects.filter(
            habitacion=habitacion,
            fecha_entrada__lt=fecha_salida,
            fecha_salida__gt=fecha_entrada,
            estado__nombre__in=ESTADOS_QUE_OCUPAN
        ).exists()

        if existe_reserva:
            raise ValidationError(
                'La habitación ya está reservada para esas fechas.'
            )

        # Registrar al cliente, o reutilizarlo si ya reservó antes
        cliente, cliente_creado = Cliente.objects.get_or_create(
            documento=datos_cliente['documento'],
            defaults={
                'nombre': datos_cliente['nombre'],
                'apellido': datos_cliente['apellido'],
                'telefono': datos_cliente['telefono'],
                'correo': datos_cliente['correo'],
            }
        )

        if not cliente_creado:
            # Cliente frecuente: el RUT ya existe.
            # Solo se acepta si el nombre coincide; así nadie puede usar
            # un RUT ajeno para modificar los datos de otra persona.
            mismo_nombre = (
                _normalizar_texto(cliente.nombre)
                == _normalizar_texto(datos_cliente['nombre'])
                and _normalizar_texto(cliente.apellido)
                == _normalizar_texto(datos_cliente['apellido'])
            )

            if not mismo_nombre:
                raise ValidationError(
                    'Este RUT ya está registrado con otro nombre. '
                    'Revisa los datos o contacta con recepción.'
                )

            # Se actualizan los datos de contacto por si cambiaron
            cliente.telefono = datos_cliente['telefono']
            cliente.correo = datos_cliente['correo']
            cliente.save(update_fields=['telefono', 'correo'])

        # Calcular precio total
        noches = (fecha_salida - fecha_entrada).days
        precio_total = noches * habitacion.precio_noche

        # Obtener estado de reserva
        estado_confirmada = EstadoReserva.objects.get(
            nombre='Confirmada'
        )

        # Generar código único
        codigo = 'HRS-' + uuid.uuid4().hex[:12].upper()

        # Crear reserva
        reserva = Reserva(
            codigo_reserva=codigo,
            cliente=cliente,
            habitacion=habitacion,
            estado=estado_confirmada,
            usuario=usuario,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            cantidad_personas=cantidad_personas,
            precio_total=precio_total,
            estado_pago='pendiente'
        )

        reserva.full_clean()
        reserva.save()

        # Armar la lista de todas las personas que se alojarán:
        # el cliente (si se aloja) + los huéspedes huesped_1 ... huesped_N
        huespedes = []

        if datos_cliente.get('cliente_es_huesped'):
            huespedes.append({
                'nombre': datos_cliente['nombre'],
                'apellido': datos_cliente['apellido'],
                'documento': datos_cliente['documento'],
            })

        adicionales = cantidad_personas - len(huespedes)

        for numero in range(1, adicionales + 1):
            huespedes.append({
                'nombre': datos_cliente[f'huesped_{numero}_nombre'],
                'apellido': datos_cliente[f'huesped_{numero}_apellido'],
                'documento': datos_cliente[f'huesped_{numero}_documento'],
            })

        documentos = [h['documento'] for h in huespedes]

        if len(documentos) != len(set(documentos)):
            raise ValidationError(
                'Hay huéspedes con el mismo documento. '
                'Cada persona debe tener un documento distinto.'
            )

        # Registrar cada huésped (o reutilizarlo si ya existe)
        # y relacionarlo con la reserva
        for datos_huesped in huespedes:
            huesped, _ = Huesped.objects.get_or_create(
                documento=datos_huesped['documento'],
                defaults={
                    'nombre': datos_huesped['nombre'],
                    'apellido': datos_huesped['apellido'],
                }
            )

            ReservaHuesped.objects.create(
                reserva=reserva,
                huesped=huesped
            )

        registrar_historial(reserva, usuario, 'Reserva creada')

        return reserva



# OPERACIONES DE RECEPCIÓN
# Cada operación:
#   - bloquea la reserva mientras se modifica,
#   - valida que el cambio sea permitido,
#   - deja registro en el historial (quién y cuándo).


def registrar_historial(reserva, usuario, accion):
    HistorialReserva.objects.create(
        reserva=reserva,
        usuario=usuario,
        accion=accion[:50]
    )


def _obtener_reserva_bloqueada(reserva_id):
    return (
        Reserva.objects
        .select_for_update()
        .select_related('estado', 'habitacion')
        .get(pk=reserva_id)
    )


def _cambiar_estado(reserva, nombre_estado):
    reserva.estado = EstadoReserva.objects.get(nombre=nombre_estado)
    reserva.save(update_fields=['estado', 'fecha_modificacion'])


def cancelar_reserva(reserva_id, usuario):
    with transaction.atomic():
        reserva = _obtener_reserva_bloqueada(reserva_id)

        if reserva.estado.nombre not in ESTADOS_POR_LLEGAR:
            raise ValidationError(
                'Solo se pueden cancelar reservas pendientes o '
                'confirmadas que aún no hacen check-in.'
            )

        _cambiar_estado(reserva, CANCELADA)
        registrar_historial(reserva, usuario, 'Reserva cancelada')

        return reserva

def cancelar_reserva_cliente(reserva_id):
    """
    Cancelación hecha por el propio cliente desde el sitio web.
    Solo se permite antes del día de llegada.
    """
    with transaction.atomic():
        reserva = _obtener_reserva_bloqueada(reserva_id)

        if reserva.estado.nombre not in ESTADOS_POR_LLEGAR:
            raise ValidationError('Esta reserva ya no se puede cancelar.')

        if timezone.localdate() >= reserva.fecha_entrada:
            raise ValidationError(
                'La reserva solo se puede cancelar en línea hasta el día '
                'anterior a la llegada. Comunícate con recepción.'
            )

        _cambiar_estado(reserva, CANCELADA)
        registrar_historial(reserva, None, 'Reserva cancelada por el cliente')

        return reserva

def hacer_checkin(reserva_id, usuario):
    with transaction.atomic():
        reserva = _obtener_reserva_bloqueada(reserva_id)
        hoy = timezone.localdate()

        if reserva.estado.nombre not in ESTADOS_POR_LLEGAR:
            raise ValidationError(
                'Esta reserva no está en condiciones de hacer check-in.'
            )

        if hoy < reserva.fecha_entrada:
            raise ValidationError(
                'El check-in solo se puede hacer desde la fecha de entrada '
                f'({reserva.fecha_entrada:%d/%m/%Y}).'
            )

        if hoy >= reserva.fecha_salida:
            raise ValidationError(
                'La fecha de salida de esta reserva ya pasó.'
            )

        if reserva.habitacion.estado != 'disponible':
            raise ValidationError(
                'La habitación no está habilitada (mantenimiento o '
                'no disponible). Reasigna o revisa la habitación.'
            )

        habitacion_ocupada = Reserva.objects.filter(
            habitacion=reserva.habitacion,
            estado__nombre=EN_CURSO
        ).exclude(pk=reserva.pk).exists()

        if habitacion_ocupada:
            raise ValidationError(
                'La habitación todavía está ocupada por otro huésped. '
                'Primero realiza el check-out de esa reserva.'
            )

        if not reserva.huespedes.exists():
            raise ValidationError(
                'Registra al menos un huésped antes del check-in.'
            )

        _cambiar_estado(reserva, EN_CURSO)
        registrar_historial(reserva, usuario, 'Check-in realizado')

        return reserva


def hacer_checkout(reserva_id, usuario):
    with transaction.atomic():
        reserva = _obtener_reserva_bloqueada(reserva_id)

        if reserva.estado.nombre != EN_CURSO:
            raise ValidationError(
                'Solo se puede hacer check-out de una reserva en curso.'
            )

        if reserva.estado_pago != 'pagado':
            raise ValidationError(
                'Registra el pago antes de hacer el check-out.'
            )

        _cambiar_estado(reserva, FINALIZADA)
        registrar_historial(reserva, usuario, 'Check-out realizado')

        return reserva


def registrar_pago(reserva_id, usuario):
    with transaction.atomic():
        reserva = _obtener_reserva_bloqueada(reserva_id)

        if reserva.estado.nombre == CANCELADA:
            raise ValidationError(
                'No se puede registrar el pago de una reserva cancelada.'
            )

        if reserva.estado_pago == 'pagado':
            raise ValidationError('Esta reserva ya figura como pagada.')

        reserva.estado_pago = 'pagado'
        reserva.save(update_fields=['estado_pago', 'fecha_modificacion'])
        registrar_historial(reserva, usuario, 'Pago registrado')

        return reserva


def agregar_huesped(reserva_id, datos, usuario):
    """
    Registra un huésped (o reutiliza uno existente por documento)
    y lo asocia a la reserva, respetando la cantidad de personas.
    """
    with transaction.atomic():
        reserva = _obtener_reserva_bloqueada(reserva_id)

        if reserva.estado.nombre not in ESTADOS_QUE_OCUPAN:
            raise ValidationError(
                'No se pueden agregar huéspedes a una reserva '
                'finalizada o cancelada.'
            )

        if reserva.huespedes.count() >= reserva.cantidad_personas:
            raise ValidationError(
                'La reserva ya tiene registrados todos sus huéspedes '
                f'({reserva.cantidad_personas}).'
            )

        huesped, _ = Huesped.objects.get_or_create(
            documento=datos['documento'],
            defaults={
                'nombre': datos['nombre'],
                'apellido': datos['apellido'],
            }
        )

        if reserva.huespedes.filter(pk=huesped.pk).exists():
            raise ValidationError(
                'Este huésped ya está registrado en la reserva.'
            )

        ReservaHuesped.objects.create(reserva=reserva, huesped=huesped)
        registrar_historial(
            reserva,
            usuario,
            f'Huésped agregado: {huesped.documento}'
        )

        return huesped


# SUGERENCIA DE FECHAS ALTERNATIVAS
# Si no hay habitaciones para las fechas pedidas, busca las fechas
# más cercanas (antes o después) con la misma cantidad de noches.

def sugerir_fechas(fecha_entrada, fecha_salida, cantidad_personas,
                   cantidad_sugerencias=3, dias_busqueda=30):

    noches = (fecha_salida - fecha_entrada).days
    hoy = timezone.localdate()

    # Habitaciones que podrían servir (habilitadas y con capacidad)
    candidatas = list(
        Habitacion.objects.filter(
            estado='disponible',
            capacidad__gte=cantidad_personas
        ).values_list('pk', flat=True)
    )

    if not candidatas:
        return []

    # Se cargan una sola vez todas las reservas del rango a revisar
    desde = max(hoy, fecha_entrada - timedelta(days=dias_busqueda))
    hasta = fecha_salida + timedelta(days=dias_busqueda)

    reservas = list(
        Reserva.objects.filter(
            habitacion_id__in=candidatas,
            estado__nombre__in=ESTADOS_QUE_OCUPAN,
            fecha_entrada__lt=hasta,
            fecha_salida__gt=desde,
        ).values_list('habitacion_id', 'fecha_entrada', 'fecha_salida')
    )

    def habitaciones_libres(inicio, fin):
        ocupadas = {
            habitacion
            for habitacion, entrada, salida in reservas
            if entrada < fin and salida > inicio
        }
        return len(candidatas) - len(ocupadas)

    sugerencias = []

    # Se revisan los días más cercanos primero: -1, +1, -2, +2, ...
    for distancia in range(1, dias_busqueda + 1):
        for sentido in (-1, 1):
            inicio = fecha_entrada + timedelta(days=distancia * sentido)

            if inicio < hoy:
                continue

            fin = inicio + timedelta(days=noches)
            libres = habitaciones_libres(inicio, fin)

            if libres > 0:
                sugerencias.append({
                    'entrada': inicio,
                    'salida': fin,
                    'noches': noches,
                    'libres': libres,
                    'dias': distancia,
                    'cuando': 'antes' if sentido < 0 else 'después',
                })

            if len(sugerencias) == cantidad_sugerencias:
                return sorted(sugerencias, key=lambda s: s['entrada'])

    return sorted(sugerencias, key=lambda s: s['entrada'])


# COMBINACIONES DE HABITACIONES PARA GRUPOS

# Si ninguna habitación sola alcanza para el grupo, busca combinaciones
# de habitaciones libres que juntas sí alcancen.
# Prioridad: menos habitaciones > menos camas sobrantes > menor precio.

def sugerir_combinaciones(fecha_entrada, fecha_salida, cantidad_personas,
                          max_habitaciones=3, cantidad_opciones=3):

    noches = (fecha_salida - fecha_entrada).days

    ocupadas = Reserva.objects.filter(
        fecha_entrada__lt=fecha_salida,
        fecha_salida__gt=fecha_entrada,
        estado__nombre__in=ESTADOS_QUE_OCUPAN,
    ).values_list('habitacion_id', flat=True)

    libres = list(
        Habitacion.objects
        .filter(estado='disponible')
        .exclude(pk__in=ocupadas)
        .order_by('numero')
    )

    for cantidad_habitaciones in range(2, max_habitaciones + 1):

        opciones = []

        for grupo in combinations(libres, cantidad_habitaciones):

            capacidad_total = sum(h.capacidad for h in grupo)

            if capacidad_total < cantidad_personas:
                continue

            # Descarta combinaciones con una habitación que sobra
            menor_capacidad = min(h.capacidad for h in grupo)
            if capacidad_total - menor_capacidad >= cantidad_personas:
                continue

            # Repartir personas: primero la habitación más grande,
            # dejando al menos 1 persona para cada habitación restante
            reparto = []
            restantes = cantidad_personas
            ordenadas = sorted(grupo, key=lambda h: h.capacidad, reverse=True)

            for indice, habitacion in enumerate(ordenadas):
                habitaciones_que_quedan = len(ordenadas) - indice - 1
                personas = min(
                    habitacion.capacidad,
                    restantes - habitaciones_que_quedan
                )
                reparto.append({
                    'habitacion': habitacion,
                    'personas': personas,
                    'precio': habitacion.precio_noche * noches,
                })
                restantes -= personas

            opciones.append({
                'habitaciones': reparto,
                'capacidad_total': capacidad_total,
                'sobrantes': capacidad_total - cantidad_personas,
                'total': sum(h['precio'] for h in reparto),
                'noches': noches,
            })

        if opciones:
            opciones.sort(key=lambda o: (o['sobrantes'], o['total']))
            return opciones[:cantidad_opciones]

    return []