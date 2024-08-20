$(document).ready(function() {
    var csrftoken = '{{ csrf_token }}';

    // Obtener el token CSRF de las cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie("csrftoken");

  // Configurar jQuery para incluir el token CSRF en las solicitudes AJAX
  $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (
          !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
          !this.crossDomain
        ) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
    });

  function formatDate(dateString) {
      var options = { day: 'numeric', month: 'long', year: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
  }

  var table = $('#calidadMicrobiologicaTable').DataTable({
    ajax: {
        url: '/control_calidad/api/calidad-microbiologica/',
        dataSrc: ''
    },
    columns: [
        { 
            data: 'fechaHora',
            render: function(data, type, row) {
                // Assuming the date is in ISO format, e.g., "2024-08-20T14:30:00Z"
                var date = new Date(data);
                var options = {
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit', 
                    second: '2-digit',
                    hour12: false // Use 24-hour time
                };
                return date.toLocaleString('es-ES', options);
            }
        },
        { data: 'planta.nombre' },
        { data: 'producto.nombre' },
        { data: 'organismos_coliformes' },
        {
            data: null,
            orderable: false,
            searchable: false,
            render: function(data, type, row) {
                return `
                <div class="d-flex justify-content-between">
                    <button class="btn btn-warning edit-btn" data-id="${row.id}" data-url="${data.edit_url}">
                        <i class="fa fa-pencil"></i>
                    </button>
                    <button class="btn btn-danger delete-btn" data-id="${row.id}" data-url="${data.delete_url}">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
                `;
            }
        }
    ],

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
          previous: "Anterior",
        },
      },
});

// Obtén el encabezado_id desde la URL actual (ej. http://127.0.0.1:8002/control_calidad/calidad-microbiologica/detalle/1/)
var urlParams = new URLSearchParams(window.location.search);
var encabezadoId = urlParams.get('id'); // o el nombre del parámetro que estás usando

// Al abrir el modal, establece el encabezado_id
$('#addDataModal').on('show.bs.modal', function (event) {
    if (!encabezadoId) {
        encabezadoId = getEncabezadoIdFromURL(); // Implementa esta función para extraer el ID de la URL si no está en `urlParams`
    }
    $('#modalEncabezadoId').val(encabezadoId);
    console.log('Encabezado ID:', encabezadoId); // Verifica que el ID no sea null
});

// Función para obtener el encabezado_id desde la URL
function getEncabezadoIdFromURL() {
    var urlPath = window.location.pathname;
    var parts = urlPath.split('/');
    return parts[parts.length - 2]; // Ajusta esto según la estructura de la URL
}

$('#addDataForm').on('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    var encabezadoId = $('#modalEncabezadoId').val(); // Asegúrate de que esto coincida con el ID en el modal
    console.log('Encabezado ID:', encabezadoId); // Ensure this logs the correct value

    if (!encabezadoId) {
        alert('Encabezado ID is missing.');
        return; // Prevent form submission if encabezado_id is missing
    }

    var formData = {
        'fechaHora': $('#modalFechaHora').val(),
        'planta': $('#modalPlanta').val(),
        'producto': $('#modalProducto').val(),
        'organismos_coliformes': $('#modalOrganismosColiformes').val(),
        'encabezado_id': encabezadoId,
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
    };
    
    console.log('Form Data:', formData); // Verifica los datos enviados
    
    $.ajax({
        url: `/control_calidad/api/calidad-microbiologica/add/${encabezadoId}/`,
        type: 'POST',
        data: JSON.stringify(formData),
        contentType: 'application/json', // Asegúrate de que el servidor acepte JSON
        success: function(response) {
            if (response.success) {
                $('#addDataModal').modal('hide');
                table.ajax.reload();
            } else {
                alert('Error adding record: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            console.log('Error submitting request:', error);
            console.log('Response Text:', xhr.responseText); // Muestra el texto de respuesta para depuración
        }
    });
});
    // Manejo del clic en el botón de editar
    $('#calidadMicrobiologicaTable').on('click', '.edit-btn', function() {
        var url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                $('#editRecordId').val(data.id);
                $('#editFechaHora').val(data.fechaHora);
                $('#editPlanta').val(data.planta.id);
                $('#editProducto').val(data.producto.id);
                $('#editOrganismosColiformes').val(data.organismos_coliformes);
                $('#editDataModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.log('Error al obtener datos para editar:', error);
            }
        });
    });

