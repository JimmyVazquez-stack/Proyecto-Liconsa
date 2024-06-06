$(document).ready(function() {
    $('#rotos').DataTable({
        ajax: {
            url: '/producto_no_conforme/lecherias/data',
            dataSrc: ''
        },
        
        columns: [
            { data: 'numero' },
            { data: 'nombre' },
            { data: 'responsable' },
            { data: 'telefono' },
            { data: 'direccion' },
            { data: 'municipio' },
            { data: 'numero_ruta' },
            { data: 'opciones'},
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
                defaultContent: "<div style='display: flex; justify-content: space-between;'><button class='btn btn-secondary' style='font-size: 14px; width:75px;'><i class='fas fa-pencil'></i></button><button class='btn btn-danger' style='font-size: 14px; width: 75px;' ><i class='fas fa-trash'></i></button></div>",                 
                orderable: false
            }
        ]
    });
});


    $(document).ready(function() {
        $('#example').DataTable({
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
                        defaultContent: "<div style='display: flex; justify-content: space-between;'><button class='btn btn-secondary' style='font-size: 14px; width:75px;'><i class='fas fa-pencil'></i></button><button class='btn btn-danger' style='font-size: 14px; width: 75px;' ><i class='fas fa-trash'></i></button></div>",                 
                        orderable: false
                    }
                ]
                
        });
    });

    