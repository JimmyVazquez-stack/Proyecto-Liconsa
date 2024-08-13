$(document).ready(function() {
    // Obtener el token CSRF de las cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // Configurar jQuery para incluir el token CSRF en las solicitudes AJAX
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var table = $('#tabla_maquinas').DataTable({
        ajax: {
            url: '/catalogos/maquinas/list/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'numero' },
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
            }
        },
        columnDefs: [
            {
                targets: -1,
                orderable: false
            }
        ]
    });


// Cargar opciones de plantas en el modal de creación/edición de máquina
function loadPlantas(selectedPlantaId = null) {
    $.ajax({
        url: '/catalogos/plantas/list/data/',
        method: 'GET',
        success: function(response) {
            var plantaSelect = $('#planta');
            plantaSelect.empty();

            if (response.length > 0) {
                // Agregar opción por defecto solo si hay plantas disponibles
                plantaSelect.append(new Option('Seleccione una planta', ''));
                response.forEach(function(planta) {
                    var option = new Option(planta.nombre, planta.id);
                    if (planta.id == selectedPlantaId) {
                        option.selected = true;
                    }
                    plantaSelect.append(option);
                });
            } else {
                plantaSelect.append(new Option('No hay plantas disponibles', ''));
            }
        },
        error: function() {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Error al cargar las plantas.",
            });
        }
    });
}


// Abrir modal para añadir máquina
$("#btnAddMaquina").click(function() {
    $("#maquinaModalLabel").text("Añadir Máquina");
    $("#maquinaForm")[0].reset();
    $("#maquinaId").val("");
    loadPlantas(); // Cargar las plantas sin seleccionar ninguna por defecto

    // Mostrar el botón "Añadir Planta" en modo de creación
    $("#btnAddPlanta").show();

    $("#maquinaModal").modal("show");
});


// Cargar datos en el modal para editar
$('#tabla_maquinas tbody').on('click', '.btn-edit', function() {
    var data = table.row($(this).parents('tr')).data();

    // Rellenar el formulario con los datos de la máquina
    $("#maquinaId").val(data.id);
    $("#numero").val(data.numero);

    // Cargar las plantas y seleccionar la planta actual
    loadPlantas(data.planta_id);

    // Cambiar el título del modal
    $("#maquinaModalLabel").text("Editar Máquina");

    // Ocultar el botón "Añadir Planta" en modo de edición
    $("#btnAddPlanta").hide();

    // Mostrar el modal
    $("#maquinaModal").modal("show");
});



// Abrir modal para añadir planta desde el modal de máquina
$("#btnAddPlanta").click(function() {
    $("#plantaModal").modal("show");
});

// Guardar planta con validación usando SweetAlert2
$("#savePlanta").click(function() {
    var nombre = $("#nombre").val().trim();
    var ubicacion = $("#ubicacion").val().trim();
    var correo = $("#correo").val().trim();
    var contacto = $("#contacto").val().trim();
    var telefono = $("#telefono").val().trim();

    // Validar que todos los campos no estén vacíos
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
        success: function(response) {
            // Añadir la nueva planta al dropdown
            var newOption = new Option(response.nombre, response.id, true, true);
            $("#nombre_planta").append(newOption).trigger("change");

            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Planta guardada con éxito",
            }).then(() => {
                // Cerrar solo el modal de añadir planta y mantener el modal de máquina abierto
                $("#plantaModal").modal("hide");
            });
        },
        error: function(xhr) {
            var errorMessage = "Error al guardar la planta";
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


// Guardar máquina (añadir o editar) con validación usando SweetAlert2
$("#saveMaquina").click(function() {
    var numero = $("#numero").val().trim();
    var planta = $("#planta").val();

    // Validar que los campos no estén vacíos
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
    var method = maquinaId ? "PUT" : "POST"; // Usamos PUT para editar y POST para crear

    $.ajax({
        url: url,
        method: method,
        data: $("#maquinaForm").serialize(),
        success: function(response) {
            $("#maquinaModal").modal("hide");
            table.ajax.reload();
            Swal.fire({
                icon: "success",
                title: "Guardado",
                text: "Máquina guardada con éxito",
            });
        },
        error: function(xhr) {
            var errorMessage = "Error al guardar la máquina";
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

// Cargar datos en el modal para editar
$('#tabla_maquinas tbody').on('click', '.btn-edit', function() {
    var data = table.row($(this).parents('tr')).data();

    // Rellenar el formulario con los datos de la máquina
    $("#maquinaId").val(data.id);
    $("#numero").val(data.numero);
    $("#planta").val(data.planta_id); // Asegúrate de que el valor del select coincida con el ID de la planta

    // Cambiar el título del modal
    $("#maquinaModalLabel").text("Editar Máquina");

    // Mostrar el modal
    $("#maquinaModal").modal("show");
});


   // Manejador para cerrar el modal al hacer clic en "Cancelar"
   $("#plantaModal").find(".btn-secondary").click(function() {
    $("#plantaModal").modal("hide");
});

// Manejador para cerrar el modal al hacer clic en la "X"
$("#plantaModal").find(".close").click(function() {
    $("#plantaModal").modal("hide");
});

    // Manejador para cerrar el modal al hacer clic en "Cancelar"
    $("#maquinaModal").find(".btn-secondary").click(function() {
        $("#maquinaModal").modal("hide");
    });

    // Manejador para cerrar el modal al hacer clic en la "X"
    $("#maquinaModal").find(".close").click(function() {
        $("#maquinaModal").modal("hide");
    });

    // Confirmar eliminación usando SweetAlert2
$('#tabla_maquinas tbody').on('click', '.btn-delete', function() {
    var data = table.row($(this).parents('tr')).data();
    var maquinaId = data ? data.id : null; // Obtener el ID de la máquina desde los datos de la fila

    if (!maquinaId) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener el ID de la máquina.',
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
                url: `/catalogos/maquinas/delete/${maquinaId}/`,
                method: 'DELETE',
                success: function(response) {
                    table.ajax.reload();
                    Swal.fire(
                        'Eliminado!',
                        'La máquina ha sido eliminada.',
                        'success'
                    );
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Error al eliminar la máquina',
                    });
                }
            });
        }
    });
});




});
    