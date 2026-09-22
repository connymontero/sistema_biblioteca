from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Editorial
    path('editoriales/', views.editorial_panel, name='editorial_panel'),
    path('editoriales/crear/', views.editorial_crear, name='editorial_crear'),
    path('editoriales/<int:pk>/editar/', views.editorial_editar, name='editorial_editar'),
    path('editoriales/eliminar/', views.editorial_eliminar, name='editorial_eliminar'),

    # Género
    path('generos/', views.genero_panel, name='genero_panel'),
    path('generos/crear/', views.genero_crear, name='genero_crear'),
    path('generos/<int:pk>/editar/', views.genero_editar, name='genero_editar'),
    path('generos/eliminar/', views.genero_eliminar, name='genero_eliminar'),

    # Libro
    path('libros/', views.libro_panel, name='libro_panel'),
    path('libros/crear/', views.libro_crear, name='libro_crear'),
    path('libros/<int:pk>/editar/', views.libro_editar, name='libro_editar'),
    path('libros/eliminar/', views.libro_eliminar, name='libro_eliminar'),
]
