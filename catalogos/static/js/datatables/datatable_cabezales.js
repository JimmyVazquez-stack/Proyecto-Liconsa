$(document).ready(function () {
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

  var table = $("#tabla_cabezales").DataTable({
    ajax: {
      url: "/catalogos/cabezales/list/data/",
      dataSrc: "",
    },

    columns: [
      { data: "nombre" },
      { data: "numero_maquina" },
      { data: "planta_maquina" },
      {
        data: null,
        defaultContent: `
                <div class="d-flex justify-content-between">
                    <button class="btn btn-edit btn-warning"><i class="fa fa-pencil"></i></button>
                    <button class="btn btn-delete btn-danger"><i class="fa fa-trash"></i></button>
                </div>
                `,
      },
    ],

    pageLength: 5,
    lengthMenu: [
      [5, 10, 25, 50, -1],
      [5, 10, 25, 50, "Todo"],
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
    columnDefs: [
        {
            targets: -1,
            orderable: false
        }
    ]
  });

// Función para cargar las máquinas en el select del modal
function loadMachines() {
    $.ajax({
        url: "/catalogos/maquinas/list/data",
        method: "GET",
        success: function(data) {
            var $maquinaSelect = $("#maquina");
            var $message = $("#maquinaMessage");

            $maquinaSelect.empty();
            if (data.length === 0) {
                $maquinaSelect.append('<option value="">No hay máquinas disponibles</option>');
                $message.text("No hay máquinas disponibles.").css("color", "red");
            } else {
                $maquinaSelect.append('<option value="">Seleccione una máquina</option>');
                $.each(data, function(index, maquina) {
                    $maquinaSelect.append('<option value="' + maquina.id + '">' + maquina.nombre_planta + ' - ' + maquina.numero + '</option>');
                });
                $message.text("Seleccione una máquina.").css("color", "black");
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "No se pudieron cargar las máquinas.",
            });
        }
    });
}

// Abrir modal para añadir cabezal
$("#btnAddCabezal").click(function() {
    $("#cabezalId").val(""); // Limpiar el ID del cabezal
    $("#cabezalModalLabel").text("Añadir Cabezal");
    $("#cabezalForm")[0].reset();
    loadMachines(); // Cargar máquinas cuando se abre el modal
    $("#cabezalModal").modal("show");
});

// Mostrar el modal de edición de cabezales
$(document).on("click", ".btn-edit-cabezal", function() {
    var cabezalId = $(this).data("id");
    $.ajax({
        url: "/catalogos/cabezales/" + cabezalId + "/edit/",
        method: "GET",
        success: function(data) {
            $("#cabezalId").val(data.id);
            $("#nombre").val(data.nombre);
            $("#maquina").val(data.maquina_id);
            $("#cabezalModalLabel").text("Editar Cabezal");
            loadMachines(); // Cargar máquinas cuando se abre el modal
            $("#cabezalModal").modal("show");
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "No se pudieron cargar los datos del cabezal.",
            });
        },
    });
});

// Guardar o actualizar el cabezal
$("#saveCabezal").click(function() {
    var cabezalId = $("#cabezalId").val();
    var url = cabezalId ? "/catalogos/cabezales/update/" + cabezalId + "/" : "/catalogos/cabezales/create/";
    var method = "POST";
    var data = $("#cabezalForm").serialize();

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function(response) {
            $("#cabezalModal").modal("hide");
            table.ajax.reload(); // Recargar la tabla de cabezales
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Cabezal guardado con éxito.",
            });
        },
        error: function(xhr) {
            var errorMessage = "Error al guardar el cabezal.";
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

// Abrir modal para añadir máquina desde el modal de cabezal
$(document).on("click", "#btnAddMaquina", function() {
    $("#maquinaModalLabel").text("Añadir Máquina");
    $("#maquinaForm")[0].reset();
    loadPlantas(); // Asumiendo que tienes una función para cargar las plantas
    $("#maquinaModal").modal("show");
});

// Guardar máquina (añadir o editar) con validación usando SweetAlert2
$("#saveMaquina").click(function() {
    var numero = $("#numero").val().trim();
    var planta = $("#planta").val();

    // Validar que los campos no estén vacíos
    if (!numero || !planta) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var maquinaId = $("#maquinaId").val();
    var url = maquinaId ? `/catalogos/maquinas/update/${maquinaId}/` : "/catalogos/maquinas/create/";
    var method = "POST"; // Usamos POST para ambos casos

    $.ajax({
        url: url,
        method: method,
        data: $("#maquinaForm").serialize(),
        success: function(response) {
            $("#maquinaModal").modal("hide");
            loadMachines(); // Actualizar la lista de máquinas
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Máquina guardada con éxito",
            });
        },
        error: function(xhr) {
            var errorMessage = "Error al guardar la máquina";
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

// Cerrar modales manualmente
$(".modal .close, .modal .btn-secondary").click(function() {
    $(this).closest('.modal').modal('hide');
});


// Confirmar eliminación usando SweetAlert2 para cabezales
$('#tabla_cabezales tbody').on('click', '.btn-delete', function() {
    var data = table.row($(this).parents('tr')).data();
    var cabezalId = data ? data.id : null; // Obtener el ID del cabezal desde los datos de la fila

    if (!cabezalId) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener el ID del cabezal.',
        });
        return;
    }

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
                url: `/catalogos/cabezales/delete/${cabezalId}/`,
                method: 'DELETE', // Cambiar el método a DELETE
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val() // Incluye el token CSRF
                },
                success: function(response) {
                    table.ajax.reload(); // Recargar la tabla de cabezales
                    Swal.fire(
                        'Eliminado!',
                        'El cabezal ha sido eliminado.',
                        'success'
                    );
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Error al eliminar el cabezal',
                    });
                }
            });
        }
    });
});


});
