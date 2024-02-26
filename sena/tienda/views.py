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
		clave = request.POST.get("passwd")

		try:
			q = Usuario.objects.get(nick=usuario, passwd=clave)
			messages.success(request, "Bienvenido!!")
			# guardar nombre del rol y no su número...
			datos = {
				"rol": q.rol,
				"nombre_rol": q.get_rol_display(),
				"nombre": f"{q.nombre} {q.apellido}",
				"foto": q.foto.url if q.foto else "/media/fotos/default.png",
				"id": q.id
			}
			request.session["logueo"] = datos
			# variables del carrito de compra
			request.session["carrito"] = []
			request.session["cantidad_productos"] = 0
			# fin - variables del carrito de compra
			return HttpResponseRedirect(reverse("tienda:index", args=('no',)))

		except Usuario.DoesNotExist:
			messages.error(request, "Usuario o contraseña no válidos...")
			return render(request, "tienda/login.html")
	else:
		if request.session.get("logueo", False):
			return HttpResponseRedirect(reverse("tienda:index", args=('no',)))
		else:
			return render(request, "tienda/login.html")


def logout(request):
	try:
		del request.session["logueo"]
		del request.session["carrito"]
		del request.session["cantidad_productos"]
		messages.success(request, "Sesión cerrada correctamente!")
	except Exception as e:
		messages.error(request, f"Error: {e}")
	return HttpResponseRedirect(reverse("tienda:login"))


def index(request, abrir_off_canvas="no"):
	if abrir_off_canvas == "si":
		print("SI")
	else:
		print("NO")

	if request.session.get("logueo", False):
		c = Categoria.objects.all()

		# Detectar si viene paramétro id categoría para filtrar o no...
		filtro_categoria = request.GET.get("id")

		if filtro_categoria != None and filtro_categoria != '0':
			p = Producto.objects.filter(categoria_id = filtro_categoria)
			request.session["submenu"] = int(filtro_categoria)
		else:
			p = Producto.objects.all()
			request.session["submenu"] = 0

		contexto = {"categorias": c, "productos": p}
		return render(request, "tienda/index.html", contexto)
	else:
		return HttpResponseRedirect(reverse("tienda:login"))


def categorias(request):
	sesion = request.session.get("logueo", False)

	if sesion["nombre_rol"] != "Usuario":
		result = Categoria.objects.all()
		context = {"data": result}
		return render(request, "tienda/categorias/listar.html", context)
	else:
		messages.warning(request, "Usted no tiene permiso para acceder...")
		return HttpResponseRedirect(reverse("tienda:index", args=('no',)))

def categorias_crear_formulario(request):
	return render(request, "tienda/categorias/cat-form.html")


def categorias_guardar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")

		if id == "":
			# crear
			try:
				cat = Categoria(
					nombre=nomb,
					descripcion=desc
				)
				cat.save()
				messages.success(request, "Guardado correctamente!!")
			except Exception as e:
				messages.error(request, f"Error. {e}")
		else:
			# actualizar
			try:
				q = Categoria.objects.get(pk=id)
				q.nombre = nomb
				q.descripcion = desc
				q.save()
				messages.success(request, "Actualizado correctamente!!")
			except Exception as e:
				messages.error(request, f"Error. {e}")

		return HttpResponseRedirect(reverse("tienda:listar_categorias", args=()))
	else:
		messages.warning(request, "No se enviaron datos...")
		return HttpResponseRedirect(reverse("tienda:form_cat", args=()))


def categorias_editar_formulario(request, id):
	q = Categoria.objects.get(pk=id)
	contexto = {"id": id, "data": q}
	return render(request, "tienda/categorias/cat-form.html", contexto)


