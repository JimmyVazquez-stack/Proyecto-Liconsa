$(document).ready(function() {
    $('#rotos').DataTable({
        ajax: {
            url: '/catalogos/lecherias/list/data/',
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
        buttons: [
            {
                extend: 'pdf',
                className: 'btn btn-success',
                text: 'Generar PDF'
            }
        ],
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


// pdf
document.getElementById('btn-exportar-pdf').addEventListener('click', function() {
    var doc = new jsPDF();
    doc.addImage('static/img/AdminLTELogo.png', 'PNG', 15, 40, 180, 160);
    var table = $('#rotos').DataTable();
    var data = table.buttons.exportData();

    doc.autoTable({
        head: data.header,
        body: data.body,
        foot: data.footer,
        styles: { fillColor: [255, 255, 255] },
        columnStyles: {
            0: { fillColor: [255, 255, 255] },
        },
    });

    doc.save('rotos.pdf');
});