// Manejo del clic en el botón de eliminar
$('#calidadMicrobiologicaTable').on('click', '.delete-btn', function() {
    var id = $(this).data('id');
    var url = $(this).data('url');
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'No podrás recuperar este registro después de eliminarlo.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: url,
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function(response) {
                    if (response.success) {
                        Swal.fire(
                            'Eliminado',
                            'El registro ha sido eliminado.',
                            'success'
                        );
                        table.ajax.reload();
                    } else {
                        Swal.fire(
                            'Error',
                            'No se pudo eliminar el registro: ' + response.error,
                            'error'
                        );
                    }
                },
                error: function(xhr, status, error) {
                    console.log('Error al enviar la solicitud de eliminación:', error);
                }
            });
        }
    });
});

 // Manejo del envío del formulario de edición
 $('#editDataForm').on('submit', function(event) {
    event.preventDefault(); // Prevenir el envío normal del formulario

    var formData = {
        'id': $('#editRecordId').val(),
        'fechaHora': $('#editFechaHora').val(),
        'planta': $('#editPlanta').val(),
        'producto': $('#editProducto').val(),
        'organismos_coliformes': $('#editOrganismosColiformes').val(),
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
    };

    $.ajax({
        url: '/control_calidad/api/calidad-microbiologica/update/',
        type: 'POST',
        data: formData,
        success: function(response) {
            if (response.success) {
                // Cerrar el modal y recargar la tabla
                $('#editDataModal').modal('hide');
                table.ajax.reload();
            } else {
                alert('Error al actualizar el registro: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            console.log('Error al enviar la solicitud de actualización:', error);
        }
    });
});
    // Cargar opciones de planta
    $.ajax({
        url: '/control_calidad/api/planta/',
        type: 'GET',
        success: function(data) {
            var $plantaSelect = $('#modalPlanta');
            $plantaSelect.empty();
            $.each(data, function(index, planta) {
                $plantaSelect.append('<option value="' + planta.id + '">' + planta.nombre + '</option>');
            });
        },
        error: function(xhr, status, error) {
            console.log('Error al cargar plantas:', error);
        }
    });

        // Cargar opciones de planta
        $.ajax({
            url: '/control_calidad/api/planta/',
            type: 'GET',
            success: function(data) {
                var $plantaSelect = $('#editPlanta');
                $plantaSelect.empty();
                $.each(data, function(index, planta) {
                    $plantaSelect.append('<option value="' + planta.id + '">' + planta.nombre + '</option>');
                });
            },
            error: function(xhr, status, error) {
                console.log('Error al cargar plantas:', error);
            }
        });

    // Cargar opciones de producto
    $.ajax({
        url: '/control_calidad/api/producto/',
        type: 'GET',
        success: function(data) {
            var $productoSelect = $('#modalProducto');
            $productoSelect.empty();
            $.each(data, function(index, producto) {
                $productoSelect.append('<option value="' + producto.id + '">' + producto.nombre + '</option>');
            });
        },
        error: function(xhr, status, error) {
            console.log('Error al cargar productos:', error);
        }
    });

        // Cargar opciones de producto
        $.ajax({
            url: '/control_calidad/api/producto/',
            type: 'GET',
            success: function(data) {
                var $productoSelect = $('#editProducto');
                $productoSelect.empty();
                $.each(data, function(index, producto) {
                    $productoSelect.append('<option value="' + producto.id + '">' + producto.nombre + '</option>');
                });
            },
            error: function(xhr, status, error) {
                console.log('Error al cargar productos:', error);
            }
        });
  

    // Manejo de la edición de un registro
    $('#calidadMicrobiologicaTable').on('click', '.edit-btn', function() {
        var data = table.row($(this).parents('tr')).data();
        $('#editRecordId').val(data.id);
        $('#editFechaHora').val(data.fechaHora);
        $('#editPlanta').val(data.planta.id); // Asumiendo que `planta` tiene un campo `id`
        $('#editProducto').val(data.producto.id); // Asumiendo que `producto` tiene un campo `id`
        $('#editOrganismosColiformes').val(data.organismos_coliformes);

        // Cargar las opciones cuando se abre el modal
        $('#editDataModal').on('shown.bs.modal', function () {
            loadOptions();
        });

        $('#editDataModal').modal('show');
    });


    // Manejo de la eliminación de un registro
    $('#calidadMicrobiologicaTable').on('click', '.delete-btn', function() {
        var recordId = table.row($(this).parents('tr')).data().id;

        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡No podrás recuperar este registro!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminarlo'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/control_calidad/api/calidad-microbiologica/delete/' + recordId + '/',
                    type: 'DELETE',
                    data: {
                        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                    },
                    success: function(response) {
                        if (response.success) {
                            // Recargar la tabla
                            table.ajax.reload();
                        } else {
                            alert('Error al eliminar el registro: ' + response.error);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.log('Error al enviar la solicitud:', error);
                    }
                });
            }
        });
    });


    $('.modal').on('click', '[data-dismiss="modal"]', function() {
        $(this).closest('.modal').modal('hide');
    });

});

