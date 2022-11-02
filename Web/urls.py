from django.urls import path, include
from .views import home, menuadmin, agregar_producto, listar_producto, modificar_producto, eliminar_producto, agregar_cliente, listar_cliente, modificar_cliente, eliminar_cliente, \
agregar_empresa, listar_empresa, modificar_empresa, eliminar_empresa, agregar_proveedor, listar_proveedor, modificar_proveedor, eliminar_proveedor, agregar_empleado, listar_empleado, \
modificar_empleado, eliminar_empleado,agregar_plato, listar_plato, modificar_plato, eliminar_plato, agregar_habitacion, listar_habitacion, modificar_habitacion, eliminar_habitacion, \
minuta_semanal, contacto, listar_reserva, modificar_reserva, eliminar_reserva, habitaciones, ordenes_pedido, listar_pedido, modificar_pedido, eliminar_pedido, ordenes_compra, listar_compra, \
modificar_compra, eliminar_compra, agregar_huesped, listar_huesped, modificar_huesped, eliminar_huesped,modificar_archivo,eliminar_archivo, agregar_perfil, listar_perfil, modificar_perfil, eliminar_perfil, registrar, Pdf, Pdf2, upload
from django.urls import path 
from .views import ReservaView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', home, name="home"),
    path('menuadmin/', menuadmin, name="menuadmin"),
    path('habitaciones/', habitaciones, name="habitaciones"),
    path('registrar/', registrar, name="registrar"),

    path('upload/', views.upload, name='upload'),
    path('manuales/', views.manual_list, name='manual_list'),
    path('manuales/upload/', views.upload_manual, name='upload_manual'),

    path('documentos/', views.documento_list, name='archivo_list'),
    path('documentos/upload/', views.upload_documento, name='upload_archivo'),
    path('modificar_archivo/<id>/', modificar_archivo, name="modificar_archivo"),
    path('eliminar_archivo/<id>/', eliminar_archivo, name="eliminar_archivo"),

    path('agregar_cliente/', agregar_cliente, name="agregar_cliente"),
    path('listar_cliente/', listar_cliente, name="listar_cliente"),
    path('modificar_cliente/<id>/', modificar_cliente, name="modificar_cliente"),
    path('eliminar_cliente/<id>/', eliminar_cliente, name="eliminar_cliente"),
    
    path('listar_reserva/', listar_reserva, name="listar_reserva"),
    path('reserva/', ReservaView.as_view(), name='reserva_view'),
    path('modificar_reserva/<id>/', modificar_reserva, name="modificar_reserva"),
    path('eliminar_reserva/<id>/', eliminar_reserva, name="eliminar_reserva"),
    
    path('agregar_empresa/', agregar_empresa, name="agregar_empresa"),
    path('listar_empresa/', listar_empresa, name="listar_empresa"),
    path('modificar_empresa/<id>/', modificar_empresa, name="modificar_empresa"),
    path('eliminar_empresa/<id>/', eliminar_empresa, name="eliminar_empresa"),

    path('agregar_habitacion/', agregar_habitacion, name="agregar_habitacion"),
    path('listar_habitacion/', listar_habitacion, name="listar_habitacion"),
    path('modificar_habitacion/<id>/', modificar_habitacion, name="modificar_habitacion"),
    path('eliminar_habitacion/<id>/', eliminar_habitacion, name="eliminar_habitacion"),

    path('agregar_huesped/', agregar_huesped, name="agregar_huesped"),
    path('listar_huesped/', listar_huesped, name="listar_huesped"),
    path('modificar_huesped/<id>/', modificar_huesped, name="modificar_huesped"),
    path('eliminar_huesped/<id>/', eliminar_huesped, name="eliminar_huesped"),

    path('agregar_producto/', agregar_producto, name="agregar_producto"),
    path('listar_producto/', listar_producto, name="listar_producto"),
    path('modificar_producto/<id>/', modificar_producto, name="modificar_producto"),
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto"),

    path('agregar_perfil/', agregar_perfil, name="agregar_perfil"),
    path('listar_perfl/', listar_perfil, name="listar_perfil"),
    path('modificar_perfil/<id>/', modificar_perfil, name="modificar_perfil"),
    path('eliminar_perfil/<id>/', eliminar_perfil, name="eliminar_perfil"),
    
    path('agregar_proveedor/', agregar_proveedor, name="agregar_proveedor"),
    path('listar_proveedor/', listar_proveedor, name="listar_proveedor"),
    path('modificar_proveedor/<id>/', modificar_proveedor, name="modificar_proveedor"),
    path('eliminar_proveedor/<id>/', eliminar_proveedor, name="eliminar_proveedor"),

    path('agregar_empleado/', agregar_empleado, name="agregar_empleado"),
    path('listar_empleado/', listar_empleado, name="listar_empleado"),
    path('modificar_empleado/<id>/', modificar_empleado, name="modificar_empleado"),
    path('eliminar_empleado/<id>/', eliminar_empleado, name="eliminar_empleado"),
    
    path('agregar_plato/', agregar_plato, name="agregar_plato"),
    path('listar_plato/', listar_plato, name="listar_plato"),
    path('modificar_plato/<id>/', modificar_plato, name="modificar_plato"),
    path('eliminar_plato/<id>/', eliminar_plato, name="eliminar_plato"),
    path('minuta_semanal', minuta_semanal, name="minuta_semanal"),
    path('contacto', contacto, name="contacto"),

    path('pdf/',Pdf.as_view(), name='pdf'),
    path('listar_pedido/', listar_pedido, name="listar_pedido"),
    path('ordenes_pedido', ordenes_pedido, name="ordenes_pedido"),
    path('modificar_pedido/<id>/', modificar_pedido, name="modificar_pedido"),
    path('eliminar_pedido/<id>/', eliminar_pedido, name="eliminar_pedido"),

    path('pdf2/', Pdf2.as_view(), name='pdf2'),
    path('listar_compra/', listar_compra, name="listar_compra"),
    path('ordenes_compra', ordenes_compra, name="ordenes_compra"),
    path('modificar_compra/<id>/', modificar_compra, name="modificar_compra"),
    path('eliminar_compra/<id>/', eliminar_compra, name="eliminar_compra"),

    
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)