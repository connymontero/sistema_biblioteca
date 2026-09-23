// Visor de descripción del panel de Libros.
//
// Muestra, debajo de la tabla, el título y la descripción del libro cuyo botón
// del ojo se pulsó. El texto ya viene en el HTML dentro de data-descripcion,
// porque el queryset de la vista trae todos los campos del modelo: por eso el
// visor no necesita pedirle nada al servidor (a diferencia del modal, que sí
// hace fetch porque necesita que Django renderice un formulario).
//
// Contrato con libros/panel.html:
//   .btn-ver-desc        botón por fila, con data-titulo y data-descripcion
//   #visor-descripcion   contenedor oculto con la clase d-none
//   #desc-titulo         donde se escribe el título del libro
//   #desc-texto          textarea de solo lectura con la descripción
//
// Este archivo se carga únicamente desde el {% block scripts %} del panel de
// libros, no desde base.html: no tiene sentido descargarlo en las demás páginas.

document.addEventListener('click', (evento) => {
    // closest: el clic puede caer en el <svg> del ícono y no en el botón
    const boton = evento.target.closest('.btn-ver-desc');
    if (!boton) return;

    const texto = document.getElementById('desc-texto');
    document.getElementById('desc-titulo').textContent = boton.dataset.titulo;
    texto.value = boton.dataset.descripcion || '(Este libro no tiene descripción)';
    document.getElementById('visor-descripcion').classList.remove('d-none');

    // El alto se ajusta al contenido para que no aparezca barra de scroll.
    // Primero 'auto' para que scrollHeight mida el texto nuevo y no conserve
    // el alto del libro anterior.
    texto.style.height = 'auto';
    texto.style.height = texto.scrollHeight + 'px';
});
