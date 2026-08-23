import django

from django.shortcuts import render


def home(request):
    contexto = {
        'titulo': 'Sesión 1',
        'estudiante': 'Johan Salazar',
        'version_django': django.get_version(),
    }
    return render(request, 'sesion1/home.html', contexto)
