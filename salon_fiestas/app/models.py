from django.db import models
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group



# Create your models here.
class RESERVACION(models.Model):

    nombre_cliente = models.CharField(max_length=100)

    fecha_evento = models.DateTimeField()

    duracion_horas = models.IntegerField(default=4)

    num_invitados = models.IntegerField()

    tipo_evento = models.CharField(max_length=50)

    telefono_contacto = models.CharField(max_length=15)

    estatus = models.CharField(max_length=20, default='Pendiente')


    def __str__(self):

        return self.nombre_cliente
    
    @property
    def estatus_actualizado(self):
        """Retorna el estatus actualizado basado en la fecha del evento."""
        if self.fecha_evento < timezone.now():
            return "Listo"
        return self.estatus
    
class SHOW(models.Model):

    nombre_show = models.CharField(max_length=100)

    descripcion = models.TextField()

    precio = models.DecimalField(max_digits=8, decimal_places=2)

    caracteristicas = models.TextField(default='Ninguna')

    def __str__(self):

        return self.nombre_show

class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Empleados')