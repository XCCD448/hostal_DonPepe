from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Producto, Cliente, Empresa, Proveedor, Empleado, Comedor, Contacto, Habitacion, Reserva, Huesped, Pedido, Compra, Manual, Archivo, Perfil
from .forms import ProductoForm, ClienteForm, EmpresaForm, ProveedorForm, EmpleadoForm, ComedorForm, ContactoForm, HabitacionForm, HuespedForm, ReservaForm, PedidoForm, CompraForm, ManualForm, ArchivoForm, CustomUserCreationForm, PerfilForm
from django.contrib import messages
from django.views.generic import ListView, FormView, View, TemplateView
from .forms import DisponibilidadForm
from django.contrib.auth import authenticate, login
from Web.reserva_functions.disponibilidad import check_disponibilidad
from xhtml2pdf import pisa 
from django.http import HttpResponse
from django.template.loader import get_template
from .utils import render_to_pdf
from django.core.files.storage import FileSystemStorage
from io import BytesIO
#create your views here 

@login_required
def home(request):
    return render(request, 'Web/home.html')

@login_required
def habitaciones(request):
    habitaciones = Habitacion.objects.all()
    data = {
        'habitaciones': habitaciones
    }
    return render(request, 'Web/habitaciones.html', data)

#subir y descargar manuales (clientes)
@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'Web/upload.html', context)

@login_required
def manual_list(request):
    manuales = Manual.objects.all()
    return render(request, 'Web/manual_list.html',{'manuales': manuales})

@login_required
def upload_manual(request):
    if request.method == 'POST':
        form = ManualForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manual_list')
    else: 
        form = ManualForm()
    return render(request, 'Web/upload_manual.html', {'form':form})
#subir y descargar manuales (clientes)

#subir y descargar documentos (admin)
@login_required
def documento_list(request):
    archivos = Archivo.objects.all()
    return render(request, 'documentos/archivo_list.html',{'archivos': archivos})
    
@login_required
def upload_documento(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('archivo_list')
    else: 
        form = ArchivoForm()
    return render(request, 'documentos/upload_documento.html', {'form':form})

@login_required
def modificar_archivo(request, id):

    archivo = get_object_or_404(Archivo, id=id)

    data = {
        'form': ArchivoForm(instance=archivo)
    }

    if request.method == 'POST':
        formulario = ArchivoForm(data=request.POST, instance=archivo, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="archivo_list")
        data["form"] = formulario

    return render(request, 'documentos/modificar.html', data)

@login_required
def eliminar_archivo(request, id):
    archivo = get_object_or_404(Archivo, id=id)
    archivo.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="archivo_list")
#subir y descargar documentos (admin)

@login_required
@permission_required('Web.add_sessions')
def menuadmin(request):
    return render(request, 'registration/menuadmin.html')

