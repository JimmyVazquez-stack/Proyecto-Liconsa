$(document).ready(function() {
    loadTipoProductos();

});


function loadTipoProductos(callback) {
    $.ajax({
        url: "/api/api/tipos_productos/",  // Cambia esta URL a la de tu API
        method: "GET",
        success: function(data) {
            var $tipoProductoSelect = $("#producto_id");
            var $message = $("#tipoProductoMessage");

            $tipoProductoSelect.empty();
            if (data.length === 0) {
                $tipoProductoSelect.append('<option value="">No hay tipos de productos disponibles</option>');
                $message.text("No hay tipos de productos disponibles.").css("color", "red");
            } else {
                $tipoProductoSelect.append('<option value="">Seleccione un tipo de producto</option>');
                $.each(data, function(index, tipo) {
                    $tipoProductoSelect.append('<option value="' + tipo.id + '">' + tipo.nombre + '</option>');
                });
                $message.text("Seleccione un tipo de producto.").css("color", "black");
            }

            if (callback) {
                callback();
            }
        },
        error: function() {
            var $tipoProductoSelect = $("#producto_id");
            var $message = $("#tipoProductoMessage");

            $tipoProductoSelect.empty();
            $tipoProductoSelect.append('<option value="">Error al cargar los tipos de productos</option>');
            $message.text("Error al cargar los tipos de productos.").css("color", "red");
        }
    });
}
