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

    var table = $('#tabla_plantas').DataTable({
        ajax: {
            url: '/catalogos/plantas/list/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'nombre' },
            { data: 'ubicacion' },
            { data: 'correo' },
            { data: 'contacto' },
            { data: 'telefono' },
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
            },
        },
        columnDefs: [
            {
                targets: -1,
                orderable: false
            }
        ]
    });

    // Abrir modal para añadir planta
    $('#addPlantaBtn').click(function() {
        $('#plantaModalLabel').text('Añadir Planta');
        $('#plantaForm')[0].reset();
        $('#plantaId').val('');
        $('#plantaModal').modal('show');
    });
    

    // Guardar planta (añadir o editar) con validación usando SweetAlert2
    $('#savePlanta').click(function() {
        var nombre = $('#nombre').val().trim();
        var ubicacion = $('#ubicacion').val().trim();
        var correo = $('#correo').val().trim();
        var contacto = $('#contacto').val().trim();
        var telefono = $('#telefono').val().trim();

        // Validar que los campos no estén vacíos
        if (!nombre || !ubicacion || !correo || !contacto || !telefono) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Todos los campos son obligatorios',
            });
            return;
        }

        var plantaId = $('#plantaId').val();
        var url = plantaId ? `/catalogos/plantas/update/${plantaId}/` : '/catalogos/plantas/create/';
        var method = 'POST';

        $.ajax({
            url: url,
            method: method,
            data: $('#plantaForm').serialize(),
            success: function(response) {
                $('#plantaModal').modal('hide');
                table.ajax.reload();
                Swal.fire({
                    icon: 'success',
                    title: 'Guardado',
                    text: 'Planta guardada con éxito',
                });
            },
            error: function(xhr) {
                var errorMessage = 'Error al guardar la planta';
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
    $('#plantaModal .close, #plantaModal .btn-secondary').click(function() {
        $('#plantaModal').modal('hide');
    });

    // Abrir modal para editar planta
    $('#tabla_plantas tbody').on('click', '.btn-edit', function() {
        var data = table.row($(this).parents('tr')).data();
        $('#plantaModalLabel').text('Editar Planta');
        $('#nombre').val(data.nombre);
        $('#ubicacion').val(data.ubicacion);
        $('#correo').val(data.correo);
        $('#contacto').val(data.contacto);
        $('#telefono').val(data.telefono);
        $('#plantaId').val(data.id);
        $('#plantaModal').modal('show');
    });

    // Confirmar eliminación usando SweetAlert2
    $('#tabla_plantas tbody').on('click', '.btn-delete', function() {
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
                    url: `/catalogos/plantas/delete/${data.id}/`,
                    method: 'DELETE',
                    success: function(response) {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'La planta ha sido eliminada.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar la planta',
                        });
                    }
                });
            }
        });
    });
});
