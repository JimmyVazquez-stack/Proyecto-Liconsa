
$(document).ready(function() {
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
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
        });



    var table = $('#tabla_tipo_producto').DataTable({
        ajax: {
            url: '/catalogos/tipo_producto/list/data/',
            dataSrc: ''
        },
        
        columns: [
            { data: 'nombre' },
            { data: 'descripcion' },
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
        },
        columnDefs: [
            {
                targets: -1,
                defaultContent: "<div style='display: flex; justify-content: space-between;'><a href='#' class='btn btn-secondary' style='font-size: 14px; width:75px;'><i class='fas fa-pencil'></i></a><a href='#' class='btn btn-danger' style='font-size: 14px; width: 75px;' ><i class='fas fa-trash'></i></a></div>",                orderable: false
            }
        ]
        
    });


// Abrir modal para añadir tipo de producto
$("#btnAddTipoProducto").click(function () {
    $("#tipoProductoModalLabel").text("Añadir Tipo de Producto");
    $("#tipoProductoForm")[0].reset();
    $("#tipoProductoId").val("");
    $("#tipoProductoModal").modal("show");
});

// Guardar tipo de producto (añadir o editar)
$("#saveTipoProducto").click(function () {
    var nombreTipoProducto = $("#nombreTipoProducto").val().trim();
    var descripcionTipoProducto = $("#descripcionTipoProducto").val().trim();
    var tipoProductoId = $("#tipoProductoId").val();

    // Validar que los campos no estén vacíos
    if (!nombreTipoProducto || !descripcionTipoProducto) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var url = tipoProductoId ? `/catalogos/tipo_producto/update/${tipoProductoId}/` : "/catalogos/tipo_producto/create/";
    var method = "POST";

    var data = {
        nombre: nombreTipoProducto,
        descripcion: descripcionTipoProducto
    };

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (response) {
            $("#tipoProductoModal").modal("hide");
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Tipo de Producto guardado con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar el tipo de producto";
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

 // Función para abrir el modal de editar TipoProducto
 $("#tabla_tipo_producto tbody").on("click", ".btn-edit", function () {
    var data = table.row($(this).parents("tr")).data();

    $("#tipoProductoModalLabel").text("Editar Tipo de Producto");
    $("#tipoProductoId").val(data.id);
    $("#nombreTipoProducto").val(data.nombre);
    $("#descripcionTipoProducto").val(data.descripcion);
    $("#tipoProductoModal").modal("show");
});

// Función para abrir el modal de eliminar TipoProducto
$("#tabla_tipo_producto tbody").on("click", ".btn-delete", function () {
    var data = table.row($(this).parents("tr")).data();

    Swal.fire({
        title: "¿Estás seguro?",
        text: "No podrás revertir esta acción",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        customClass: {
            confirmButton: 'btn btn-danger',
            cancelButton: 'btn btn-secondary'
        },
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/catalogos/tipo_producto/delete/${data.id}/`,
                method: "POST",
                success: function (response) {
                    table.ajax.reload();
                    Swal.fire(
                        "Eliminado",
                        "El tipo de producto ha sido eliminado.",
                        "success"
                    );
                },
                error: function () {
                    Swal.fire(
                        "Error",
                        "Hubo un problema al eliminar el tipo de producto.",
                        "error"
                    );
                }
            });
        }
    });
});


// Manejadores manuales para cerrar el modal de tipo de producto
$("#tipoProductoModal .close, #tipoProductoModal .btn-secondary").click(function () {
    $("#tipoProductoModal").modal("hide");
});





});