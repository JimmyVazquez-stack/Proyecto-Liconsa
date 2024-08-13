$(document).ready(function() {
    // Obtener el token CSRF de las cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // Configurar jQuery para incluir el token CSRF en las solicitudes AJAX
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var table = $('#tabla_turnos').DataTable({
        ajax: {
            url: '/catalogos/turnos/list/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'nombre' },
            { data: 'descripcion' },
            { data: 'hora_inicio' },
            { data: 'hora_fin' },
            {
                data: 'estatus',
                render: function (data, type, row) {
                    if (type === 'display') {
                        if (data) {
                            return '<i class="fas fa-check-circle" style="color: green;" title="Activo"></i>';
                        } else {
                            return '<i class="fas fa-times-circle" style="color: red;" title="Inactivo"></i>';
                        }
                    }
                    return data;  // Devuelve el dato sin formato para otros tipos de renderizado
                }
            },
            {
                data: null,
                defaultContent: `
                    <div class="d-flex justify-content-between">
                        <button class="btn btn-edit btn-warning"><i class="fa fa-pencil"></i></button>
                        <button class="btn btn-delete btn-danger"><i class="fa fa-trash"></i></button>
                    </div>
                `
            }
        ],
        pageLength: 5,
        lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "Todo"]],
        language: {
            lengthMenu: "Mostrar _MENU_ entradas",
            zeroRecords: "No se encontraron resultados",
            info: "Mostrando entradas _START_ a _END_ de _TOTAL_",
            infoEmpty: "Mostrando entradas 0 a 0 de 0",
            infoFiltered: "(filtrado de _MAX_ entradas totales)",
            search: "Buscar:",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            }
        },
        columnDefs: [
            {
                targets: -1,
                orderable: false
            }
        ]
    });

  // Abrir modal para añadir turno
$('#btnAddTurno').click(function() {
    $('#turnoModalLabel').text('Añadir Turno');
    $('#turnoForm')[0].reset(); // Resetea el formulario
    $('#nombre').val(''); // Selecciona la opción por defecto
    $('#activo').prop('checked', true); // Asume que el turno está activo por defecto
    $('#turnoId').val(''); // Limpia el ID del turno
    $('#turnoModal').modal('show');
});


// Abrir modal para editar turno
$('#tabla_turnos tbody').on('click', '.btn-edit', function() {
    var data = table.row($(this).parents('tr')).data();
    
    // Configurar el título del modal
    $('#turnoModalLabel').text('Editar Turno');
    
    // Rellenar los campos del formulario con los datos del turno
    $('#nombre').val(data.nombre);
    $('#descripcion').val(data.descripcion);
    $('#hora_inicio').val(data.hora_inicio.substring(0, 5));  // Ajustar formato de hora (HH:MM)
    $('#hora_fin').val(data.hora_fin.substring(0, 5));  // Ajustar formato de hora (HH:MM)
    
    // Establecer el estado del checkbox
    $('#estatus').prop('checked', data.estatus); 
    
    // Guardar el ID del turno para la edición
    $('#turnoId').val(data.id);
    
    // Mostrar el modal
    $('#turnoModal').modal('show');
});





// Guardar turno (añadir o editar) con validación usando SweetAlert2
$('#saveTurno').click(function() {
    var nombre = $('#nombre').val().trim();
    var descripcion = $('#descripcion').val().trim();
    var hora_inicio = $('#hora_inicio').val().trim();
    var hora_fin = $('#hora_fin').val().trim();
    var estatus = $('#estatus').is(':checked');  // Obtener el estado del checkbox

    // Validar que los campos no estén vacíos
    if (!nombre || !descripcion || !hora_inicio || !hora_fin) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Todos los campos son obligatorios',
        });
        return;
    }

    // Convertir las horas a objetos Date para validación
    var horaInicioDate = new Date('1970-01-01T' + hora_inicio + ':00Z');
    var horaFinDate = new Date('1970-01-01T' + hora_fin + ':00Z');
    var horaLimiteMatutino = new Date('1970-01-01T14:00:00Z');  // 2:00 PM
    var horaLimiteVespertino = new Date('1970-01-01T23:59:59Z');  // 11:59 PM

    // Validación específica para turnos matutinos
    if (nombre === 'Matutino') {
        if (horaInicioDate >= horaLimiteMatutino || horaFinDate > horaLimiteMatutino) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El turno matutino debe ser entre las 00:00 AM y las 2:00 PM',
            });
            return;
        }
    }

    // Validación específica para turnos vespertinos
    if (nombre === 'Vespertino') {
        if (horaInicioDate < horaLimiteMatutino || horaFinDate > horaLimiteVespertino) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El turno vespertino debe ser después de las 2:00 PM y antes de las 11:59 PM',
            });
            return;
        }
    }

    // Obtener el ID del turno si se está editando
    var turnoId = $('#turnoId').val();
    var url = turnoId ? `/catalogos/turnos/update/${turnoId}/` : '/catalogos/turnos/create/';
    var method = 'POST';

    $.ajax({
        url: url,
        method: method,
        data: $('#turnoForm').serialize() + '&estatus=' + estatus,
        success: function(response) {
            $('#turnoModal').modal('hide');
            table.ajax.reload();
            Swal.fire({
                icon: 'success',
                title: 'Guardado',
                text: 'Turno guardado con éxito',
            });
        },
        error: function(xhr) {
            var errorMessage = 'Error al guardar el turno';
            if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: errorMessage,
            });
        }
    });
});






// Manejadores manuales para cerrar el modal
$('#turnoModal .close, #turnoModal .btn-secondary').click(function() {
    $('#turnoModal').modal('hide');
});
    



    // Confirmar eliminación usando SweetAlert2
    $('#tabla_turnos tbody').on('click', '.btn-delete', function() {
        var data = table.row($(this).parents('tr')).data();
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡No podrás revertir esto!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: 'red',
            cancelButtonColor: 'gray',
            confirmButtonText: 'Sí, eliminarlo!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: `/catalogos/turnos/delete/${data.id}/`,
                    method: 'DELETE',
                    success: function(response) {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'El turno ha sido eliminado.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar el turno',
                        });
                    }
                });
            }
        });
    });
});
