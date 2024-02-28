from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from django.db.models import Q





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    objects = CustomUserManager()

    def __str__(self):
        return self.nome_completo if self.nome_completo else self.username




class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=50)
    data_aquisicao = models.DateField(default=timezone.now)
    usuarios = models.ManyToManyField(Usuario, related_name='equipamentos', blank=True)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    cliente_nome = models.CharField(max_length=100)
    cliente_cpf = models.CharField(max_length=11, default="00000000000")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)  
    data = models.DateTimeField(default=timezone.now)
    hora = models.TimeField()
    cancelado = models.BooleanField(default=False)  # Novo campo para indicar se o agendamento foi cancelado

    def __str__(self):
        return f"Agendamento para {self.cliente_nome} em {self.equipamento.nome}"
