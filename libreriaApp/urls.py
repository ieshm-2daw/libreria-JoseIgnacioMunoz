from django.urls import path
from .views import LibroListView, LibroDetailView, LibroCreateView, LibroUpdateView, LibroDeleteView, CrearPrestamoView, DevolucionView, ListPrestamoUsuarioView, PanelView

urlpatterns = [
    path('', LibroListView.as_view(), name='list'),
    path('libros/nuevo/', LibroCreateView.as_view(), name='new'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='detail'),
    path('libros/<int:pk>/editar/', LibroUpdateView.as_view(), name='update'),
    path('libros/<int:pk>/eliminar/', LibroDeleteView.as_view(), name='delete'),
    path('libros/<int:pk>/prestar/', CrearPrestamoView.as_view(), name='prestar'),
    path('libros/<int:pk>/devolver/', DevolucionView.as_view(), name='devolver'),
    path('libros/prestamosUsuario/', ListPrestamoUsuarioView.as_view(), name='prestamosUsuario'),
    path('libros/panel/', PanelView.as_view(), name='panel'),
]
