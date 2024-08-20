$(document).ready(function () {
    var encabezadosApiUrl = "/control_calidad/api/encabezados/";
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

    var table = $('#calidad_microbiologica_encabezados_Table').DataTable({
        "processing": true,
        "serverSide": false,
        "ajax": {
            "url": encabezadosApiUrl,
            "type": "GET",
            "dataSrc": ""
        },
        "columns": [
            { "data": "folio" },
            {
                "data": "fecha_creacion",
                "render": function(data, type, row) {
                    return formatDate(data);
                }
            },
            {
                "data": null,
                "render": function(data, type, row) {
                    var detalleUrl = `/control_calidad/calidad-microbiologica/detalle/${row.id}/`;

                    return `
                        <div class="d-flex justify-content-between">
                            <a href="${detalleUrl}" class="btn btn-warning btn-sm"><i class="fa fa-pencil"></i></a>
                            <button class="btn btn-danger btn-sm btn-delete" data-id="${row.id}"><i class="fa fa-trash"></i></button>
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

    // Confirmar eliminación usando SweetAlert2
    $('#calidad_microbiologica_encabezados_Table').on('click', '.btn-delete', function() {
        var encabezadoId = $(this).data('id');

        if (!encabezadoId) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo obtener el ID del encabezado.',
            });
            return;
        }

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
                    url: `/control_calidad/calidad-microbiologica/delete/${encabezadoId}/`,
                    method: 'DELETE',
                    data: {
                        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                    },
                    success: function() {
                        table.ajax.reload();
                        Swal.fire(
                            'Eliminado!',
                            'El encabezado ha sido eliminado.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'No se pudo eliminar el encabezado.',
                        });
                    }
                });
            }
        });
    });

// Manejo del formulario de agregar encabezado
$('#addEncabezadoForm').on('submit', function(event) {
    event.preventDefault();
    $.ajax({
        url: "/control_calidad/calidad_microbiologica/",
        type: "POST",
        data: $(this).serialize(),
        success: function(response) {
            $('#addModal').modal('hide');
            $('#calidad_microbiologica_encabezados_Table').DataTable().ajax.reload();
        }
    });
});



});