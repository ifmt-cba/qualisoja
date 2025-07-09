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
    horario = models.TimeField(
        verbose_name="Horário da Análise", default=timezone.localtime().time()
    )
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
    horario = models.TimeField(
        verbose_name="Horário da Análise", default=timezone.localtime().time()
    )
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
        validators=[MinValueValidator(0.01)],
        blank=True,
        null=True,
    )
    ml_gasto = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="mL Amostra", blank=True, null=True
    )
    ml_branco = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="mL Branco",
        help_text="Valor do branco, entre 0 e 0.5",
        validators=[MinValueValidator(0.0), MaxValueValidator(0.5)],
        blank=True,
        null=True,
    )
    normalidade = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        verbose_name="Normalidade do titulante (N)",
        help_text="O valor máximo de normalidade é 0.3 N.",
        validators=[MinValueValidator(0.0), MaxValueValidator(Decimal("0.3"))],
        blank=True,
        null=True,
    )
    resultado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Resultado (%)",
        blank=True,
        null=True,
    )
    resultado_corrigido = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Resultado Corrigido (%)",
        blank=True,
        null=True,
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
            umidade_percentual = self._to_decimal(umidade_percentual)

            logger.info(
                f"ml_amostra={ml_amostra}, ml_branco={ml_branco}, N={N}, peso_g={peso_g}, umidade={umidade_percentual}"
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

            if umidade_percentual is None or umidade_percentual == 0:
                proteina_corrigida = proteina_bruta
            else:
                proteina_corrigida = (proteina_bruta * 100) / (
                    Decimal("100") - umidade_percentual
                )

            def safe_quantize(val):
                try:
                    return val.quantize(Decimal("0.01"))
                except Exception:
                    return Decimal("0.00")

            self.resultado = proteina_bruta
            self.resultado_corrigido = proteina_corrigida

            logger.info(
                f"Resultado calculado: resultado={self.resultado}, resultado_corrigido={self.resultado_corrigido}"
            )
            return self.resultado, self.resultado_corrigido
        except Exception as e:
            logger.error(f"Erro no cálculo de proteína: {e}")

            self.resultado = Decimal("0.00")
            self.resultado_corrigido = Decimal("0.00")
            return self.resultado, self.resultado_corrigido

    def clean(self):
        """
        Garante que resultado e resultado_corrigido sejam Decimal válidos ou None.
        """

        from decimal import Decimal, InvalidOperation

        for field in ["resultado", "resultado_corrigido"]:
            val = getattr(self, field)
            if val is not None:
                try:
                    # Tenta converter para Decimal
                    setattr(self, field, Decimal(str(val)))
                except (InvalidOperation, ValueError, TypeError):
                    setattr(self, field, None)

    def _validate_decimal_field(self, field_name, max_value=Decimal("99999.99")):
        """
        Valida e quantiza um campo Decimal, definindo-o como None se inválido ou fora do intervalo [0, max_value].
        """

        value = getattr(self, field_name)
        if value is not None:
            try:
                value = Decimal(str(value))
                if value < 0 or value > max_value:
                    setattr(self, field_name, None)
                else:
                    setattr(self, field_name, value.quantize(Decimal("0.01")))
            except (InvalidOperation, ValueError, TypeError):
                setattr(self, field_name, None)

    def save(self, *args, **kwargs):
        """
        Calcula a proteína (se todos os dados necessários estiverem disponíveis),
        limpa e valida os campos decimais antes de salvar.
        """
        if (
            self.ml_gasto is not None
            and self.ml_branco is not None
            and self.peso_amostra
            and self.normalidade
        ):
            # Assumindo umidade zero para o cálculo inicial; ajuste conforme necessário
            self.calcular_proteina(umidade_percentual=0)
        self.clean()  # Limpeza para garantir que os decimais sejam válidos

        # Validação dos campos resultado
        self._validate_decimal_field("resultado")
        self._validate_decimal_field("resultado_corrigido")
        super().save(*args, **kwargs)


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
        ("OP", "Óleo Produção"),
        ("OE", "Óleo Expedição"),
    ]

    TIPO_ANALISE_CHOICES = [
        ("UMI", "Analise de Umidade"),
        ("ACI", "Analise de Acidez"),
        ("SAB", "Analise de Sabões"),
    ]

    data = models.DateField(
        verbose_name="Data da Análise",
        default=timezone.localdate,
        validators=[validate_not_future_date],
    )

    horario = models.TimeField(
        verbose_name="Horário da Análise", default=timezone.localtime().time()
    )

    tipo_amostra = models.CharField(
        max_length=2,
        choices=TIPO_AMOSTRA_CHOICES,
        verbose_name="Tipo de Amostra",
        default="OP",  # Oleo de Produção como padrão
    )

    tipo_analise = models.CharField(
        max_length=3,
        choices=TIPO_ANALISE_CHOICES,
        verbose_name="Tipo de Analise",
        default="UMI",  # Analise de Umidade como padrão
    )

    tara = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Tara"
    )
    liquido = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Líquido"
    )
    peso_amostra = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Peso da Amostra"
    )
    resultado = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Resultado"
    )
    titulacao = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Titulação"
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
        return f"Análise de Oleo Degomado - {self.get_tipo_amostra_display()} - {self.data}"

    def save(self, *args, **kwargs):
        """
        Calcula o resultado automaticamente com base no tipo de análise
        antes de salvar o objeto.
        """
        # Garante que os valores sejam Decimais para o cálculo, tratando Nones
        tara = self.tara or Decimal("0")
        liquido = self.liquido or Decimal("0")
        peso_amostra = self.peso_amostra or Decimal("0")
        titulacao = self.titulacao or Decimal("0")
        fator_correcao = self.fator_correcao or Decimal("0")

        resultado_calculado = None

        if self.tipo_analise == "UMI":
            if peso_amostra > 0:
                resultado_calculado = (
                    ((tara + peso_amostra) - liquido) / peso_amostra * 100
                )

        elif self.tipo_analise == "ACI":
            if peso_amostra > 0:
                resultado_calculado = (
                    titulacao * fator_correcao * Decimal("28.2") * 100
                ) / peso_amostra

        elif self.tipo_analise == "SAB":
            if peso_amostra > 0:
                resultado_calculado = (
                    titulacao * fator_correcao * Decimal("300.4") * 100
                ) / peso_amostra

        if resultado_calculado is not None:
            self.resultado = resultado_calculado.quantize(Decimal("0.01"))

        super().save(*args, **kwargs)


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
    horario = models.TimeField(
        verbose_name="Horário da Análise", default=timezone.localtime().time()
    )
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
