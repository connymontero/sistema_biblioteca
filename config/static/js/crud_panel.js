// Comportamiento común de los paneles CRUD (libros, editoriales, géneros).
// Contrato con el template del panel:
//   #form-tabla                 <form method="post" action="{% url '..._eliminar' %}"> que envuelve la tabla
//   input[name=seleccionados]   un checkbox por fila, value = pk
//   #chk-todos                  checkbox de cabecera para marcar/desmarcar todo
//   #btn-anadir                 data-url="{% url '..._crear' %}"  data-titulo="Nuevo ..."
//   #btn-modificar              data-url-editar="{% url '..._editar' 0 %}" (el 0 se reemplaza por el pk)
//   #btn-eliminar
// Los modales #modal-form y #modal-eliminar vienen de _modales.html (incluido en base.html).

document.addEventListener('DOMContentLoaded', () => {
    const formTabla = document.getElementById('form-tabla');
    if (!formTabla) return;                       // página sin panel (ej. inicio): no hay nada que hacer

    const btnAnadir    = document.getElementById('btn-anadir');
    const btnModificar = document.getElementById('btn-modificar');
    const btnEliminar  = document.getElementById('btn-eliminar');
    const chkTodos     = document.getElementById('chk-todos');

    const modalFormEl   = document.getElementById('modal-form');
    const modalForm     = new bootstrap.Modal(modalFormEl);
    const modalBody     = modalFormEl.querySelector('.modal-body');
    const modalTitulo   = modalFormEl.querySelector('.modal-title');
    const modalEliminar = new bootstrap.Modal(document.getElementById('modal-eliminar'));

    // ---- selección de filas ----
    const seleccionados = () => [...formTabla.querySelectorAll('input[name="seleccionados"]:checked')];

    function actualizarBotones() {
        const n = seleccionados().length;
        btnModificar.disabled = (n !== 1);        // modificar: exactamente una fila
        btnEliminar.disabled  = (n === 0);        // eliminar: al menos una
    }

    formTabla.addEventListener('change', (e) => {
        if (e.target === chkTodos) {
            formTabla.querySelectorAll('input[name="seleccionados"]')
                     .forEach(chk => { chk.checked = chkTodos.checked; });
        }
        actualizarBotones();
    });

    // ---- añadir / modificar: pedir el fragmento del form y mostrarlo en el modal ----
    async function abrirFormulario(url, titulo) {
        const respuesta = await fetch(url);       // GET -> la vista devuelve solo el <form> (_form.html)
        modalBody.innerHTML = await respuesta.text();
        modalTitulo.textContent = titulo;
        modalForm.show();
    }

    btnAnadir.addEventListener('click', () => {
        abrirFormulario(btnAnadir.dataset.url, btnAnadir.dataset.titulo);
    });

    btnModificar.addEventListener('click', () => {
        const pk = seleccionados()[0].value;
        const url = btnModificar.dataset.urlEditar.replace('/0/', '/' + pk + '/');
        abrirFormulario(url, btnModificar.dataset.titulo);
    });

    // ---- envío del form del modal ----
    // Se escucha en modalBody (delegación) porque el <form> se crea después.
    modalBody.addEventListener('submit', async (e) => {
        e.preventDefault();                       // no navegar: lo mandamos por fetch
        const form = e.target;
        const respuesta = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),             // incluye el csrfmiddlewaretoken del {% csrf_token %}
        });
        const tipo = respuesta.headers.get('content-type') || '';
        if (tipo.includes('application/json')) {
            location.reload();                    // {"ok": true}: guardado -> recargar tabla y ver el message
        } else {
            modalBody.innerHTML = await respuesta.text();   // HTML: el form con errores; el modal sigue abierto
        }
    });

    // ---- eliminar ----
    btnEliminar.addEventListener('click', () => {
        const n = seleccionados().length;
        document.getElementById('eliminar-texto').textContent =
            '¿Eliminar ' + n + (n === 1 ? ' registro' : ' registros') + '? Esta acción no se puede deshacer.';
        modalEliminar.show();
    });

    document.getElementById('btn-confirmar-eliminar').addEventListener('click', () => {
        formTabla.submit();                       // POST normal con los checkboxes marcados
    });

    actualizarBotones();
});
