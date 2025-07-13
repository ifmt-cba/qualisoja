"""
Testes para o módulo de análises do QualiSoja.
"""

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import AnaliseUmidade, AnaliseProteina
from datetime import date, timedelta


class AnaliseUmidadeModelTest(TestCase):
    """Testes para o modelo de análise de umidade."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.data_hoje = timezone.localdate()
        self.data_anterior = self.data_hoje - timedelta(days=1)

        self.analise = AnaliseUmidade.objects.create(
            data=self.data_anterior,
            tipo_amostra="FG",
            peso_amostra=Decimal("100.0"),
            resultado=Decimal("12.5"),
        )

    def test_criacao_analise(self):
        """Testa se a análise foi criada corretamente."""
        self.assertEqual(self.analise.tipo_amostra, "FG")
        self.assertEqual(self.analise.peso_amostra, Decimal("100.0"))
        self.assertEqual(self.analise.resultado, Decimal("12.5"))

    def test_data_futura_invalida(self):
        """Testa se data futura é rejeitada."""
        data_futura = self.data_hoje + timedelta(days=1)
        analise_invalida = AnaliseUmidade(
            data=data_futura, tipo_amostra="FG", peso_amostra=Decimal("100.0")
        )
        with self.assertRaises(ValidationError):
            analise_invalida.full_clean()


class AnaliseProteinaModelTest(TestCase):
    """Testes para o modelo de análise de proteína."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.data_hoje = timezone.localdate()

    def test_calcular_proteina_cenarios(self):
        """Testa o método calcular_proteina com diferentes cenários."""
        # Cenário 1: Cálculo padrão com valores realistas e sem umidade
        analise1 = AnaliseProteina(
            peso_amostra=Decimal("0.5"),
            ml_gasto=Decimal("14.80"),
            ml_branco=Decimal("0.1"),
            normalidade=Decimal("0.1015"),
        )
        resultado_bruto, resultado_corrigido = analise1.calcular_proteina(
            umidade_percentual=0
        )

        # Resultado esperado: ((14.80 - 0.1) * 0.1015 * 14.007) / (0.5 * 10) * 6.25 = 26.12
        self.assertAlmostEqual(resultado_bruto, Decimal("26.12"), places=2)
        self.assertAlmostEqual(
            resultado_corrigido, Decimal("26.12"), places=2
        )  # Sem umidade, deve ser igual

        # Cenário 2: Cálculo com correção de umidade
        analise2 = AnaliseProteina(
            peso_amostra=Decimal("0.5"),
            ml_gasto=Decimal("14.80"),
            ml_branco=Decimal("0.1"),
            normalidade=Decimal("0.1015"),
        )
        resultado_bruto, resultado_corrigido = analise2.calcular_proteina(
            umidade_percentual=Decimal("12.0")
        )

        # Resultado esperado: (26.12 * 100) / (100 - 12) = 29.69
        self.assertAlmostEqual(resultado_bruto, Decimal("26.12"), places=2)
        self.assertAlmostEqual(resultado_corrigido, Decimal("29.69"), places=2)

        # Cenário 3: Edge case com peso da amostra zero
        analise3 = AnaliseProteina(
            peso_amostra=Decimal("0"),
            ml_gasto=Decimal("14.80"),
            ml_branco=Decimal("0.1"),
            normalidade=Decimal("0.1015"),
        )
        resultado_bruto, resultado_corrigido = analise3.calcular_proteina(
            umidade_percentual=0
        )
        self.assertEqual(resultado_bruto, Decimal("0.00"))
        self.assertEqual(resultado_corrigido, Decimal("0.00"))

    def test_data_futura_invalida(self):
        """Testa se data futura é rejeitada."""
        data_futura = self.data_hoje + timedelta(days=1)
        analise_invalida = AnaliseProteina(
            data=data_futura, tipo_amostra="FL", peso_amostra=Decimal("0.50")
        )
        with self.assertRaises(ValidationError):
            analise_invalida.full_clean()
