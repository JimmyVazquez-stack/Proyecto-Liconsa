$(document).ready(function () {
  var table = $("#listar_usuarios").DataTable({
    ajax: {
      url: "/usuarios/data/",
      dataSrc: "data",
    },
    columns: [
      { data: "username" },
      { data: "first_name" },
      { data: "last_name" },
      { data: "email" },
      { data: "telefono" },
      { data: "area" },
      { data: "grupo" },
      {
        data: null,
        render: function (data, type, row) {
          var botones = `<button class="btn btn-editar" data-id="${row.id}"><i class="fas fa-pencil-alt"></i></button>`;
          
          if (row.username !== usuarioAutenticadoUsername) {
            botones += `<button class="btn btn-delete" data-id="${row.id}"><i class="fas fa-trash text-red"></i></button>`;
          }
          
          return botones;
        }
      }
    ],
    language: {
      search: "Buscar:",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior",
      },
      lengthMenu: "Mostrar _MENU_ entradas",
      info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
      infoEmpty: "Mostrando 0 a 0 de 0 entradas",
      loadingRecords: "Cargando...",
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla",
      aria: {
        sortAscending: ": activar para ordenar la columna ascendente",
        sortDescending: ": activar para ordenar la columna descendente",
      },
    },
  });

  // Delegación de evento para manejar clic en botón de editar
  $(document).on('click', '.btn-editar', function() {
    var userId = $(this).data('id');
    $.ajax({
      url: '/usuarios/editar_usuario/' + userId,
      success: function(data) {
        $('#editModal .modal-body').html(data);
        $('#editModal').modal('show');
      },
      error: function(xhr, status, error) {
        console.error("Error al cargar el formulario de edición:", error);
        alert("No se pudo cargar el formulario de edición. Por favor, intente de nuevo.");
      }
    });
  });

// Manejar clic en botón de editar
$('.btn-editar').on('click', function() {
  var userId = $(this).data('id');
  $.ajax({
    url: '/usuarios/editar_usuario/' + userId,
    success: function(data) {
      $('#editModal .modal-body').html(data);
      $('#editModal').modal('show');
    },
    error: function(xhr, status, error) {
      console.error("Error al cargar el formulario de edición:", error);
      alert("No se pudo cargar el formulario de edición. Por favor, intente de nuevo."); // Mostrar mensaje de error al usuario
    }
  });
});

// Manejar clic en botón de guardar cambios en el modal de editar
$('#editModal .btn-primary').on('click', function() {
  var userId = $('#editForm').data('userid'); // Asegúrate de que el formulario tenga un atributo data-userid
  $.ajax({
    url: '/usuarios/editar_usuario/' + userId,
    type: 'POST',
    data: $('#editForm').serialize(), // Envía los datos del formulario
    success: function(result) {
      $('#editModal').modal('hide');
      alert("Usuario actualizado con éxito."); // Mostrar mensaje de éxito
      location.reload(); // Opcional: recargar la página para ver los cambios
    },
    error: function(xhr, status, error) {
      console.error("Error al actualizar el usuario:", error);
      alert("Error al actualizar el usuario. Por favor, intente de nuevo."); // Mostrar mensaje de error dentro del modal
    }
  });
});

  // Manejar clic en botón de eliminar
  $('#listar_usuarios tbody').on('click', '.btn-delete', function() {
    var data = table.row($(this).parents('tr')).data();
    var userId = data.id; // Asume que `id` es la propiedad que contiene el ID del usuario
    var userName = data.username; // Asume que `username` es la propiedad que contiene el nombre del usuario

    // Actualiza el modal con la información del usuario
    $('#userNameToDelete').text(userName);
    $('#confirmDelete').data('userid', userId); // Guarda el ID en el botón de confirmar del modal

    // Muestra el modal
    $('#deleteModal').modal('show');
  });

  // Manejar la confirmación de eliminación
  $('#confirmDelete').on('click', function() {
    var userId = $(this).data('userid');

    // Envía una solicitud AJAX al servidor para eliminar el usuario
    $.ajax({
      url: '/usuarios/eliminar_usuario/' + userId,
      type: 'DELETE',
      success: function(result) {
        // Cerrar el modal
        $('#deleteModal').modal('hide');

        // Actualizar el DataTable o mostrar un mensaje de éxito
        table.row($('.btn-delete[data-id="' + userId + '"]').parents('tr')).remove().draw();
      },
      error: function(xhr, status, error) {
        // Manejar errores
        console.error("Error al eliminar el usuario:", error);
      }
    });
  });
  // Para el botón de cerrar (X)
$('.close').click(function() {
  $('#deleteModal').modal('hide');
});

// Para el botón de cancelar
$('.btn-secondary').click(function() {
  $('#deleteModal').modal('hide');
});
});
