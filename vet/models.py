from django.db import models


class Mascota(models.Model):
    ESPECIES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('otro', 'Otro'),
    ]
    SEXOS = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIES)
    raza = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXOS)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    nombre_dueno = models.CharField(max_length=100)
    telefono_dueno = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombre} ({self.get_especie_display()})'