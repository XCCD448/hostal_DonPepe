$("#formulario1").validate({
    rules: {
        "txtEmail": {
            required: true,
            email: true
        },
        "txtContrasena": {
            required: true,
            minlength: 5
        },
        "txtRepetirContrasena": {
            required: true,
            equalTo: '#id_txtContrasena'
        }
    }, // --> Fin de reglas
    messages: {
        "txtEmail": {
            required: 'Ingrese email!!!',
            email: 'No cumple formato'
        },
        "txtContrasena": {
            required: 'Ingrese Password!!!',
            minlength: 'Min. 5 caract'
        },
        "txtRepetirContrasena": {
            required: 'Repita el Password!!',
            equalTo: ' deben ser iguales!!!!'
        }
    } //-->Fin de mensajes

});