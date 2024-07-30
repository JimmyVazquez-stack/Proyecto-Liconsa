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

    var table = $('#tabla_rutas').DataTable({
        ajax: {
            url: '/catalogos/rutas/list/data/',
            dataSrc: ''
        },
        columns: [
            
            { data: 'nombre' },
            { data: 'numero' },
            {
                data: null,
                defaultContent: `
                    <button class="btn btn-edit"><i class="fas fa-pencil-alt text-gray"></i></button>
                    <button class="btn btn-delete"><i class="fas fa-trash text-red"></i></button>
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

    // Abrir modal para añadir ruta
    $('#btnAddRuta').click(function() {
        $('#rutaModalLabel').text('Añadir Ruta');
        $('#rutaForm')[0].reset();
        $('#rutaId').val('');
        $('#rutaModal').modal('show');
    });

    // Guardar ruta (añadir o editar) con validación usando SweetAlert2
    $('#saveRuta').click(function() {
        var nombre = $('#nombre').val().trim();
        var numero = $('#numero').val().trim();
    
        // Validar que los campos no estén vacíos
        if (!nombre || !numero) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Todos los campos son obligatorios',
            });
            return;
        }
    
        var rutaId = $('#rutaId').val();
        console.log(rutaId); // Para depuración
        var url = rutaId ? `/catalogos/rutas/update/${rutaId}/` : '/catalogos/rutas/create/';
        var method = 'POST';
    
        $.ajax({
            url: url,
            method: method,
            data: $('#rutaForm').serialize(),
            success: function(response) {
                $('#rutaModal').modal('hide');
                table.ajax.reload();
                Swal.fire({
                    icon: 'success',
                    title: 'Guardado',
                    text: 'Ruta guardada con éxito',
                });
            },
            error: function(xhr) {
                var errorMessage = 'Error al guardar la ruta';
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
     $('#rutaModal .close, #rutaModal .btn-secondary').click(function() {
        $('#rutaModal').modal('hide');
    });

    // Abrir modal para editar ruta
    $('#tabla_rutas tbody').on('click', '.btn-edit', function() {
        var data = table.row($(this).parents('tr')).data();
        $('#rutaModalLabel').text('Editar Ruta');
        $('#nombre').val(data.nombre);
        $('#numero').val(data.numero);
        $('#rutaId').val(data.id);
        $('#rutaModal').modal('show');
    });

    // Confirmar eliminación usando SweetAlert2
    $('#tabla_rutas tbody').on('click', '.btn-delete', function() {
        var data = table.row($(this).parents('tr')).data();
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡No podrás revertir esto!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminarlo!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: `/catalogos/rutas/delete/${data.id}/`,
                    method: 'DELETE',
                    success: function(response) {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'La ruta ha sido eliminada.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar la ruta',
                        });
                    }
                });
            }
        });
    });
});
