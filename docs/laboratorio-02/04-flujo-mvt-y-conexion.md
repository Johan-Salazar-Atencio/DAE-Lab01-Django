---
title: "Laboratorio 02 — Flujo MVT y conexión con config"
tags: [django, mvt, mvc, vet, config, templates, urls]
---

# Flujo MVT y conexión de la app `vet` con `config`

## 1. Qué es el patrón MVT

Django implementa **MVT: Model-View-Template**. Es la variante de Django del patrón clásico **MVC (Model-View-Controller)**:

| MVC | MVT (Django) | Responsabilidad |
|---|---|---|
| Model | **Model** (`models.py`) | Datos, esquema de BD y reglas de negocio a nivel de entidad. |
| Controller | **View** (`views.py`) | Lógica de la petición: decide qué datos leer/escribir y qué template renderizar. |
| View | **Template** (`templates/*.html`) | Presentación: HTML con placeholders y lógica mínima de visualización. |

Diferencia clave: en Django el *framework* actúa como Controller (resuelve URLs, despacha la request, aplica middleware). La `View` de Django es más cercana al Controller de MVC, y el `Template` es la View de MVC. `urls.py` es el enrutador que conecta la URL con la View correspondiente.

## 2. MVT aplicado a la app `vet`

La app `vet` implementa el caso **Veterinaria — gestión de mascotas** con CRUD mínimo (listar y registrar). Archivos:

```
vet/
├── models.py
├── forms.py
├── views.py
├── urls.py
└── templates/vet/
    ├── listado.html
    └── formulario.html
templates/base.html
```

### 2.1 Model — `vet/models.py`

Entidad `Mascota` (`models.Model`). Representa `vet_mascota` en SQLite.

**Campos:**

| Campo | Tipo | Notas |
|---|---|---|
| `nombre` | `CharField(max_length=100)` | Requerido |
| `especie` | `CharField(max_length=20, choices=ESPECIES)` | `perro`, `gato`, `ave`, `otro` |
| `raza` | `CharField(max_length=100, blank=True)` | Opcional |
| `sexo` | `CharField(max_length=10, choices=SEXOS)` | `macho`, `hembra` |
| `fecha_nacimiento` | `DateField(null=True, blank=True)` | Opcional |
| `peso_kg` | `DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)` | Ej. `23.50` |
| `color` | `CharField(max_length=50, blank=True)` | Opcional |
| `nombre_dueno` | `CharField(max_length=100)` | Requerido |
| `telefono_dueno` | `CharField(max_length=20)` | Requerido |
| `observaciones` | `TextField(blank=True)` | Opcional |
| `fecha_registro` | `DateTimeField(auto_now_add=True)` | Se asigna al crear |
| `activo` | `BooleanField(default=True)` | Paciente activo/inactivo |

**`class Meta`:**

```python
verbose_name = 'Mascota'
verbose_name_plural = 'Mascotas'
ordering = ['-fecha_registro']  # más recientes primero
```

**`__str__`:**

```python
def __str__(self):
    return f'{self.nombre} ({self.get_especie_display()})'
```

> `get_especie_display()` devuelve el label del `choices` (ej. `perro` -> `Perro`).

`vet/forms.py` expone el modelo mediante `MascotaForm(ModelForm)` con `fields = '__all__'`, `DateInput(type="date")` para `fecha_nacimiento` y `labels` en español.

### 2.2 View — `vet/views.py`

Dos funciones basadas en función (FBV):

#### `listado(request)`

```python
def listado(request):
    _sembrar_mascotas()
    mascotas = Mascota.objects.all()
    contexto = {'titulo': 'Pacientes de la Veterinaria', 'mascotas': mascotas}
    return render(request, 'vet/listado.html', contexto)
```

- Llama a `_sembrar_mascotas()` antes de consultar.
- `_sembrar_mascotas()` verifica `Mascota.objects.count() == 0` y, si la tabla está vacía, inserta 5 registros con `get_or_create(nombre=..., defaults=datos)`:

| # | nombre | especie | raza | sexo | peso_kg | color | dueño |
|---|---|---|---|---|---|---|---|
| 1 | Luna | perro | Golden Retriever | hembra | 23.50 | dorado | María Pérez |
| 2 | Rocky | perro | Beagle | macho | 12.80 | tricolor | Carlos López |
| 3 | Misi | gato | — | hembra | 4.10 | negro | Ana García |
| 4 | Kiwi | ave | Perico australiano | macho | 0.05 | verde y amarillo | Luis Ramírez |
| 5 | Tom | perro | Pastor alemán | macho | 35.20 | negro y fuego | Johan Salazar |

- Luego hace `Mascota.objects.all()` (respeta `ordering = ['-fecha_registro']`) y renderiza `vet/listado.html`.

#### `registrar(request)`

```python
def registrar(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota registrada correctamente.')
            return redirect('vet:listado')
    else:
        form = MascotaForm()
    return render(request, 'vet/formulario.html', {'titulo': 'Registrar mascota', 'form': form})
```

