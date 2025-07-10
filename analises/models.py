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
        raise ValidationError("A data não pode estar no futuro.")


class BaseModel(models.Model):
    """
    Modelo base que contém campos e métodos comuns a todos os modelos.
    """

    criado_em = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação", null=True, blank=True
    )
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização", null=True, blank=True
    )

    class Meta:
        abstract = True


class AnaliseUmidade(BaseModel):
    """
    Modelo para armazenar análises de umidade na soja.
    """

    TIPO_AMOSTRA_CHOICES = [
        ("FG", "Farelo Grosso"),
        ("FF", "Farelo Fino"),
        ("SI", "Soja Industrializada"),
        ("PE", "Peletizado"),
    ]

    data = models.DateField(
        verbose_name="Data da Análise",
        default=timezone.localdate,
        validators=[validate_not_future_date],
    )
    horario = models.TimeField(verbose_name="Horário da Análise")
    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default="FG",  # Farelo Grosso como padrão
    )
    tara = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Tara"
    )
    liquido = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Líquido"
    )
    peso_amostra = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Peso da Amostra"
    )
    resultado = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Resultado"
    )
    fator_correcao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fator de Correção",
        validators=[MinValueValidator(-1000), MaxValueValidator(1000)],
    )

    def __str__(self):
        return f"Análise de Umidade - {self.get_tipo_amostra_display()} - {self.data}"

    class Meta:
        verbose_name = "Análise de Umidade"
        verbose_name_plural = "Análises de Umidade"
        ordering = ["-data", "-horario"]


class AnaliseProteina(BaseModel):
    TIPO_AMOSTRA_CHOICES = [
        ("FL", "Farelo"),
        ("SI", "Soja Industrializada"),
        ("FP", "Fábrica parada"),
        ("SA", "Sem amostra"),
    ]

    data = models.DateField(
        verbose_name="Data da Análise",
        default=timezone.localdate,
        validators=[validate_not_future_date],
    )
    horario = models.TimeField(verbose_name="Horário da Análise")
    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default="FL",
    )
    peso_amostra = models.DecimalField(
        max_digits=6,  # Aceita até 9999.99
        decimal_places=2,
        verbose_name="Peso da Amostra (g)",
        validators=[MinValueValidator(0.0)],
        default=Decimal("0.00"),
    )
    ml_gasto = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="mL Amostra",
        default=Decimal("0.00"),
    )
    ml_branco = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="mL Branco",
        help_text="Valor do branco, entre 0 e 0.5",
        validators=[MinValueValidator(0.0), MaxValueValidator(0.5)],
        default=Decimal("0.00"),
    )
    normalidade = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        verbose_name="Normalidade do titulante (N)",
        help_text="O valor máximo de normalidade é 0.3 N.",
        validators=[MinValueValidator(0.0), MaxValueValidator(Decimal("0.3"))],
        default=Decimal("0.00"),
    )
    resultado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Resultado (%)",
        default=Decimal("0.00"),
    )
    resultado_corrigido = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Resultado Corrigido (%)",
        default=Decimal("0.00"),
    )
    eh_media_24h = models.BooleanField(default=False, verbose_name="É média de 24h?")

    def _to_decimal(self, val):
        if val is None:
            return Decimal("0")
        if isinstance(val, Decimal):
            return val
        if isinstance(val, str):
            val = val.replace(",", ".")
        return Decimal(str(val))

    def calcular_proteina(self, umidade_percentual):
        """Calcula a proteína bruta e a proteína corrigida pela umidade."""
        try:
            ml_amostra = self._to_decimal(self.ml_gasto)
            ml_branco = self._to_decimal(self.ml_branco)
            N = self._to_decimal(self.normalidade)
            peso_g = self._to_decimal(self.peso_amostra)  # Peso da amostra em gramas
            umidade = self._to_decimal(umidade_percentual)

            logger.info(
                f"ml_amostra={ml_amostra}, ml_branco={ml_branco}, N={N}, peso_g={peso_g}, umidade={umidade}"
            )

            if peso_g <= 0:
                logger.warning("Peso da amostra inválido. Cálculo impossível.")
                return Decimal("0.00"), Decimal("0.00")

            # Calcula o percentual de nitrogênio
            percentual_nitrogenio = (
                (ml_amostra - ml_branco) * N * Decimal("14.007")
            ) / (peso_g * 10)
            # Calcula a proteína bruta
            proteina_bruta = percentual_nitrogenio * Decimal("6.25")

            if umidade == 0 or umidade >= 100:
                proteina_corrigida = proteina_bruta
            else:
                proteina_corrigida = (proteina_bruta * 100) / (Decimal("100") - umidade)

            self.resultado = proteina_bruta.quantize(Decimal("0.01"))
            self.resultado_corrigido = proteina_corrigida.quantize(Decimal("0.01"))

            logger.info(
                f"Resultado calculado: resultado={self.resultado}, resultado_corrigido={self.resultado_corrigido}"
            )
            return self.resultado, self.resultado_corrigido
        except Exception as e:
            logger.error(f"Erro no cálculo de proteína: {e}")
            self.resultado = Decimal("0.00")
            self.resultado_corrigido = Decimal("0.00")
            return self.resultado, self.resultado_corrigido


