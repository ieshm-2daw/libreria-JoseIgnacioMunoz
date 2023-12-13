from typing import Any
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Libro, Prestamo
from .forms import LibroForm
from django.urls import reverse_lazy
from datetime import date, timedelta
from django.shortcuts import get_object_or_404, render, redirect

class LibroCreateView(CreateView):
    model = Libro
    template_name = 'new.html'
    success_url = reverse_lazy('list')
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

class LibroUpdateView(UpdateView):
    model = Libro
    template_name = 'edit.html'
    success_url = reverse_lazy('list')
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

class LibroListView(ListView):
    model = Libro
    template_name = 'list.html'

    #Para filtrar los libros disponibles: 
    #queryset = Libro.objects.filter(disponibilidad='disponible')


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #son como los context_object_name 
        context = super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad = 'disponible')
        context['libros_prestados'] = Libro.objects.filter(disponibilidad = 'prestado')

        return context

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'detail.html'

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'delete.html'
    success_url = reverse_lazy('list')

class CrearPrestamoView(View):
    template_name = 'prestamo.html'

    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return render(request, self.template_name, {'libroPrestado': libro})

    def post(self, request, pk):
        usuario = request.user
        libro = get_object_or_404(Libro, pk=pk)
        fecha_prestamo = date.today()
        fecha_devolucion=fecha_prestamo+timedelta(days=30)

        prestamo = Prestamo.objects.create(libro_prestado=libro, fecha_prestamo=fecha_prestamo, fecha_devolucion=fecha_devolucion, usuario=usuario, estado="prestado")
        prestamo.save()

        libro.disponibilidad = 'prestado'
        libro.save()

        return redirect('list')
    
class DevolucionView(View):
    template_name = 'devolucion.html'

    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return render(request, self.template_name, {'libroDevuelto': libro})

    def post(self, request, pk):
        usuario = request.user
        libro = get_object_or_404(Libro, pk=pk)
        prestamo = get_object_or_404(Prestamo, libro_prestado=libro, usuario=usuario, estado='prestado')
        fecha_prestamo = prestamo.fecha_prestamo
        fecha_devolucion=date.today()

        #prestamo = Prestamo.objects.create(libro_prestado=libro, fecha_prestamo=fecha_prestamo, fecha_devolucion=fecha_devolucion, usuario=usuario, estado="disponible")
        prestamo.fecha_prestamo = fecha_prestamo
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.estado = "devuelto"
        prestamo.save()

        libro.disponibilidad = 'disponible'
        libro.save()

        return redirect('list')
    
class ListPrestamoUsuarioView(ListView):
    model = Prestamo
    template_name = 'libros_prestados_usuario.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #son como los context_object_name 
        context = super().get_context_data(**kwargs)
        context['prestamo_prestado'] = Prestamo.objects.filter(estado = 'prestado', usuario=self.request.user)
        context['prestamo_devuelto'] = Prestamo.objects.filter(estado = 'devuelto', usuario=self.request.user)

        return context
    
class PrestamosExpiranPronto(ListView):
    model = Prestamo
    template_name = 'prestamos_expiran_pronto.html'
    prestamo = get_object_or_404(Prestamo, estado='prestado')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        fecha_limite = date.today() + timedelta(days=5)
        context = super().get_context_data(**kwargs) 
        context['expiranPronto'] = Prestamo.objects.filter(estado = 'prestado', fecha_devolucion__lte=fecha_limite)

        return context
    