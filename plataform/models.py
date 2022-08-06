from ast import Delete
from pyexpat import model
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

class Evento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nome}"
        

class Produto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    #imagem = models.ImageField(upload_to='images', null=True, blank=True)
    descricao = models.CharField(max_length=200)
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=9, decimal_places=2)
    ehReservado = models.BooleanField(default=False)

    def __str__(self):
        return f"Produto: {self.nome} - preco: {self.preco}"

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
