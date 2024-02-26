from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.db import IntegrityError, transaction

from django.db.models import Q

from django.contrib import messages

from .models import *

# Create your views here.

def login(request):
    if request.method == "POST":
        usuario = request.POST.get("nick")
        clave = request.POST.get("password")

        try:
            q = Usuario.objects.get(nick=usuario, password=clave)
            messages.success(request, "Bienvenido!!")
            # Guardar nombre del rol  y no su número
            datos = {
                "rol": q.rol,
                "nombre_rol": q.get_rol_display(),
                "nombre": f"{q.nombre} {q.apellido}",
				"foto": q.foto.url,
                "id": q.id

            }
            request.session["logueo"] = datos

            return render(request, "tienda/index.html")

        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña no válidos..")

            return render(request, "login.html")
    else:

        if request.session.get("logueo", False):
            return render(request, "tienda/index.html")
        else:
            return render(request, "login.html")
        


def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente!")
    except Exception as e:
        messages.error(request, f"Error: {e} ")
    return HttpResponseRedirect(reverse("login"))


def home(request):
    return render(request,"tienda/index.html")

