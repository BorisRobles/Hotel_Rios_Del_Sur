from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import transaction

from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Case, F, IntegerField, Q, Sum, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from habitaciones.models import Habitacion
from web import views as web_views
from reservas import services
from reservas.constantes import (
    CANCELADA,
    EN_CURSO,
    ESTADOS_POR_LLEGAR,
    ESTADOS_QUE_OCUPAN,
)
from reservas.models import HistorialReserva, Reserva

from .forms import (
    FiltroReservasForm,
    HabitacionForm,
    HuespedForm,
    PersonalForm,
)


# ROLES
def es_personal_hotel(usuario):
    return (
        usuario.is_authenticated
        and usuario.is_active
        and (
            usuario.is_superuser
            or usuario.groups.filter(
                name__in=['Administrador hotel', 'Recepcionista']
            ).exists()
        )
    )


def es_administrador_hotel(usuario):
    return (
        usuario.is_authenticated
        and usuario.is_active
        and (
            usuario.is_superuser
            or usuario.groups.filter(name='Administrador hotel').exists()
        )
    )


def _mostrar_errores(request, error):
    for mensaje in error.messages:
        messages.error(request, mensaje)


# INICIO DEL PANEL
# Bloque de recepción: lo ven todos los funcionarios.
# Bloque de administración: solo el administrador.


@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
def inicio_panel(request):

    hoy = timezone.localdate()
    es_administrador = es_administrador_hotel(request.user)

    reservas_en_curso = Reserva.objects.filter(estado__nombre=EN_CURSO)
    ids_ocupadas = reservas_en_curso.values_list('habitacion_id', flat=True)

    # Reservas vigentes para esta noche que aún no hacen check-in
    ids_reservadas = Reserva.objects.filter(
        estado__nombre__in=ESTADOS_POR_LLEGAR,
        fecha_entrada__lte=hoy,
        fecha_salida__gt=hoy,
    ).values_list('habitacion_id', flat=True)

    habitaciones_ocupadas = (
        Habitacion.objects.filter(pk__in=ids_ocupadas).count()
    )
    habitaciones_reservadas = (
        Habitacion.objects
        .filter(pk__in=ids_reservadas)
        .exclude(pk__in=ids_ocupadas)
        .count()
    )
    habitaciones_libres = (
        Habitacion.objects
        .filter(estado='disponible')
        .exclude(pk__in=ids_ocupadas)
        .exclude(pk__in=ids_reservadas)
        .count()
    )

    # Bloque recepcionista 
    llegadas_hoy = (
        Reserva.objects
        .filter(fecha_entrada=hoy, estado__nombre__in=ESTADOS_POR_LLEGAR)
        .select_related('cliente', 'habitacion', 'estado')
        .order_by('habitacion__numero')
    )

    # Incluye salidas atrasadas (fecha de salida ya pasó)
    salidas_hoy = (
        reservas_en_curso
        .filter(fecha_salida__lte=hoy)
        .select_related('cliente', 'habitacion', 'estado')
        .order_by('fecha_salida', 'habitacion__numero')
    )

    contexto = {
        'hoy': hoy,
        'es_administrador': es_administrador,
        'total_habitaciones': Habitacion.objects.count(),
        'total_reservas': Reserva.objects.count(),
        'habitaciones_mantenimiento': Habitacion.objects.filter(
            estado='mantenimiento'
        ).count(),
        'habitaciones_ocupadas': habitaciones_ocupadas,
        'habitaciones_reservadas': habitaciones_reservadas,
        'habitaciones_libres': habitaciones_libres,
        'llegadas_hoy': llegadas_hoy,
        'salidas_hoy': salidas_hoy,
    }

    # Bloque administrador
    if es_administrador:
        # Reservas cuya fecha de entrada cae en el mes actual
        reservas_mes = Reserva.objects.filter(
            fecha_entrada__year=hoy.year,
            fecha_entrada__month=hoy.month,
        )

        habitaciones_operativas = Habitacion.objects.filter(
            estado='disponible'
        ).count()

        contexto.update({
            'reservas_mes': reservas_mes.count(),
            'canceladas_mes': reservas_mes.filter(
                estado__nombre=CANCELADA
            ).count(),
            'ingresos_mes': reservas_mes.filter(
                estado_pago='pagado'
            ).aggregate(total=Sum('precio_total'))['total'] or 0,
            'pagos_pendientes': Reserva.objects.filter(
                estado__nombre__in=ESTADOS_QUE_OCUPAN,
                estado_pago='pendiente'
            ).aggregate(total=Sum('precio_total'))['total'] or 0,
            'porcentaje_ocupacion': round(
                habitaciones_ocupadas * 100 / habitaciones_operativas
            ) if habitaciones_operativas else 0,
            'ultimas_acciones': (
                HistorialReserva.objects
                .select_related('reserva', 'usuario')
                .order_by('-fecha')[:10]
            ),
        })

    return render(request, 'panel/inicio.html', contexto)


