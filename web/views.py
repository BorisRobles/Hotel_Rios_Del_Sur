from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from habitaciones.models import Habitacion
from reservas.models import Reserva
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.http import require_POST

from .forms import (
    CancelarReservaForm,
    ConsultaReservaForm,
    ReservaClienteForm,
)
from reservas.services import (
    cancelar_reserva_cliente,
    crear_reserva,
    sugerir_combinaciones,
    sugerir_fechas,
)
from reservas.constantes import (
    ESTADOS_POR_LLEGAR,
    ESTADOS_QUE_OCUPAN,
    MAX_NOCHES,
)

def _en_panel(request):
    """True si la página se está usando desde el panel del personal."""
    return request.path.startswith('/panel/')

def inicio(request):
    habitaciones = Habitacion.objects.filter(
        estado='disponible'
    ).order_by('numero')

    return render(request, 'web/inicio.html', {
        'habitaciones': habitaciones
    })


def buscar_disponibilidad(request):
    habitaciones = Habitacion.objects.none()
    busqueda_realizada = False
    error = None
    sugerencias = []
    sin_capacidad = False
    combinaciones = []

    entrada = request.GET.get('entrada', '')
    salida = request.GET.get('salida', '')
    personas = request.GET.get('personas', '')

    if entrada or salida or personas:
        busqueda_realizada = True

        try:
            fecha_entrada = date.fromisoformat(entrada)
            fecha_salida = date.fromisoformat(salida)
            cantidad_personas = int(personas)

            if fecha_entrada < date.today():
                error = 'La fecha de entrada no puede ser anterior a hoy.'

            elif fecha_salida <= fecha_entrada:
                error = 'La fecha de salida debe ser posterior a la entrada.'

            elif (fecha_salida - fecha_entrada).days > MAX_NOCHES:
                error = (
                    f'No se puede reservar más de {MAX_NOCHES} noches seguidas.'
                )

            elif cantidad_personas < 1:
                error = 'La cantidad de personas debe ser mayor que cero.'

            else:
                reservas_ocupadas = Reserva.objects.filter(
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada,
                    estado__nombre__in=ESTADOS_QUE_OCUPAN
                ).values_list('habitacion_id', flat=True)

                habitaciones = Habitacion.objects.filter(
                    estado='disponible',
                    capacidad__gte=cantidad_personas
                ).exclude(
                    pk__in=reservas_ocupadas
                ).order_by('numero')

                # Ninguna habitación sola alcanza
                if not habitaciones.exists():

                    # 1) Grupos: combinar varias habitaciones libres
                    combinaciones = sugerir_combinaciones(
                        fecha_entrada,
                        fecha_salida,
                        cantidad_personas
                    )

                    # 2) Si no hay combinación, sugerir otras fechas
                    if not combinaciones:
                        sin_capacidad = not Habitacion.objects.filter(
                            estado='disponible',
                            capacidad__gte=cantidad_personas
                        ).exists()

                        if not sin_capacidad:
                            sugerencias = sugerir_fechas(
                                fecha_entrada,
                                fecha_salida,
                                cantidad_personas
                            )

        except (ValueError, TypeError):
            error = 'Ingresa fechas y cantidad de personas válidas.'

    return render(request, 'web/disponibilidad.html', {
        'habitaciones': habitaciones,
        'busqueda_realizada': busqueda_realizada,
        'error': error,
        'entrada': entrada,
        'salida': salida,
        'personas': personas,
        'sugerencias': sugerencias,
        'sin_capacidad': sin_capacidad,
        'combinaciones': combinaciones,
        'en_panel': _en_panel(request),
    })


def reservar_habitacion(request, habitacion_id):

    habitacion = get_object_or_404(
        Habitacion,
        pk=habitacion_id
    )

    if request.method == 'POST':
        entrada = request.POST.get('entrada', '')
        salida = request.POST.get('salida', '')
        personas = request.POST.get('personas', '')
    else:
        entrada = request.GET.get('entrada', '')
        salida = request.GET.get('salida', '')
        personas = request.GET.get('personas', '')

    try:
        cantidad_personas = int(personas)
    except (ValueError, TypeError):
        cantidad_personas = 1

    # Evitar generar una cantidad excesiva de campos
    cantidad_personas = max(
        1,
        min(cantidad_personas, habitacion.capacidad)
    )

    if request.method == 'POST':
        formulario = ReservaClienteForm(
            request.POST,
            cantidad_personas=cantidad_personas
        )

        if formulario.is_valid():
            try:
                fecha_entrada = date.fromisoformat(entrada)
                fecha_salida = date.fromisoformat(salida)

                reserva = crear_reserva(
                    habitacion_id=habitacion.pk,
                    fecha_entrada=fecha_entrada,
                    fecha_salida=fecha_salida,
                    cantidad_personas=cantidad_personas,
                    datos_cliente=formulario.cleaned_data,
                    usuario=request.user if _en_panel(request) else None
                )

                # Reserva hecha por recepción: vuelve al detalle en el panel
                if _en_panel(request):
                    messages.success(
                        request,
                        f'Reserva {reserva.codigo_reserva} creada correctamente.'
                    )
                    return redirect('detalle_reserva', pk=reserva.pk)

                return redirect(
                    'reserva_confirmada',
                    codigo=reserva.codigo_reserva
                )

            except (ValueError, TypeError):
                formulario.add_error(
                    None,
                    'Las fechas o la cantidad de personas no son válidas.'
                )

            except ValidationError as error:
                formulario.add_error(None, error)

    else:
        formulario = ReservaClienteForm(
            cantidad_personas=cantidad_personas
        )

    return render(request, 'web/reservar.html', {
        'habitacion': habitacion,
        'formulario': formulario,
        'entrada': entrada,
        'salida': salida,
        'personas': cantidad_personas,
        'en_panel': _en_panel(request),
    })

