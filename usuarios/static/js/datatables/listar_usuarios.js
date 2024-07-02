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
        defaultContent: `
                    <button class="btn btn-edit"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-delete"><i class="fas fa-trash text-red"></i></button>
                `,
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
    // Aquí puedes llenar el formulario en el modal de edición con los datos del usuario
    // Por ejemplo: $('#editUserField').val(data.first_name);
    $('#editModal').modal('show');
  });

  // Manejar clic en botón eliminar
  $('#listar_usuarios tbody').on('click', 'button.btn-delete', function() {
    var data = table.row($(this).parents('tr')).data();
    // Aquí puedes establecer datos o identificadores en el modal de eliminación si es necesario
    $('#deleteModal').modal('show');
  });
});