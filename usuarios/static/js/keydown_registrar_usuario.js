document.addEventListener('keydown', function(event) {
    const key = event.key; // Identificar qué tecla fue presionada
    if (key === "ArrowUp" || key === "ArrowDown") {
        const inputs = Array.from(document.querySelectorAll('#form_table input, #form_table select, #form_table textarea'));
        const activeElement = document.activeElement;
        const currentIndex = inputs.indexOf(activeElement);
        let nextIndex = currentIndex;

        if (key === "ArrowUp" && currentIndex > 0) {
            nextIndex = currentIndex - 1;
        } else if (key === "ArrowDown" && currentIndex < inputs.length - 1) {
            nextIndex = currentIndex + 1;
        }

        if (nextIndex !== currentIndex) {
            inputs[nextIndex].focus(); // Mover el foco al próximo campo
            event.preventDefault(); // Prevenir el comportamiento predeterminado de las teclas de flecha
        }
    }
});