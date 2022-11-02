from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

TIPO_USUARIO = (
('Cliente', 'Cliente'),
('Proveedor', 'Proveedor'),
('Empleado', 'Empleado'),
('Huesped', 'Huesped'),
)
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    telefono= models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=200, null=True)
    tipo = models.CharField(default='Cliente', max_length=50, choices=TIPO_USUARIO)

    def __str__(self):
              return f'{self.usuario} {self.tipo}'

class Cliente(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.CharField(max_length=500, null=True) 
    nombre = models.CharField(max_length=120, null=True)
    apellido = models.CharField(max_length=120, null=True)
    rut = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=100, null=True)
    cliente_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        perfil='Sin Perfil Asociado'
        if self.perfil is None:
            return perfil
        else:
            return self.perfil.nombre
    
    @property
    def is_cliente(self):
        cliente = False
        tipo = self.perfil.tipo
        if (tipo == 'Cliente'):
            cliente = True
        else:
            cliente = False
        return cliente

class Proveedor(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, blank=True)
    nombre = models.CharField(max_length=120, null=True)
    apellido = models.CharField(max_length=120, null=True)
    rut = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=100, null=True)
    rubro = models.CharField(max_length=50)
    telefono = models.CharField(max_length=100, null=True)
    direccion = models.TextField()
    proveedor_id = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.perfil.nombre

    @property
    def is_proveedor(self):
        proveedor = False
        tipo = self.perfil.tipo
        if (tipo == 'Proveedor'):
            proveedor = True
        else:
            proveedor= False
        return proveedor

class Empleado(models.Model):
    perfil= models.OneToOneField(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=250)
    direccion= models.TextField()
    empleado_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.perfil.nombre
    
    @property
    def is_empleado(self):
        empleado = False
        tipo = self.perfil.tipo
        if (tipo == 'Empleado'):
            empleado = True
        else:
            empleado = False
        return empleado

class Huesped(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    empresa = models.CharField(max_length=500, null=True) 
    rut = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=100, null=True)
    huesped_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        perfil='Sin Perfil Asociado'
        if self.perfil is None:
            return perfil
        else:
            return self.perfil.nombre
    
    @property
    def is_huesped(self):
        huesped = False
        tipo = self.perfil.tipo
        if (tipo == 'Huesped'):
            huesped = True
        else:
            huesped = False
        return huesped

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    fecha_vencimiento = models.DateField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    stock_disponible = models.CharField(max_length=200)
    stock_critico = models.CharField(max_length=200)
    familia_producto = models.ForeignKey('FamiliaProducto', on_delete=models.CASCADE, db_column='nro_familia_producto', blank=True, null=True)
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE, db_column='nro_tipo_producto', blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    stock = models.IntegerField(default=0, null=True, blank=True)
    stock_critico = models.IntegerField(default=10, null=True, blank=True)

    def __str__(self):
         return f' Stock  {self.producto}  '

class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=50)
    tipo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=250)
    direccion = models.TextField()
    
    def __str__(self):
        return self.nombre



estado_habitacion = [
    [0, "Disponible"],
    [1, "No Disponible"],
    [2, "En Mantencion"],
    [3, "Fuera de servicio"],
]

class Habitacion(models.Model):
    ROOM_CATEGORIES=(
        ('privada-1', 'DORMITORIO ORO 1'),
        ('privada-2', 'DORMITORIO ORO 2'),
        ('compartida-1', 'DORMITORIO PLATA 1'),
        ('compartida-2', 'DORMITORIO PLATA 2'),
    )
    numero = models.IntegerField()
    nombre_habitacion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, choices=ROOM_CATEGORIES)
    camas = models.IntegerField()
    baños = models.IntegerField()
    precio = models.IntegerField()
    cantidad_personas = models.IntegerField()
    estado_habitacion = models.IntegerField(choices=estado_habitacion)
    imagen = models.ImageField(upload_to="habitaciones", null=True)

    def __str__(self):
        return self.nombre_habitacion

class Reserva (models.Model):
    APROBADA = 'APROBADA'
    CANCELADA = 'CANCELADA'

    ESTADO_RESERVA = ((APROBADA, 'Aprobada'),
                       (CANCELADA, 'Cancelada'),)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    estado = models.CharField(choices=ESTADO_RESERVA, default=APROBADA, max_length=150)

    def __str__(self):
        return f'El {self.usuario} ha reservado {self.habitacion} desde {self.check_in} hasta {self.check_out} '

class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    tipo_servicio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_servicio


class Comedor(models.Model):
    nombre_plato = models.CharField(max_length=100)
    precio_plato = models.IntegerField()
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="comedor", null=True)

    def __str__(self):
        return self.nombre_plato

class FamiliaProducto(models.Model):
    id_familia_producto = models.AutoField(primary_key=True)
    nro_familia_producto = models.CharField(max_length=999)
    familia_producto = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nro_familia_producto

class TipoProducto(models.Model):
    id_tipo_producto = models.AutoField(primary_key=True)
    nro_tipo_producto = models.CharField(max_length=999)
    tipo_producto = models.CharField(max_length=999)
    def __str__(self):
        return self.nro_tipo_producto
        
opcion_consultas = [
    [0, "Problema"],
    [1, "Reservar"],
    [2, "Solicitud"],
    [3, "Registro Usuario"],
    [4, "Solicitud cambio de contraseña"],
    [5, "Cancelar"],
]
class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    asunto = models.IntegerField(choices=opcion_consultas)
    mensaje = models.TextField()


    def __str__(self):
        return self.nombre

estado_ordenpedido = (
    ('Pendiente', 'Pendiente'),
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado')
)
class Pedido(models.Model):
    correo_empleado = models.EmailField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    familia_producto = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50,null=False, blank=False,choices=estado_ordenpedido,default='Pendiente')
    detalle_del_pedido = models.TextField()
    comentarios = models.TextField()

    def __str__(self):
         return f' Orden de Pedido {self.id}  '

Estado_orden_compra = (
    ('En espera', 'En espera'),
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado')
)
class Compra(models.Model):
    huesped = models.ForeignKey(Huesped, on_delete=models.PROTECT)
    habitacion = models.CharField(max_length=100)
    plato = models.ForeignKey(Comedor, on_delete=models.PROTECT)
    tipo_servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    detalle_de_la_compra = models.CharField(max_length=100)
    estado_orden_compra = models.CharField(max_length=50,null=False, blank=False,choices=Estado_orden_compra,default='En espera')
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f' Orden de Compra {self.id} {self.fecha} '

class Manual(models.Model):
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='manuales/pdfs/')

    def __str__(self):
        return self.titulo

class Archivo(models.Model):
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documentos/pdfs/')

    def __str__(self):
        return self.titulo

