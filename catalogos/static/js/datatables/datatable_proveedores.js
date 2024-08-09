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

// Función para cargar opciones de plantas en el modal de creación/edición de máquina
function loadPlantas(selectedPlantaId = null) {
    $.ajax({
        url: '/catalogos/plantas/list/data/',
        method: 'GET',
        success: function(response) {
            var plantaSelect = $('#planta');
            plantaSelect.empty();

            if (response.length > 0) {
                // Añadir opción por defecto si hay más de 2 plantas
                if (response.length > 2) {
                    plantaSelect.append(new Option('Seleccione una planta', '', true, true));
                } else if (response.length === 1) {
                    plantaSelect.append(new Option('Seleccione una planta', '', false, false));
                } else {
                    plantaSelect.append(new Option('Seleccione una planta', '', true, true));
                }

                response.forEach(function(planta) {
                    plantaSelect.append(new Option(planta.nombre, planta.id));
                });

                if (selectedPlantaId) {
                    plantaSelect.val(selectedPlantaId);
                }
            } else {
                plantaSelect.append(new Option('No hay plantas disponibles', '', true, true));
            }
        },
        error: function() {
            alert('Error al cargar las plantas.');
        }
    });
}

// Abrir modal para añadir proveedor
$("#btnAddProveedor").click(function () {
    $("#proveedorModalLabel").text("Añadir Proveedor");
    $("#proveedorForm")[0].reset();
    $("#proveedorId").val("");
    loadPlantas();
    $("#proveedorModal").modal("show");
});


// Guardar proveedor (añadir o editar) con validación usando SweetAlert2
$("#saveProveedor").click(function () {
    var nombre = $("#nombre").val().trim();
    var telefono = $("#telefono").val().trim();
    var correo = $("#correo").val().trim();
    var plantaId = $("#planta").val();

    // Validar que los campos no estén vacíos
    if (!nombre || !telefono || !correo || !plantaId) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var proveedorId = $("#proveedorId").val();
    var url = proveedorId ? `/catalogos/proveedores/update/${proveedorId}/` : "/catalogos/proveedores/create/";
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


 // Abrir modal para añadir planta
$("#btnAddPlanta").click(function () {
    $("#plantaModalLabel").text("Añadir Planta");
    $("#plantaForm")[0].reset();
    $("#plantaModal").modal("show");
});

// Guardar planta
$("#savePlanta").click(function () {
    var nombrePlanta = $("#nombre").val().trim();
    var ubicacionPlanta = $("#ubicacion").val().trim();
    var correoPlanta = $("#correo").val().trim();
    var contactoPlanta = $("#contacto").val().trim();
    var telefonoPlanta = $("#telefono").val().trim();

     // Mensajes de depuración
     console.log("Evento de clic activado");
     console.log("Nombre:", nombrePlanta);
     console.log("Ubicación:", ubicacionPlanta);
     console.log("Correo:", correoPlanta);
     console.log("Contacto:", contactoPlanta);
     console.log("Teléfono:", telefonoPlanta);
 

    // Validar que todos los campos estén llenos
    if (!nombrePlanta || !ubicacionPlanta || !correoPlanta || !contactoPlanta || !telefonoPlanta) {
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
        data: {
            nombre: nombrePlanta,
            ubicacion: ubicacionPlanta,
            correo: correoPlanta,
            contacto: contactoPlanta,
            telefono: telefonoPlanta
        },
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


// Manejadores manuales para cerrar el modal
$("#proveedorModal .close, #proveedorModal .btn-secondary").click(function () {
    $("#proveedorModal").modal("hide");
});

// Manejadores manuales para cerrar el modal de planta
$("#plantaModal .close, #plantaModal .btn-secondary").click(function () {
    $("#plantaModal").modal("hide");
});


// Abrir modal para editar proveedor
$("#tabla_proveedores tbody").on("click", ".btn-edit", function () {
    var data = table.row($(this).parents("tr")).data();
    
    // Llenar campos del formulario con los datos del proveedor seleccionado
    $("#proveedorId").val(data.id);
    $("#nombre").val(data.nombre);
    $("#telefono").val(data.telefono);
    $("#correo").val(data.correo);

    // Cargar las opciones de plantas y seleccionar la que corresponde al proveedor
    loadPlantas(data.planta_id);

    // Mostrar el modal
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
                url: `/catalogos/proveedores/delete/${data.id}/`,
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

