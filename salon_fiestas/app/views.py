from django.shortcuts import render, redirect, get_object_or_404
from .models import RESERVACION, SHOW
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from django.utils import timezone 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User



# Create your views here.


def inicio(request):
    return render(request, 'index.html')

def listar_reservaciones(request):
    reservaciones = RESERVACION.objects.all()
    return render(request, 'listar.html', {'reservaciones': reservaciones})

def listar_empleado(request):
    reservaciones = RESERVACION.objects.all()
    return render(request, 'listar_empleado.html', {'reservaciones': reservaciones})

def crear_reservacion(request):
    if request.method == 'POST':
        nombre_cliente = request.POST['txtNombre_Cliente']
        fecha_evento = request.POST['txtFecha']
        duracion_horas = request.POST['ddlDuracion']
        num_invitados = request.POST['txtNum_Inv']
        tipo_evento = request.POST['ddlTipo_Evento']
        telefono_contacto = request.POST['txtTelefono_Contacto']
        estatus = request.POST['ddlestatus']
        
        
        errores = {}
        
        fecha_evento_dt = datetime.strptime(fecha_evento, '%Y-%m-%dT%H:%M')
        ## Convierte la fecha naive del formulario en una fecha aware usando make_aware
        fecha_evento_aware = timezone.make_aware(fecha_evento_dt)
        duracion_horas_int = int(duracion_horas)

        if fecha_evento_aware < timezone.now():
            errores['txtFecha'] = 'No se puede registrar una fecha anterior a la actual.'
            return render(request, 'crear.html', {'errores': errores})
        
        if duracion_horas_int <= 0:
            errores['ddlDuracion'] = 'La duración debe ser un entero positivo.'
            return render(request, 'crear.html', {'errores': errores})
        
        num_invitados = int(request.POST['txtNum_Inv'], 0)
        if num_invitados <= 0:
            errores['txtNum_Inv'] = 'El número de invitados debe ser un entero positivo.'
            return render(request, 'crear.html', {'errores': errores})

        if RESERVACION.objects.filter(telefono_contacto=telefono_contacto).exists():
            errores['txtTelefono_Contacto'] = 'Este número ya está registrado.'
            return render(request, 'crear.html', {'errores': errores})
        if RESERVACION.objects.filter(fecha_evento=fecha_evento_aware).exists():
            errores['txtFecha'] = 'Esta fecha ya está registrada.'
            return render(request, 'crear.html', {'errores': errores})
        
        hora_fin_evento_propuesto = fecha_evento_aware + timedelta(hours=duracion_horas_int)

        reservaciones_existentes = RESERVACION.objects.filter(
            fecha_evento__range=(fecha_evento_aware, hora_fin_evento_propuesto)
        ).exists()

        if reservaciones_existentes:
            errores['txtFecha'] = f'Ya existe una reservación con este horario (Duración: {duracion_horas_int}h).'
            return render(request, 'crear.html', {'errores': errores})
        

        RESERVACION.objects.create(nombre_cliente=nombre_cliente, fecha_evento=fecha_evento_aware, duracion_horas=duracion_horas_int, num_invitados=num_invitados, tipo_evento=tipo_evento, telefono_contacto=telefono_contacto, estatus=estatus)
        return redirect('listar')
    return render(request, 'crear.html')

def editar_reservacion(request, id):
    reservacion = get_object_or_404(RESERVACION, id=id)
    if request.method == 'POST':
        reservacion.nombre_cliente = request.POST['txtNombre_Cliente']
        reservacion.fecha_evento = request.POST['txtFecha']
        reservacion.duracion_horas = request.POST['ddlDuracion']
        reservacion.num_invitados = request.POST['txtNum_Inv']
        reservacion.tipo_evento = request.POST['ddlTipo_Evento']
        reservacion.telefono_contacto = request.POST['txtTelefono_Contacto']
        reservacion.estatus = request.POST['ddlestatus']
        
        errores = {}
        fecha_evento_dt = datetime.strptime(reservacion.fecha_evento, '%Y-%m-%dT%H:%M')
        fecha_evento_aware = timezone.make_aware(fecha_evento_dt) # HAZLA AWARE
        duracion_horas_int = int(reservacion.duracion_horas)

        if fecha_evento_aware < timezone.now():
            errores['txtFecha'] = 'No se puede registrar una fecha anterior a la actual.'
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})   
        num_invitados = int(request.POST['txtNum_Inv'], 0)
        if num_invitados <= 0:
            errores['txtNum_Inv'] = 'El número de invitados debe ser un entero positivo.'
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})

        if RESERVACION.objects.filter(telefono_contacto=request.POST['txtTelefono_Contacto']).exclude(id=reservacion.id).exists():
            errores['txtTelefono_Contacto'] = 'Este número ya está registrado.'
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})
        if RESERVACION.objects.filter(fecha_evento=fecha_evento_aware).exclude(id=reservacion.id).exists():
            errores['txtFecha'] = 'Esta fecha ya está registrada.'
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})
        
        hora_fin_evento_propuesto = fecha_evento_aware + timedelta(hours=duracion_horas_int)

        reservaciones_existentes = RESERVACION.objects.filter(
            fecha_evento__range=(fecha_evento_aware, hora_fin_evento_propuesto)
        ).exclude(id=reservacion.id).exists()
        
        reservacion.fecha_evento = fecha_evento_aware # ASIGNALA AWARE
        reservacion.duracion_horas = duracion_horas_int
        reservacion.save()
        return redirect('listar')
    return render(request, 'editar.html', {'reservacion': reservacion})

def eliminar_reservicion(request, id):
    reservacion = get_object_or_404(RESERVACION, id=id)
    reservacion.delete()
    return redirect('listar')

class RoleLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=[('admin', 'Administrador'), ('empleado', 'Empleado')],
        label='Tipo de usuario'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'id': 'id_role'})

def is_admin(user):
    return user.is_superuser

def is_empleado(user):
    return user.groups.filter(name='Empleados').exists()

@login_required
@user_passes_test(is_admin)
def listar_reservaciones(request):
    reservaciones = RESERVACION.objects.all()
    return render(request, 'listar.html', {'reservaciones': reservaciones})

@login_required
@user_passes_test(is_empleado)
def listar_empleado(request):
    reservaciones = RESERVACION.objects.all()
    return render(request, 'listar_empleado.html', {'reservaciones': reservaciones})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = RoleLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        
        if user.is_superuser:
            return redirect('listar')
        elif is_empleado(user):
            return redirect('listar_empleado')
        return response


@login_required
@user_passes_test(is_admin)
def crear_empleado(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                password=password
            )
            empleados_group = Group.objects.get(name='Empleados')
            user.groups.add(empleados_group)
            return redirect('listar')
            
    return render(request, 'crear_empleado.html')

        
def marcar_listo(request, id):
    reservacion = get_object_or_404(RESERVACION, id=id)
    reservacion.estatus = "Listo"
    reservacion.save()
    return redirect('listar_empleado')