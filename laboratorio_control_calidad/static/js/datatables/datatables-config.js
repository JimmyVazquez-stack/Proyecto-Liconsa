// static/js/datatables-config.js

$(document).ready(function() {
    // Configurar DataTables para cada tabla
    var tablaPesoBruto = $('#tablaPesoBruto').DataTable({
        "pageLength": 10, // Mostrar 10 registros por página
        "responsive": true, // Hacer la tabla responsiva
        "lengthChange": true, // Mostrar opciones de cantidad de registros
        "searching": true, // Habilitar la búsqueda
        "ordering": true, // Habilitar la ordenación de columnas
        "info": true, // Mostrar la información sobre los registros
        "autoWidth": false, // Deshabilitar ajuste automático de ancho
        "dom": 'Bfrtip', // Integrar botones con la tabla
        "buttons":{
            "buttons":[
                {
                    extend:'copy',
                    text:'<i class="bi bi-clipboard-fill"></i>',
                    tittleAttr:'Copiar',
                    className:'btn btn-secondary'
                },
                {
                    extend:'excel',
                    text:'<i class="bi bi-file-earmark-spreadsheet"></i>',
                    tittleAttr:'Exportar a excel',
                    className:'btn btn-success'
                },
                {
                    extend:'pdf',
                    text:'<i class="bi bi-file-earmark-pdf"></i>',
                    tittleAttr:'Exportar a pdf',
                    className:'btn btn-secondary'
                },
                {
                    extend:'print',
                    text:'<i class="bi bi-printer"></i>',
                    tittleAttr:'Imprimir',
                    className:'btn btn-secondary'
                },
                {
                    extend:'colvis',
                    text:'Filtrar columnas'
                },
                

            ]
        },
        /*"buttons": [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],*/
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json" // Traducción al español (opcional)
        }
    });
    // Inicializar los botones
    tablaPesoBruto.buttons().container().appendTo('#tablaPesoBruto_wrapper .col-md-6:eq(0)');

    // Repetir la configuración para las otras tablas
    var tablaDensidad = $('#tablaDensidad').DataTable({
        "pageLength": 10,
        "responsive": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "dom": 'Bfrtip', // Integrar botones con la tabla
        "buttons": [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
    });
    // Inicializar los botones
    tablaDensidad.buttons().container().appendTo('#tablaDensidad_wrapper .col-md-6:eq(0)');

    var tablaPesoEnvVacio = $('#tablaPesoEnvVacio').DataTable({
        "pageLength": 10,
        "responsive": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "dom": 'Bfrtip', // Integrar botones con la tabla
        "buttons": [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
    });
    // Inicializar los botones
    tablaPesoEnvVacio.buttons().container().appendTo('#tablaPesoEnvVacio_wrapper .col-md-6:eq(0)');
});
