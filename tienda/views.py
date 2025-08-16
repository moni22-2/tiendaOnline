from django.shortcuts import render
from rest_framework import status
from decimal import Decimal
from .models import Producto, Categoria,  Orden, OrdenItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import ProductoSerializer, CategoriaSerializer
from django.shortcuts import render, redirect, get_object_or_404


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer




@api_view(['POST'])

def crear_orden(request):
    data = request.data
    nombre = data.get('nombre_cliente', '')
    telefono = data.get('telefono', '')
    items = data.get('items', [])

    if not items:
        return Response({'detail': 'La orden no tiene items.'}, status=status.HTTP_400_BAD_REQUEST)

    orden = Orden.objects.create(nombre_cliente=nombre, telefono=telefono)
    total = Decimal('0.00')

    for it in items:
        prod_id = it.get('producto_id')
        cantidad = int(it.get('cantidad', 1))
        try:
            prod = Producto.objects.get(id=prod_id)
        except Producto.DoesNotExist:
            continue  # ignorar items inválidos

        precio = prod.precio
        subtotal = precio * cantidad
        OrdenItem.objects.create(
            orden=orden,
            producto=prod,
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=subtotal
        )
        total += subtotal

    orden.total = total
    orden.save()
    return Response({'orden_id': orden.id, 'total': str(orden.total)}, status=status.HTTP_201_CREATED)


def catalogo_view(request):
    productos = Producto.objects.all()
    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    return render(request, 'catalogo.html', {'productos': productos, 'total_items': total_items})






def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1
        }

    request.session['carrito'] = carrito 
    return redirect('catalogo')      

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    for item in carrito.values():
        item['subtotal'] = item['precio'] * item['cantidad']
        total += item['subtotal']
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})


from urllib.parse import quote

def enviar_whatsapp(request):
    carrito = request.session.get('carrito', {})
    nombre = request.POST.get('nombre_cliente', '')
    telefono = request.POST.get('telefono', '')

    if not carrito:
        return redirect('catalogo_view')

    mensaje = f"Hola, soy {nombre}. Mi pedido:\n"
    total = 0
    for item in carrito.values():
        subtotal = item['precio'] * item['cantidad']
        mensaje += f"{item['nombre']} x {item['cantidad']} = ${subtotal}\n"
        total += subtotal
    mensaje += f"Total: ${total}"

    mensaje_codificado = quote(mensaje)
    url = f"https://wa.me/{593996374392}?text={mensaje_codificado}"

    request.session['carrito'] = {}
    request.session.modified = True 

    return redirect(url)