class AnaliseOleoDegomado(BaseModel):
    """
    Modelo para armazenar análises de óleo degomado de soja.
    """

    TIPO_AMOSTRA_CHOICES = [
        ("CR", "Óleo Cru"),
        ("DG", "Óleo Degomado"),
        ("RF", "Óleo Refinado"),
        ("RS", "Resíduo"),
    ]
    TIPO_ANALISE_CHOICES = [
        ("UMI", "Análise de Umidade"),
        ("ACI", "Análise de Acidez"),
        ("SAB", "Análise de Sabões"),
    ]

    data = models.DateField(
        verbose_name="Data da Análise",
        default=timezone.localdate,
        validators=[validate_not_future_date],
    )
    horario = models.TimeField(verbose_name="Horário da Análise")
    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default="DG",  # Óleo Degomado como padrão
    )
    tipo_analise = models.CharField(
        max_length=3,
        choices=TIPO_ANALISE_CHOICES,
        verbose_name="Tipo de Análise",
        default="ACI",
    )
    tara = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name="Tara"
    )
    liquido = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name="Líquido"
    )
    peso_amostra = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0.0"),
        verbose_name="Peso da Amostra",
    )
    resultado = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Resultado"
    )
    titulacao = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name="Titulação"
    )
    fator_correcao = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Fator de Correção",
        validators=[MinValueValidator(-1000), MaxValueValidator(1000)],
    )

    def __str__(self):
        return f"Análise de Óleo Degomado - {self.get_tipo_amostra_display()} - {self.data}"

    class Meta:
        verbose_name = "Análise de Óleo Degomado"
        verbose_name_plural = "Análises de Óleo Degomado"
        ordering = ["-data", "-horario"]


class AnaliseUrase(BaseModel):
    """
    Modelo para armazenar análises de urase na soja.
    """

    TIPO_AMOSTRA_CHOICES = [
        ("FL", "Farelo"),
        ("SI", "Soja Industrializada"),
        ("PE", "Peletizado"),
    ]

    data = models.DateField(
        verbose_name="Data da Análise",
        default=timezone.localdate,
        validators=[validate_not_future_date],
    )
    horario = models.TimeField(verbose_name="Horário da Análise")
    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default="FL",
    )
    amostra_1 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amostra 1",
        help_text="Valor da primeira amostra",
    )
    amostra_2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amostra 2",
        help_text="Valor da segunda amostra",
    )
    resultado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Resultado",
        blank=True,
        null=True,
        help_text="Resultado calculado automaticamente (Amostra 1 - Amostra 2)",
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
        ordering = ["-data", "-horario"]
