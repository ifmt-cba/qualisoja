from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
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
        ('FP', 'Fábrica Parada'),
        ('SA', 'Sem Amostra'),
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
        ('FP', 'Fábrica Parada'),
        ('SA', 'Sem Amostra'),
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
        ('FP', 'Fábrica Parada'),
        ('SA', 'Sem Amostra'),
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
    
    peso_tara = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        verbose_name="Peso da Tara (g)",
        help_text="Peso do recipiente vazio (antes da extração)"
    )
    
    peso_liquido = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        verbose_name="Peso Líquido (g)",
        help_text="Peso do recipiente com óleo extraído (após extração)"
    )

    teor_oleo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Teor de Óleo (%)",
        blank=True,
        null=True,
        help_text="Calculado automaticamente: (Peso_liquido - Peso_tara) / Peso_amostra * 100"
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
        
        if self.peso_liquido and self.peso_tara and self.peso_liquido < self.peso_tara:
            raise ValidationError({'peso_liquido': 'O peso líquido (tara + óleo) deve ser maior que o peso da tara vazia.'})
        
        if self.peso_tara and self.peso_tara <= 0:
            raise ValidationError({'peso_tara': 'O peso da tara deve ser maior que zero.'})

    def save(self, *args, **kwargs):
        """
        Calcula automaticamente o teor de óleo (%).
        Fórmula: Teor = (peso_liquido - peso_tara) / peso_amostra * 100
        """
        if (self.peso_tara is not None and 
            self.peso_liquido is not None and 
            self.peso_amostra is not None and 
            self.peso_amostra != 0):
            
            self.teor_oleo = round(
                ((self.peso_liquido - self.peso_tara) / self.peso_amostra) * Decimal('100'),
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
        ('FP', 'Fábrica Parada'),
        ('SA', 'Sem Amostra'),
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
    peso_tara = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Tara (g)",
        validators=[MinValueValidator(0.0001)]
    )
    peso_fibra = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Fibra (g)",
        validators=[MinValueValidator(0.0001)]
    )
    peso_branco = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso do Branco (g)",
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
        if self.peso_amostra and self.peso_tara and self.peso_fibra and self.peso_branco:
            # Fórmula: (peso_tara - peso_fibra - peso_branco) / peso_amostra * 100
            self.resultado = ((self.peso_tara - self.peso_fibra - self.peso_branco) / self.peso_amostra) * 100
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
    Fórmula: Fósforo (ppm) = (Aa × Cp × V × 1000 × 1000) / (P × VAl × Ap)
    O usuário insere apenas a absorbância da amostra, os outros valores são padrões.
    """
    TIPO_AMOSTRA_CHOICES = [
        ('FL', 'Farelo'),
        ('SI', 'Soja Industrializada'),
        ('FP', 'Fábrica Parada'),
        ('SA', 'Sem Amostra'),
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
    
    # Campo principal que o usuário preenche
    absorbancia_amostra = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name="Absorbância da Amostra",
        validators=[MinValueValidator(0.000001)],
        help_text="Digite apenas o valor da absorbância lida no equipamento"
    )
    
    # Campos com valores padrão que podem ser ajustados se necessário
    peso_amostra = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        verbose_name="Peso da Amostra (g)",
        default=Decimal('1.0000'),
        validators=[MinValueValidator(0.0001)],
        help_text="Peso da amostra em gramas (padrão: 1.0000g)"
    )
    concentracao_padrao = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        verbose_name="Concentração Padrão (mg/L)",
        default=Decimal('10.0000'),
        validators=[MinValueValidator(0.0001)],
        help_text="Concentração do padrão em mg/L (padrão: 10.0000)"
    )
    volume_solucao = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Volume da Solução (mL)",
        default=Decimal('100.00'),
        validators=[MinValueValidator(0.01)],
        help_text="Volume da solução em mL (padrão: 100.00)"
    )
    volume_aliquota = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Volume da Alíquota (mL)",
        default=Decimal('10.00'),
        validators=[MinValueValidator(0.01)],
        help_text="Volume da alíquota em mL (padrão: 10.00)"
    )
    absorbancia_padrao = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name="Absorbância do Padrão",
        default=Decimal('0.250000'),
        validators=[MinValueValidator(0.000001)],
        help_text="Absorbância do padrão (padrão: 0.250000)"
    )
    
    # Resultado calculado automaticamente
    resultado = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Fósforo (ppm)",
        help_text="Resultado calculado automaticamente usando a fórmula: (Aa × Cp × V × 1000 × 1000) / (P × VAl × Ap)"
    )
    
    # Campo para controlar as casas decimais do resultado
    casas_decimais = models.IntegerField(
        default=0,
        verbose_name="Casas Decimais",
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        help_text="Número de casas decimais para exibir o resultado (0-6). 0 = número inteiro"
    )
    
    def save(self, *args, **kwargs):
        """
        Calcular resultado automaticamente usando a fórmula corrigida:
        Fósforo (ppm) = ((Aa/Ap) × Cp × (V/VAl)) / P
        """
        if self.absorbancia_amostra:
            try:
                # Converter todos os valores para Decimal para precisão
                aa = Decimal(str(self.absorbancia_amostra))
                cp = Decimal(str(self.concentracao_padrao))
                v = Decimal(str(self.volume_solucao))
                p = Decimal(str(self.peso_amostra))
                val = Decimal(str(self.volume_aliquota))
                ap = Decimal(str(self.absorbancia_padrao))
                
                # Fórmula corrigida: ((Aa/Ap) × Cp × (V/VAl)) / P
                if ap != 0 and val != 0 and p != 0:
                    concentracao_aliquota = (aa / ap) * cp  # mg/L na alíquota
                    concentracao_original = concentracao_aliquota * (v / val)  # mg/L na solução original
                    resultado_calculado = concentracao_original / p  # mg/g = ppm
                    
                    # Arredondar para 3 casas decimais para armazenamento
                    self.resultado = resultado_calculado.quantize(Decimal('0.001'))
                else:
                    self.resultado = None
                    
            except (ValueError, TypeError, AttributeError, Exception) as e:
                logger.error(f"Erro no cálculo de fósforo: {e}")
                self.resultado = None
                
        super().save(*args, **kwargs)
    
    def get_resultado_formatado(self):
        """Retorna o resultado formatado com as casas decimais configuradas"""
        try:
            if self.resultado is None:
                return "0"
            
            # Garantir que temos um valor válido para casas_decimais
            casas = 0
            if hasattr(self, 'casas_decimais') and self.casas_decimais is not None:
                casas = int(self.casas_decimais)
            
            # Converter para Decimal com proteção
            if isinstance(self.resultado, Decimal):
                valor = self.resultado
            else:
                valor = Decimal(str(self.resultado))
            
            # Formatar conforme as casas decimais
            if casas == 0:
                # Arredondar para inteiro
                return str(int(valor.quantize(Decimal('1'))))
            else:
                # Formatar com casas decimais específicas
                formato = '0.' + '0' * casas
                return str(valor.quantize(Decimal(formato)))
                
        except Exception as e:
            logger.error(f"Erro ao formatar resultado: {e}")
            return "0"
    
    def __str__(self):
        return f"Análise de Fósforo - {self.get_tipo_amostra_display()} - {self.data}"
    
    class Meta:
        verbose_name = "Análise de Fósforo"
        verbose_name_plural = "Análises de Fósforo"
        ordering = ['-data', '-horario']