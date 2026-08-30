# DjangoLab01 — DAE

Laboratorio de desarrollo web con Django. Estudiante: **Johan Salazar**.

Repositorio: [Johan-Salazar-Atencio/DAE-Lab01-Django](https://github.com/Johan-Salazar-Atencio/DAE-Lab01-Django)

## Stack

- Python 3.14.7
- Django 6.1
- SQLite (desarrollo)
- Entorno virtual en `.venv`

## Instalación

```powershell
# clonar
git clone https://github.com/Johan-Salazar-Atencio/DAE-Lab01-Django.git
Set-Location DAE-Lab01-Django

# crear entorno e instalar dependencias
"$env:LOCALAPPDATA\Programs\Python\Python314\python.exe" -m venv .venv
& .\.venv\Scripts\python.exe -m pip install django

# migraciones y servidor
& .\.venv\Scripts\python.exe manage.py migrate
& .\.venv\Scripts\python.exe manage.py runserver
```

Abrir http://127.0.0.1:8000

## Uso

- `/` — Landing de Sesión 1
- `/vet/` — Listado de pacientes (Veterinaria)
- `/vet/nueva/` — Formulario de registro
- `/admin/` — Panel de administración

## Laboratorios

| Laboratorio | Estado | Entregables |
|---|---|---|
| **Lab 01 — Sesión 1** | ✅ Completado | Proyecto Django, app `sesion1`, landing, 10 agentes en `.opencode/agent/` |
| **Lab 02 — Veterinaria** | ✅ **Completado** | Investigación de la problemática, 5 requisitos funcionales, modelo `Mascota` (12 campos), app `vet` (models/forms/views/urls/templates con herencia de `base.html` y 5 registros estáticos), Vault de Obsidian en `docs/` |

> **Confirmación Lab 02:** La documentación de los Ejercicios 1, 2 y 3 está en `docs/laboratorio-02/` y la app `vet` está implementada, migrada y verificada en local (HTTP 200 en `/vet/` y `/vet/nueva/`).

## Estructura

```
.
├── config/                 # settings, urls, wsgi/asgi
├── sesion1/                # Lab 01
├── vet/                    # Lab 02 — Veterinaria
├── templates/base.html     # base compartida
├── static/css/base.css     # estilos
├── docs/                   # Vault de Obsidian
│   └── laboratorio-02/
├── manage.py
└── .opencode/agent/        # 10 agentes IA
```

## Agentes IA

`arquitecto`, `programacion`, `documentador`, `ui-ux`, `testing`, `git-ops`, `db-optimizer`, `api-docs`, `seguimiento`, `memoria`.

## Documentación (Vault Obsidian)

`docs/README.md` es el índice del vault. Abrir la carpeta `docs/` como vault en Obsidian.

## Licencia

Uso académico — DAE.
