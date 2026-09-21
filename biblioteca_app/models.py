from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


def anio_actual():
    """Devuelve el año en curso. Se usa como límite superior del validador
    de anio_publicacion; al ser una función, se evalúa en cada validación
    y no una sola vez al importar el módulo."""
    return datetime.date.today().year


class Editorial(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre  # lo que se ve en selects y admin


class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Género')

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    titulo = models.CharField(max_length=40, verbose_name='Título')
    autor = models.CharField(max_length=30)
    precio = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Precio ($)',
        validators=[MinValueValidator(0.01)],
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    anio_publicacion = models.IntegerField(
        verbose_name='Año de publicación',
        validators=[MinValueValidator(1900), MaxValueValidator(anio_actual)],
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, verbose_name='Género')

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
