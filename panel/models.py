from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class User1(models.Model):
    nombreusuario=models.CharField(max_length=100)
    nombres=models.CharField(max_length=100)
    apellidos=models.CharField(max_length=100)
    correo=models.EmailField(unique=True)
    doc_ide=models.CharField(max_length=9, null=True)
    password=models.TextField()
    telefono_contacto=models.CharField(max_length=10)
    anexo=models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    area=models.CharField(max_length=5)
    id_red=models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        db_table='panel_user'
        ordering=['id']

class Solicitud(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    dni = models.CharField(max_length=9, null=True)
    telefono_contacto = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    anexo = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    red = models.CharField(max_length=100, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    area = models.CharField(max_length=100, null=True) 
    area1 = models.CharField(max_length=100, null=True) 
    estado_soli = models.CharField(max_length=3, null=True)
    cod_arch = models.CharField(max_length=100, null=True) 

    
    class Meta:
        db_table='panel_solicitud'
        ordering=['id']

class Registro(models.Model):
    ip = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='panel_registro'
        ordering=['id']

