from django.db import models
from django.contrib.auth.models import User

class LogPersonalizado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.data.strftime('%d/%m/%Y %H:%M')}] {self.acao}"

# Create your models here.
