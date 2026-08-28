from django import forms

from .models import Mascota


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'placeholder': 'AAAA-MM-DD'}),
        }
        labels = {
            'nombre': 'Nombre',
            'especie': 'Especie',
            'raza': 'Raza',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'peso_kg': 'Peso (kg)',
            'color': 'Color',
            'nombre_dueno': 'Nombre del dueño',
            'telefono_dueno': 'Teléfono del dueño',
            'observaciones': 'Observaciones',
            'activo': '¿Paciente activo?',
        }