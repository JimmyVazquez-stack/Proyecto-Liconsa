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

    var table = $('#tabla_areas').DataTable({
        ajax: {
            url: '/catalogos/areas/list/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'nombre' },
            { data: 'descripcion' },
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

    // Abrir modal para añadir área
    $('#btnAddArea').click(function() {
        $('#areaModalLabel').text('Añadir Área');
        $('#areaForm')[0].reset();
        $('#areaId').val('');
        $('#areaModal').modal('show');
    });

    // Guardar área (añadir o editar) con validación usando SweetAlert2
    $('#saveArea').click(function() {
        var nombre = $('#nombre').val().trim();
        var descripcion = $('#descripcion').val().trim();
    
        // Validar que los campos no estén vacíos
        if (!nombre || !descripcion) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Todos los campos son obligatorios',
            });
            return;
        }
    
        var areaId = $('#areaId').val();
        var url = areaId ? `/catalogos/areas/update/${areaId}/` : '/catalogos/areas/create/';
        var method = 'POST';
    
        $.ajax({
            url: url,
            method: method,
            data: $('#areaForm').serialize(),
            success: function(response) {
                $('#areaModal').modal('hide');
                table.ajax.reload();
                Swal.fire({
                    icon: 'success',
                    title: 'Guardado',
                    text: 'Área guardada con éxito',
                });
            },
            error: function(xhr) {
                var errorMessage = 'Error al guardar el área';
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
    $('#areaModal .close, #areaModal .btn-secondary').click(function() {
        $('#areaModal').modal('hide');
    });

    // Abrir modal para editar área
    $('#tabla_areas tbody').on('click', '.btn-edit', function() {
        var data = table.row($(this).parents('tr')).data();
        $('#areaModalLabel').text('Editar Área');
        $('#nombre').val(data.nombre);
        $('#descripcion').val(data.descripcion);
        $('#areaId').val(data.id);
        $('#areaModal').modal('show');
    });

    // Confirmar eliminación usando SweetAlert2
    $('#tabla_areas tbody').on('click', '.btn-delete', function() {
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
                    url: `/catalogos/areas/delete/${data.id}/`,
                    method: 'DELETE',
                    success: function(response) {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'El área ha sido eliminada.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar el área',
                        });
                    }
                });
            }
        });
    });
});
