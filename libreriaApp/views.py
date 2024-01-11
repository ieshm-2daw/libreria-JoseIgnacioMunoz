from typing import Any
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Libro, Prestamo, Autor 
from .forms import LibroForm
from django.urls import reverse_lazy
from datetime import date, timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 


class LibroCreateView(LoginRequiredMixin, CreateView):
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

class LibroUpdateView(LoginRequiredMixin, UpdateView):
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
    form_class = LibroForm

    def get_queryset(self):
        queryset = Libro.objects.all()
        
        autor_nombre = self.request.GET.get('autores')
        genero = self.request.GET.get('genero')

        if autor_nombre:
            queryset = queryset.filter(autores__nombre__icontains=autor_nombre)

        if genero:
            queryset = queryset.filter(genero=genero)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor_filter'] = Autor.objects.all()
        
        autores_seleccionados = self.request.GET.getlist('autores')
        genero_seleccionado = self.request.GET.get('genero')

        if autores_seleccionados and genero_seleccionado:
            context['disponibles'] = Libro.objects.filter(disponibilidad='disponible', autores__nombre__in=autores_seleccionados, genero = genero_seleccionado)
            context['prestados'] = Libro.objects.filter(disponibilidad='prestado', autores__nombre__in=autores_seleccionados, genero = genero_seleccionado)

        context['generos'] = Libro.objects.values_list('genero', flat=True).distinct()

        return context

class LibroDetailView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = 'detail.html'
    paginate_by = 2

class LibroDeleteView(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = 'delete.html'
    success_url = reverse_lazy('list')

class CrearPrestamoView(LoginRequiredMixin, View):
    template_name = 'prestamo.html'

    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return render(request, self.template_name, {'libro': libro})

    def post(self, request, pk):
        usuario = request.user
        libro = get_object_or_404(Libro, pk=pk)
        fecha_prestamo = date.today()
        fecha_devolucion=fecha_prestamo+timedelta(days=7) # HE PUESTO 7 PARA COMPROBAR QUE FUNCIONA LA VISTA DE PRESTAMOS QUE EXPIRAN PRONTO (EN MENOS DE 5 DIAS)

        prestamo = Prestamo.objects.create(libro_prestado=libro, fecha_prestamo=fecha_prestamo, fecha_devolucion=fecha_devolucion, usuario=usuario, estado="prestado")
        prestamo.save()

        libro.disponibilidad = 'prestado'
        libro.save()

        return redirect('list')
    
class DevolucionView(LoginRequiredMixin, View):
    template_name = 'devolucion.html'

    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return render(request, self.template_name, {'libro': libro})

    def post(self, request, pk):
        usuario = request.user
        libro = get_object_or_404(Libro, pk=pk)
        prestamo = Prestamo.objects.filter(libro_prestado=libro, usuario=usuario, estado='prestado').first()
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

class ListPrestamoUsuarioView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'libros_prestados_usuario.html' 

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #son como los context_object_name 
        context = super().get_context_data(**kwargs)
        context['prestamo_prestado'] = Prestamo.objects.filter(estado = 'prestado', usuario=self.request.user)
        context['prestamo_devuelto'] = Prestamo.objects.filter(estado = 'devuelto', usuario=self.request.user)

        return context
"""
#Siguientes dos vistas para panel de control:
class PrestamosExpiranPronto(ListView):
    model = Prestamo
    template_name = 'panel.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        fecha_limite = date.today() + timedelta(days=7)
        context = super().get_context_data(**kwargs) 
        context['expiranPronto'] = Prestamo.objects.filter(estado = 'prestado', fecha_devolucion__lte=fecha_limite)
        #__lte: https://stackoverflow.com/questions/4668619/how-do-i-filter-query-objects-by-date-range-in-django
        return context
"""
class PanelView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'panel.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['disponiblesLength'] = len(Libro.objects.filter(disponibilidad = 'disponible'))
        context['prestadosLength'] = len(Libro.objects.filter(disponibilidad='prestado'))

        fecha_actual = date.today()
        context['noDevueltos'] = Prestamo.objects.filter(estado = 'prestado', fecha_devolucion__lt=fecha_actual)

        ultimaSemana = fecha_actual + timedelta(days=7)
        context['expiranPronto'] = Prestamo.objects.filter(estado = 'prestado', fecha_devolucion__lte=ultimaSemana, fecha_devolucion__gte=fecha_actual)
        #__lte: https://stackoverflow.com/questions/4668619/how-do-i-filter-query-objects-by-date-range-in-django

        #context['topLibros'] 

        return context
        """
         Aunque model=Libro está configurado a nivel de la clase ListView, se puede trabajar 
         con otros modelos según las necesidades específicas de cada vista y su lógica.
        """

"""
class PanelPrestamoView(ListView):
    model = Prestamo
    template_name = 'panel.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        fecha_actual = date.today()
        context['noDevueltos'] = Prestamo.objects.filter(estado = 'prestado', fecha_devolucion__lt=fecha_actual)

        return context
"""