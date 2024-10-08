
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

    var table = $('#tabla_productos').DataTable({
        ajax: {
            url: '/catalogos/productos/list/data/',
            dataSrc: ''
        },
        
        columns: [
            { data: 'nombre' },
            { data: 'nombre_tipo_producto' },
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
// Función para cargar opciones de tipos de productos en el modal de creación/edición de producto
function loadTiposProducto(selectedTipoProductoId = null) {
    $.ajax({
        url: '/catalogos/tipo_producto/list/data/',
        method: 'GET',
        success: function(response) {
            var tipoProductoSelect = $('#tipoProducto');
            tipoProductoSelect.empty();

            if (response.length > 0) {
                tipoProductoSelect.append(new Option('Seleccione un tipo de producto', '', true, true));
                response.forEach(function(tipoProducto) {
                    tipoProductoSelect.append(new Option(tipoProducto.nombre, tipoProducto.id));
                });

                if (selectedTipoProductoId) {
                    tipoProductoSelect.val(selectedTipoProductoId);
                }
            } else {
                tipoProductoSelect.append(new Option('No hay tipos de productos disponibles', '', true, true));
            }
        },
        error: function() {
            alert('Error al cargar los tipos de productos.');
        }
    });
}

// Abrir modal para añadir producto
$("#btnAddProducto").click(function () {
    $("#productoModalLabel").text("Añadir Producto");
    $("#productoForm")[0].reset();
    $("#productoId").val("");  // ID vacío para nueva creación
    loadTiposProducto();  // Cargar opciones de tipos de productos
    $("#btnAddTipoProducto").show();  // Mostrar el botón para añadir tipo de producto
    $("#productoModal").modal("show");
});

// Guardar producto (añadir o editar) con validación usando SweetAlert2
$("#saveProducto").click(function () {
    var nombreProducto = $("#nombreProducto").val().trim();
    var tipoProductoId = $("#tipoProducto").val();
    var productoId = $("#productoId").val();

    // Validar que los campos no estén vacíos
    if (!nombreProducto || !tipoProductoId) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var url = productoId ? `/catalogos/productos/update/${productoId}/` : "/catalogos/productos/create/";
    var method = "POST";

    var data = {
        nombre: nombreProducto,
        tipo_producto_id: tipoProductoId
    };


    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (response) {
            $("#productoModal").modal("hide");
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Producto guardado con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar el producto";
            if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                icon: "error",
                title: "Error",
                text: errorMessage,
            });
        }
    });
});



// Abrir modal para añadir tipo de producto
$("#btnAddTipoProducto").click(function () {
    $("#tipoProductoModalLabel").text("Añadir Tipo de Producto");
    $("#tipoProductoForm")[0].reset();
    $("#tipoProductoModal").modal("show");
});

// Guardar tipo de producto con validación usando SweetAlert2
$("#saveTipoProducto").click(function () {
    var nombreTipoProducto = $("#nombreTipoProducto").val().trim();
    var descripcionTipoProducto = $("#descripcionTipoProducto").val().trim();

    if (!nombreTipoProducto || !descripcionTipoProducto) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var tipoProductoId = $("#tipoProductoId").val();
    var url = tipoProductoId ? `/catalogos/tipo_producto/update/${tipoProductoId}/` : "/catalogos/tipo_producto/create/";
    var method = "POST";

    $.ajax({
        url: url,
        method: method,
        data: {
            nombre: nombreTipoProducto,
            descripcion: descripcionTipoProducto
        },
        success: function (response) {
            $("#tipoProductoModal").modal("hide");
            loadTiposProducto();  // Recargar tipos de productos si es necesario
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Tipo de producto guardado con éxito",
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

// Manejadores manuales para cerrar el modal
$("#productoModal .close, #productoModal .btn-secondary").click(function () {
    $("#productoModal").modal("hide");
});

$("#tipoProductoModal .close, #tipoProductoModal .btn-secondary").click(function () {
    $("#tipoProductoModal").modal("hide");
});

// Abrir modal para editar producto
$("#tabla_productos tbody").on("click", ".btn-edit", function () {
    var data = table.row($(this).parents("tr")).data();
    
    $("#productoModalLabel").text("Editar Producto");
    $("#productoId").val(data.id);
    $("#nombreProducto").val(data.nombre);
    loadTiposProducto(data.tipo_producto_id);  // Seleccionar el tipo de producto adecuado
    $("#btnAddTipoProducto").hide();  // Ocultar el botón para añadir tipo de producto
    $("#productoModal").modal("show");
});
// Confirmar eliminación usando SweetAlert2
$("#tabla_productos tbody").on("click", ".btn-delete", function () {
    var data = table.row($(this).parents("tr")).data();
    Swal.fire({
        title: "¿Estás seguro?",
        text: `¿Deseas eliminar el producto ${data.nombre}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "red", 
        cancelButtonColor: "gray",
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/catalogos/productos/delete/${data.id}/`,
                method: "DELETE",
                success: function (response) {
                    table.ajax.reload();
                    Swal.fire(
                        "Eliminado",
                        "Producto eliminado exitosamente",
                        "success"
                    );
                },
                error: function (error) {
                    Swal.fire(
                        "Error",
                        "Hubo un problema al eliminar el producto",
                        "error"
                    );
                },
            });
        }
    });
});



});

