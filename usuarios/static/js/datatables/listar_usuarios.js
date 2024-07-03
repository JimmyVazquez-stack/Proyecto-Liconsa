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
          return `
            <button onclick="cargarFormularioEdicion(${row.id})" class="btn btn-sm btn-primary" data-id="${row.id}">Editar</button>
            <button class="btn btn-delete" data-id="${row.id}"><i class="fas fa-trash text-red"></i></button>
          `;
        },
      },
    ],
    language: {
      search: "Buscar:",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      lengthMenu: "Mostrar _MENU_ entradas",
      info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
      infoEmpty: "Mostrando 0 a 0 de 0 entradas",
      loadingRecords: "Cargando...",
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla",
      aria: {
        sortAscending: ": activar para ordenar la columna ascendente",
        sortDescending: ": activar para ordenar la columna descendente"
      }
    }
  });

// Manejar clic en botón editar
$('#listar_usuarios tbody').on('click', 'button.btn-edit', function() {
  var data = table.row($(this).parents('tr')).data();
  var userId = data.id; // Asegúrate de que 'id' corresponde al nombre de la propiedad que contiene el ID del usuario

  // Realizar solicitud AJAX para obtener el formulario de edición
  $.ajax({
    url: '/ruta/a/vista/editar/usuario/' + userId, // Asegúrate de reemplazar esto con la URL correcta
    method: 'GET',
    success: function(formHtml) {
      // Insertar el formulario en el modal
      $('#editModal .modal-body').html(formHtml);
      // Mostrar el modal
      $('#editModal').modal('show');
    },
    error: function(xhr, status, error) {
      // Manejar errores (opcional)
      console.error("Error al cargar el formulario de edición:", error);
    }
  });
});
  // Manejar clic en botón eliminar
  $('#listar_usuarios tbody').on('click', 'button.btn-delete', function() {
    var data = table.row($(this).parents('tr')).data();
    // Aquí puedes establecer datos o identificadores en el modal de eliminación si es necesario
    $('#deleteModal').modal('show');
  });
});