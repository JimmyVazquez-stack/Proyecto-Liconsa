
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

    var table = $('#tabla_silos').DataTable({
        ajax: {
            url: '/catalogos/silos/list/data/',
            dataSrc: ''
        },
        
        columns: [
            { data: 'numero' },
            { data: 'capacidad' },
            { data: 'nombre_producto' },
            { data: 'nombre_planta' },
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

    function openSiloModal(siloId) {
        if (siloId) {
            // Modo edición
            $("#siloModalLabel").text("Editar Silo");
            $("#saveSilo").data("id", siloId); // Guarda el ID del silo en el botón de guardar
            $.ajax({
                url: `/catalogos/silos/${siloId}/`,
                method: "GET",
                success: function (data) {
                    // Rellena los campos del formulario con los datos del silo
                    $("#numeroSilo").val(data.numero);
                    $("#capacidadSilo").val(data.capacidad);
                    $("#productoSilo").val(data.producto_id);
                    $("#plantaSilo").val(data.planta_id);
    
                    // Ocultar botones de añadir producto y planta
                    $("#btnAddProducto").hide();
                    $("#btnAddPlanta").hide();
                    
                    $("#siloModal").modal("show");
                },
                error: function (xhr) {
                    console.error("Error al cargar los datos del silo:", xhr);
                }
            });
        } else {
            // Modo creación
            $("#siloModalLabel").text("Añadir Silo");
            $("#saveSilo").removeData("id"); // Elimina el ID del silo del botón de guardar
    
            // Mostrar botones de añadir producto y planta
            $("#btnAddProducto").show();
            $("#btnAddPlanta").show();
    
            $("#siloModal").modal("show");
        }
    }
    
    // Llama a openSiloModal con el ID del silo para abrir en modo edición
    // Llama a openSiloModal() sin parámetros para abrir en modo creación
    


// Función para cargar opciones de tipos de productos en el modal de creación/edición de producto
function loadTiposProducto(selectedTipoProductoId = null) {
    $.ajax({
        url: '/catalogos/tipo_producto/list/data/',
        method: 'GET',
        success: function(response) {
            var tipoProductoSelect = $('#tipoProducto');
            tipoProductoSelect.empty();

            if (response.length > 0) {
                // Agregar la opción predeterminada si hay más de 2 tipos de productos
                if (response.length > 2) {
                    tipoProductoSelect.append(new Option('Seleccione un tipo de producto', '', true, false));
                }
                response.forEach(function(tipoProducto) {
                    tipoProductoSelect.append(new Option(tipoProducto.nombre, tipoProducto.id));
                });

                // Si se proporciona un ID seleccionado, seleccionarlo
                if (selectedTipoProductoId) {
                    tipoProductoSelect.val(selectedTipoProductoId);
                }
            } else {
                // Agregar una opción para el caso cuando no hay tipos de productos disponibles
                tipoProductoSelect.append(new Option('No hay tipos de productos disponibles', '', true, false));
            }
        },
        error: function() {
            alert('Error al cargar los tipos de productos.');
        }
    });

}


    // Función para mostrar/ocultar botones según el modo (crear/editar)
    function toggleAddButtons(isEditMode) {
        if (isEditMode) {
            $("#btnAddProducto").hide();
            $("#btnAddPlanta").hide();
        } else {
            $("#btnAddProducto").show();
            $("#btnAddPlanta").show();
        }
    }
    

// Eventos que se ejecutan al cargar la página
$(document).ready(function () {

   // Evento al abrir el modal
$('#siloModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Botón que disparó el modal
    var isEditMode = button.hasClass('btn-edit'); // Comprueba si es el botón de editar

    // Cambia el título del modal según el modo
    $("#siloModalLabel").text(isEditMode ? "Editar Silo" : "Añadir Silo");

    // Llama a la función para mostrar/ocultar botones
    toggleAddButtons(isEditMode);

    if (isEditMode) {
        // Cargar datos del silo en el formulario para edición
        var data = table.row(button.parents("tr")).data();
        $("#numeroSilo").val(data.numero);
        $("#capacidadSilo").val(data.capacidad);
        $("#productoSilo").val(data.producto_id);
        $("#plantaSilo").val(data.planta_id);
    } else {
        // Limpiar el formulario para añadir un nuevo silo
        $("#siloForm")[0].reset();
    }

    // Cargar las opciones de productos y plantas
    loadProductos();
    loadPlantas();
});
    // Aquí puedes añadir otros eventos relacionados con la funcionalidad de los silos
});



//Abrir modal creacion de silo
$("#btnAddSilo").click(function () {
    $("#siloModalLabel").text("Añadir Silo");
    $("#siloForm")[0].reset();  // Resetea el formulario
    $("#siloId").val('');  // Limpia el campo oculto
    $("#siloModal").modal("show");
    openSiloModal();
});

// Guardar o actualizar silo
$("#saveSilo").click(function () {
    var numeroSilo = $("#numeroSilo").val().trim();
    var capacidadSilo = $("#capacidadSilo").val().trim();
    var productoId = $("#productoSilo").val();
    var plantaId = $("#plantaSilo").val();
    var siloId = $("#siloId").val(); // En caso de edición, obtener el ID del silo

    // Validar que los campos no estén vacíos
    if (!numeroSilo || !capacidadSilo || !productoId || !plantaId) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    // Validar que los campos numéricos son válidos
    if (isNaN(capacidadSilo) || capacidadSilo <= 0) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Capacidad debe ser un número positivo",
        });
        return;
    }

    var url = siloId ? `/catalogos/silos/update/${siloId}/` : "/catalogos/silos/create/";
    var method = "POST";

    var data = {
        numero: numeroSilo,
        capacidad: capacidadSilo,
        producto_id: productoId,
        planta_id: plantaId
    };

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (response) {
            closeModal(); // Cierra el modal al guardar con éxito
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: response.message || "Silo guardado con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar el silo";
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




// Abrir modal para editar silo
$("#tabla_silos tbody").on("click", ".btn-edit", function () {
    var data = table.row($(this).parents("tr")).data();

    $("#siloModalLabel").text("Editar Silo");
    $("#siloId").val(data.id);

    // Cargar productos y plantas y luego asignar los valores
    loadProductos(data.producto_id, function() {
        $("#productoSilo").val(data.producto_id);
    });

    loadPlantas(data.planta_id, function() {
        $("#plantaSilo").val(data.planta_id);
    });

    // Asignar otros valores que no dependan de AJAX
    $("#numeroSilo").val(data.numero);
    $("#capacidadSilo").val(data.capacidad);

    $("#siloModal").modal("show");
});



// Eliminar silo
$("#tabla_silos tbody").on("click", ".btn-delete", function () {
    var data = table.row($(this).parents("tr")).data();
    
    // Extraer detalles del silo
    var numeroSilo = data.numero;
    var nombreProducto = data.nombre_producto;  // Asegúrate de que estos nombres coincidan con los campos de la tabla
    var nombrePlanta = data.nombre_planta;

    // Personalizar el texto de confirmación
    var confirmText = `¿Estás seguro de que deseas eliminar el silo  número ${numeroSilo}
    , que contiene el producto ${nombreProducto} y está ubicado en la planta ${nombrePlanta}? 
    No podrás revertir esta acción.`;

    Swal.fire({
        title: "¿Estás seguro?",
        text: confirmText,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "gray",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/catalogos/silos/delete/${data.id}/`,
                method: "POST",
                success: function (response) {
                    table.ajax.reload();
                    Swal.fire({
                        icon: "success",
                        title: "Eliminado",
                        text: `El silo número ${numeroSilo} ha sido eliminado con éxito`,
                    });
                },
                error: function (xhr) {
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: "Error al eliminar el silo",
                    });
                },
            });
        }
    });
});



// Abrir modal para añadir un nuevo producto
$("#btnAddProducto").on("click", function () {
    // Cambiar el título del modal
    $("#productoModalLabel").text("Añadir Producto");

    // Restablecer el formulario del modal
    $("#productoForm")[0].reset();

    // Asegurarse de que el campo oculto de ID esté vacío
    $("#productoId").val("");

    // Cargar tipos de productos disponibles en el select
    loadTiposProducto(); 

    // Mostrar el modal
    $("#productoModal").modal("show");
});




// Abrir modal para añadir tipo de producto
$("#btnAddTipoProducto").click(function () {
    $("#tipoProductoModalLabel").text("Añadir Tipo de Producto");
    $("#tipoProductoForm")[0].reset();
    $("#tipoProductoId").val("");
    $("#tipoProductoModal").modal("show");
});

// Manejadores manuales para cerrar el modal de tipo de producto
$("#tipoProductoModal .close, #tipoProductoModal .btn-secondary").click(function () {
    $("#tipoProductoModal").modal("hide");
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

// Cargar productos y plantas en los select
function loadProductos() {
    $.ajax({
        url: '/catalogos/productos/list/data/',
        method: 'GET',
        success: function(data) {
            let productoSelect = $("#productoSilo");
            productoSelect.empty();
            
            if (data.length === 0) {
                productoSelect.append('<option disabled selected>No hay productos disponibles</option>');
            } else {
                if (data.length >= 1) {
                    productoSelect.append('<option disabled selected>Seleccione un producto</option>');
                }
                data.forEach(function(producto) {
                    productoSelect.append(`<option value="${producto.id}">${producto.nombre}</option>`);
                });
            }
        },
        error: function(xhr) {
            console.error('Error al cargar los productos:', xhr);
        }
    });

}



function loadPlantas() {
    $.ajax({
        url: '/catalogos/plantas/list/data/',
        method: 'GET',
        success: function(data) {
            let plantaSelect = $("#plantaSilo");
            plantaSelect.empty();
            
            if (data.length === 0) {
                plantaSelect.append('<option disabled selected>No hay plantas disponibles</option>');
            } else {
                // Agregar la opción "Seleccione una planta" y seleccionarla por defecto
                plantaSelect.append('<option disabled selected>Seleccione una planta</option>');
                
                data.forEach(function(planta) {
                    plantaSelect.append(`<option value="${planta.id}">${planta.nombre}</option>`);
                });
            }
        },
        error: function(xhr) {
            console.error('Error al cargar las plantas:', xhr);
        }
    });
}

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



// Llamar a estas funciones al abrir el modal
$('#siloModal').on('show.bs.modal', function() {
    loadProductos();
    loadPlantas();
});

// Al hacer clic en el botón de añadir producto
$("#btnAddProducto").click(function() {
    $("#productoModal").modal("show");
});

// Al hacer clic en el botón de añadir planta
$("#btnAddPlanta").click(function() {
    $("#plantaModal").modal("show");
});

// Función para cerrar el modal
function closeModal() {
    $('#siloModal').modal('hide'); // Cierra el modal
}

// Ejemplo de uso después de guardar o editar
$("#saveSilo").click(function () {
    var numeroSilo = $("#numeroSilo").val().trim();
    var capacidadSilo = $("#capacidadSilo").val().trim();
    var productoId = $("#productoSilo").val();
    var plantaId = $("#plantaSilo").val();
    var siloId = $("#siloId").val(); // En caso de edición, obtener el ID del silo

    // Validar que los campos no estén vacíos
    if (!numeroSilo || !capacidadSilo || !productoId || !plantaId) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Todos los campos son obligatorios",
        });
        return;
    }

    var url = siloId ? `/catalogos/silos/update/${siloId}/` : "/catalogos/silos/create/";
    var method = siloId ? "POST" : "POST";

    var data = {
        numero: numeroSilo,
        capacidad: capacidadSilo,
        producto_id: productoId,
        planta_id: plantaId
    };

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (response) {
            closeModal(); // Cierra el modal al guardar con éxito
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Silo guardado con éxito",
            });
        },
        error: function (xhr) {
            var errorMessage = "Error al guardar el silo";
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

// Evento al hacer clic en el botón de cancelar
$('#siloModal .btn-secondary').click(function () {
    closeModal(); // Cierra el modal cuando se cancela
});

// Función para cerrar el modal manualmente
function closeModal() {
    $('#siloModal').modal('hide');
}

// Ejemplo de uso al hacer clic en el botón de cerrar
$('.close').click(function() {
    closeModal();
});


// Manejadores manuales para cerrar el modal
$("#productoModal .close, #productoModal .btn-secondary").click(function () {
    $("#productoModal").modal("hide");
});



    // Manejadores manuales para cerrar el modal
    $('#plantaModal .close, #plantaModal .btn-secondary').click(function() {
        $('#plantaModal').modal('hide');
    });

        // Guardar planta (añadir o editar) con validación usando SweetAlert2
        $('#savePlanta').click(function() {
            var nombre = $('#nombre').val().trim();
            var ubicacion = $('#ubicacion').val().trim();
            var correo = $('#correo').val().trim();
            var contacto = $('#contacto').val().trim();
            var telefono = $('#telefono').val().trim();
    
            // Validar que los campos no estén vacíos
            if (!nombre || !ubicacion || !correo || !contacto || !telefono) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Todos los campos son obligatorios',
                });
                return;
            }
    
            var plantaId = $('#plantaId').val();
            var url = plantaId ? `/catalogos/plantas/update/${plantaId}/` : '/catalogos/plantas/create/';
            var method = 'POST';
    
            $.ajax({
                url: url,
                method: method,
                data: $('#plantaForm').serialize(),
                success: function(response) {
                    $('#plantaModal').modal('hide');
                    table.ajax.reload();
                    Swal.fire({
                        icon: 'success',
                        title: 'Guardado',
                        text: 'Planta guardada con éxito',
                    });
                },
                error: function(xhr) {
                    var errorMessage = 'Error al guardar la planta';
                    if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error) {
                        errorMessage = xhr.responseJSON.error;
                    }
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: errorMessage,
                    });
                }
            });
        });

        // Manejador para el botón "Cancelar" del modal de tipo de producto
$("#tipoProductoModal .btn-secondary").click(function () {
    // Cierra el modal actual
    $("#tipoProductoModal").modal("hide");

    // Abre el modal anterior, por ejemplo, el modal de productos
    $("#productoModal").modal("show");
});

});