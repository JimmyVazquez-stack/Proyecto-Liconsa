$(document).ready(function(){
$('#listar_usuarios').DataTable({
        ajax: {
            url: '/usuarios/data/',
            dataSrc: ''
        },
        columns: [
            { data: 'username' },
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'telefono' },
            { data: 'area' },
            { data: 'grupo' },
            {
                data: null,
                defaultContent: `
                    <button class="btn btn-edit"><i class="fas fa-pencil-alt text-gray"></i></button>
                    <button class="btn btn-delete"><i class="fas fa-trash text-red"></i></button>
                `
            }
        ],
    });
});