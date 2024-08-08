document.addEventListener('DOMContentLoaded', function() {
    // Verifica si hay errores en el formulario
    const errorMessages = document.querySelectorAll('.error-message');
    if (errorMessages.length > 0) {
        alert('Por favor corrige los errores en el formulario.');
    }
});