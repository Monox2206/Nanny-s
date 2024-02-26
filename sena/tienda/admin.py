from django.contrib import admin
from django.utils.html import mark_safe

# Register your models here.
from .models import *


class ProductoAdmin(admin.ModelAdmin):
    fields = ["categoria", "nombre", "precio", "fecha_compra", "stock", "foto"]
    list_display = ["id", "categoria", "nombre", "precio", "fecha_compra", "stock", "foto_producto"]
    search_fields = ["nombre", "categoria__nombre", "categoria__descripcion"]
    list_filter = ["categoria", "fecha_compra"]
    # list_editable = ["nombre", "categoria"]

    def foto_producto(self, obj):
        try:
            return mark_safe(f"<img src='{obj.foto.url}' width='20%'>")
        except Exception as e:
            return f"Error, el archivo fue eliminado."

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "descripcion"]
    search_fields = ["nombre", "descripcion"]


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre_completo", "nick", "sueldo", "rol", "verfoto", "passwd"]

    def sueldo(self, obj):
        return f"${obj.id*3}"

    def nombre_completo(self, obj):
        return mark_safe(f"<span style='color:red;'>{obj.nombre}</span> {obj.apellido}")

    def verfoto(self, obj):
        try:
            return mark_safe(f"<img src='{obj.foto.url}' width='10%'>")
        except Exception as e:
            return f"Error, el archivo fue eliminado."


class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_venta', 'usuario']


class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'producto', 'cantidad', 'precio_historico', 'subtotal']

    def subtotal(self, obj):
        return f"{obj.cantidad * obj.precio_historico}"


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)