- **GET:** instancia `MascotaForm()` vacío y renderiza `vet/formulario.html`.
- **POST:** vincula `MascotaForm(request.POST)`, valida con `form.is_valid()`, guarda con `form.save()`, agrega mensaje con `messages.success` y redirige con `redirect('vet:listado')`. Si no es válido, re-renderiza el formulario con errores.

Requiere `{% csrf_token %}` en el template (protección `CsrfViewMiddleware`).

### 2.3 Template — `vet/templates/vet/*.html` + `templates/base.html`

#### `templates/base.html` (layout global)

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<title>{% block title %}DjangoLab01{% endblock %}</title>

<nav>
  <a href="/">Inicio</a>
  <a href="{% url 'vet:listado' %}">Veterinaria</a>
  <a href="/admin/">Admin</a>
</nav>

{% if messages %}
  <ul class="alerts">
    {% for message in messages %}
      <li class="alert alert-{{ message.tags }}">{{ message }}</li>
    {% endfor %}
  </ul>
{% endif %}

{% block content %}{% endblock %}
```

- Carga el tag `static` y el CSS en `static/css/base.css`.
- Define `block title` y `block content`.
- Muestra mensajes del framework `messages`.

#### `vet/templates/vet/listado.html`

```django
{% extends 'base.html' %}
{% block title %}{{ titulo }} — DjangoLab01{% endblock %}
{% block content %}
<header><h1>{{ titulo }}</h1><a href="{% url 'vet:nueva' %}">Registrar nueva mascota</a></header>
{% if mascotas %}
  <table>... {% for mascota in mascotas %} ... {% endfor %}</table>
{% else %}
  <p>Aún no hay mascotas registradas.</p>
{% endif %}
{% endblock %}
```

- Hereda de `base.html`.
- Itera `mascotas` y usa `{{ mascota.get_especie_display }}`, `{{ mascota.get_sexo_display }}`, filtros `|default:"—"` y `|date:"d/m/Y"` para `fecha_registro`.
- Muestra estado con `{% if mascota.activo %}`.

#### `vet/templates/vet/formulario.html`

```django
{% extends 'base.html' %}
{% block content %}
<form method="post" class="form-wrap">
  {% csrf_token %}
  {% for field in form %}
    <label for="{{ field.id_for_label }}">{{ field.label }}</label>
    {{ field }}
    {% for error in field.errors %}<small class="error">{{ error }}</small>{% endfor %}
  {% endfor %}
  <button type="submit">Guardar</button>
  <a href="{% url 'vet:listado' %}">Cancelar</a>
</form>
{% endblock %}
```

- Hereda de `base.html`.
- `method="post"` + `{% csrf_token %}` obligatorio.
- Renderizado genérico `{% for field in form %}` con `field.label`, `field`, `field.errors` y `field.help_text`.
- Botón Guardar y enlace Cancelar hacia `vet:listado`.

## 3. Conexión con el módulo principal `config`

### 3.1 Registro de la app en `config/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sesion1',
    'vet',        # <-- Laboratorio 02
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],  # templates/base.html global
    'APP_DIRS': True,                  # habilita vet/templates/vet/
    'OPTIONS': {'context_processors': [..., 'django.contrib.messages.context_processors.messages']},
}]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # static/css/base.css
```

Sin `'vet'` en `INSTALLED_APPS`, Django no detecta modelos, migraciones ni templates de la app.

### 3.2 Inclusión de URLs en `config/urls.py`

```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sesion1.urls')),
    path('vet/', include('vet.urls')),  # delega a vet/urls.py
]
```

### 3.3 URLs de la app `vet/urls.py`

```python
app_name = 'vet'
urlpatterns = [
    path('', views.listado, name='listado'),       # /vet/
    path('nueva/', views.registrar, name='nueva'), # /vet/nueva/
]
```

El `app_name = 'vet'` habilita el namespacing `{% url 'vet:listado' %}` y `redirect('vet:listado')`.

### 3.4 Flujo de una request

Diagrama textual:

```
Navegador
  │
  │ GET /vet/  o  GET/POST /vet/nueva/
  ▼
config/urls.py  ── path('vet/', include('vet.urls')) ──► vet/urls.py
                                                      ├─ ''       → views.listado
                                                      └─ 'nueva/' → views.registrar
                                                              │
                           ┌──────────────────────────────────┼───────────────────────┐
                           ▼                                  ▼                       ▼
                      vet/models.Mascota              vet/forms.MascotaForm     messages framework
                      (ORM / SQLite)                  (validación)              (success)
                           │                                  │                       │
                           └──────────────────┬───────────────┘                       │
                                              ▼                                       ▼
                                     views.py construye contexto
                                     {'titulo': ..., 'mascotas'|'form': ...}
                                              │
                                              ▼
                                     Template (herencia)
                                     base.html ← vet/listado.html | vet/formulario.html
                                     + static/css/base.css, {% csrf_token %}
                                              │
                                              ▼
                                     HttpResponse (HTML renderizado)
                                              │
                                              ▼
                                         Navegador
