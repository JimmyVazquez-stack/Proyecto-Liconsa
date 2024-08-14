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
            { data: 'ruta_info' },
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
// ==================== Funciones de carga ====================

// Función para cargar opciones de población
function loadPoblaciones(selectedPoblacion) {
    $.ajax({
        url: '/catalogos/poblaciones/list/data',
        method: 'GET',
        success: function(response) {
            var $poblacionSelect = $('#poblacion');
            $poblacionSelect.empty();
            
            if (response.length === 0) {
                $poblacionSelect.append('<option value="">No hay ninguna población disponible</option>');
            } else {
                $poblacionSelect.append('<option value="">Seleccione una población</option>');
                response.forEach(function(poblacion) {
                    var selected = poblacion.id == selectedPoblacion ? 'selected' : '';
                    var displayText = `${poblacion.nombre} (${poblacion.municipio}, ${poblacion.estado})`;
                    $poblacionSelect.append(`<option value="${poblacion.id}" ${selected}>${displayText}</option>`);
                });
            }
        },
        error: function(xhr) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudieron cargar las poblaciones.',
            });
        }
    });
}


// Función para cargar opciones de rutas
function loadRutas(selectedRuta) {
    $.ajax({
        url: '/catalogos/rutas/list/data',
        method: 'GET',
        success: function(response) {
            var $rutaSelect = $('#ruta');
            $rutaSelect.empty();
            
            if (response.length === 0) {
                $rutaSelect.append('<option value="">No hay ninguna ruta disponible</option>');
            } else {
                $rutaSelect.append('<option value="">Seleccione una ruta</option>');
                response.forEach(function(ruta) {
                    var selected = ruta.id == selectedRuta ? 'selected' : '';
                    $rutaSelect.append(`<option value="${ruta.id}" ${selected}>${ruta.numero} - ${ruta.nombre}</option>`);
                });
            }
        },
        error: function(xhr) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudieron cargar las rutas.',
            });
        }
    });
}
// ==================== Eventos de Modales ====================

// Abrir modal para añadir ruta
$('#btnAddRuta').click(function() {
    // Cerrar el modal de lechería si está abierto
    if ($('#lecheriaModal').hasClass('show')) {
        $('#lecheriaModal').modal('hide');
    }

    $('#rutaModalLabel').text('Añadir Ruta');
    $('#rutaForm')[0].reset();
    $('#rutaId').val('');
    $('#rutaModal').modal('show');
});

// Abrir modal para añadir población
$('#btnAddPoblacion').click(function() {
    // Cerrar el modal de lechería si está abierto
    if ($('#lecheriaModal').hasClass('show')) {
        $('#lecheriaModal').modal('hide');
    }

    $('#poblacionModalLabel').text('Añadir Población');
    $('#poblacionForm')[0].reset();
    $('#poblacionId').val('');
    $('#poblacionModal').modal('show');
});

// Abrir modal para añadir lechería
$('#btnAddLecheria').click(function() {
    // Cerrar los modales de población y ruta si están abiertos
    if ($('#poblacionModal').hasClass('show')) {
        $('#poblacionModal').modal('hide');
    }
    if ($('#rutaModal').hasClass('show')) {
        $('#rutaModal').modal('hide');
    }

    $('#lecheriaModalLabel').text('Añadir Lechería');
    $('#lecheriaForm')[0].reset();
    $('#lecheriaId').val('');
    $('#btnAddPoblacion').show();
    $('#btnAddRuta').show();
    $('#lecheriaModal').modal('show');
    loadPoblaciones(); // Cargar opciones de población
    loadRutas(); // Cargar opciones de ruta
});


// Cerrar modales cuando se presiona cancelar o cerrar
$('#cancelMaquinaModal, #cancelPlantaModal, #saveCabezal, #saveMaquina, #savePlanta').click(function() {
    $(this).closest('.modal').modal('hide');
});

$('.modal').on('click', '[data-dismiss="modal"]', function() {
    $(this).closest('.modal').modal('hide');
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
    $('#poblacion').val(data.poblacion);
    $('#ruta').val(data.ruta);
    $('#lecheriaId').val(data.id);
    $('#btnAddPoblacion').hide();
    $('#btnAddRuta').hide();
    $('#lecheriaModal').modal('show');
    loadPoblaciones(data.poblacion); // Cargar opciones de población con la seleccionada
    loadRutas(data.ruta); // Cargar opciones de ruta con la seleccionada
});

// ==================== Guardar y Eliminar ====================

// Guardar ruta (añadir o editar) con validación usando SweetAlert2
$('#saveRuta').click(function() {
    var nombre = $('#nombreRuta').val().trim();
    var numero = $('#numeroRuta').val().trim();

    if (!nombre || !numero) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Todos los campos son obligatorios',
        });
        return;
    }

    var rutaId = $('#rutaId').val();
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

// Guardar población (añadir o editar) con validación usando SweetAlert2
$("#savePoblacion").click(function () {
    var nombre = $("#nombrePoblacion").val().trim();
    var municipio = $("#municipio").val().trim();
    var estado = $("#estado").val().trim();

    if (!nombre || !municipio || !estado) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var poblacionId = $("#poblacionId").val();
    var url = poblacionId ? `/catalogos/poblaciones/update/${poblacionId}/` : "/catalogos/poblaciones/create/";
    var method = "POST";

    $.ajax({
        url: url,
        method: method,
        data: $("#poblacionForm").serialize(),
        success: function (response) {
            $("#poblacionModal").modal("hide");
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Población guardada con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar la población";
            if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                icon: "error",
                title: "Error",
                text: errorMessage,
            });
        },
    });
});

// Guardar lechería (añadir o editar) con validación usando SweetAlert2
$('#saveLecheria').click(function() {
    var numero = $('#numero').val().trim();
    var nombre = $('#nombre').val().trim();
    var responsable = $('#responsable').val().trim();
    var telefono = $('#telefono').val().trim();
    var direccion = $('#direccion').val().trim();
    var ruta = $('#ruta').val().trim();
    var poblacion = $('#poblacion').val().trim();

    if (!numero || !nombre || !responsable || !telefono || !direccion || !ruta || !poblacion) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Todos los campos son obligatorios',
        });
        return;
    }

    var numberPattern = /^\d{10}$/;
    if (!numberPattern.test(numero)) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El número debe tener exactamente 10 dígitos',
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

// Mostrar el modal de confirmación y establecer el ID de la lechería
$('#tabla_lecherias tbody').on('click', '.btn-delete', function () {
    var data = table.row($(this).parents('tr')).data();
    var lecheriaId = data ? data.id : null;

    if (!lecheriaId) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener el ID de la lechería.',
        });
        return;
    }

    // Establecer el ID de la lechería en el campo oculto
    $('#lecheriaId').val(lecheriaId);

    // Mostrar el modal de confirmación
    $('#modalEliminarLecheria').modal('show');
});

// Confirmar eliminación
$('#btnEliminarLecheria').on('click', function () {
    var lecheriaId = $('#lecheriaId').val();

    if (!lecheriaId) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'ID de lechería no encontrado.',
        });
        return;
    }

    $.ajax({
        url: `/catalogos/lecherias/delete/${lecheriaId}/`,
        method: 'DELETE',
        data: {
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function (response) {
            table.ajax.reload();
            $('#modalEliminarLecheria').modal('hide');
            Swal.fire(
                'Eliminado!',
                'La lechería ha sido eliminada.',
                'success'
            );
        },
        error: function (xhr) {
            var errorMessage = "Error al eliminar la lechería.";
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                icon: "error",
                title: "Error",
                text: errorMessage,
            });
        }
    });
});


});
