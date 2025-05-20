from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def validate_not_future_date(value):
    """Valida que uma data não está no futuro."""
    if value > timezone.localdate():
        raise ValidationError('A data não pode estar no futuro.')

class BaseModel(models.Model):
    """
    Modelo base que contém campos e métodos comuns a todos os modelos.
    """
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    class Meta:
        abstract = True

class AnaliseUmidade(BaseModel):
    """
    Modelo para armazenar análises de umidade na soja.
    """
    TIPO_AMOSTRA_CHOICES = [
        ('FG', 'Farelo Grosso'),
        ('FF', 'Farelo Fino'),
        ('SI', 'Soja Industrializada'),
        ('PE', 'Peletizado'),
    ]
    
    data = models.DateField(
        verbose_name="Data da Análise", 
        default=timezone.localdate,
        validators=[validate_not_future_date]
    )
    horario = models.TimeField(
        verbose_name="Horário da Análise",
        default=timezone.localtime().time()
    )
    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default='FG'  # Farelo Grosso como padrão
    )
    tara = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Tara")
    liquido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Líquido")
    peso_amostra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso da Amostra")
    resultado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Resultado")
    fator_correcao = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="Fator de Correção",
        validators=[MinValueValidator(-1000), MaxValueValidator(1000)]
    )
    
    def __str__(self):
        return f"Análise de Umidade - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Umidade"
        verbose_name_plural = "Análises de Umidade"
        ordering = ['-data', '-horario']

class AnaliseProteina(BaseModel):
    """
    Modelo para armazenar análises de proteína na soja.
    """
    TIPO_AMOSTRA_CHOICES = [
        ('FL', 'Farelo'),
        ('SI', 'Soja Industrializada'),
    ]
    
    data = models.DateField(
        verbose_name="Data da Análise", 
        default=timezone.localdate,
        validators=[validate_not_future_date]
    )
    horario = models.TimeField(
        verbose_name="Horário da Análise",
        default=timezone.localtime().time()
    )
    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default='FL'
    )
    peso_amostra = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Peso da Amostra (g)",
        default=0.50,
        validators=[MinValueValidator(0.01)]
    )
    ml_gasto = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="ML Gastos",
        blank=True,
        null=True
    )
    resultado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Resultado (%)",
        blank=True,
        null=True
    )
    resultado_corrigido = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Resultado Corrigido (%)",
        blank=True,
        null=True
    )
    eh_media_24h = models.BooleanField(
        default=False,
        verbose_name="É média de 24h?"
    )
    
    def __str__(self):
        media = " (Média 24h)" if self.eh_media_24h else ""
        return f"{self.get_tipo_amostra_display()} - {self.data} {self.horario}{media}"
    
    class Meta:
        verbose_name = "Análise de Proteína"
        verbose_name_plural = "Análises de Proteína"
        ordering = ['-data', '-horario']

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
