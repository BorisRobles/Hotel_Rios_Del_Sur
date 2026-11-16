"""
Se usan en el formulario de reserva web y en el registro de huéspedes
del panel, para que ambos acepten y guarden los datos en el mismo formato.

"""

import re

from django.core.exceptions import ValidationError


# Formato obligatorio: 12.345.678-9 o 1.234.567-K (con puntos y guion)
PATRON_RUT = re.compile(r'^\d{1,2}\.\d{3}\.\d{3}-[\dK]$')

# El cliente escribe solo los 9 dígitos (el +56 viene fijo en el formulario)
PATRON_TELEFONO = re.compile(r'^\d{9}$')

PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' \-]{2,50}$")


# Funciones de apoyo

def normalizar_nombre(texto):
    """'  maría   josé ' -> 'María José'"""
    return ' '.join((texto or '').split()).title()


# Validadores para formularios

def validar_documento(texto):
    """
    Exige el formato de RUT con puntos y guion: 12.345.678-9
    (el dígito verificador puede ser un número o K).
    Solo revisa el formato, no si el RUT existe.
    """
    documento = (texto or '').strip().upper()

    if not PATRON_RUT.match(documento):
        raise ValidationError(
            'Formato de RUT no válido. Debe llevar puntos y guion, '
            'por ejemplo: 12.345.678-9'
        )

    return documento


def validar_telefono(texto):
    """
    Recibe solo los 9 dígitos del número (ej: 912345678),
    porque el +56 aparece fijo en el formulario.
    Devuelve el número completo para guardarlo: +56912345678
    """
    digitos = (texto or '').strip()

    if not PATRON_TELEFONO.match(digitos):
        raise ValidationError(
            'Ingresa solo los 9 dígitos del teléfono, sin espacios. '
            'Ejemplo: 912345678'
        )

    return '+56' + digitos


def validar_nombre(texto):
    nombre = normalizar_nombre(texto)

    if not PATRON_NOMBRE.match(nombre):
        raise ValidationError(
            'Usa solo letras, espacios o guión.'
        )

    return nombre