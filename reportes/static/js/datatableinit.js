$(document).ready(function() {
    $('#rotos1').DataTable ({
        
        ajax: {
            url: '/producto_no_conforme/lecherias/data/',
            dataSrc: ''
        },
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
        info: false,
        ordering: false,
        paging: false,
        searching: false
    });
    $('#rotos2').DataTable ({
        
        ajax: {
            url: '/producto_no_conforme/lecherias/data/',
            dataSrc: ''
        },
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
        info: false,
        ordering: false,
        paging: false,
        searching: false
    });
    // Repite para cada DataTable que quieras mostrar
});