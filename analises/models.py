from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def validate_not_future_date(value):
    """Valida que uma data não está no futuro."""
    if value > timezone.localdate():
        raise ValidationError('A data não pode estar no futuro.')

class BaseModel(models.Model):
    """
    Modelo base que contém campos e métodos comuns a todos os modelos.
    """
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação", null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização", null=True, blank=True)
    
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

# class AnaliseOleoDegomado(BaseModel):
#     """
#     Modelo para armazenar análises de óleo degomado de soja.
#     """
#     TIPO_AMOSTRA_CHOICES = [
#         ('CR', 'Óleo Cru'),
#         ('DG', 'Óleo Degomado'),
#         ('RF', 'Óleo Refinado'),
#         ('RS', 'Resíduo'),
#     ]
    
#     data = models.DateField(
#         verbose_name="Data da Análise", 
#         default=timezone.localdate,
#         validators=[validate_not_future_date]
#     )
#     horario = models.TimeField(
#         verbose_name="Horário da Análise",
#         default=timezone.localtime().time()
#     )
#     tipo_amostra = models.CharField(
#         max_length=2,
#         choices=TIPO_AMOSTRA_CHOICES,
#         verbose_name="Tipo de Amostra",
#         default='DG'  # Óleo Degomado como padrão
#     )
#     acidez = models.DecimalField(
#         max_digits=6,
#         decimal_places=3,
#         verbose_name="Acidez (mg KOH/g)",
#         blank=True,
#         null=True,
#         validators=[MinValueValidator(0)]
#     )
#     umidade_oleo = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         verbose_name="Umidade do Óleo (%)",
#         blank=True,
#         null=True,
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )
#     impurezas = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         verbose_name="Impurezas (%)",
#         blank=True,
#         null=True,
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )
#     indice_iodo = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         verbose_name="Índice de Iodo (g I₂/100g)",
#         blank=True,
#         null=True,
#         validators=[MinValueValidator(0)]
#     )
#     cor = models.CharField(
#         max_length=10,
#         verbose_name="Cor (Lovibond)",
#         blank=True,
#         null=True
#     )
#     resultado = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         verbose_name="Resultado da Análise (%)",
#         blank=True,
#         null=True,
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )
#     observacoes = models.TextField(
#         verbose_name="Observações",
#         blank=True,
#         null=True,
#         max_length=500
#     )
    
#     def __str__(self):
#         return f"Análise de Óleo Degomado - {self.get_tipo_amostra_display()} - {self.data}"
    
#     class Meta:
#         verbose_name = "Análise de Óleo Degomado"
#         verbose_name_plural = "Análises de Óleo Degomado"
#         ordering = ['-data', '-horario']

# # O modelo ConfiguracaoRelatorio foi removido e suas funcionalidades 
# # foram migradas para o aplicativo 'relatorios'

class AnaliseOleoDegomado(BaseModel):
    """
    Modelo para armazenar análises de Oleo Degomado
    """
    TIPO_AMOSTRA_CHOICES = [
        ('OP', 'Óleo Produção'),
        ('OE', 'Óleo Expedição'),
    ]

    TIPO_ANALISE_CHOICES =[
        ('UMI', 'Analise de Umidade'),
        ('ACI', 'Analise de Acidez'),
        ('SAB', 'Analise de Sabões')
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
        default='OP'  # Oleo de Produção como padrão
    )

    tipo_analise = models.CharField(
        max_length=3,
        choices=TIPO_ANALISE_CHOICES,
        verbose_name="Tipo de Analise",
        default='UMI'  # Analise de Umidade como padrão
    )

    tara = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Tara")
    liquido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Líquido")
    peso_amostra = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Peso da Amostra")
    resultado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Resultado")
    titulacao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Titulação")
    fator_correcao = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="Fator de Correção",
        validators=[MinValueValidator(-1000), MaxValueValidator(1000)]
    )

    def __str__(self):
        return f"Análise de Oleo Degomado - {self.get_tipo_amostra_display()} - {self.data}"

class AnaliseUrase(BaseModel):
    """
    Modelo para armazenar análises de urase na soja.
    """
    TIPO_AMOSTRA_CHOICES = [
        ('FL', 'Farelo'),
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
        default='FL'
    )
    amostra_1 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amostra 1",
        help_text="Valor da primeira amostra"
    )
    amostra_2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amostra 2",
        help_text="Valor da segunda amostra"
    )
    resultado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Resultado",
        blank=True,
        null=True,
        help_text="Resultado calculado automaticamente (Amostra 1 - Amostra 2)"
    )
    
    def save(self, *args, **kwargs):
        """
        Calcula o resultado automaticamente antes de salvar.
        Resultado = Amostra 1 - Amostra 2
        """
        if self.amostra_1 is not None and self.amostra_2 is not None:
            self.resultado = self.amostra_1 - self.amostra_2
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Análise de Urase - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Urase"
        verbose_name_plural = "Análises de Urase"
        ordering = ['-data', '-horario']

