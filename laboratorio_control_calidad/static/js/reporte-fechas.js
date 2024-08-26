    
    $(document).ready(function() {
        $('#form-fechas').on('submit', function(event) {
            event.preventDefault();
    
            var fechaInicial = $('#fecha-inicial').val();
            var fechaFinal = $('#fecha-final').val();
    
            $.ajax({
                url: '/reportes/diario_Semanal_Data/',  // URL de tu vista ReporteR49RangoFechaView
                method: 'POST',
                data: {
                    'fecha-inicial': fechaInicial,
                    'fecha-final': fechaFinal,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                // success: function(data) {
                //     // Suponiendo que quieres redirigir a una URL específica después de recibir los resultados
                //     window.location.href = '/reportes/mostrar-resultados/?datos=' + encodeURIComponent(JSON.stringify(data));
                // },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        });
    });


    // $(function() {
    //     // Manejar el envío del formulario del modal
    //     $('#form-fechas').on('submit', function(event) {
    //         event.preventDefault(); // Evita el comportamiento predeterminado del formulario

    //         // Realiza la solicitud AJAX
    //         $.ajax({
    //             url: $(this).attr('action'), // Usa la URL de la acción del formulario
    //             type: 'POST', // Cambia a 'GET' si así lo prefieres
    //             data: $(this).serialize(), // Serializa los datos del formulario
    //             dataType: 'json',
    //             success: function(data) {
    //                 console.log('Datos del reporte:', data); // Maneja los datos recibidos en la respuesta

    //                 // Puedes agregar lógica aquí para actualizar la UI según los datos recibidos
    //             },
    //             error: function(xhr, status, error) {
    //                 console.error("Error al obtener los cálculos:", error);
    //                 // Manejar el error
    //             }
    //         });
    //     });
    // });
