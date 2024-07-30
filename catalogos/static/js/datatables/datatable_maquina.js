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

    var table = $('#tabla_maquinas').DataTable({
        ajax: {
            url: '/catalogos/maquinas/list/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'numero' },
            { data: 'nombre_planta' },
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

    // Cargar opciones de plantas en el modal de creación/edición de máquina
    function loadPlantas() {
        $.ajax({
            url: '/catalogos/plantas/list/data/',
            method: 'GET',
            success: function(response) {
                var plantaSelect = $('#planta');
                plantaSelect.empty();
                if (response.length > 0) {
                    response.forEach(function(planta) {
                        plantaSelect.append(new Option(planta.nombre, planta.id));
                    });
                } else {
                    plantaSelect.append(new Option('No hay plantas disponibles', ''));
                }
            },
            error: function() {
                alert('Error al cargar las plantas.');
            }
        });
    }

    // Abrir modal para añadir maquina
    $('#btnAddMaquina').click(function() {
        $('#maquinaModalLabel').text('Añadir Maquina');
        $('#maquinaForm')[0].reset();
        $('#maquinaId').val('');
        loadPlantas();
        $('#maquinaModal').modal('show');
    });

    // Guardar maquina (añadir o editar) con validación usando SweetAlert2
    $('#saveMaquina').click(function() {
        var numero = $('#numero').val().trim();
        var planta = $('#planta').val();
    
        // Validar que los campos no estén vacíos
        if (!numero || !planta) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Todos los campos son obligatorios',
            });
            return;
        }
    
        var maquinaId = $('#maquinaId').val();
        var url = maquinaId ? `/catalogos/maquinas/update/${maquinaId}/` : '/catalogos/maquinas/create/';
        var method = 'POST';
    
        $.ajax({
            url: url,
            method: method,
            data: $('#maquinaForm').serialize(),
            success: function(response) {
                $('#maquinaModal').modal('hide');
                table.ajax.reload();
                Swal.fire({
                    icon: 'success',
                    title: 'Guardado',
                    text: 'Maquina guardada con éxito',
                });
            },
            error: function(xhr) {
                var errorMessage = 'Error al guardar la maquina';
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
    $('#maquinaModal .close, #maquinaModal .btn-secondary').click(function() {
        $('#maquinaModal').modal('hide');
    });

    // Abrir modal para editar maquina
    $('#tabla_maquinas tbody').on('click', '.btn-edit', function() {
        var data = table.row($(this).parents('tr')).data();
        $('#maquinaModalLabel').text('Editar Maquina');
        $('#numero').val(data.numero);
        $('#planta').val(data.planta_id);
        $('#maquinaId').val(data.id);
        loadPlantas();
        $('#maquinaModal').modal('show');
    });

    // Confirmar eliminación usando SweetAlert2
    $('#tabla_maquinas tbody').on('click', '.btn-delete', function() {
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
                    url: `/catalogos/maquinas/delete/${data.id}/`,
                    method: 'DELETE',
                    success: function(response) {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'La maquina ha sido eliminada.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar la maquina',
                        });
                    }
                });
            }
        });
    });

    // Abrir modal para añadir planta
    $('#addPlantaLink').click(function() {
        // Aquí puedes abrir un modal o redirigir a una página para añadir una nueva planta
        alert('Función para añadir una nueva planta no implementada.');
    });
});
