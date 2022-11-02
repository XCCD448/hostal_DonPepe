from django import forms
from .models import Producto, Cliente, Empresa, Proveedor, Empleado, Comedor, Contacto, Habitacion, Huesped, Reserva, Pedido, Compra, Manual, Archivo, Perfil
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {

            "fecha_vencimiento": forms.SelectDateWidget()

        }

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = '__all__'

        widgets = {

            "fecha_vencimiento": forms.SelectDateWidget()

        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2",]

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'


class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = '__all__'

class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = '__all__'


class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = '__all__'

class ComedorForm(forms.ModelForm):

    imagen = forms.ImageField(required=False)

    class Meta:
        model = Comedor
        fields = '__all__'

class HuespedForm(forms.ModelForm):

    class Meta:
        model = Huesped
        fields = ["perfil","nombre","apellido","empresa","rut","correo","telefono"]

class HabitacionForm(forms.ModelForm):

    nombre_habitacion = forms.CharField(min_length=3, max_length=50)
    imagen = forms.ImageField(required=False)
    precio_por_noche = forms.IntegerField(min_value=1, max_value=40000)

    class Meta:
        model = Habitacion
        fields = '__all__'

class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = '__all__'

class ContactoForm(forms.ModelForm):
    
    class Meta: 
        model = Contacto
        fields = '__all__'

class PedidoForm(forms.ModelForm):

    comentarios = forms.CharField(required=False)

    class Meta: 
        model = Pedido
        fields = ["correo_empleado","proveedor","familia_producto","tipo_producto","detalle_del_pedido","estado","comentarios"]

class CompraForm(forms.ModelForm):

    class Meta: 
        model = Compra
         
        fields = ["huesped","habitacion","plato","tipo_servicio","detalle_de_la_compra"]

class DisponibilidadForm(forms.Form):
    ROOM_CATEGORIES=(
        ('privada-1', 'DORMITORIO ORO 1'),
        ('privada-2', 'DORMITORIO ORO 2'),
        ('compartida-1', 'DORMITORIO PLATA 1'),
        ('compartida-2', 'DORMITORIO PLATA 2'),
    )
    habitacion_categoria = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=["%d-%m-%YT%H:%M",]) 
    check_out = forms.DateTimeField(required=True, input_formats=["%d-%m-%YT%H:%M",]) 

class ManualForm(forms.ModelForm):

    class Meta: 
        model = Manual
         
        fields = ["titulo","tipo","pdf"]


class ArchivoForm(forms.ModelForm):

    class Meta: 
        model = Archivo
         
        fields = ["titulo","tipo","archivo"]