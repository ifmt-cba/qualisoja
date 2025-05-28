"""
Testes para o módulo de análises do QualiSoja.
"""
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import AnaliseUmidade, AnaliseProteina, ConfiguracaoRelatorio
from datetime import timedelta, date


class AnaliseUmidadeModelTest(TestCase):
    """Testes para o modelo de análise de umidade."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.data_hoje = timezone.localdate()
        self.data_anterior = self.data_hoje - timedelta(days=1)
        
        self.analise = AnaliseUmidade.objects.create(
            data=self.data_anterior,
            tipo_amostra='FG',
            peso_amostra=Decimal('100.0'),
            resultado=Decimal('12.5')
        )

    def test_criacao_analise(self):
        """Testa se a análise foi criada corretamente."""
        self.assertEqual(self.analise.tipo_amostra, 'FG')
        self.assertEqual(self.analise.peso_amostra, Decimal('100.0'))
        self.assertEqual(self.analise.resultado, Decimal('12.5'))

    def test_data_futura_invalida(self):
        """Testa se data futura é rejeitada."""
        data_futura = self.data_hoje + timedelta(days=1)
        analise_invalida = AnaliseUmidade(
            data=data_futura,
            tipo_amostra='FG',
            peso_amostra=Decimal('100.0')
        )
        
        with self.assertRaises(ValidationError):
            analise_invalida.full_clean()


class AnaliseProteinaModelTest(TestCase):
    """Testes para o modelo de análise de proteína."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.data_hoje = timezone.localdate()
        self.data_anterior = self.data_hoje - timedelta(days=1)
        
        self.analise = AnaliseProteina.objects.create(
            data=self.data_anterior,
            tipo_amostra='FL',
            peso_amostra=Decimal('0.50'),
            ml_gasto=Decimal('25.5'),
            resultado=Decimal('46.5'),
            resultado_corrigido=Decimal('47.0')
        )

    def test_criacao_analise(self):
        """Testa se a análise foi criada corretamente."""
        self.assertEqual(self.analise.tipo_amostra, 'FL')
        self.assertEqual(self.analise.peso_amostra, Decimal('0.50'))
        self.assertEqual(self.analise.ml_gasto, Decimal('25.5'))
        self.assertEqual(self.analise.resultado, Decimal('46.5'))
        self.assertEqual(self.analise.resultado_corrigido, Decimal('47.0'))

    def test_data_futura_invalida(self):
        """Testa se data futura é rejeitada."""
        data_futura = self.data_hoje + timedelta(days=1)
        analise_invalida = AnaliseProteina(
            data=data_futura,
            tipo_amostra='FL',
            peso_amostra=Decimal('0.50')
        )
        
        with self.assertRaises(ValidationError):
            analise_invalida.full_clean()


class ConfiguracaoRelatorioModelTest(TestCase):
    """Testes para o modelo de configuração de relatório."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.config = ConfiguracaoRelatorio.objects.create(
            nome="Relatório Semanal de Umidade",
            tipo_relatorio="UMIDADE",
            periodo_padrao=7
        )

    def test_criacao_config(self):
        """Testa se a configuração foi criada corretamente."""
        self.assertEqual(self.config.nome, "Relatório Semanal de Umidade")
        self.assertEqual(self.config.tipo_relatorio, "UMIDADE")
        self.assertEqual(self.config.periodo_padrao, 7)
        self.assertTrue(self.config.ativo)
