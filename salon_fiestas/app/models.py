from django.db import models


# Create your models here.
class RESERVACION(models.Model):

    nombre_cliente = models.CharField(max_length=100)

    fecha_evento = models.DateTimeField()

    num_invitados = models.IntegerField()

    tipo_evento = models.CharField(max_length=50)

    telefono_contacto = models.CharField(max_length=15)

    estatus = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):

        return self.nombre_cliente
    
class SHOW(models.Model):

    nombre_show = models.CharField(max_length=100)

    descripcion = models.TextField()

    precio = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):

        return self.nombre_show