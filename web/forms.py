import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from reservas.validadores import (
    validar_documento,
    validar_nombre,
    validar_telefono,
)


class TelefonoChileWidget(forms.TextInput):
    """Campo de texto con el prefijo +56 fijo a la izquierda."""

    def render(self, name, value, attrs=None, renderer=None):
        campo = super().render(name, value, attrs, renderer)
        return format_html(
            '<div class="campo-telefono">'
            '<span class="prefijo-telefono">+56</span>{}'
            '</div>',
            campo
        )


class ReservaClienteForm(forms.Form):

    nombre = forms.CharField(
        max_length=50,
        label='Nombre'
    )

    apellido = forms.CharField(
        max_length=50,
        label='Apellido'
    )

    documento = forms.CharField(
        max_length=20,
        label='RUT',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 12.345.678-9'})
    )

    telefono = forms.CharField(
        max_length=9,
        label='Teléfono',
        widget=TelefonoChileWidget(attrs={
            'placeholder': '912345678',
            'inputmode': 'numeric',
        })
     )

    correo = forms.EmailField(
        max_length=100,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'Ej: nombre@correo.cl'}),
        error_messages={
            'invalid': 'Correo no válido. Ejemplo: nombre@correo.cl',
        }
    )

    cliente_es_huesped = forms.BooleanField(
        label='La persona que realiza la reserva también se alojará',
        required=False,
        initial=True
    )

    def __init__(self, *args, cantidad_personas=1, **kwargs):
        super().__init__(*args, **kwargs)

        self.cantidad_personas = cantidad_personas

        for numero in range(1, cantidad_personas + 1):

            for campo, etiqueta, longitud in [
                ('nombre', 'Nombre', 50),
                ('apellido', 'Apellido', 50),
                ('documento', 'RUT', 20),
            ]:
                atributos = {
                    'class': 'campo-huesped',
                    'data-huesped': numero,
                }

                if campo == 'documento':
                    atributos['placeholder'] = 'Ej: 12.345.678-9'

                self.fields[f'huesped_{numero}_{campo}'] = forms.CharField(
                    max_length=longitud,
                    label=f'{etiqueta} del huésped {numero}',
                    required=False,
                    widget=forms.TextInput(attrs=atributos)
                )

    # Validación de los datos del cliente

    def clean_nombre(self):
        return validar_nombre(self.cleaned_data['nombre'])

    def clean_apellido(self):
        return validar_nombre(self.cleaned_data['apellido'])

    def clean_documento(self):
        return validar_documento(self.cleaned_data['documento'])

    def clean_telefono(self):
        return validar_telefono(self.cleaned_data['telefono'])

    def clean(self):
        datos = super().clean()

        cliente_es_huesped = datos.get('cliente_es_huesped')

        # Si el cliente se aloja, ya tenemos sus datos
        cantidad_adicionales = self.cantidad_personas

        if cliente_es_huesped:
            cantidad_adicionales -= 1

        # Validar los huéspedes que deben registrarse
        for numero in range(1, cantidad_adicionales + 1):

            for campo in ['nombre', 'apellido', 'documento']:

                nombre_campo = f'huesped_{numero}_{campo}'

                if not datos.get(nombre_campo):
                    self.add_error(
                        nombre_campo,
                        'Este campo es obligatorio.'
                    )
                    continue

                # Validar el formato de los datos del huésped
                validador = (
                    validar_documento if campo == 'documento'
                    else validar_nombre
                )

                try:
                    datos[nombre_campo] = validador(datos[nombre_campo])
                except ValidationError as error:
                    self.add_error(nombre_campo, error)

        return datos


# CONSULTA DE RESERVA POR EL CLIENTE

PATRON_CODIGO = re.compile(r'^HRS-[0-9A-F]{12}$')

class ConsultaReservaForm(forms.Form):

    codigo = forms.CharField(
        max_length=20,
        label='Código de reserva',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: HRS-878C8194E8B9'})
    )

    documento = forms.CharField(
        max_length=20,
        label='RUT de quien reservó',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 12.345.678-9'})
    )

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip().upper()

        if not PATRON_CODIGO.match(codigo):
            raise ValidationError(
                'Formato de código no válido. Ejemplo: HRS-878C8194E8B9'
            )

        return codigo

    def clean_documento(self):
        return validar_documento(self.cleaned_data['documento'])


class CancelarReservaForm(forms.Form):

    confirmar = forms.BooleanField(
        label='Confirmo que quiero cancelar esta reserva',
        error_messages={
            'required': 'Marca la casilla para confirmar la cancelación.',
        }
    )