from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Modelo Usuario heredando de User
class Usuario(AbstractUser):
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
    
    GENEROS = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]

    OBJETIVOS = [
        ('Perder peso', 'Perder peso'),
        ('Mantener peso', 'Mantener peso'),
        ('Ganar peso', 'Ganar peso'),
    ]    
    ACTIVIDAD = [
        ('Nula', 'Nula'),
        ('1 a 2 veces en semana', '1 a 2 veces en semana'),
        ('3 a 5 veces en semana', '3 a 5 veces en semana'),
        ('6 a 7 veces en semana', '6 a 7 veces en semana'),
        ('Ejercicio intenso a diario', 'Ejercicio intenso a diario'),
    ]

    altura = models.FloatField(max_length=5,null=True, blank=True)
    edad=models.IntegerField(validators=[MinValueValidator(12)],null=True, blank=True)
    peso = models.FloatField(max_length=5,null=True, blank=True)
    #imagen_Perfil = models.ImageField()
    genero = models.CharField(max_length=100, choices=GENEROS, default='Selecciona biologicamente',null=True, blank=True)
    objetivo = models.CharField(max_length=200, choices=OBJETIVOS, default='Selecciona una opcion',null=True, blank=True)
    actividad=models.CharField(max_length=30, choices=ACTIVIDAD, default='Selecciona una opcion',null=True, blank=True)
    perfil_completado=models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.first_name


class Alimento(models.Model):
    MEDIDAS = [
        ('Gramos', 'Gramos'),
        ('Mililitros', 'Mililitros'),
    ]

    nombre = models.CharField(max_length=200, unique=True)
    calorias = models.FloatField(max_length=10)
    medida = models.CharField(max_length=12, choices=MEDIDAS, default='GR')

    def __str__(self):
        return f"{self.nombre} ---> Calorías por 100 {self.medida}: {self.calorias}"


class Comida(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='comida')

    def __str__(self):
        return f"{self.nombre}"


class Ingrediente(Alimento):
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE, related_name='ingredientes')
    cantidad = models.FloatField(max_length=10)

    def __str__(self):
        return f"{self.nombre} {self.cantidad}{self.medida} {self.calorias * self.cantidad / 100} cal"


class Diario(models.Model):
    calorias = models.FloatField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='dirio')
    fecha = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Usuario: {self.usuario.first_name} Fecha: {self.fecha} Calorias: {self.calorias} calorías"

class Pesos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pesos')
    peso = models.FloatField(max_length=5)
    fechaMedida = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name='Peso'
        verbose_name_plural='Pesos'

    def __str__(self):
        return f"{self.usuario.username} - {self.peso} kg - {self.fechaMedida.strftime('%Y-%m-%d')}"

