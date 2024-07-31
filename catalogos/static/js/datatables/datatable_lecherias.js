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

    var table = $('#tabla_lecherias').DataTable({
        ajax: {
            url: '/catalogos/lecherias/list/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'numero' },
            { data: 'nombre' },
            { data: 'responsable' },
            { data: 'telefono' },
            { data: 'direccion' },
            { data: 'nombre_ruta' },
            { data: 'nombre_poblacion' },
            {
                data: null,
                defaultContent: `
                <div class="d-flex justify-content-between">
                    <button class="btn btn-edit btn-warning"><i class="fa fa-pencil"></i></button>
                    <button class="btn btn-delete btn-danger"><i class="fa fa-trash"></i></button>
                </div>
            `,
                orderable: false
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
        }
    });

    // Función para cargar opciones de población
    function loadPoblaciones(selectedPoblacion) {
        $.ajax({
            url: '/catalogos/poblaciones/list/',
            method: 'GET',
            success: function(response) {
                var poblacionSelect = $('#poblacion');
                poblacionSelect.empty();
                poblacionSelect.append(`<option value="">Seleccione una población</option>`);
                response.forEach(function(poblacion) {
                    var selected = poblacion.nombre === selectedPoblacion ? 'selected' : '';
                    poblacionSelect.append(`<option value="${poblacion.nombre}" ${selected}>${poblacion.nombre}</option>`);
                });
            },
            error: function(xhr) {
                console.error('Error al cargar las poblaciones:', xhr);
            }
        });
    }

    // Abrir modal para añadir lechería
    $('#btnAddLecheria').click(function() {
        $('#lecheriaModalLabel').text('Añadir Lechería');
        $('#lecheriaForm')[0].reset();
        $('#lecheriaId').val('');
        $('#lecheriaModal').modal('show');
        loadPoblaciones(); // Cargar opciones de población
    });

    // Abrir modal para editar lechería
    $('#tabla_lecherias tbody').on('click', '.btn-edit', function() {
        var data = table.row($(this).parents('tr')).data();
        $('#lecheriaModalLabel').text('Editar Lechería');
        $('#numero').val(data.numero);
        $('#nombre').val(data.nombre);
        $('#responsable').val(data.responsable);
        $('#telefono').val(data.telefono);
        $('#direccion').val(data.direccion);
        $('#nombre_ruta').val(data.nombre_ruta);
        $('#poblacion').val(data.nombre_poblacion);
        $('#lecheriaId').val(data.id);
        $('#lecheriaModal').modal('show');
        loadPoblaciones(data.nombre_poblacion); // Cargar opciones de población con la seleccionada
    });

    // Guardar lechería (añadir o editar)
    $('#saveLecheria').click(function() {
        var nombre = $('#nombre').val().trim();
        var responsable = $('#responsable').val().trim();
        var telefono = $('#telefono').val().trim();
        var direccion = $('#direccion').val().trim();
        var nombre_ruta = $('#nombre_ruta').val().trim();
        var poblacion = $('#poblacion').val().trim();

        // Validar que los campos no estén vacíos
        if (!nombre || !responsable || !telefono || !direccion || !nombre_ruta || !poblacion) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Todos los campos son obligatorios',
            });
            return;
        }

        var lecheriaId = $('#lecheriaId').val();
        var url = lecheriaId ? `/catalogos/lecherias/update/${lecheriaId}/` : '/catalogos/lecherias/create/';
        var method = 'POST';

        $.ajax({
            url: url,
            method: method,
            data: $('#lecheriaForm').serialize(),
            success: function(response) {
                $('#lecheriaModal').modal('hide');
                table.ajax.reload();
                Swal.fire({
                    icon: 'success',
                    title: 'Guardado',
                    text: 'Lechería guardada con éxito',
                });
            },
            error: function(xhr) {
                var errorMessage = 'Error al guardar la lechería';
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

    // Confirmar eliminación usando SweetAlert2
    $('#tabla_lecherias tbody').on('click', '.btn-delete', function() {
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
                    url: `/catalogos/lecherias/delete/${data.id}/`,
                    method: 'DELETE',
                    success: function(response) {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'La lechería ha sido eliminada.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar la lechería',
                        });
                    }
                });
            }
        });
    });
});
