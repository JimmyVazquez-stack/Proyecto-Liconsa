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


// ==================== Funciones de carga ====================

// Función para cargar las máquinas en el select del modal
function loadMachines(callback) {
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

            if (callback) {
                callback();
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

// Función para cargar las plantas en el select del modal
function loadPlantas() {
    $.ajax({
        url: "/catalogos/plantas/list/data",
        method: "GET",
        success: function(data) {
            var $plantaSelect = $("#planta");
            $plantaSelect.empty();
            if (data.length === 0) {
                $plantaSelect.append('<option value="">No hay plantas disponibles</option>');
            } else {
                $plantaSelect.append('<option value="">Seleccione una planta</option>');
                $.each(data, function(index, planta) {
                    $plantaSelect.append('<option value="' + planta.id + '">' + planta.nombre + '</option>');
                });
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "No se pudieron cargar las plantas.",
            });
        }
    });
}

// ==================== Eventos de Modales ====================

// Abrir modal para añadir planta
$(document).on("click", "#btnAddPlanta", function () {
    $("#plantaForm")[0].reset();
    $("#plantaModalLabel").text("Añadir Planta");
    $("#maquinaModal").modal("hide");
    $("body").removeClass("modal-open");
    $(".modal-backdrop").remove();
    $("#plantaModal").modal("show");
});

// Abrir modal para añadir cabezal
$("#btnAddCabezal").click(function () {
    $("#cabezalId").val("");
    $("#cabezalModalLabel").text("Añadir Cabezal");
    $("#cabezalForm")[0].reset();
    loadMachines();
    $('#btnAddMaquina').show();
    $("#cabezalModal").modal("show");
});

// Abrir modal para editar cabezal
$('#tabla_cabezales tbody').on('click', '.btn-edit', function() {
    var data = table.row($(this).parents('tr')).data();
    $('#cabezalModalLabel').text('Editar Cabezal');
    $('#nombre').val(data.nombre);
    $('#cabezalId').val(data.id);
    loadMachines(function() {
        $('#maquina').val(data.maquina_id).change();
    });
    $('#btnAddMaquina').hide();
    $('#cabezalModal').modal('show');
});

// Abrir modal para añadir máquina desde el modal de cabezal
$(document).on("click", "#btnAddMaquina", function () {
    $("#maquinaModalLabel").text("Añadir Máquina");
    $("#maquinaForm")[0].reset();
    loadPlantas();
    $("#cabezalModal").modal("hide");

    $('#cabezalModal').on('hidden.bs.modal', function () {
        $("#maquinaModal").modal("show");
        $('#cabezalModal').off('hidden.bs.modal');
    });
});


// Cerrar modales cuando se presiona cancelar o cerrar
$('#cancelMaquinaModal, #cancelPlantaModal, #saveCabezal, #saveMaquina, #savePlanta').click(function() {
    $(this).closest('.modal').modal('hide');
});

$('.modal').on('click', '[data-dismiss="modal"]', function() {
    $(this).closest('.modal').modal('hide');
});

// ==================== Guardar y Eliminar ====================

// Guardar planta
$("#savePlanta").click(function () {
    var nombre = $("#nombrePlanta").val().trim();
    var ubicacion = $("#ubicacionPlanta").val().trim();
    var correo = $("#correoPlanta").val().trim();
    var contacto = $("#contactoPlanta").val().trim();
    var telefono = $("#telefonoPlanta").val().trim();

    if (!nombre || !ubicacion || !correo || !contacto || !telefono) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    $.ajax({
        url: "/catalogos/plantas/create/",
        method: "POST",
        data: $("#plantaForm").serialize(),
        success: function (response) {
            $("#plantaModal").modal("hide");
            loadPlantas();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Planta guardada con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar la planta";
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

// Guardar o actualizar el cabezal
$("#saveCabezal").click(function () {
    var cabezalId = $("#cabezalId").val();
    var url = cabezalId
        ? `/catalogos/cabezales/update/${cabezalId}/`
        : "/catalogos/cabezales/create/";
    var method = "POST"; // Cambiar a POST para ambos casos
    var data = $("#cabezalForm").serialize();

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (response) {
            $("#cabezalModal").modal("hide");
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Cabezal guardado con éxito.",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar el cabezal.";
            if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                icon: "error",
                title: "Error",
                html: `<p>${errorMessage}</p>`,
            });
        }
    });
});

// Guardar máquina (añadir o editar) con validación usando SweetAlert2
$("#saveMaquina").click(function () {
    var numero = $("#numero").val().trim();
    var planta = $("#planta").val();

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
    var method = "POST";

    $.ajax({
        url: url,
        method: method,
        data: $("#maquinaForm").serialize(),
        success: function (response) {
            $("#maquinaModal").modal("hide");
            loadMachines();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Máquina guardada con éxito",
            });
        },
        error: function (xhr) {
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

// Confirmar eliminación usando SweetAlert2 para cabezales
$('#tabla_cabezales tbody').on('click', '.btn-delete', function () {
    var data = table.row($(this).parents('tr')).data();
    var cabezalId = data ? data.id : null;

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
                method: 'DELETE',
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function (response) {
                    table.ajax.reload();
                    Swal.fire(
                        'Eliminado!',
                        'El cabezal ha sido eliminado.',
                        'success'
                    );
                },
                error: function (xhr) {
                    var errorMessage = "Error al eliminar el cabezal.";
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
        }
    });
});



});
