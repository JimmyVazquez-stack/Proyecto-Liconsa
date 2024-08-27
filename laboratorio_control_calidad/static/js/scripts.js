document.addEventListener('DOMContentLoaded', function() {
    // Verifica si hay errores en el formulario
    const errorMessages = document.querySelectorAll('.error-message');
    if (errorMessages.length > 0) {
        alert('Por favor corrige los errores en el formulario.');
    }
});


//  Page specific script datatable 
$(function() {
    $('.btnTest').on('click', function() {
        $.ajax({
            url: "{% url 'laboratorio_control_calidad:encabezador49V2_List'%}" , 
            type: 'POST',
            data: {
                id: 1
            },
            dataType: 'json'
        }).done(function(data) {
            console.log(data)
        }).fail(function(data) {
            alert("error");
        }).always(function(data) {

        })
    });

});