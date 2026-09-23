// Limita cuántos dígitos se pueden escribir en los campos numéricos.
//
// Por qué hace falta: <input type="number"> ignora el atributo maxlength del HTML,
// así que sin esto el usuario puede teclear un número de cualquier largo y recién
// se entera del error al guardar.
//
// Contrato: cualquier <input data-maxlen="N"> queda limitado a N caracteres.
// Los valores salen de los límites del modelo y se ponen en los widgets de forms.py:
//   precio -> 8 dígitos (max_digits=10, decimal_places=2)
//   stock  -> 3 dígitos (máximo 100)
//   año    -> 4 dígitos
//
// Se escucha en document (delegación de eventos) porque los formularios se
// inyectan dentro del modal después de que la página cargó: los inputs todavía
// no existen cuando se ejecuta este archivo.
//
// No reemplaza ninguna validación: los validadores del modelo y los clean_<campo>()
// del formulario se siguen ejecutando en el servidor.

document.addEventListener('input', (evento) => {
    const campo = evento.target;
    const maximo = Number(campo.dataset.maxlen);   // undefined -> NaN -> se ignora
    if (!maximo) return;

    if (campo.value.length > maximo) {
        campo.value = campo.value.slice(0, maximo);
    }
});
