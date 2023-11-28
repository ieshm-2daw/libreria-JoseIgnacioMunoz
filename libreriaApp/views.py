from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Libro
from .forms import LibroForm
from django.urls import reverse_lazy

class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'new.html'
    success_url = reverse_lazy('list')

class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'edit.html'
    success_url = reverse_lazy('list')

class LibroListView(ListView):
    model = Libro
    template_name = 'list.html'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'detail.html'

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'delete.html'
    success_url = reverse_lazy('list')
