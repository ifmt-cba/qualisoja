#!/usr/bin/env python3
"""
Script para testar o salvamento de análises de teor de óleo através do formulário
"""

from analises.forms import AnaliseTeorOleoForm
from analises.models import AnaliseTeorOleo
import os
import sys
import django
from decimal import Decimal
from datetime import date, time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()


def teste_formulario():
    """Testa o formulário de teor de óleo"""

    print("=== TESTE DO FORMULÁRIO DE TEOR DE ÓLEO ===")

    # Dados de teste válidos
    dados_teste = {
        'data': date.today(),
        'horario': time(16, 0),
        'tipo_amostra': 'FL',
        'peso_amostra': Decimal('2.250'),
        'peso_tara': Decimal('25.000'),      # Recipiente vazio
        'peso_liquido': Decimal('25.180'),   # Recipiente com óleo
        'observacoes': 'Teste via formulário'
    }

    print("Dados de teste:")
    for key, value in dados_teste.items():
        print(f"  {key}: {value}")

    # Criar formulário
    form = AnaliseTeorOleoForm(data=dados_teste)

    print(f"\nFormulário válido: {form.is_valid()}")

    if not form.is_valid():
        print("Erros encontrados:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    else:
        print("Formulário válido! Tentando salvar...")

        # Salvar
        analise = form.save()
        print(f"Análise salva com ID: {analise.pk}")
        print(f"Teor de óleo calculado: {analise.teor_oleo}%")

        # Verificar se está na lista
        total = AnaliseTeorOleo.objects.count()
        print(f"Total de análises no banco: {total}")

        # Listar todas
        print("\nTodas as análises:")
        for a in AnaliseTeorOleo.objects.all():
            print(f"  - ID: {a.pk}, Data: {a.data}, Teor: {a.teor_oleo}%")


def teste_salvamento_direto():
    """Testa salvamento direto no modelo"""

    print("\n=== TESTE DE SALVAMENTO DIRETO ===")

    # Criar nova análise
    analise = AnaliseTeorOleo(
        data=date.today(),
        horario=time(17, 0),
        tipo_amostra='FL',
        peso_amostra=Decimal('2.100'),
        peso_tara=Decimal('18.000'),
        peso_liquido=Decimal('18.120'),
        observacoes='Teste salvamento direto'
    )

    print(f"Antes de salvar - Teor: {analise.teor_oleo}")

    # Salvar
    analise.save()

    print(f"Depois de salvar - ID: {analise.pk}, Teor: {analise.teor_oleo}%")

    # Verificar total
    total = AnaliseTeorOleo.objects.count()
    print(f"Total no banco: {total}")


if __name__ == "__main__":
    # Limpar análises existentes para teste limpo
    AnaliseTeorOleo.objects.all().delete()
    print("Análises anteriores removidas para teste limpo")

    # Executar testes
    teste_formulario()
    teste_salvamento_direto()

    print("\n=== RESUMO FINAL ===")
    total = AnaliseTeorOleo.objects.count()
    print(f"Total de análises criadas: {total}")

    if total > 0:
        print("✅ SUCESSO: Análises estão sendo salvas corretamente!")
    else:
        print("❌ ERRO: Nenhuma análise foi salva!")