class AnaliseCinza(BaseModel):
    """
    Modelo para armazenar análises de cinza na soja.
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
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Amostra (g)",
        validators=[MinValueValidator(0.0001)]
    )
    peso_cadinho = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso do Cadinho (g)",
        validators=[MinValueValidator(0.0001)]
    )
    peso_cinza = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Cinza (g)",
        validators=[MinValueValidator(0.0001)]
    )
    resultado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Resultado (%)"
    )
    
    def save(self, *args, **kwargs):
        """Calcular resultado automaticamente"""
        if self.peso_amostra and self.peso_cadinho and self.peso_cinza:
            self.resultado = ((self.peso_cinza - self.peso_cadinho) / self.peso_amostra) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Análise de Cinza - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Cinza"
        verbose_name_plural = "Análises de Cinza"
        ordering = ['-data', '-horario']


class AnaliseTeorOleo(BaseModel):
    """
    Modelo para armazenar análises de teor de óleo na soja.
    """
    TIPO_AMOSTRA_CHOICES = [
        ('FL', 'Farelo'),
        ('SI', 'Soja Industrializada'),
        ('LE', 'Lex'),
        ('CA', 'Casca'),
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
        max_digits=6,
        decimal_places=3,
        verbose_name="Peso da Amostra (g)",
        help_text="Entre 2,000 g e 2,500 g"
    )
    
    peso_liquido = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        verbose_name="Peso Líquido de Óleo (g)"
    )

    teor_oleo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Teor de Óleo (%)",
        blank=True,
        null=True,
        help_text="Calculado automaticamente: ((L - A) / A) * 100"
    )

    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações",
        help_text="Observações adicionais sobre a análise"
    )

    def clean(self):
        """
        Validação dos valores antes de salvar.
        """
        if self.peso_amostra and not (2.000 <= float(self.peso_amostra) <= 2.500):
            raise ValidationError({'peso_amostra': 'O peso da amostra deve estar entre 2,000 g e 2,500 g.'})
        if self.peso_liquido and self.peso_amostra and self.peso_liquido > self.peso_amostra:
            raise ValidationError({'peso_liquido': 'O peso líquido não pode ser maior que o peso da amostra.'})

    def save(self, *args, **kwargs):
        """
        Calcula automaticamente o teor de óleo (%).
        Fórmula: Teor = ((peso_liquido - peso_amostra) / peso_amostra) * 100
        """
        if self.peso_liquido is not None and self.peso_amostra is not None and self.peso_amostra != 0:
            self.teor_oleo = round(
                ((self.peso_liquido - self.peso_amostra) / self.peso_amostra) * Decimal('100'),
                2
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Análise de Teor de Óleo - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Teor de Óleo"
        verbose_name_plural = "Análises de Teor de Óleo"
        ordering = ['-data', '-horario']


class AnaliseFibra(BaseModel):
    """
    Modelo para armazenar análises de fibra na soja.
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
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Amostra (g)",
        validators=[MinValueValidator(0.0001)]
    )
    peso_fibra = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Fibra (g)",
        validators=[MinValueValidator(0.0001)]
    )
    resultado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Teor de Fibra (%)"
    )
    
    def save(self, *args, **kwargs):
        """Calcular resultado automaticamente"""
        if self.peso_amostra and self.peso_fibra:
            self.resultado = (self.peso_fibra / self.peso_amostra) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Análise de Fibra - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Fibra"
        verbose_name_plural = "Análises de Fibra"
        ordering = ['-data', '-horario']


class AnaliseFosforo(BaseModel):
    """
    Modelo para armazenar análises de fósforo na soja.
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
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Amostra (g)",
        validators=[MinValueValidator(0.0001)]
    )
    volume_titulacao = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Volume de Titulação (mL)",
        validators=[MinValueValidator(0.01)]
    )
    fator_correcao = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Fator de Correção",
        default=1.0000,
        validators=[MinValueValidator(0.0001)]
    )
    resultado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Teor de Fósforo (%)"
    )
    
    def save(self, *args, **kwargs):
        """Calcular resultado automaticamente"""
        if self.peso_amostra and self.volume_titulacao and self.fator_correcao:
            # Fórmula: (Volume × Fator × 0.062 × 100) / Peso da amostra
            self.resultado = (self.volume_titulacao * self.fator_correcao * Decimal('0.062') * 100) / self.peso_amostra
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Análise de Fósforo - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Fósforo"
        verbose_name_plural = "Análises de Fósforo"
        ordering = ['-data', '-horario']