---
tags: [laboratorio-02, ejercicio-02, requisitos, funcionales]
---

# Ejercicio 2 · Requisitos funcionales

Requisitos funcionales del registro de pacientes, cada uno con su criterio de aceptación.

## RF-01 · Registrar una nueva mascota

> El sistema debe permitir al recepcionista registrar una nueva mascota con sus datos y los de su dueño para llevar el expediente actualizado.

**Criterio de aceptación:** al enviar el formulario con datos válidos, la mascota se guarda y aparece en el listado; si un campo obligatorio falta, se muestra un error sin perder lo cargado.

## RF-02 · Listar todas las mascotas

> El sistema debe permitir al usuario listar todas las mascotas registradas para consultar el padrón de pacientes.

**Criterio de aceptación:** el listado muestra nombre, especie, raza, dueño y estado activo, ordenadas por fecha de registro descendente.

## RF-03 · Marcar una mascota como activa o inactiva

> El sistema debe permitir al usuario marcar una mascota como activa o inactiva para reflejar si sigue siendo paciente.

**Criterio de aceptación:** campo booleano con valor por defecto activo, editable.

## RF-04 · Registrar fecha de nacimiento y peso

> El sistema debe permitir registrar la fecha de nacimiento y el peso de la mascota para estimar su edad y seguir su evolución corporal.

**Criterio de aceptación:** ambos campos editables en el formulario y visibles en el listado; el peso admite decimales.

## RF-05 · Registrar observaciones libres

> El sistema debe permitir registrar observaciones libres sobre la mascota para anotar alergias o condiciones relevantes.

**Criterio de aceptación:** campo de texto opcional que se conserva con el expediente.
