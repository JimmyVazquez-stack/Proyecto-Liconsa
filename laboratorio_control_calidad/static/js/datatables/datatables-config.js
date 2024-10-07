// static/js/datatables-config.js

$(document).ready(function() {

    // Función para obtener el título basado en la pestaña activa
    function getActiveTabTitle() {
        // Obtiene la pestaña activa
        var activeTab = $('.nav-tabs .nav-link.active').text();
        // Retorna el título basado en la pestaña activa
        return activeTab.trim(); // Limpia espacios en blanco
    }

    // Configurar DataTables para cada tabla
    var tablaPesoBruto = $('#tablaPesoBruto').DataTable({
        "pageLength": 10,
        "responsive": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "dom": 'Bfrtip',
        "buttons": [
            {
                extend: 'copy',
                text: '<i class="bi bi-clipboard-fill"></i>',
                titleAttr: 'Copiar',
                className: 'btn btn-secondary',
                title: function() { return getActiveTabTitle(); } // Título basado en la pestaña activa
            },
            {
                extend: 'excel',
                text: '<i class="bi bi-file-earmark-spreadsheet"></i>',
                titleAttr: 'Exportar a excel',
                className: 'btn btn-success',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)' // Excluir la última columna
                }
            },
            {
                extend: 'pdf',
                text: '<i class="bi bi-file-earmark-pdf"></i>',
                titleAttr: 'Exportar a pdf',
                className: 'btn btn-danger',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)' // Excluir la última columna
                }
            },
            {
                extend: 'print',
                text: '<i class="bi bi-printer"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-secondary',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)' // Excluir la última columna
                }
            },
        ]
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
        "dom": 'Bfrtip',
        "buttons": [
            {
                extend: 'copy',
                text: '<i class="bi bi-clipboard-fill"></i>',
                titleAttr: 'Copiar',
                className: 'btn btn-secondary',
                title: function() { return getActiveTabTitle(); } // Título basado en la pestaña activa
            },
            {
                extend: 'excel',
                text: '<i class="bi bi-file-earmark-spreadsheet"></i>',
                titleAttr: 'Exportar a excel',
                className: 'btn btn-success',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            },
            {
                extend: 'pdf',
                text: '<i class="bi bi-file-earmark-pdf"></i>',
                titleAttr: 'Exportar a pdf',
                className: 'btn btn-danger',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            },
            {
                extend: 'print',
                text: '<i class="bi bi-printer"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-secondary',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            },
        ]
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
        "dom": 'Bfrtip',
        "buttons": [
            {
                extend: 'copy',
                text: '<i class="bi bi-clipboard-fill"></i>',
                titleAttr: 'Copiar',
                className: 'btn btn-secondary',
                title: function() { return getActiveTabTitle(); } // Título basado en la pestaña activa
            },
            {
                extend: 'excel',
                text: '<i class="bi bi-file-earmark-spreadsheet"></i>',
                titleAttr: 'Exportar a excel',
                className: 'btn btn-success',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            },
            {
                extend: 'pdf',
                text: '<i class="bi bi-file-earmark-pdf"></i>',
                titleAttr: 'Exportar a pdf',
                className: 'btn btn-danger',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            },
            {
                extend: 'print',
                text: '<i class="bi bi-printer"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-secondary',
                title: function() { return getActiveTabTitle(); }, // Título basado en la pestaña activa
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            },
        ]
    });

    // Inicializar los botones
    tablaPesoEnvVacio.buttons().container().appendTo('#tablaPesoEnvVacio_wrapper .col-md-6:eq(0)');
});