def reserva_confirmada(request, codigo):
    reserva = get_object_or_404(
        Reserva,
        codigo_reserva=codigo
    )

    return render(request, 'web/reserva_confirmada.html', {
        'reserva': reserva
    })


# MI RESERVA: consulta y cancelación por el cliente

# Seguridad:
#   - Se exigen el código Y el RUT: con solo uno no se ve nada.
#   - Mensaje genérico si no coinciden (no revela cuál dato falló).
#   - Máximo 5 consultas fallidas por IP cada 5 minutos (fuerza bruta).
#   - La reserva encontrada se guarda en la sesión: para cancelar no se
#     envía ningún id desde el navegador, así nadie cancela reservas ajenas.
#   - La cancelación exige POST, token CSRF y casilla de confirmación.

MAX_CONSULTAS_FALLIDAS = 5
MINUTOS_BLOQUEO_CONSULTA = 5
CLAVE_SESION_RESERVA = 'mi_reserva_id'


def _clave_consultas(request):
    return 'consultas_reserva:' + request.META.get('REMOTE_ADDR', '')


def mi_reserva(request):

    reserva = None
    formulario = ConsultaReservaForm()
    bloqueado = cache.get(_clave_consultas(request), 0) >= MAX_CONSULTAS_FALLIDAS

    if request.method == 'POST':

        # Botón "Consultar otra reserva"
        if 'salir' in request.POST:
            request.session.pop(CLAVE_SESION_RESERVA, None)
            return redirect('mi_reserva')

        formulario = ConsultaReservaForm(request.POST)

        if not bloqueado and formulario.is_valid():
            reserva = Reserva.objects.filter(
                codigo_reserva=formulario.cleaned_data['codigo'],
                cliente__documento=formulario.cleaned_data['documento'],
            ).first()

            if reserva:
                cache.delete(_clave_consultas(request))
                request.session[CLAVE_SESION_RESERVA] = reserva.pk
                return redirect('mi_reserva')

            intentos = cache.get(_clave_consultas(request), 0) + 1
            cache.set(
                _clave_consultas(request),
                intentos,
                MINUTOS_BLOQUEO_CONSULTA * 60
            )
            bloqueado = intentos >= MAX_CONSULTAS_FALLIDAS

            if not bloqueado:
                formulario.add_error(
                    None,
                    'No encontramos una reserva con esos datos. '
                    'Revisa el código y el RUT.'
                )

    else:
        reserva_id = request.session.get(CLAVE_SESION_RESERVA)

        if reserva_id:
            reserva = (
                Reserva.objects
                .select_related('habitacion', 'estado', 'cliente')
                .filter(pk=reserva_id)
                .first()
            )

    contexto = {
        'formulario': formulario,
        'bloqueado': bloqueado,
        'minutos_bloqueo': MINUTOS_BLOQUEO_CONSULTA,
        'reserva': reserva,
    }

    if reserva:
        contexto.update({
            'huespedes': reserva.huespedes.all().order_by('apellido'),
            'noches': (reserva.fecha_salida - reserva.fecha_entrada).days,
            'puede_cancelar': (
                reserva.estado.nombre in ESTADOS_POR_LLEGAR
                and timezone.localdate() < reserva.fecha_entrada
            ),
            'formulario_cancelar': CancelarReservaForm(),
        })

    return render(request, 'web/mi_reserva.html', contexto)


@require_POST
def cancelar_mi_reserva(request):

    reserva_id = request.session.get(CLAVE_SESION_RESERVA)

    if not reserva_id:
        return redirect('mi_reserva')

    formulario = CancelarReservaForm(request.POST)

    if not formulario.is_valid():
        messages.error(
            request,
            'Marca la casilla para confirmar la cancelación.'
        )
        return redirect('mi_reserva')

    try:
        cancelar_reserva_cliente(reserva_id)
        messages.success(request, 'Tu reserva fue cancelada.')
    except ValidationError as error:
        for mensaje in error.messages:
            messages.error(request, mensaje)

    return redirect('mi_reserva')