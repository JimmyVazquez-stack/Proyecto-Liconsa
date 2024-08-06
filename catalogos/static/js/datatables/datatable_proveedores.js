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
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    });

    var table = $("#tabla_proveedores").DataTable({
        ajax: {
            url: "/catalogos/proveedores/list/data/",
            dataSrc: "",
        },
        columns: [
            { data: "nombre" },
            { data: "contacto" },
            { data: "telefono" },
            { data: "correo" },
            { data: "nombre_planta" },
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
                orderable: false,
            },
        ],
    });

  // Abrir modal para añadir proveedor
  $("#btnAddProveedor").click(function () {
    $("#proveedorModalLabel").text("Añadir Proveedor");
    $("#proveedorForm")[0].reset();
    $("#proveedorId").val("");
    $("#proveedorModal").modal("show");
});

// Guardar proveedor (añadir o editar) con validación usando SweetAlert2
$("#saveProveedor").click(function () {
    var nombre = $("#nombre").val().trim();
    var direccion = $("#direccion").val().trim();
    var telefono = $("#telefono").val().trim();
    var correo = $("#correo").val().trim();

    // Validar que los campos no estén vacíos
    if (!nombre || !direccion || !telefono || !correo) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var proveedorId = $("#proveedorId").val();
    var url = proveedorId ? `/proveedores/update/${proveedorId}/` : "/proveedores/create/";
    var method = "POST";

    $.ajax({
        url: url,
        method: method,
        data: $("#proveedorForm").serialize(),
        success: function (response) {
            $("#proveedorModal").modal("hide");
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Proveedor guardado con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar el proveedor";
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
$("#proveedorModal .close, #proveedorModal .btn-secondary").click(function () {
    $("#proveedorModal").modal("hide");
});

// Abrir modal para editar proveedor
$("#tabla_proveedores tbody").on("click", ".btn-edit", function () {
    var data = table.row($(this).parents("tr")).data();
    $("#proveedorModalLabel").text("Editar Proveedor");
    $("#nombre").val(data.nombre);
    $("#direccion").val(data.direccion);
    $("#telefono").val(data.telefono);
    $("#correo").val(data.correo);
    $("#proveedorId").val(data.id);
    $("#proveedorModal").modal("show");
});

// Confirmar eliminación usando SweetAlert2
$("#tabla_proveedores tbody").on("click", ".btn-delete", function () {
    var data = table.row($(this).parents("tr")).data();
    Swal.fire({
        title: "¿Estás seguro?",
        text: `¿Deseas eliminar el proveedor ${data.nombre}?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "red", // Color personalizado para el botón de confirmar (ej. rojo)
        cancelButtonColor: "gray", // Color personalizado para el botón de cancelar (ej. azul)
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/proveedores/delete/${data.id}/`,
                method: "DELETE",
                success: function (response) {
                    table.ajax.reload();
                    Swal.fire(
                        "Eliminado",
                        "Proveedor eliminado exitosamente",
                        "success"
                    );
                },
                error: function (error) {
                    Swal.fire(
                        "Error",
                        "Hubo un problema al eliminar el proveedor",
                        "error"
                    );
                },
            });
        }
    });
});
});