```

Ejemplo concreto `GET /vet/`:

1. `config/urls.py` hace match `vet/` y delega a `vet/urls.py`.
2. `vet/urls.py` hace match `''` -> `views.listado`.
3. `listado` ejecuta `_sembrar_mascotas()` (si `Mascota.objects.count() == 0` inserta Luna/Rocky/Misi/Kiwi/Tom), luego `Mascota.objects.all()`.
4. `render(request, 'vet/listado.html', contexto)` busca el template (APP_DIRS + DIRS), lo hereda de `base.html` y lo renderiza con `mascotas`.
5. Respuesta HTML vuelve al navegador con tabla y nav.

Ejemplo `POST /vet/nueva/`:

1. Routing idéntico hacia `views.registrar`.
2. `MascotaForm(request.POST)` valida; si ok, `form.save()` escribe en `vet_mascota`, `messages.success` encola mensaje y `redirect('vet:listado')` responde 302 a `/vet/`.
3. El navegador sigue el redirect y repite el flujo de `listado`, mostrando el `alert` de éxito desde `base.html`.

### 3.5 Mapa archivo → rol MVT

| Archivo | Rol MVT | Qué aporta |
|---|---|---|
| `vet/models.py` | **Model** | Define `Mascota`, campos, `Meta`, `__str__`; mapea a tabla SQLite |
| `vet/forms.py` | **Model + View (apoyo)** | `MascotaForm` valida y guarda `Mascota`; puente Model-View |
| `vet/views.py` | **View (Controller)** | `listado` y `registrar`; siembra, consulta ORM, valida form, redirige |
| `vet/urls.py` | **Enrutador** | Mapea `/vet/` y `/vet/nueva/` a views; `app_name='vet'` para namespacing |
| `vet/templates/vet/listado.html` | **Template** | Tabla de mascotas, herencia de `base.html` |
| `vet/templates/vet/formulario.html` | **Template** | Formulario con `csrf_token` y render de campos |
| `templates/base.html` | **Template base** | Layout, `static/css/base.css`, nav, blocks, mensajes |
| `config/settings.py` | **Configuración** | `INSTALLED_APPS=['vet']`, `TEMPLATES.DIRS`, `STATICFILES_DIRS` |
| `config/urls.py` | **Configuración / Dispatcher** | `path('vet/', include('vet.urls'))` integra la app al proyecto |

## 4. Cómo probarlo

### 4.1 Levantar el entorno (PowerShell)

```powershell
# desde C:\DjangoLab01
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # o pip install django==6.1
python manage.py migrate
python manage.py runserver
```

> Si `vet/migrations/` no existe o se modificó `models.py`:

```powershell
python manage.py makemigrations vet
python manage.py migrate
```

### 4.2 URLs a verificar

| URL | View | Qué ver |
|---|---|---|
| `http://127.0.0.1:8000/vet/` | `listado` | Título "Pacientes de la Veterinaria", tabla con 5 registros sembrados (Luna, Rocky, Misi, Kiwi, Tom) si la BD estaba vacía. Botón "Registrar nueva mascota" -> `/vet/nueva/` |
| `http://127.0.0.1:8000/vet/nueva/` | `registrar` (GET) | Formulario con campos `nombre`, `especie`, `raza`, `sexo`, `fecha_nacimiento` (type=date), `peso_kg`, `color`, `nombre_dueno`, `telefono_dueno`, `observaciones`, `activo`. Token CSRF oculto en el HTML. |
| `http://127.0.0.1:8000/vet/nueva/` (POST) | `registrar` (POST) | Al enviar válido, redirige a `/vet/` y muestra alerta "Mascota registrada correctamente." |

Navegación desde `base.html`: el enlace **Veterinaria** (`{% url 'vet:listado' %}`) debe estar visible en todas las páginas.

### 4.3 Comandos `manage.py` relevantes

```powershell
# Ver migraciones de vet
python manage.py showmigrations vet

# Crear superusuario para revisar datos en /admin/
python manage.py createsuperuser

# Shell para inspeccionar datos sin pasar por la view
python manage.py shell
>>> from vet.models import Mascota
>>> Mascota.objects.count()
>>> list(Mascota.objects.values_list('nombre', flat=True))

# Tests (si existen)
python manage.py test vet
```

### 4.4 Casos de prueba manual

1. Borrar `db.sqlite3` y correr `migrate` -> `GET /vet/` debe re-sembrar los 5 registros automáticamente.
2. `GET /vet/nueva/` -> enviar sin `nombre` -> debe mostrar error de campo requerido y no redirigir.
3. Registrar mascota nueva válida -> aparece en `GET /vet/` y persiste tras recargar (orden descendente por `fecha_registro`).