def registrar(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registrado Correctamente")
            return redirect(to="home")
        data["form"] = formulario 
    return render(request, 'registration/registro.html', data)
#Contacto

def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Enviado correctamente")
        else:
            data["form"] = formulario
    return render(request, 'contacto/contacto.html', data)

#Contacto 

#Ordenes de pedido (proveedores)
@login_required  
def ordenes_pedido(request):
    data = {
        'form': PedidoForm()
    }
    if request.method == 'POST':
        formulario = PedidoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Solicitado correctamente")
        else:
            data["form"] = formulario
    return render(request, 'pedido/ordenesdepedidos.html', data)

@login_required   
@permission_required('Web.view_compra')
def listar_pedido(request):
    pedidos = Pedido.objects.all()

    data = {
        'pedidos': pedidos
    }
    return render(request, 'pedido/listar.html', data)

@login_required
@permission_required('Web.change_pedido')
def modificar_pedido(request, id):

    pedido = get_object_or_404(Pedido, id=id)

    data = {
        'form': PedidoForm(instance=pedido)
    }

    if request.method == 'POST':
        formulario = PedidoForm(data=request.POST, instance=pedido, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_pedido")
        data["form"] = formulario

    return render(request, 'pedido/modificar.html', data)

@login_required
@permission_required('Web.delete_pedido')
def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_pedido")

#Ordenes de pedido (exportar a pdf)
class Pdf(View):
    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.all()
        data = {
            'pedidos': pedidos
        }
        pdf = render_to_pdf('pedido/pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        
#Ordenes de pedido (exportar a pdf)

#Ordenes de compras (Comedor)

def ordenes_compra(request):
    data = {
        'form': CompraForm()
    }
    if request.method == 'POST':
        formulario = CompraForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Solicitado correctamente")
        else:
            data["form"] = formulario
    return render(request, 'compra/ordenesdecompras.html', data)

#Ordenes de compras (exportar a pdf)
class Pdf2(View):
    def get(self, request, *args, **kwargs):
        compras = Compra.objects.all()
        data = {
            'compras': compras
        }
        pdf = render_to_pdf('compra/pdf2.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        
#Ordenes de compras (exportar a pdf)

@login_required   
@permission_required('Web.view_compra')
def listar_compra(request):
    compras = Compra.objects.all()

    data = {
        'compras': compras
    }
    return render(request, 'compra/listar.html', data)

@login_required
@permission_required('Web.change_compra')
def modificar_compra(request, id):

    compra = get_object_or_404(Compra, id=id)

    data = {
        'form': CompraForm(instance=compra)
    }

    if request.method == 'POST':
        formulario = CompraForm(data=request.POST, instance=compra, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_compra")
        data["form"] = formulario

    return render(request, 'compra/modificar.html', data)

@login_required
@permission_required('Web.delete_compra')
def eliminar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    compra.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_compra")

#Ordenes de compras (Comedor)

#Reservas
@login_required   
@permission_required('Web.view_reserva')
def listar_reserva(request):
    reservas = Reserva.objects.all()

    data = {
        'reservas': reservas
    }
    return render(request, 'reserva/listar.html', data)

@login_required
@permission_required('Web.change_reserva')
def modificar_reserva(request, id):

    reserva = get_object_or_404(Reserva, id=id)

    data = {
        'form': ReservaForm(instance=reserva)
    }

    if request.method == 'POST':
        formulario = ReservaForm(data=request.POST, instance=reserva, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_reserva")
        data["form"] = formulario

    return render(request, 'reserva/modificar.html', data)

@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_reserva")


class ReservaView(FormView):
    form_class = DisponibilidadForm
    template_name = 'reserva/reserva.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        habitacion_list = Habitacion.objects.filter(categoria=data['habitacion_categoria'])
        disponible_habitacion=[]
        for habitacion in habitacion_list:
            if check_disponibilidad(habitacion, data['check_in'], data['check_out']):
                disponible_habitacion.append(habitacion)
        if len(disponible_habitacion)>0:
            habitacion = disponible_habitacion[0]
            reserva = Reserva.objects.create(
                usuario=self.request.user, 
                habitacion=habitacion, 
                check_in=data['check_in'],
                check_out=data['check_out'],
            )
            reserva.save()
            return HttpResponse(reserva)
        else:
            return HttpResponse('Lo sentimos esta habitacion esta reservada para esta fecha intenta elegir otra.')
        
#Reservas

#Gestion Clientes (CRUD)
@login_required
@permission_required('Web.add_cliente')
def agregar_cliente(request):
 
    data = {
        'form': ClienteForm()
    }

    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'cliente/agregar.html', data)

@login_required
@permission_required('Web.view_cliente')
def listar_cliente(request):
    clientes = Cliente.objects.all()

    data = {
        'clientes': clientes
    }

    return render(request, 'cliente/listar.html', data)

@login_required
@permission_required('Web.change_cliente')
def modificar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    data = {
        'form': ClienteForm(instance=cliente)
    }

    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, instance=cliente, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_cliente")
        data["form"] = formulario

    return render(request, 'cliente/modificar.html', data)

@login_required
@permission_required('Web.delete_cliente')
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_cliente")

#Gestion Clientes (CRUD)

#Gestion Empresas (CRUD)

@login_required
@permission_required('Web.add_empresa')
def agregar_empresa(request):
    
    data = {
        'form': EmpresaForm()
    }

    if request.method == 'POST':
        formulario = EmpresaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Empresa Registrada Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'empresa/agregar.html', data)

@login_required
@permission_required('Web.view_empresa')
def listar_empresa(request):
    empresas = Empresa.objects.all()

    data = {
        'empresas': empresas
    }
    
    return render(request, 'empresa/listar.html', data)

@login_required
@permission_required('Web.change_empresa')
def modificar_empresa(request, id):

    empresa = get_object_or_404(Empresa, id=id)

    data = {
        'form': EmpresaForm(instance=empresa)
    }

    if request.method == 'POST':
        formulario = EmpresaForm(data=request.POST, instance=empresa, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_empresa")
        data["form"] = formulario

    return render(request, 'empresa/modificar.html', data)

@login_required
@permission_required('Web.delete_empresa')
def eliminar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    empresa.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_empresa")

#Gestion Empresas (CRUD) 

#Gestion Perfil (CRUD) 

@login_required
@permission_required('Web.add_perfil')
def agregar_perfil(request):

    data = {
        'form': PerfilForm()
    }

    if request.method == 'POST':
        formulario = PerfilForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Perfil Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'perfil/agregar.html', data)


@login_required
@permission_required('Web.view_perfil')
def listar_perfil(request):
    perfiles = Perfil.objects.all()

    data = {
        'perfiles': perfiles
    }
    
    return render(request, 'perfil/listar.html', data)

@login_required
@permission_required('Web.change_perfil')
def modificar_perfil(request, id):

    perfiles = get_object_or_404(Perfil, id=id)

    data = {
        'form': PerfilForm(instance=perfiles)
    }

    if request.method == 'POST':
        formulario = PerfilForm(data=request.POST, instance=perfiles, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_perfil")
        data["form"] = formulario

    return render(request, 'perfil/modificar.html', data)

@login_required
@permission_required('Web.delete_perfil')
def eliminar_perfil(request, id):
    perfiles = get_object_or_404(Perfil, id=id)
    perfiles.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_perfil") 
#Gestion Perfil (CRUD) 

#Gestion Productos (CRUD) 

@login_required
@permission_required('Web.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'producto/agregar.html', data)

@login_required
@permission_required('Web.view_producto')
def listar_producto(request):
    productos = Producto.objects.all()

    data = {
        'productos': productos
    }
    
    return render(request, 'producto/listar.html', data)

@login_required
@permission_required('Web.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_producto")
        data["form"] = formulario

    return render(request, 'producto/modificar.html', data)

@login_required
@permission_required('Web.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_producto")

#Gestion Productos (CRUD) 

#Gestion Proveedores (CRUD) 

@login_required
@permission_required('Web.add_proveedor')
def agregar_proveedor(request):
    
    data = {
        'form': ProveedorForm()
    }

    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Proveedor Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'proveedor/agregar.html', data)


@login_required
@permission_required('Web.view_proveedor')
def listar_proveedor(request):
    proveedores = Proveedor.objects.all()

    data = {
        'proveedores': proveedores
    }
    
    return render(request, 'proveedor/listar.html', data)


@login_required
@permission_required('Web.change_proveedor')
def modificar_proveedor(request, id):

    proveedor = get_object_or_404(Proveedor, id=id)

    data = {
        'form': ProveedorForm(instance=proveedor)
    }

    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST, instance=proveedor, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_proveedor")
        data["form"] = formulario

    return render(request, 'proveedor/modificar.html', data)


@login_required
@permission_required('Web.delete_proveedor')
def eliminar_proveedor(request, id):


    proveedor = get_object_or_404(Proveedor, id=id)
    proveedor.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_proveedor")

#Gestion Proveedores (CRUD) 

#Gestion Habitaciones (CRUD) 

@login_required
@permission_required('Web.add_habitacion')
def agregar_habitacion(request):
    
    data = {
        'form': HabitacionForm()
    }

    if request.method == 'POST':
        formulario = HabitacionForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Habitacion Registrada Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'habitacion/agregar.html', data)


@login_required
@permission_required('Web.view_habitacion')
def listar_habitacion(request):
    habitaciones = Habitacion.objects.all()

    data = {
        'habitaciones': habitaciones
    }
    
    return render(request, 'habitacion/listar.html', data)

@login_required
@permission_required('Web.change_habitacion')
def modificar_habitacion(request, id):

    habitacion = get_object_or_404(Habitacion, id=id)

    data = {
        'form': HabitacionForm(instance=habitacion)
    }

    if request.method == 'POST':
        formulario = HabitacionForm(data=request.POST, instance=habitacion, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_habitacion")
        data["form"] = formulario

    return render(request, 'habitacion/modificar.html', data)

@login_required
@permission_required('Web.delete_habitacion')
def eliminar_habitacion(request, id):

    habitacion = get_object_or_404(Habitacion, id=id)
    habitacion.delete()
    messages.success(request, "Eliminado Correctamente")

    return redirect(to="listar_habitacion")
#Gestion Habitaciones (CRUD) 

#Gestion Huespedes (CRUD) 

@login_required
@permission_required('Web.add_huesped')
def agregar_huesped(request):
    
    data = {
        'form': HuespedForm()
    }

    if request.method == 'POST':
        formulario = HuespedForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Huesped Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'huesped/agregar.html', data)

@login_required
@permission_required('Web.view_huesped')
def listar_huesped(request):
    huespedes = Huesped.objects.all()

    data = {
        'huespedes': huespedes
    }
    
    return render(request, 'huesped/listar.html', data)


@login_required
@permission_required('Web.change_huesped')
def modificar_huesped(request, id):

    huesped = get_object_or_404(Huesped, id=id)

    data = {
        'form': HuespedForm(instance=huesped)
    }

    if request.method == 'POST':
        formulario = HuespedForm(data=request.POST, instance=huesped, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_huesped")
        data["form"] = formulario

    return render(request, 'huesped/modificar.html', data)



@login_required
@permission_required('Web.delete_huesped')
def eliminar_huesped(request, id):


    huesped = get_object_or_404(Huesped, id=id)
    huesped.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_huesped")
#Gestion Huespedes (CRUD) 

#Gestion Empleados (CRUD) 

@login_required
@permission_required('Web.add_empleado')
def agregar_empleado(request):
    
    data = {
        'form': EmpleadoForm()
    }

    if request.method == 'POST':
        formulario = EmpleadoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Empleado Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'empleado/agregar.html', data)


@login_required
@permission_required('Web.view_empleado')
def listar_empleado(request):
    empleados = Empleado.objects.all()

    data = {
        'empleados': empleados
    }
    
    return render(request, 'empleado/listar.html', data)



@login_required
@permission_required('Web.change_empleado')
def modificar_empleado(request, id):

    empleado = get_object_or_404(Empleado, id=id)

    data = {
        'form': EmpleadoForm(instance=empleado)
    }

    if request.method == 'POST':
        formulario = EmpleadoForm(data=request.POST, instance=empleado, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_empleado")
        data["form"] = formulario

    return render(request, 'empleado/modificar.html', data)


@login_required
@permission_required('Web.delete_empleado')
def eliminar_empleado(request, id):


    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_empleado")
#Gestion Empleados (CRUD) 

#Gestion Comedor (CRUD)
@login_required
@permission_required('Web.add_plato')
def agregar_plato(request):
    
    data = {
        'form': ComedorForm()
    }

    if request.method == 'POST':
        formulario = ComedorForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Plato Registrado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'comedor/agregar.html', data)

@login_required
@permission_required('Web.view_plato')
def listar_plato(request):
    comedores = Comedor.objects.all()

    data = {
        'comedores': comedores
    }
    
    return render(request, 'comedor/listar.html', data)

@login_required
@permission_required('Web.change_plato')
def modificar_plato(request, id):

    comedor = get_object_or_404(Comedor, id=id)

    data = {
        'form': ComedorForm(instance=comedor)
    }

    if request.method == 'POST':
        formulario = ComedorForm(data=request.POST, instance=comedor, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_plato")
        data["form"] = formulario

    return render(request, 'comedor/modificar.html', data)

@login_required
@permission_required('Web.delete_plato')
def eliminar_plato(request, id):

    comedor = get_object_or_404(Comedor, id=id)
    comedor.delete()
    messages.success(request, "Eliminado Correctamente")

    return redirect(to="listar_plato")

@login_required
def minuta_semanal(request):
    comedores = Comedor.objects.all()
    data = {
        'comedores': comedores
    }
    return render(request, 'comedor/minutasemanal.html', data)
 
#Gestion Comedor (CRUD) 


