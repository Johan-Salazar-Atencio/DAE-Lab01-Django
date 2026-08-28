from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MascotaForm
from .models import Mascota

DATOS_INICIALES = [
    {
        'nombre': 'Luna',
        'especie': 'perro',
        'raza': 'Golden Retriever',
        'sexo': 'hembra',
        'fecha_nacimiento': '2024-03-15',
        'peso_kg': '23.50',
        'color': 'dorado',
        'nombre_dueno': 'María Pérez',
        'telefono_dueno': '+52 555 123 4567',
        'observaciones': 'Alérgica a penicilina',
    },
    {
        'nombre': 'Rocky',
        'especie': 'perro',
        'raza': 'Beagle',
        'sexo': 'macho',
        'fecha_nacimiento': '2021-07-02',
        'peso_kg': '12.80',
        'color': 'tricolor',
        'nombre_dueno': 'Carlos López',
        'telefono_dueno': '+52 555 987 6543',
        'observaciones': '',
    },
    {
        'nombre': 'Misi',
        'especie': 'gato',
        'raza': '',
        'sexo': 'hembra',
        'fecha_nacimiento': '2023-11-20',
        'peso_kg': '4.10',
        'color': 'negro',
        'nombre_dueno': 'Ana García',
        'telefono_dueno': '+52 555 456 7890',
        'observaciones': 'Castrada en enero 2024',
    },
    {
        'nombre': 'Kiwi',
        'especie': 'ave',
        'raza': 'Perico australiano',
        'sexo': 'macho',
        'fecha_nacimiento': None,
        'peso_kg': '0.05',
        'color': 'verde y amarillo',
        'nombre_dueno': 'Luis Ramírez',
        'telefono_dueno': '+52 555 321 0987',
        'observaciones': '',
    },
    {
        'nombre': 'Tom',
        'especie': 'perro',
        'raza': 'Pastor alemán',
        'sexo': 'macho',
        'fecha_nacimiento': '2020-01-30',
        'peso_kg': '35.20',
        'color': 'negro y fuego',
        'nombre_dueno': 'Johan Salazar',
        'telefono_dueno': '+52 555 222 3344',
        'observaciones': 'En tratamiento por displasia',
    },
]


def _sembrar_mascotas():
    if Mascota.objects.count() == 0:
        for datos in DATOS_INICIALES:
            Mascota.objects.get_or_create(nombre=datos['nombre'], defaults=datos)


def listado(request):
    _sembrar_mascotas()
    mascotas = Mascota.objects.all()
    contexto = {
        'titulo': 'Pacientes de la Veterinaria',
        'mascotas': mascotas,
    }
    return render(request, 'vet/listado.html', contexto)


def registrar(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota registrada correctamente.')
            return redirect('vet:listado')
    else:
        form = MascotaForm()
    contexto = {
        'titulo': 'Registrar mascota',
        'form': form,
    }
    return render(request, 'vet/formulario.html', contexto)