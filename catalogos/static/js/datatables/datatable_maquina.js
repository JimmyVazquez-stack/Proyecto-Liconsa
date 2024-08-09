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

// Función para cargar opciones de plantas en el modal de creación/edición de máquina
function loadPlantas(selectedPlantaId = null) {
    $.ajax({
        url: '/catalogos/plantas/list/data/',
        method: 'GET',
        success: function(response) {
            var plantaSelect = $('#planta');
            plantaSelect.empty();

            if (response.length > 0) {
                // Añadir opción por defecto si hay más de 2 plantas
                if (response.length > 2) {
                    plantaSelect.append(new Option('Seleccione una planta', '', true, true));
                } else if (response.length === 1) {
                    plantaSelect.append(new Option('Seleccione una planta', '', false, false));
                } else {
                    plantaSelect.append(new Option('Seleccione una planta', '', true, true));
                }

                response.forEach(function(planta) {
                    plantaSelect.append(new Option(planta.nombre, planta.id));
                });

                if (selectedPlantaId) {
                    plantaSelect.val(selectedPlantaId);
                }
            } else {
                plantaSelect.append(new Option('No hay plantas disponibles', '', true, true));
            }
        },
        error: function() {
            alert('Error al cargar las plantas.');
        }
    });
}

// Abrir modal para añadir máquina
$('#btnAddMaquina').click(function() {
    $('#maquinaModalLabel').text('Añadir Máquina');
    $('#maquinaForm')[0].reset();
    $('#maquinaId').val('');
    loadPlantas();
    $('#maquinaModal').modal('show');
});

$(function() {
  // Abrir modal para añadir planta desde el modal de máquina
$('#btnAddPlanta').click(function() {
    $('#plantaModal').modal('show');
});

// Guardar planta con validación usando SweetAlert2
$('#savePlanta').click(function() {
    var nombre = $('#nombre').val().trim();
    var ubicacion = $('#ubicacion').val().trim();
    var correo = $('#correo').val().trim();
    var contacto = $('#contacto').val().trim();
    var telefono = $('#telefono').val().trim();


    // Validar que todos los campos no estén vacíos
    if (!nombre || !ubicacion || !correo || !contacto || !telefono) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Todos los campos son obligatorios',
        });
        return;
    }

    $.ajax({
        url: '/catalogos/plantas/create/',
        method: 'POST',
        data: $('#plantaForm').serialize(),
        success: function(response) {
            // Añadir la nueva planta al dropdown
            var newOption = new Option(response.nombre, response.id, true, true);
            $('#nombre_planta').append(newOption).trigger('change');

            Swal.fire({
                icon: 'success',
                title: 'Guardado',
                text: 'Planta guardada con éxito',
            }).then(() => {
                // Cerrar solo el modal de añadir planta y mantener el modal de máquina abierto
                $('#plantaModal').modal('hide');
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

});

// Guardar máquina (añadir o editar) con validación usando SweetAlert2
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
    var method = 'POST'; // Usamos POST para ambos casos

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
                text: 'Máquina guardada con éxito',
            });
        },
        error: function(xhr) {
            var errorMessage = 'Error al guardar la máquina';
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

// Manejadores manuales para cerrar los modales
$('#maquinaModal .close, #maquinaModal .btn-secondary, #plantaModal .close, #plantaModal .btn-secondary').click(function() {
    $('#maquinaModal').modal('hide');
    $('#plantaModal').modal('hide');
});
// Abrir modal para editar máquina
$('#tabla_maquinas tbody').on('click', '.btn-edit', function() {
    var data = table.row($(this).parents('tr')).data();
    $('#maquinaModalLabel').text('Editar Máquina');
    $('#numero').val(data.numero);
    $('#maquinaId').val(data.id);
    loadPlantas(data.planta_id); // Cargar las plantas y seleccionar la planta correcta
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
        confirmButtonColor: 'red',
        cancelButtonColor: 'gray',
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
                        'La máquina ha sido eliminada.',
                        'success'
                    );
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Error al eliminar la máquina',
                    });
                }
            });
        }
    });
});
    });
