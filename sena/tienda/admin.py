from django.contrib import admin
from django.utils.html import mark_safe
from .models import *




# Register your models here.


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre_completo", "nick", "rol", "verfoto", "password"]

    def nombre_completo(self, obj):
        return mark_safe(f"{obj.nombre} {obj.apellido}")

    def verfoto(self, obj):
        try:
            return mark_safe(f"<img src='{obj.foto.url}' width='10%'>")
        except Exception as e:
            return f"Error, el archivo fue eliminado."

class ServicioAdmin(admin.ModelAdmin):
    list_display = ["id","nombre", "precio" , "descripcion"]

    def nombre(self, obj):
        return mark_safe(f"{obj.nombre}") 
    
    def precio(self, obj):
        return mark_safe(f"{obj.precio}") 

    def descripcion(self, obj):
        return mark_safe(f"{obj.descripcion}") 
    


class PadreAdmin(admin.ModelAdmin):
    list_display = ["id","nombre","fecha_nacimiento","email","telefono","direccion","descripcion" ]
    

    def nombre(self, obj):
        return mark_safe(f"{obj.nombre}") 

    def fecha_nacimiento(self, obj):
        return mark_safe(f"{obj.fecha_nacimiento}") 

    def email(self, obj):
        return mark_safe(f"{obj.email}") 

    def telefono(self, obj):
        return mark_safe(f"{obj.telefono}") 

    def direccion(self, obj):
        return mark_safe(f"{obj.direccion}") 

    def descripcion(self, obj):
        return mark_safe(f"{obj.descripcion}") 


class NinoabueloAdmin(admin.ModelAdmin):
    list_display = ["id","nombre","fecha_nacimiento","numero_identificacion","descripcion"]

    def nombre(self, obj):
        return mark_safe(f"{obj.nombre}") 
    

    def fecha_nacimiento(self, obj):
        return mark_safe(f"{obj.fecha_nacimiento}") 
    

    def numero_identificacion(self, obj):
        return mark_safe(f"{obj.numero_identificacion}") 
    

    def descripcion(self, obj):
        return mark_safe(f"{obj.descripcion}") 
    

class PagoAdmin(admin.ModelAdmin):

    list_display = ["monto","fecha_pago","metodo_pago","descripcion"]


    def monto(self, obj):
        return mark_safe(f"{obj.monto}") 
    
    def fecha_pago(self, obj):
        return mark_safe(f"{obj.fecha_pago}") 

    def metodo_pago(self, obj):
        return mark_safe(f"{obj.metodo_pago}") 

    def descripcion(self, obj):
        return mark_safe(f"{obj.descripcion}") 
    


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Padre, PadreAdmin)
admin.site.register(Ninoabuelo , NinoabueloAdmin)
admin.site.register(Pago, PagoAdmin)

















