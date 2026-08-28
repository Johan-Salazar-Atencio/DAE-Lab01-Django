---
tags: [laboratorio-02, ejercicio-03, modelo-datos, mascota, django]
---

# Ejercicio 3 · Modelo de datos del paciente / mascota

Documentación del modelo de datos estático de la entidad **PACIENTE / MASCOTA**: los campos que la componen, la justificación de la entidad raíz y su implementación fiel en la app `vet`.

## Tabla de campos

| Campo | Tipo de dato | Ejemplo | Justificación |
| --- | --- | --- | --- |
| nombre | `CharField(max_length=100)` | `"Luna"` | Identificador descriptivo usado en listados y buscador |
| especie | `CharField` con choices (`perro`/`gato`/`ave`/`otro`) | `"perro"` | Determina el tipo de paciente y condiciona el seguimiento; conjunto cerrado |
| raza | `CharField(max_length=100, blank=True)` | `"Golden Retriever"` | Complementa la identificación y aporta contexto clínico; opcional |
| sexo | `CharField` con choices (`macho`/`hembra`) | `"hembra"` | Dato clínico relevante (castración, gestación); dos valores |
| fecha_nacimiento | `DateField(null=True, blank=True)` | `2024-03-15` | Permite calcular la edad y programar controles; opcional |
| peso_kg | `DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)` | `23.50` | Esencial para dosificación y seguimiento; admite decimal |
| color | `CharField(max_length=50, blank=True)` | `"blanco con manchas"` | Identificación física; opcional |
| nombre_dueno | `CharField(max_length=100)` | `"María Pérez"` | Vínculo humano obligatorio para contacto y titularidad |
| telefono_dueno | `CharField(max_length=20)` | `"+52 555 123 4567"` | Canal de contacto para citas y recordatorios; obligatorio |
| observaciones | `TextField(blank=True)` | `"Alérgica a penicilina"` | Notas libres; contexto no estructurado |
| fecha_registro | `DateTimeField(auto_now_add=True)` | `2026-08-28 09:15` | Trazabilidad del alta; se llena solo |
| activo | `BooleanField(default=True)` | `True` | Marca pacientes inactivos sin eliminar el registro |

## Justificación de Mascota como entidad raíz

En una veterinaria el paciente es la **mascota**, no quien paga ni quien atiende; toda la información clínica se ancla en el animal y da identidad al expediente.

El dueño hoy se modela **embebido** (`nombre_dueno`, `telefono_dueno`) por alcance mínimo. En el futuro se extraerá a una entidad **Dueño/Cliente** con identidad propia, y Mascota tendrá una `ForeignKey(Dueno)`. Es deuda técnica consciente (KISS): agregar la tabla Dueño hoy complicaría el CRUD sin aportar al laboratorio.

## Implementación en Django

Descripción fiel del código ya escrito en la app `vet`.

### Modelo `Mascota` en `vet/models.py`

Define la clase `Mascota` con **12 campos**:

- `nombre`: `CharField(max_length=100)`
- `especie`: `CharField` con choices `perro`/`gato`/`ave`/`otro`
- `raza`: `CharField(max_length=100, blank=True)`
- `sexo`: `CharField` con choices `macho`/`hembra`
- `fecha_nacimiento`: `DateField(null=True, blank=True)`
- `peso_kg`: `DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)`
- `color`: `CharField(max_length=50, blank=True)`
- `nombre_dueno`: `CharField(max_length=100)`
- `telefono_dueno`: `CharField(max_length=20)`
- `observaciones`: `TextField(blank=True)`
- `fecha_registro`: `DateTimeField(auto_now_add=True)`
- `activo`: `BooleanField(default=True)`

La `Meta` de la clase define `verbose_name = 'Mascota'`, `verbose_name_plural = 'Mascotas'` y `ordering = ['-fecha_registro']` (de más reciente a más antigua). El método `__str__` devuelve el nombre seguido de la especie legible, por ejemplo `Luna (Perro)`, usando `get_especie_display()`.

### Registros de ejemplo

Hay **5 registros de ejemplo estáticos** (Luna, Rocky, Misi, Kiwi y Tom) que se siembran automáticamente en el listado cuando la tabla está vacía.

### Formulario

`MascotaForm` en `vet/forms.py` es un `ModelForm` basado en `Mascota` con `fields = '__all__'`, configurado con `DateInput` de tipo `date` para la fecha de nacimiento y con etiquetas legibles en español para todos los campos.

### Vistas

`vet/views.py` expone dos vistas:

- **`listado`**: siembra los datos de ejemplo si no hay registros y renderiza `vet/listado.html` con todas las mascotas.
- **`registrar`**: maneja `GET` (formulario vacío) y `POST` (valida, guarda, muestra un mensaje de éxito y redirige al listado).

### URLs

En `vet/urls.py` con `app_name = 'vet'`:

| Ruta | Nombre | Vista |
| --- | --- | --- |
| `''` | `listado` | listado de mascotas |
| `'nueva/'` | `nueva` | registrar mascota |

### Templates

- `vet/listado.html`: lista las mascotas registradas.
- `vet/formulario.html`: formulario para registrar una mascota.

Ambos heredan de `base.html`, la plantilla común del proyecto.
