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

<<<<<<< HEAD
$(document).ready(function() {
    $('#tabla_poblacion').DataTable({
        ajax: {
            url: '/catalogos/poblaciones/list/data/',
            dataSrc: ''
        },
        
        columns: [
            { data: 'nombre_poblacion' },
            { data: 'municipio_poblacion' },
            { data: 'estado_poblacion' },
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
=======
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
>>>>>>> 9648d260015e696f90a21b7ad043d27f80636329

  var table = $("#tabla_poblacion").DataTable({
    ajax: {
      url: "/catalogos/poblaciones/list/data/",
      dataSrc: "",
    },
    columns: [
      { data: "nombre" },
      { data: "municipio" },
      { data: "estado" },
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
    columnDefs: [{ orderable: false, targets: -1 }],
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

  // Manejadores manuales para cerrar el modal
  $("#poblacionModal .close, #poblacionModal .btn-secondary").click(
    function () {
      $("#poblacionModal").modal("hide");
    }
  );

  // Abrir modal para editar población
  $("#tabla_poblacion tbody").on("click", ".btn-edit", function () {
    var data = table.row($(this).parents("tr")).data();
    $("#poblacionModalLabel").text("Editar Población");
    $("#nombre").val(data.nombre);
    $("#municipio").val(data.municipio);
    $("#estado").val(data.estado);
    $("#poblacionId").val(data.id);
    $("#poblacionModal").modal("show");
  });

  // Confirmar eliminación usando SweetAlert2
  $("#tabla_poblacion tbody").on("click", ".btn-delete", function () {
    var data = table.row($(this).parents("tr")).data();
    Swal.fire({
      title: "¿Estás seguro?",
      text: `¿Deseas eliminar la población ${data.nombre}?`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: `/catalogos/poblaciones/delete/${data.id}/`,
          method: "DELETE",
          success: function (response) {
            table.ajax.reload();
            Swal.fire(
              "Eliminado",
              "Población eliminada exitosamente",
              "success"
            );
          },
          error: function (error) {
            Swal.fire(
              "Error",
              "Hubo un problema al eliminar la población",
              "error"
            );
          },
        });
      }
    });
  });
});
