from django.contrib import admin
from .models import Producto, Categoria, Orden, OrdenItem

admin.site.register(Producto)
admin.site.register(Categoria)


class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'telefono', 'total', 'creado_en')
    inlines = [OrdenItemInline]