def categorias_eliminar(request, id):
	try:
		q = Categoria.objects.get(pk=id)
		q.delete()
		messages.success(request, "Registro eliminado correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return HttpResponseRedirect(reverse("tienda:listar_categorias", args=()))


def cat_buscar(request):
	if request.method == "POST":

		buscar = request.POST.get("buscar")

		query = Categoria.objects.filter(
			Q(nombre__istartswith=buscar) |
			Q(descripcion__istartswith=buscar)
		)
		context = {"data": query, "buscado": buscar}
		return render(request, "tienda/categorias/listar.html", context)
	else:
		messages.warning(request, "No se enviaron datos...")
	return HttpResponseRedirect(reverse("tienda:listar_categorias", args=()))


def productos(request):
	registros = Producto.objects.all()
	contexto = {"data": registros}
	return render(request, "tienda/productos/listar.html", contexto)

def productos_formulario(request):
	query = Categoria.objects.all()
	contexto = {"categorias": query}
	return render(request, "tienda/productos/pro-form.html", contexto)

def productos_guardar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		precio = request.POST.get("precio")
		fecha_c = request.POST.get("fecha_compra")

		# foráneas, deben ser instancias de su clase
		cat = Categoria.objects.get(pk=request.POST.get("categoria"))

		if id == "":
			# crear
			try:
				pro = Producto(
					nombre=nomb,
					precio=precio,
					fecha_compra=fecha_c,
					categoria=cat
				)
				pro.save()
				messages.success(request, "Guardado correctamente!!")
			except Exception as e:
				messages.error(request, f"Error. {e}")
		else:
			# actualizar
			try:
				q = Producto.objects.get(pk=id)
				q.nombre = nomb
				q.precio = precio
				q.fecha_compra = fecha_c
				q.categoria = cat
				q.save()
				messages.success(request, "Actualizado correctamente!!")
			except Exception as e:
				messages.error(request, f"Error. {e}")

		return HttpResponseRedirect(reverse("tienda:productos", args=()))
	else:
		messages.warning(request, "No se enviaron datos...")
		return HttpResponseRedirect(reverse("tienda:form_pro", args=()))


def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Registro eliminado correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return HttpResponseRedirect(reverse("tienda:productos", args=()))


def productos_editar_formulario(request, id):
	q = Producto.objects.get(pk=id)
	query = Categoria.objects.all()
	contexto = {"id": id, "data": q, "categorias": query}

	return render(request, "tienda/productos/pro-form.html", contexto)

def pro_buscar(request):
	if request.method == "POST":

		buscar = request.POST.get("buscar")

		query = Producto.objects.filter(nombre__icontains=buscar)

		context = {"data": query, "buscado": buscar}
		return render(request, "tienda/productos/listar.html", context)
	else:
		messages.warning(request, "No se enviaron datos...")
	return HttpResponseRedirect(reverse("tienda:productos", args=()))


def cambiar_clave(request, actual):
	contexto = {"actual": actual}
	return render(request, "tienda/usuarios/cambio_clave.html", contexto)


def guarda_clave(request):
	usuario = request.session.get("logueo", False)
	if usuario:
		if request.method == "POST":
			actual = request.POST.get("actual")
			clave1 = request.POST.get("clave1")
			clave2 = request.POST.get("clave2")
			try:
				q = Usuario.objects.get(pk=usuario["id"], passwd=actual)
				if clave1 == clave2:
					q.passwd = clave1
					q.save()
					messages.success(request, "Contraseña actualizada correctamente!!")
				else:
					messages.warning(request, "Nuevas Contraseñas no coinciden...")
			except Exception as e:
				messages.warning(request, f"Contraseña no válida.... {e}")
			return HttpResponseRedirect(reverse("tienda:cambiar_clave", kwargs={'actual': actual}))
	else:
		return HttpResponseRedirect(reverse("tienda:login"))


def ver_perfil(request):
	usuario = request.session.get("logueo", False)
	q = Usuario.objects.get(pk = usuario["id"])
	contexto = {"data": q}
	return render(request, "tienda/usuarios/perfil.html", contexto)


def carrito_agregar(request):
	if request.method == "POST":
		id_producto = request.POST.get("id")
		cantidad = int(request.POST.get("cantidad"))

		if not request.session.get("carrito", False):
			request.session["carrito"] = []
			request.session["cantidad_productos"] = 0

		carrito = request.session.get("carrito", False)

		# Buscar producto para obtener stock
		pro = Producto.objects.get(pk=id_producto)

		encontrado = False
		for p in carrito:
			if p["id"] == id_producto:
				encontrado = True
				# Sí existe y no supera el stock... incrementamos la cantidad
				if cantidad > 0 and (p["cantidad"] + cantidad) <= pro.stock:
					p["cantidad"] += cantidad
					messages.success(request, "Producto ya en carrito, se incrementa la cantidad!!")
				else:
					messages.warning(request, "La cantidad supera el stock del Producto....")
				break

		if not encontrado:
			# Si no existe y no supero el stock, agrego el elemento completo, es decir el diccionario
			if cantidad > 0 and cantidad <= pro.stock:
				carrito.append({"id": id_producto, "cantidad": cantidad})
				messages.success(request, "Producto agregado al carrito!!")
			else:
				messages.warning(request, "La cantidad supera el stock del Producto....")

		# Sobreescribo la sesión
		request.session["carrito"] = carrito
		request.session["cantidad_productos"] = len(request.session["carrito"])
	else:
		messages.warning(request, "No se enviaron datos...")

	return redirect("tienda:index", abrir_off_canvas='si')


def carrito_listar(request):
	carrito = request.session.get("carrito", False)
	if carrito is not False:
		total = 0
		for indice, p in enumerate(carrito):
			try:
				print(p)
				query = Producto.objects.get(pk=int(p["id"]))
				p["nombre"] = query.nombre
				p["precio"] = query.precio
				p["foto"] = query.foto.url
				p["stock"] = query.stock
				p["subtotal"] = p["cantidad"] * query.precio
				total += p["subtotal"]
			except Producto.DoesNotExist:
				print(f"No existe {p}")
				# Caso especial, se eliminó un producto de la DB, entonces elimino de carrito.
				carrito.pop(indice)
				request.session["carrito"] = carrito

	contexto = {"datos": carrito, "total": total}
	return render(request, "tienda/carrito/listar_carrito.html", contexto)


def carrito_eliminar_producto(request, id):
	if request.method == "GET":
		carrito = request.session.get("carrito", False)
		if carrito:
			if int(id) == 0:
				carrito.clear()
			else:
				encontrado = False
				cont = 0
				for p in carrito:
					if int(p["id"]) == id:
						encontrado = True
						# Sí existe, lo eliminamos
						carrito.remove(p)
						messages.success(request, "Producto eliminado!!")
						break
					cont += 1

			request.session["carrito"] = carrito
			request.session["cantidad_productos"] = len(request.session["carrito"])
		else:
			messages.warning(request, "Carrito vacío...")
	else:
		messages.warning(request, "No se enviaron datos...")

	return redirect("tienda:index", abrir_off_canvas='si')


def carrito_actualizar(request):
	if request.method == "GET":
		id_producto = request.GET.get("id")
		cantidad = int(request.GET.get("cantidad"))
		print(cantidad)
		# Capturo sesión
		carrito = request.session.get("carrito", False)
		# Buscar producto para obtener stock
		pro = Producto.objects.get(pk=id_producto)

		encontrado = False
		for p in carrito:
			if p["id"] == id_producto:
				encontrado = True
				# Sí existe y no supera el stock... incrementamos la cantidad
				if cantidad > 0 and cantidad <= pro.stock:
					print(f"nuevo valor: {cantidad}")
					p["cantidad"] = cantidad
				break

		print(carrito)
		# Sobreescribo la sesión
		request.session["carrito"] = carrito
		return HttpResponse("OK")
	else:
		messages.warning(request, "No se enviaron datos...")
		return HttpResponse("Error")


@transaction.atomic
def establecer_venta(request):
	# ========== transacción ================
	try:
		# Crear el encabezado de la venta

		logueo = request.session.get("logueo", False)

		user = Usuario.objects.get(pk=logueo["id"])

		query_venta = Venta(usuario=user)
		query_venta.save()

		# obtener ID inmediatamente
		id_venta = Venta.objects.latest('id')

		# Obtengo el objeto venta a través de su ID
		# v = Venta.objects.get(pk=id_venta)

		carrito = request.session.get("carrito", False)
		for p in carrito:
			# Obtengo el producto venta a través de su ID
			try:
				p_object = Producto.objects.get(pk=p["id"])
			except Producto.DoesNotExist:
				messages.error(request, f"El producto {p} ya no existe")
				raise Exception(f"No se pudo realizar la compra, El producto {p} ya no existe..")

			if p_object.stock >= p["cantidad"]:
				# Asociar los productos del carrito al ID de la venta, previamente creado.
				q = DetalleVenta(
					venta = id_venta,
					producto = p_object,
					cantidad = p["cantidad"],
					precio_historico = p_object.precio
				)
				q.save()
				# Disminuir stock de productos
				p_object.stock -= p["cantidad"]
				p_object.save()
			else:
				messages.warning(request, f"El producto {p_object} no cuenta con suficientes unidades. sólo tiene {p_object.stock}")
				raise ValueError(f"El producto {p_object} no cuenta con suficientes unidades. sólo tiene {p_object.stock}")

		# Vaciar carrito y redirigir a inicio
		carrito.clear()
		request.session["carrito"] = carrito
		request.session["cantidad_productos"] = 0

		messages.success(request, f"Muchas gracias por su compra << {id_venta} >>!!")

		return redirect("tienda:index", abrir_off_canvas='no')
		# ========== fin transacción si ok ===========
	except Exception as e:
		# ************* si ERROR **********
		transaction.set_rollback(True)
		# rollback
		messages.error(request, f"Occurrió un error, intente de nuevo. {e}")
		return redirect("tienda:index", abrir_off_canvas='no')
	# == fin ==================
