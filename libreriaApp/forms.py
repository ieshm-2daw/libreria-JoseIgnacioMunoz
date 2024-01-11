from django import forms
from .models import Autor, Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo',
            'autores',
            'editorial',
            'fecha_publicacion',
            'genero',
            'isbn',
            'resumen',
            'disponibilidad',
            'portada',
        ]