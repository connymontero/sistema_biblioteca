from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


# definir el modelo 

class Libro(models.Model):
    titulo = models.CharField(max_length=40)
    autor = models.CharField(max_length=30)
    isbn = models.CharField(max_length=13, unique=True)
    precio = models.DecimalField(
        max_digits=6,
        decimal_places=2, 
        verbose_name='Precio ($)', 
        validators=[MinValueValidator(0.01)],
    )

genero = models.CharField(
    max_length=20,
        )

editorial = models.CharField(
    max_length=30,
        )

stock = models.IntegerField(
    verbose_name='Stock',
    validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

anio_publicacion = models.IntegerField(
    validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
    verbose_name='Año de publicación',
    )

descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')



def __str__(self):
    return f"{self.titulo} - {self.autor}" 