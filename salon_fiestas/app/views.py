from django.shortcuts import render, redirect, get_object_or_404
from .models import RESERVACION, SHOW
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from django.utils import timezone 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db import models



# Create your views here.
def inicio(request):
    shows = SHOW.objects.all()
    return render(request, 'index.html' , {'shows': shows})

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
        duracion_horas = request.POST['txtDuracion']
        num_invitados = request.POST['txtNum_Inv']
        tipo_evento = request.POST['ddlTipo_Evento']
        telefono_contacto = request.POST['txtTelefono_Contacto']
        estatus = request.POST['ddlestatus']
        
        fecha_evento_dt = datetime.strptime(fecha_evento, '%Y-%m-%dT%H:%M')
        ## Convierte la fecha naive del formulario en una fecha aware usando make_aware
        fecha_evento_aware = timezone.make_aware(fecha_evento_dt)
        duracion_horas_int = int(duracion_horas)

        hora_fin_evento_propuesto = fecha_evento_aware + timedelta(hours=duracion_horas_int)
        hora_inicio_permitida= fecha_evento_aware.replace(hour=9, minute=0, second=0, microsecond=0)
        hora_fin_permitida= fecha_evento_aware.replace(hour=22, minute=0, second=0, microsecond=0)

        
        
        errores = {}
            
        if fecha_evento_aware < timezone.now():
            errores['txtFecha'] = 'No se puede registrar una fecha anterior a la actual.'
        elif fecha_evento_aware < hora_inicio_permitida or hora_fin_evento_propuesto > hora_fin_permitida:
            errores['txtFecha'] = 'La hora del evento debe estar entre las 9:00 AM y las 10:00 PM.'
        
        if duracion_horas_int <= 0 or duracion_horas_int > 6:
            errores['txtDuracion'] = 'La duración debe ser válida (entre 1 y 6 horas).'
            
        
        num_invitados = int(request.POST['txtNum_Inv'], 0)
        if num_invitados <= 0 or num_invitados > 140:
            errores['txtNum_Inv'] = 'El número de invitados debe ser un entero positivo y menor a 140.'

        if RESERVACION.objects.filter(telefono_contacto=telefono_contacto).exists():
            errores['txtTelefono_Contacto'] = 'Este número ya está registrado.'
            
        if RESERVACION.objects.filter(fecha_evento=fecha_evento_aware).exists():
            errores['txtFecha'] = 'Esta fecha ya está registrada.'
            
        
        reservaciones_existentes=RESERVACION.objects.all()
        for r in reservaciones_existentes:
            inicio_evento_existente = r.fecha_evento
            fin_existente = inicio_evento_existente + timedelta(hours=r.duracion_horas)

            if (inicio_evento_existente < hora_fin_evento_propuesto and fin_existente > fecha_evento_aware):
                errores['txtFecha'] = (
                    f'Ya existe una reservación en el horario de {inicio_evento_existente.strftime("%I:%M %p")} '
                    f'a {fin_existente.strftime("%I:%M %p")}. '
                    f'Por favor elige otro horario.'
                )
                break
    
        if errores:
            return render(request, 'editar.html', {'errores': errores})
        
        RESERVACION.objects.create(nombre_cliente=nombre_cliente, fecha_evento=fecha_evento_aware, duracion_horas=duracion_horas_int, num_invitados=num_invitados, tipo_evento=tipo_evento, telefono_contacto=telefono_contacto, estatus=estatus)
        return redirect('/listar/?exito=1')
    return render(request, 'crear.html')

def editar_reservacion(request, id):
    reservacion = get_object_or_404(RESERVACION, id=id)

    if request.method == 'POST':
        errores = {}

        # Captura los datos del formulario
        nombre_cliente = request.POST['txtNombre_Cliente']
        fecha_evento_str = request.POST['txtFecha']  # ← string crudo del input
        duracion_str = request.POST['txtDuracion']
        num_invitados_str = request.POST['txtNum_Inv']
        tipo_evento = request.POST['ddlTipo_Evento']
        telefono_contacto = request.POST['txtTelefono_Contacto']
        estatus = request.POST['ddlestatus']

        # Cargados de nuevo en el formulario Atributos temporales
        reservacion.nombre_cliente = nombre_cliente
        reservacion.fecha_evento_input = fecha_evento_str
        reservacion.duracion_horas = duracion_str
        reservacion.num_invitados = num_invitados_str
        reservacion.tipo_evento = tipo_evento
        reservacion.telefono_contacto = telefono_contacto
        reservacion.estatus = estatus

        try:
            fecha_evento_dt = datetime.strptime(fecha_evento_str, '%Y-%m-%dT%H:%M')
            fecha_evento_aware = timezone.make_aware(fecha_evento_dt)
        except ValueError:
            errores['txtFecha'] = 'Formato de fecha inválido.'
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})

        try:
            duracion_horas_int = int(duracion_str)
            num_invitados = int(num_invitados_str)
        except ValueError:
            errores['txtDuracion'] = 'Duración inválida.'
            errores['txtNum_Inv'] = 'Número de invitados inválido.'
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})

        hora_fin_evento_propuesto = fecha_evento_aware + timedelta(hours=duracion_horas_int)
        hora_inicio_permitida = fecha_evento_aware.replace(hour=9, minute=0, second=0, microsecond=0)
        hora_fin_permitida = fecha_evento_aware.replace(hour=22, minute=0, second=0, microsecond=0)

        if fecha_evento_aware < timezone.now():
            errores['txtFecha'] = 'No se puede registrar una fecha anterior a la actual.'
        elif fecha_evento_aware < hora_inicio_permitida or hora_fin_evento_propuesto > hora_fin_permitida:
            errores['txtFecha'] = 'La hora del evento debe estar entre las 9:00 AM y las 10:00 PM.'

        if duracion_horas_int <= 0 or duracion_horas_int > 6:
            errores['txtDuracion'] = 'La duración debe ser válida (entre 1 y 6 horas).'

        if num_invitados <= 0 or num_invitados > 140:
            errores['txtNum_Inv'] = 'El número de invitados debe ser un entero positivo y menor a 140.'

        if RESERVACION.objects.filter(telefono_contacto=telefono_contacto).exclude(id=reservacion.id).exists():
            errores['txtTelefono_Contacto'] = 'Este número ya está registrado.'

        if RESERVACION.objects.filter(fecha_evento=fecha_evento_aware).exclude(id=reservacion.id).exists():
            errores['txtFecha'] = 'Esta fecha ya está registrada.'

        for r in RESERVACION.objects.exclude(id=reservacion.id):
            inicio = r.fecha_evento
            fin = inicio + timedelta(hours=r.duracion_horas)
            if inicio < hora_fin_evento_propuesto and fin > fecha_evento_aware:
                errores['txtFecha'] = (
                    f'Ya existe una reservación de {inicio.strftime("%I:%M %p")} a {fin.strftime("%I:%M %p")}. '
                    f'Por favor elige otro horario.'
                )
                break

        if errores:
            return render(request, 'editar.html', {'reservacion': reservacion, 'errores': errores})

        # Guardar los datos queverientos
        reservacion.fecha_evento = fecha_evento_aware
        reservacion.duracion_horas = duracion_horas_int
        reservacion.num_invitados = num_invitados
        reservacion.save()

        return redirect('/listar/?exito=1')

    # Aqui se prepara la fecha para el input
    reservacion.fecha_evento_input = reservacion.fecha_evento.strftime('%Y-%m-%dT%H:%M')
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