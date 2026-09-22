from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Editorial, Genero, Libro
from .forms import EditorialForm, GeneroForm


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


# ---------- Libro (Conny agrega aquí: libro_panel, libro_crear, libro_editar, libro_eliminar) ----------
