
$(document).ready(function() {
    $('#tabla_proveedores').DataTable({
        ajax: {
            url: '/catalogos/proveedores/list/data/',
            dataSrc: ''
        },
        
        columns: [
            { data: 'nombre' },
            { data: 'contacto' },
            { data: 'telefono' },
            { data: 'correo' },
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
});