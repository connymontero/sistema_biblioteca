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

    # Libro (Conny agrega aquí sus rutas: libro_panel, libro_crear,
    # libro_editar con <str:isbn>, libro_eliminar)
]
