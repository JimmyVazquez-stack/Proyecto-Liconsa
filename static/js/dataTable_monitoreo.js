let dataTable;
let dataTableIsIintialized = false;

const dataTableOptions = {
    // scrollX:"2000px", //Habilitar scroll horizontal
    lengthMenu: [3, 5, 10, 25, 50, 75, 100], //Cantidad de registros por página
    columnDefs: [
        {className: 'centered', targets: [0, 1, 2, 3, 4,5,6]}, //Centrar contenido de las columnas
        {orderable: false, targets: [5, 6]},
        {"width": "5%", "targets": [0]},], //Ancho de las columnas en este caso la columna con índice 0
    pageLength: 3,
    destroy: true,
    language: {
        lengthMenu: 'Mostrar _MENU_ registros por página', // Mostrar _MENU_ registros por página
        zeroRecords: 'No se encontraron resultados',
        info: 'Mostrando de _START_ a _END_ de _TOTAL_ registros',
        infoEmpty: 'No hay registros',
        infoFiltered: '(filtrado de _MAX_ registros totales)',
        search: 'Buscar:',
        laodingRecords: 'Cargando...',
        paginate:{
            first: 'Primero',
            last: 'Último',
            next: 'Siguiente',
            previous: 'Anterior'
        }
    },
};

const initDatatable = async() => {
    if (dataTableIsIintialized) {
        dataTable.destroy();
    }
    await listUsers();
    dataTable=$("#datatable_users").DataTable(dataTableOptions);
    dataTableIsIintialized = true;
};

const listUsers = async () => {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users');
        const users = await response.json();
        let = content = '';
        users.forEach((user, index) => {
            content += `
            <tr>
                <td>${index + 1}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.address.city}</td>
                <td>${user.company.name}</td>
                <td><i class="fa-solid fa-check" style="color: green;"></i></td>
                <td>
                <button class="btn btn-sm btn primary"><i class="fa-solid fa-pencil"></i></button>
                <button class="btn btn-sm btn danger"><i class="fa-solid fa-trash"></i></button>
                </td>
            </tr>`;
        });
        tableBody_users.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};
window.addEventListener('load', async () => {
    await initDatatable();
});