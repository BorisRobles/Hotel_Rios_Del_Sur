from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from habitaciones.models import Habitacion
from reservas.constantes import TODOS_LOS_ESTADOS
from reservas.validadores import validar_documento, validar_nombre



class HabitacionForm(forms.ModelForm):

    class Meta:
        model = Habitacion

        fields = [
            'numero',
            'tipo',
            'capacidad',
            'precio_noche',
            'descripcion',
            'estado',
        ]

        labels = {
            'numero': 'Número de habitación',
            'tipo': 'Tipo de habitación',
            'capacidad': 'Capacidad de personas',
            'precio_noche': 'Precio por noche (CLP)',
            'descripcion': 'Descripción',
            'estado': 'Estado de la habitación',
        }

        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'Ej: 101'}),
            'tipo': forms.TextInput(attrs={'placeholder': 'Ej: Matrimonial'}),
            'capacidad': forms.NumberInput(attrs={'min': 1}),
            'precio_noche': forms.NumberInput(attrs={'min': 1}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

        error_messages = {
            'numero': {
                'unique': 'Ya existe habitacion con este número.',
            },
        }

        
    # Límites razonables para evitar datos absurdos
    CAPACIDAD_MAXIMA = 10
    PRECIO_MAXIMO = 2000000

    def clean_numero(self):
        numero = self.cleaned_data['numero'].strip()

        if not numero.isdigit():
            raise forms.ValidationError(
                'El número de habitación debe contener solo dígitos. Ej: 101'
            )

        return numero

    def clean_tipo(self):
        tipo = ' '.join(self.cleaned_data['tipo'].split())

        if len(tipo) < 3:
            raise forms.ValidationError(
                'El tipo debe tener al menos 3 caracteres. Ej: Matrimonial'
            )

        return tipo

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']

        if capacidad > self.CAPACIDAD_MAXIMA:
            raise forms.ValidationError(
                f'La capacidad máxima es de {self.CAPACIDAD_MAXIMA} personas.'
            )

        return capacidad

    def clean_precio_noche(self):
        precio = self.cleaned_data['precio_noche']

        if precio > self.PRECIO_MAXIMO:
            raise forms.ValidationError(
                'El precio por noche no puede superar $2.000.000.'
            )

        return precio



# FORMULARIOS DE RECEPCIÓN
class FiltroReservasForm(forms.Form):
    q = forms.CharField(
        label='Buscar',
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Código, documento o apellido'
        })
    )

    estado = forms.ChoiceField(
        label='Estado',
        required=False,
        choices=[('', 'Todos')] + [(e, e) for e in TODOS_LOS_ESTADOS]
    )

    fecha = forms.DateField(
        label='Alojados en la fecha',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class HuespedForm(forms.Form):
    nombre = forms.CharField(max_length=50, label='Nombre')
    apellido = forms.CharField(max_length=50, label='Apellido')
    documento = forms.CharField(
        max_length=20,
        label='RUT o documento',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 12.345.678-5'})
    )

    def clean_nombre(self):
        return validar_nombre(self.cleaned_data['nombre'])

    def clean_apellido(self):
        return validar_nombre(self.cleaned_data['apellido'])

    def clean_documento(self):
        return validar_documento(self.cleaned_data['documento'])

    
# GESTIÓN DEL PERSONAL (solo administrador del hotel)

# Roles que se pueden asignar desde el panel.
# El superusuario NO está en la lista: no se puede crear desde aquí.
ROLES_PERSONAL = [
    ('Recepcionista', 'Recepcionista'),
    ('Administrador hotel', 'Administrador'),
]


class PersonalForm(UserCreationForm):
    """
    Crea una cuenta del personal del hotel.
    Hereda de UserCreationForm, que ya valida que el usuario no exista
    y aplica las reglas de contraseña segura de Django.
    El rol solo puede ser uno de ROLES_PERSONAL (se valida en el servidor).
    """

    first_name = forms.CharField(max_length=50, label='Nombre')
    last_name = forms.CharField(max_length=50, label='Apellido')
    rol = forms.ChoiceField(
        choices=[('', 'Selecciona un rol')] + ROLES_PERSONAL,
        label='Rol'
    )

    field_order = [
        'username', 'first_name', 'last_name', 'rol',
        'password1', 'password2',
    ]

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username': 'Nombre de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.help_text = ''

        self.fields['username'].widget.attrs['placeholder'] = 'Ej: recepcion2'

    def clean_first_name(self):
        return validar_nombre(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return validar_nombre(self.cleaned_data['last_name'])