
$(document).ready(function() {
    $('#catalogo_lecherias').DataTable({
        ajax: {
            url: '/catalogos/lecherias/list/data/',
            dataSrc: ''
        },
        
        columns: [
            { data: 'numero_ruta' },
            { data: 'numero' },
            { data: 'nombre' },
            { data: 'responsable' },
            { data: 'telefono' },
            { data: 'direccion' },
            { data: 'numero_ruta' },
            { data: 'nombre_poblacion' },
            { data: 'rotos_reportados' },
            {
                data: null,
                defaultContent: `
                    <button class="btn btn-edit"><i class="fas fa-pencil-alt text-gray"></i></button>
                    <button class="btn btn-delete"><i class="fas fa-trash text-red"></i></button>
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