// static/js/datatables-config.js

$(document).ready(function() {
    // Configurar DataTables para cada tabla
    $('#tablaPesoBruto').DataTable({
        "pageLength": 10, // Mostrar 10 registros por página
        "responsive": true, // Hacer la tabla responsiva
        "lengthChange": true, // Mostrar opciones de cantidad de registros
        "searching": true, // Habilitar la búsqueda
        "ordering": true, // Habilitar la ordenación de columnas
        "info": true, // Mostrar la información sobre los registros
        "autoWidth": false, // Deshabilitar ajuste automático de ancho
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json" // Traducción al español (opcional)
        }
    });

    // Repetir la configuración para las otras tablas
    $('#tablaDensidad').DataTable({
        "pageLength": 10,
        "responsive": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
    });

    $('#tablaPesoEnvVacio').DataTable({
        "pageLength": 10,
        "responsive": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
    });
});