# RESERVAS (recepcionista y administrador)

@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.view_reserva', raise_exception=True)
def lista_reservas(request):

    filtros = FiltroReservasForm(request.GET or None)

    reservas = (
        Reserva.objects
        .select_related('cliente', 'habitacion', 'estado')
        .annotate(
            prioridad=Case(
                When(estado__nombre=EN_CURSO, then=Value(0)),
                When(estado__nombre__in=ESTADOS_POR_LLEGAR, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        )
        .order_by(
            'prioridad',
            Case(
                When(prioridad=0, then=F('fecha_salida')),
                When(prioridad=1, then=F('fecha_entrada')),
            ).asc(nulls_last=True),
            F('fecha_entrada').desc(),
            '-pk',
        )
    )

    if filtros.is_valid():
        texto = filtros.cleaned_data.get('q')
        estado = filtros.cleaned_data.get('estado')
        fecha = filtros.cleaned_data.get('fecha')

        if texto:
            reservas = reservas.filter(
                Q(codigo_reserva__icontains=texto)
                | Q(cliente__documento__icontains=texto)
                | Q(cliente__apellido__icontains=texto)
                | Q(huespedes__documento__icontains=texto)
            ).distinct()

        if estado:
            reservas = reservas.filter(estado__nombre=estado)

        if fecha:
            reservas = reservas.filter(
                fecha_entrada__lte=fecha,
                fecha_salida__gt=fecha
            )

    pagina = Paginator(reservas, 20).get_page(request.GET.get('pagina'))

    # Conserva los filtros al cambiar de página
    parametros = request.GET.copy()
    parametros.pop('pagina', None)

    return render(request, 'panel/reservas.html', {
        'filtros': filtros,
        'pagina': pagina,
        'parametros': parametros.urlencode(),
    })


@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.view_reserva', raise_exception=True)
def detalle_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    return _mostrar_detalle(request, reserva)


def _mostrar_detalle(request, reserva, formulario_huesped=None):
    """Arma la página de detalle (se reutiliza al mostrar errores)."""

    reserva = (
        Reserva.objects
        .select_related('cliente', 'habitacion', 'estado', 'usuario')
        .get(pk=reserva.pk)
    )

    hoy = timezone.localdate()
    estado = reserva.estado.nombre
    total_huespedes = reserva.huespedes.count()

    contexto = {
        'reserva': reserva,
        'huespedes': reserva.huespedes.all().order_by('apellido'),
        'historial': reserva.historial.select_related(
            'usuario'
        ).order_by('-fecha'),
        'noches': (reserva.fecha_salida - reserva.fecha_entrada).days,
        'formulario_huesped': formulario_huesped or HuespedForm(),
        'puede_cancelar': estado in ESTADOS_POR_LLEGAR,
        'puede_checkin': (
            estado in ESTADOS_POR_LLEGAR
            and reserva.fecha_entrada <= hoy < reserva.fecha_salida
        ),
        'puede_checkout': estado == EN_CURSO,
        'puede_pagar': (
            estado != CANCELADA and reserva.estado_pago == 'pendiente'
        ),
        'puede_agregar_huesped': (
            estado in ESTADOS_QUE_OCUPAN
            and total_huespedes < reserva.cantidad_personas
        ),
        'total_huespedes': total_huespedes,
    }

    return render(request, 'panel/detalle_reserva.html', contexto)


def _accion_reserva(request, pk, funcion, mensaje_exito):
    """Ejecuta una operación de recepción y muestra el resultado."""
    get_object_or_404(Reserva, pk=pk)

    try:
        funcion(pk, request.user)
        messages.success(request, mensaje_exito)
    except ValidationError as error:
        _mostrar_errores(request, error)

    return redirect('detalle_reserva', pk=pk)


@require_POST
@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.change_reserva', raise_exception=True)
def checkin_reserva(request, pk):
    return _accion_reserva(
        request, pk, services.hacer_checkin,
        'Check-in realizado. La habitación quedó ocupada.'
    )


@require_POST
@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.change_reserva', raise_exception=True)
def checkout_reserva(request, pk):
    return _accion_reserva(
        request, pk, services.hacer_checkout,
        'Check-out realizado. La habitación quedó libre.'
    )


@require_POST
@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.change_reserva', raise_exception=True)
def cancelar_reserva(request, pk):
    return _accion_reserva(
        request, pk, services.cancelar_reserva,
        'La reserva fue cancelada.'
    )


@require_POST
@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.change_reserva', raise_exception=True)
def pagar_reserva(request, pk):
    return _accion_reserva(
        request, pk, services.registrar_pago,
        'Pago registrado correctamente.'
    )


@require_POST
@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('reservas.add_huesped', raise_exception=True)
def agregar_huesped(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    formulario = HuespedForm(request.POST)

    if formulario.is_valid():
        try:
            services.agregar_huesped(
                pk, formulario.cleaned_data, request.user
            )
            messages.success(request, 'Huésped registrado en la reserva.')
            return redirect('detalle_reserva', pk=pk)

        except ValidationError as error:
            # Errores de reglas de negocio (cupo lleno, huésped repetido...)
            formulario.add_error(None, error)

    # Se vuelve a mostrar la página con los errores bajo cada campo
    return _mostrar_detalle(request, reserva, formulario_huesped=formulario)


# NUEVA RESERVA DESDE RECEPCIÓN
# Reutiliza la búsqueda y el formulario del sitio público, pero dentro
# del panel: exige sesión del personal y registra quién creó la reserva.

def es_recepcionista(usuario):
    return (
        usuario.is_authenticated
        and usuario.is_active
        and usuario.groups.filter(name='Recepcionista').exists()
    )


def _solo_recepcion(request):
    if not es_recepcionista(request.user):
        raise PermissionDenied


@login_required(login_url='login')
def disponibilidad_panel(request):
    _solo_recepcion(request)
    return web_views.buscar_disponibilidad(request)

@login_required(login_url='login')
def reservar_panel(request, habitacion_id):
    _solo_recepcion(request)
    return web_views.reservar_habitacion(request, habitacion_id)


# CONTROL DE HABITACIONES OCUPADAS Y DISPONIBLES

@login_required(login_url='login')
@user_passes_test(es_personal_hotel, login_url='inicio')
@permission_required('habitaciones.view_habitacion', raise_exception=True)
def estado_habitaciones(request):

    hoy = timezone.localdate()

    en_curso = {
        r.habitacion_id: r
        for r in Reserva.objects.filter(
            estado__nombre=EN_CURSO
        ).select_related('cliente')
    }

    # Reservas vigentes para esta noche que aún no hacen check-in
    reservadas = {
        r.habitacion_id: r
        for r in Reserva.objects.filter(
            estado__nombre__in=ESTADOS_POR_LLEGAR,
            fecha_entrada__lte=hoy,
            fecha_salida__gt=hoy,
        ).select_related('cliente')
    }

    filas = []
    resumen = {'ocupada': 0, 'reservada': 0, 'libre': 0, 'fuera': 0}

    for habitacion in Habitacion.objects.order_by('numero'):

        reserva = None

        if habitacion.pk in en_curso:
            situacion, etiqueta = 'ocupada', 'Ocupada'
            reserva = en_curso[habitacion.pk]

        elif habitacion.estado != 'disponible':
            situacion = 'fuera'
            etiqueta = habitacion.get_estado_display()

        elif habitacion.pk in reservadas:
            situacion = 'reservada'
            reserva = reservadas[habitacion.pk]

            if reserva.fecha_entrada == hoy:
                etiqueta = 'Reservada - Llega Hoy'
            else:
                etiqueta = 'Reservada - Llegada Atrasada'

        else:
            situacion, etiqueta = 'libre', 'Libre'

        resumen[situacion] += 1
        filas.append({
            'habitacion': habitacion,
            'situacion': situacion,
            'etiqueta': etiqueta,
            'reserva': reserva,
        })

    return render(request, 'panel/estado_habitaciones.html', {
        'filas': filas,
        'resumen': resumen,
        'hoy': hoy,
    })


# ADMINISTRACIÓN DE HABITACIONES

@login_required(login_url='login')
@permission_required(
    'habitaciones.view_habitacion',
    raise_exception=True
)
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all().order_by('numero')

    return render(
        request,
        'panel/habitaciones.html',
        {'habitaciones': habitaciones}
    )


@login_required(login_url='login')
@permission_required(
    'habitaciones.add_habitacion',
    raise_exception=True
)
def agregar_habitacion(request):
    if request.method == 'POST':
        formulario = HabitacionForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Habitación agregada correctamente.')
            return redirect('lista_habitaciones')
    else:
        formulario = HabitacionForm()

    return render(
        request,
        'panel/form_habitacion.html',
        {
            'formulario': formulario,
            'titulo': 'Agregar habitación'
        }
    )


@login_required(login_url='login')
@permission_required(
    'habitaciones.change_habitacion',
    raise_exception=True
)
def editar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)

    if request.method == 'POST':
        formulario = HabitacionForm(request.POST, instance=habitacion)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Habitación actualizada correctamente.')
            return redirect('lista_habitaciones')
    else:
        formulario = HabitacionForm(instance=habitacion)

    return render(
        request,
        'panel/form_habitacion.html',
        {
            'formulario': formulario,
            'titulo': f'Editar habitación {habitacion.numero}'
        }
    )


# GESTIÓN DEL PERSONAL (solo administrador del hotel)

# Controles de seguridad (OWASP A01 - control de acceso):
#   - Solo el Administrador hotel o el superusuario entran aquí.
#   - Solo se pueden crear cuentas Recepcionista o Administrador;
#     nunca superusuarios.
#   - Un administrador puede activar/desactivar recepcionistas.
#     Solo el superusuario puede activar/desactivar administradores
#     (así un administrador no puede dejar fuera a los demás).
#   - Nadie puede desactivar su propia cuenta ni la del superusuario.
#   - Las cuentas no se borran: se desactivan, para conservar el historial.
#   - Cada acción queda registrada en la auditoría de Django (A09).


GRUPO_RECEPCIONISTA = 'Recepcionista'
GRUPO_ADMINISTRADOR = 'Administrador hotel'
GRUPOS_PERSONAL = [GRUPO_RECEPCIONISTA, GRUPO_ADMINISTRADOR]


# Nombres que se muestran en pantalla
NOMBRE_VISIBLE = {
    GRUPO_RECEPCIONISTA: 'Recepcionista',
    GRUPO_ADMINISTRADOR: 'Administrador',
}


def _solo_administrador(request):
    if not es_administrador_hotel(request.user):
        raise PermissionDenied


def _rol_de(usuario):
    if usuario.groups.filter(name=GRUPO_ADMINISTRADOR).exists():
        return GRUPO_ADMINISTRADOR
    return GRUPO_RECEPCIONISTA


def _puede_cambiar_estado(autor, usuario):
    """Reglas para activar o desactivar una cuenta del personal."""
    if usuario.is_superuser or usuario == autor:
        return False

    if _rol_de(usuario) == GRUPO_ADMINISTRADOR:
        return autor.is_superuser

    return True


def _registrar_accion_usuario(autor, usuario, tipo, mensaje):
    """Guarda la acción en la auditoría de Django (LogEntry)."""
    LogEntry.objects.create(
        user=autor,
        content_type=ContentType.objects.get_for_model(User),
        object_id=str(usuario.pk),
        object_repr=usuario.username[:200],
        action_flag=tipo,
        change_message=mensaje,
    )


@login_required(login_url='login')
def lista_personal(request):
    _solo_administrador(request)

    if request.method == 'POST':
        formulario = PersonalForm(request.POST)

        if formulario.is_valid():
            rol = formulario.cleaned_data['rol']
            grupo = Group.objects.filter(name=rol).first()

            if grupo is None:
                messages.error(
                    request,
                    f'No existe el grupo {rol}. '
                    'Ejecuta: python manage.py configurar_roles'
                )
                return redirect('lista_personal')

            with transaction.atomic():
                usuario = formulario.save(commit=False)
                usuario.is_staff = False
                usuario.is_superuser = False
                usuario.is_active = True
                usuario.save()
                usuario.groups.set([grupo])

                _registrar_accion_usuario(
                    request.user, usuario, ADDITION,
                    f'Cuenta creada desde el panel con el rol {NOMBRE_VISIBLE[rol]}'
                )

            messages.success(
                request,
                f'Cuenta "{usuario.username}" creada con el rol {NOMBRE_VISIBLE[rol]}.'
            )
            return redirect('lista_personal')
    else:
        formulario = PersonalForm()

    usuarios = (
        User.objects
        .filter(Q(groups__name__in=GRUPOS_PERSONAL) | Q(is_superuser=True))
        .distinct()
        .order_by('-is_superuser', '-is_active', 'username')
    )

    personal = [
        {
            'usuario': usuario,
            'rol': (
                'Administrador principal' if usuario.is_superuser
                else NOMBRE_VISIBLE[_rol_de(usuario)]
            ),
            'puede_cambiar': _puede_cambiar_estado(request.user, usuario),
        }
        for usuario in usuarios
    ]

    acciones = (
        LogEntry.objects
        .filter(content_type=ContentType.objects.get_for_model(User))
        .select_related('user')
        .order_by('-action_time')[:10]
    )

    return render(request, 'panel/personal.html', {
        'formulario': formulario,
        'personal': personal,
        'acciones': acciones,
    })


@require_POST
@login_required(login_url='login')
def cambiar_estado_recepcionista(request, pk):
    _solo_administrador(request)

    usuario = get_object_or_404(
        User.objects.filter(groups__name__in=GRUPOS_PERSONAL).distinct(),
        pk=pk
    )

    if not _puede_cambiar_estado(request.user, usuario):
        raise PermissionDenied

    usuario.is_active = not usuario.is_active
    usuario.save(update_fields=['is_active'])

    estado = 'activada' if usuario.is_active else 'desactivada'

    _registrar_accion_usuario(
        request.user, usuario, CHANGE,
        f'Cuenta ({NOMBRE_VISIBLE[_rol_de(usuario)]}) {estado} desde el panel'
    )

    messages.success(request, f'Cuenta "{usuario.username}" {estado}.')
    return redirect('lista_personal')