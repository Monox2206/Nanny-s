from django.urls import path

from . import views

app_name = "tienda"

urlpatterns = [
    path("inicio/<str:abrir_off_canvas>/", views.index, name="index"),
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    path("listar_categorias/", views.categorias, name="listar_categorias"),
    path("form_cat/", views.categorias_crear_formulario, name="form_cat"),
    path("categorias_guardar/", views.categorias_guardar, name="categorias_guardar"),
    path("form_edit_cat/<int:id>/", views.categorias_editar_formulario, name="form_edit_cat"),
    path("categorias_eliminar/<int:id>/", views.categorias_eliminar, name="categorias_eliminar"),
    path("cat_buscar/", views.cat_buscar, name="cat_buscar"),

    path("productos/", views.productos, name="productos"),
    path("form_pro/", views.productos_formulario, name="form_pro"),
    path("productos_guardar/", views.productos_guardar, name="productos_guardar"),
    path("productos_eliminar/<int:id>/", views.productos_eliminar, name="productos_eliminar"),
    path("form_edit_pro/<int:id>/", views.productos_editar_formulario, name="form_edit_pro"),
    path("pro_buscar/", views.pro_buscar, name="pro_buscar"),

    path("cambiar_clave/<str:actual>", views.cambiar_clave, name="cambiar_clave"),
    path("guarda_clave/", views.guarda_clave, name="guarda_clave"),
    path("perfil/", views.ver_perfil, name="perfil"),

    # Carrito de compra...
    path("carrito_agregar/", views.carrito_agregar, name="carrito_agregar"),
    path("carrito_listar/", views.carrito_listar, name="carrito_listar"),
    path("carrito_eliminar_producto/<int:id>", views.carrito_eliminar_producto, name="carrito_eliminar_producto"),
    path("carrito_actualizar/", views.carrito_actualizar, name="carrito_actualizar"),

    path("establecer_venta/", views.establecer_venta, name="establecer_venta"),

]
