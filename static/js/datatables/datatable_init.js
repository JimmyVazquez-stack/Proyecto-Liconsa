


$(document).ready(function() {
    $('#rotos').DataTable({
        ajax: {
<<<<<<< HEAD
            url: '/catalogos/lecherias/list/data/',
=======
>>>>>>> 028cbab0fb47dbe932537953c429f277cddd49a7
            url: '/producto_no_conforme/lecherias/data/',
            dataSrc: ''
        },
        dom : "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6 text-right'f>>" +
              "<'row'<'col-sm-12'tr>>" +
              "<'row'<'col-sm-12 col-md-6'i><'col-sm-12 col-md-6 text-right'B>>" +
              "<'row'<'col-sm-12'p>>",
        columns: [
            { data: 'numero_ruta' },
            { data: 'numero' },
            { data: 'nombre' },
            { data: 'responsable' },
            { data: 'telefono' },
            { data: 'direccion' },
            { data: 'nombre_poblacion' },
            { data: 'rotos_reportados' },
        ],
<<<<<<< HEAD

=======
>>>>>>> 028cbab0fb47dbe932537953c429f277cddd49a7
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
                defaultContent: "", 
            }
        ],
<<<<<<< HEAD
        buttons: [
            {
                extend: 'pdf',
                className: 'btn btn-success',
                text: 'Generar PDF'
            }
        ],
=======
>>>>>>> 028cbab0fb47dbe932537953c429f277cddd49a7
    });
});


    $(document).ready(function() {
        $('#example').DataTable({
            pageLength: 5,
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "Todo"]],
            headers: {
                'X-CSRFToken': csrftoken
            },
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
                        defaultContent: "<div style='display: flex; justify-content: space-between;'><button class='btn btn-secondary' style='font-size: 14px; width:75px;'><i class='fas fa-pencil'></i></button><button class='btn btn-danger' style='font-size: 14px; width: 75px;' ><i class='fas fa-trash'></i></button></div>",                 
                        orderable: false
                    }
                ]
                
        });
    });

    
    $(document).ready(function() {
        $('#crear_rotos').DataTable({
            ajax: {
                url: '/producto_no_conforme/lecherias/data',
                dataSrc: ''
            },
            
            columns: [
                { data: 'numero_ruta' },
                { data: 'numero' },
                { data: 'nombre' },
                { data: 'responsable' },
                { data: 'telefono' },
                { data: 'direccion' },
                { data: 'municipio' },
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
<<<<<<< HEAD

=======
$(document).ready(function(){
    $('#rotos1').DataTable ({
        
        ajax: {
            url: '/producto_no_conforme/lecherias/data/',
            dataSrc: ''
        },
        info: false,
        ordering: false,
        paging: false
    });
});
>>>>>>> 028cbab0fb47dbe932537953c429f277cddd49a7
