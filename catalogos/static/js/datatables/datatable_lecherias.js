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

// Función para cargar opciones de población
function loadPoblaciones(selectedPoblacion) {
    $.ajax({
        url: '/catalogos/poblaciones/list/data',
        method: 'GET',
        success: function(response) {
            var poblacionSelect = $('#poblacion');
            poblacionSelect.empty();
            poblacionSelect.append('<option value="">Seleccione una población</option>');
            response.forEach(function(poblacion) {
                var selected = poblacion.id == selectedPoblacion ? 'selected' : '';
                var displayText = `${poblacion.nombre} (${poblacion.municipio}, ${poblacion.estado})`;
                poblacionSelect.append(`<option value="${poblacion.id}" ${selected}>${displayText}</option>`);
            });
        },
        error: function(xhr) {
            console.error('Error al cargar las poblaciones:', xhr);
        }
    });
}


// Función para cargar opciones de rutas
function loadRutas(selectedRuta) {
    $.ajax({
        url: '/catalogos/rutas/list/data', // Ajusta la URL según tu configuración
        method: 'GET',
        success: function(response) {
            var rutaSelect = $('#ruta');
            rutaSelect.empty();
            rutaSelect.append('<option value="">Seleccione una ruta</option>');
            response.forEach(function(ruta) {
                var selected = ruta.id == selectedRuta ? 'selected' : '';
                rutaSelect.append(`<option value="${ruta.id}" ${selected}>${ruta.numero} - ${ruta.nombre}</option>`);
            });
        },
        error: function(xhr) {
            console.error('Error al cargar las rutas:', xhr);
        }
    });
}

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


// Abrir modal para añadir población
$("#btnAddPoblacion").click(function () {
    $("#poblacionModalLabel").text("Añadir Población");
    $("#poblacionForm")[0].reset();
    $("#poblacionId").val("");
    $("#poblacionModal").modal("show");
});

  // Guardar población (añadir o editar) con validación usando SweetAlert2
  $("#savePoblacion").click(function () {
    var nombre = $("#nombre").val().trim();
    var municipio = $("#municipio").val().trim();
    var estado = $("#estado").val().trim();

    // Validar que los campos no estén vacíos
    if (!nombre || !municipio || !estado) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "Todos los campos son obligatorios",
      });
      return;
    }

    var poblacionId = $("#poblacionId").val();
    var url = poblacionId
      ? `/catalogos/poblaciones/update/${poblacionId}/`
      : "/catalogos/poblaciones/create/";
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


// Abrir modal para añadir lechería
$('#btnAddLecheria').click(function() {
    // Cerrar el modal de población si está abierto
    if ($('#poblacionModal').hasClass('show')) {
        $('#poblacionModal').modal('hide');
    }
    // Cerrar el modal de rutas si está abierto
    if ($('#rutaModal').hasClass('show')) {
        $('#rutaModal').modal('hide');
    }
    
    // Configurar el modal para añadir lechería
    $('#lecheriaModalLabel').text('Añadir Lechería');
    $('#lecheriaForm')[0].reset();
    $('#lecheriaId').val('');
    $('#btnAddPoblacion').show(); // Mostrar el botón para añadir población
    $('#btnAddRuta').show(); // Mostrar el botón para añadir ruta
    $('#lecheriaModal').modal('show');
    
    // Cargar las opciones de población y ruta
    loadPoblaciones(); // Cargar opciones de población
    loadRutas(); // Cargar opciones de ruta
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
    $('#poblacion').val(data.poblacion); // Cambiar si es necesario
    $('#ruta').val(data.ruta); // Cambiar si es necesario
    $('#lecheriaId').val(data.id);
    $('#btnAddPoblacion').hide(); // Ocultar el botón para añadir población
    $('#btnAddRuta').hide(); // Ocultar el botón para añadir ruta
    $('#lecheriaModal').modal('show');
    
    // Cargar las opciones de población y ruta
    loadPoblaciones(data.poblacion); // Cargar opciones de población con la seleccionada
    loadRutas(data.ruta); // Cargar opciones de ruta con la seleccionada
});
// Guardar lechería (añadir o editar)
$('#saveLecheria').click(function() {
    var numero = $('#numero').val().trim();
    var nombre = $('#nombre').val().trim();
    var responsable = $('#responsable').val().trim();
    var telefono = $('#telefono').val().trim();
    var direccion = $('#direccion').val().trim();
    var ruta = $('#ruta').val().trim();
    var poblacion = $('#poblacion').val().trim();

    // Validar que los campos no estén vacíos
    if (!numero || !nombre || !responsable || !telefono || !direccion || !ruta || !poblacion) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Todos los campos son obligatorios',
        });
        return;
    }

    // Validar que el número sea único y de 10 dígitos
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
    var method = lecheriaId ? 'POST' : 'POST';

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
$("#tabla_lecherias tbody").on("click", ".btn-delete", function () {
    var data = table.row($(this).parents("tr")).data();
    
    // Verificar que 'data' tenga un campo 'id'
    if (!data || !data.id) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'ID de lechería no encontrado.',
        });
        return;
    }

    Swal.fire({
        title: "¿Estás seguro?",
        text: `¿Deseas eliminar la lechería número ${data.numero} con nombre ${data.nombre}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "red", // Color personalizado para el botón de confirmar (ej. rojo)
        cancelButtonColor: "gray" // Color personalizado para el botón de cancelar (ej. gris)
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/catalogos/lecherias/delete/${data.id}/`, // Utiliza 'data.id' como el pk
                method: "DELETE",
                success: function (response) {
                    table.ajax.reload(); // Recargar la tabla después de eliminar
                    Swal.fire(
                        "Eliminado",
                        "Lechería eliminada exitosamente",
                        "success"
                    );
                },
                error: function (xhr) {
                    var errorMessage = "Hubo un problema al eliminar la lechería.";
                    if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.message) {
                        errorMessage = xhr.responseJSON.message;
                    }
                    Swal.fire(
                        "Error",
                        errorMessage,
                        "error"
                    );
                },
            });
        }
    });
});




// Cerrar modales cuando se presiona cancelar, cerrar, o guardar
$('#cancelLecheriaModal, #cancelPoblacionModal, #saveLecheria, #savePoblacion').click(function() {
    $(this).closest('.modal').modal('hide');
});

// Cerrar modales cuando se presiona el botón de cerrar del modal
$('.modal').on('click', '[data-dismiss="modal"]', function() {
    $(this).closest('.modal').modal('hide');
});



});
