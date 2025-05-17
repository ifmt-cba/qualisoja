from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class AnaliseUmidade(models.Model):
    TIPO_AMOSTRA_CHOICES = [
        ('FG', 'Farelo Grosso'),
        ('FF', 'Farelo Fino'),
        ('SI', 'Soja Industrializada'),
        ('PE', 'Peletizado'),
    ]
    
    data = models.DateField(verbose_name="Data da Análise", default=timezone.localdate)
    horario = models.TimeField(verbose_name="Horário da Análise",default=timezone.localtime().time())
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

class AnaliseProteina(models.Model):
    TIPO_AMOSTRA_CHOICES = [
        ('FL', 'Farelo'),
        ('SI', 'Soja Industrializada'),
    ]
    
    
    data = models.DateField(verbose_name="Data da Análise", default=timezone.localdate)
    horario = models.TimeField(verbose_name="Horário da Análise",default=timezone.localtime().time())
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
        return f"{self.horario} - {self.get_tipo_amostra_display()}{media}"
    
    class Meta:
        verbose_name = "Análise de Proteína"
        verbose_name_plural = "Análises de Proteína"
        ordering = ['data', 'horario']

        # Adicione ao final do seu arquivo models.py existente

class ConfiguracaoRelatorio(models.Model):
    TIPO_RELATORIO_CHOICES = [
        ('UMIDADE', 'Relatório de Umidade'),
        ('PROTEINA', 'Relatório de Proteína'),
        ('COMBINADO', 'Relatório Combinado'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome do Relatório")
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
    ativo = models.BooleanField(default=True, verbose_name="Relatório Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_relatorio_display()})"
    
    class Meta:
        verbose_name = "Configuração de Relatório"
        verbose_name_plural = "Configurações de Relatórios"