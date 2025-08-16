"""
URL configuration for tiendaOline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tienda.views import ProductoViewSet, CategoriaViewSet
from tienda.views import enviar_whatsapp,ver_carrito,catalogo_view, agregar_al_carrito
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', catalogo_view, name='catalogo'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('enviar-whatsapp/', enviar_whatsapp, name='enviar_whatsapp'),

    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#monimonidev