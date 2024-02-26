function confirmar_eliminar(url){
    if(confirm("Está seguro de eliminar el registro?")){
        location.href = url;
    }
}


function ver_carrito(url_django){
    $.ajax({
      url: url_django
    })
    .fail(function( result ) {
        alert( "Error: " + result );
    })
    .done(function( result ) {
        cuerpo = $('#respuesta_carrito');
        // Sobre-escribir el contenido del offcanvas
        cuerpo.html(result)

        // Mostrar el offcanvas
        const myOffcanvas = $('#offcanvasRight');
        myOffcanvas.offcanvas('toggle');
    });

}

$( document ).ready(function() {
    console.log( "ready!" );
    // abrir off canvas en caso especial después de agregar producto
    var pathname = window.location.pathname;
    pathname = pathname.split("/")
    if (pathname[2] == "si"){
        ver_carrito("/carrito_listar/")
    }
});


function actualizar_totales(id, cantidad, precio){
    //console.log(`Id producto ${id} - Cantidad ${cantidad} - Precio ${precio}`)

    id_subtotal = document.getElementById("subtotal_"+id)
    total_carrito = document.getElementById("total_carrito")

    id_subtotal.innerHTML = "$"+ (cantidad * precio).toLocaleString()

    precios = document.getElementsByName("precios")
    cantidades = document.getElementsByName("cantidades")

    total = 0
    for (obj=0; obj < precios.length; obj++){
        total = total + (precios[obj].value * cantidades[obj].value);
    }

    total_carrito.innerHTML = total.toLocaleString()
}

function actualizar_carrito(url_django, id, cantidad){
    console.log(`Id producto ${id} - Cantidad ${cantidad}`)
    loader = $('#loading_cc');
    loader.removeClass("d-none");
    loader.addClass("d-block");

    $.ajax({
      url: url_django,
      method: "GET",
      data: { "id": id, "cantidad": cantidad }
    })
    .fail(function( result ) {
        alert( "Error: " + result );
        loader.removeClass("d-block");
        loader.addClass("d-none");
    })
    .done(function( result ) {
        loader.removeClass("d-block");
        loader.addClass("d-none");
    });

}