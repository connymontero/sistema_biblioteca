from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import ProtectedError, Q
from .models import Editorial, Genero, Libro
from .forms import EditorialForm, GeneroForm, LibroForm


def inicio(request):
    return render(request, 'inicio.html')


# ---------- Editorial ----------

def editorial_panel(request):
    q = request.GET.get('q', '')                 # texto del buscador ('' si no viene)
    orden = request.GET.get('orden', 'asc')      # 'asc' por defecto

    editoriales = Editorial.objects.all()
    if q:
        editoriales = editoriales.filter(nombre__icontains=q)
    editoriales = editoriales.order_by('nombre' if orden == 'asc' else '-nombre')

    return render(request, 'editoriales/panel.html', {
        'editoriales': editoriales,
        'q': q,
        'orden': orden,
    })


def editorial_crear(request):
    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()                                          # INSERT
            messages.success(request, 'Editorial creada.')
            return JsonResponse({'ok': True})
    else:
        form = EditorialForm()
    return render(request, 'editoriales/_form.html', {
        'form': form,
        'accion': request.path,                                  # URL a la que el form hace POST
    })


def editorial_editar(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    if request.method == 'POST':
        form = EditorialForm(request.POST, instance=editorial)
        if form.is_valid():
            form.save()                                          # UPDATE
            messages.success(request, 'Editorial actualizada.')
            return JsonResponse({'ok': True})
    else:
        form = EditorialForm(instance=editorial)
    return render(request, 'editoriales/_form.html', {
        'form': form,
        'accion': request.path,
    })


def editorial_eliminar(request):
    if request.method == 'POST':
        ids = request.POST.getlist('seleccionados')             # lista de pks marcados
        try:
            cantidad, _ = Editorial.objects.filter(pk__in=ids).delete()
            messages.success(request, f'{cantidad} editorial(es) eliminada(s).')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: hay libros asociados a alguna editorial seleccionada.')
    return redirect('editorial_panel')


# ---------- Género ----------

def genero_panel(request):
    q = request.GET.get('q', '')
    orden = request.GET.get('orden', 'asc')

    generos = Genero.objects.all()
    if q:
        generos = generos.filter(nombre__icontains=q)
    generos = generos.order_by('nombre' if orden == 'asc' else '-nombre')

    return render(request, 'generos/panel.html', {
        'generos': generos,
        'q': q,
        'orden': orden,
    })


def genero_crear(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Género creado.')
            return JsonResponse({'ok': True})
    else:
        form = GeneroForm()
    return render(request, 'generos/_form.html', {
        'form': form,
        'accion': request.path,
    })


def genero_editar(request, pk):
    genero = get_object_or_404(Genero, pk=pk)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            messages.success(request, 'Género actualizado.')
            return JsonResponse({'ok': True})
    else:
        form = GeneroForm(instance=genero)
    return render(request, 'generos/_form.html', {
        'form': form,
        'accion': request.path,
    })


def genero_eliminar(request):
    if request.method == 'POST':
        ids = request.POST.getlist('seleccionados')
        try:
            cantidad, _ = Genero.objects.filter(pk__in=ids).delete()
            messages.success(request, f'{cantidad} género(s) eliminado(s).')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: hay libros asociados a algún género seleccionado.')
    return redirect('genero_panel')


# ---------- Libro ----------

# Columnas por las que se permite ordenar desde el panel (lista blanca:
# nunca se pasa request.GET directo a order_by).
ORDEN_LIBRO = {
    'titulo': 'titulo', '-titulo': '-titulo',
    'autor': 'autor', '-autor': '-autor',
    'precio': 'precio', '-precio': '-precio',
    'stock': 'stock', '-stock': '-stock',
    'anio': 'anio_publicacion', '-anio': '-anio_publicacion',
}


def libro_panel(request):
    q = request.GET.get('q', '')                    # texto: busca en título, autor o ISBN
    editorial_id = request.GET.get('editorial', '') # id de editorial ('' = todas)
    genero_id = request.GET.get('genero', '')       # id de género ('' = todos)
    orden = request.GET.get('orden', 'titulo')

    # select_related hace un solo SELECT con JOIN a editorial y genero;
    # sin él, la tabla haría 2 consultas extra por cada fila (problema N+1).
    libros = Libro.objects.select_related('editorial', 'genero')
    if q:
        libros = libros.filter(
            Q(titulo__icontains=q) | Q(autor__icontains=q) | Q(isbn__icontains=q)
        )
    if editorial_id:
        libros = libros.filter(editorial_id=editorial_id)
    if genero_id:
        libros = libros.filter(genero_id=genero_id)
    libros = libros.order_by(ORDEN_LIBRO.get(orden, 'titulo'))

    return render(request, 'libros/panel.html', {
        'libros': libros,
        'editoriales': Editorial.objects.order_by('nombre'),   # para el <select> del filtro
        'generos': Genero.objects.order_by('nombre'),
        'q': q,
        'editorial_id': editorial_id,
        'genero_id': genero_id,
        'orden': orden,
    })


def libro_crear(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()                                          # INSERT
            messages.success(request, 'Libro creado.')
            return JsonResponse({'ok': True})
    else:
        form = LibroForm()
    return render(request, 'libros/_form.html', {
        'form': form,
        'accion': request.path,
    })


def libro_editar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()                                          # UPDATE
            messages.success(request, 'Libro actualizado.')
            return JsonResponse({'ok': True})
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/_form.html', {
        'form': form,
        'accion': request.path,
    })


def libro_eliminar(request):
    # Sin try/except ProtectedError: ningún modelo apunta a Libro con FK,
    # así que borrar un libro nunca está protegido.
    if request.method == 'POST':
        ids = request.POST.getlist('seleccionados')
        cantidad, _ = Libro.objects.filter(pk__in=ids).delete()
        messages.success(request, f'{cantidad} libro(s) eliminado(s).')
    return redirect('libro_panel')
