from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class BaseModel(models.Model):
    """
    Modelo base que contém campos e métodos comuns a todos os modelos.
    """
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação", null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização", null=True, blank=True)
    
    class Meta:
        abstract = True

class ConfiguracaoRelatorio(BaseModel):
    """
    Modelo para armazenar configurações de relatórios.
    Permite personalizar como os relatórios são gerados e exibidos.
    """
    TIPO_RELATORIO_CHOICES = [
        ('UMIDADE', 'Relatório de Umidade'),
        ('PROTEINA', 'Relatório de Proteína'),
        ('COMBINADO', 'Relatório Combinado'),
    ]
    
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome do Relatório"
    )
    tipo_relatorio = models.CharField(
        max_length=15,
        choices=TIPO_RELATORIO_CHOICES,
        verbose_name="Tipo de Relatório"
    )
    periodo_padrao = models.IntegerField(
        default=7,
        verbose_name="Período padrão em dias",
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    ativo = models.BooleanField(
        default=True, 
        verbose_name="Relatório Ativo"
    )
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_relatorio_display()})"
    
    class Meta:
        verbose_name = "Configuração de Relatório"
        verbose_name_plural = "Configurações de Relatórios"
        ordering = ['nome']
