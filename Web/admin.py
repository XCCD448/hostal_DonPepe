from django.contrib import admin
from .models import Marca, Perfil, Producto, Empresa, Comedor, Servicio, FamiliaProducto, TipoProducto, Contacto, Habitacion, Reserva, Cliente,Proveedor,Empleado,Huesped,Pedido,Compra,Stock, Manual, Archivo

admin.site.register(Perfil)
admin.site.register(Cliente)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Proveedor)

admin.site.register(Empresa)

admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Pedido)
admin.site.register(Empleado)
admin.site.register(Huesped)

admin.site.register(Stock)
admin.site.register(Comedor)
admin.site.register(Compra)

admin.site.register(Servicio)
admin.site.register(Contacto)
admin.site.register(Manual)
admin.site.register(Archivo)

admin.site.register(FamiliaProducto)
admin.site.register(TipoProducto)



