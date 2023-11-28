# gestion_biblioteca/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

class Usuario(AbstractUser):
    dni = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/')

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    sitio_web = models.URLField()

class Libro(models.Model):
    DISPONIBILIDAD_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
    ]

    titulo = models.CharField(max_length=255)
    autores = models.ManyToManyField(Autor)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)
    resumen = models.TextField()
    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDAD_CHOICES, default='disponible')
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
    ]

    libro_prestado = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prestado')