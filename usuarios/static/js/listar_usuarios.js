document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('cargarUsuarios').addEventListener('click', function() {
        fetch('usuarios:listar_usuarios')  // Asegúrate de reemplazar esto con la URL correcta
            .then(response => response.json())
            .then(data => {
                const lista = document.getElementById('listaUsuarios');
                lista.innerHTML = '';  // Limpiar la lista actual
                data.data.forEach(usuario => {
                    const elemento = document.createElement('div');
                    elemento.textContent = `ID: ${usuario.id}, Nombre: ${usuario.nombre}, Email: ${usuario.email}`;
                    lista.appendChild(elemento);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});