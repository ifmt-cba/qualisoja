# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    TIPO_FUNCIONARIO_CHOICES = [
        ('analista', 'Analista'),
        ('producao', 'Produção'),
        ('classificacao-producao', 'Classificação - Produção'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_funcionario = models.CharField(max_length=30, choices=TIPO_FUNCIONARIO_CHOICES)

    def __str__(self):
        return self.user.username


# Create your models here.
