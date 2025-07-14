#!/usr/bin/env python
"""
Script para testar os parâmetros obrigatórios nos relatórios de expedição.
Testa tanto lotes de óleo quanto de farelo.
"""

import os
import sys
import django
from datetime import datetime, date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from relatorios.models import Cliente, EspecificacaoContrato, Lote, RelatorioExpedicao
from relatorios.forms import RelatorioExpedicaoForm
from django.contrib.auth.models import User

def test_parametros_obrigatorios():
    print("=== TESTE DE PARÂMETROS OBRIGATÓRIOS ===")
    print()
    
    # Obter cliente e lotes
    cliente = Cliente.objects.filter(codigo='CLI001').first()
    if not cliente:
        print("❌ Cliente de teste não encontrado!")
        return
    
    # Obter lotes de farelo e óleo
    lote_farelo = Lote.objects.filter(codigo__startswith='FAR').first()
    lote_oleo = Lote.objects.filter(codigo__startswith='OLE').first()
    
    if not lote_farelo:
        print("❌ Lote de farelo não encontrado!")
        return
    
    if not lote_oleo:
        print("❌ Lote de óleo não encontrado!")
        return
    
    print(f"✓ Cliente: {cliente.nome}")
    print(f"✓ Lote de farelo: {lote_farelo.codigo}")
    print(f"✓ Lote de óleo: {lote_oleo.codigo}")
    print()
    
    # Teste 1: Relatório com lote de FARELO
    print("=== TESTE 1: LOTE DE FARELO ===")
    form_data_farelo = {
        'usar_cliente_cadastrado': True,
        'cliente': cliente.id,
        'usar_contrato_cadastrado': False,
        'contrato_nome_manual': 'Contrato Teste Farelo',
        'contrato_numero_manual': 'CTF001',
        'lotes': [lote_farelo.id],
        'parametros_incluidos': ['fibra', 'cinza'],  # Parâmetros adicionais
        'data_inicial': date(2025, 7, 1),
        'data_final': date(2025, 7, 31),
        'formato': 'PDF',
        'observacoes_manuais': 'Teste de relatório com lote de farelo'
    }
    
    form_farelo = RelatorioExpedicaoForm(data=form_data_farelo)
    form_farelo.fields['lotes'].queryset = Lote.objects.filter(cliente=cliente)
    
    if form_farelo.is_valid():
        cleaned_data = form_farelo.cleaned_data
        print(f"✓ Parâmetros obrigatórios: {cleaned_data['parametros_obrigatorios']}")
        print(f"✓ Parâmetros incluídos: {cleaned_data['parametros_incluidos']}")
        
        # Verificar se os parâmetros corretos estão incluídos para farelo
        expected_farelo = ['umidade', 'proteina', 'teor_oleo']
        actual_obligatory = cleaned_data['parametros_obrigatorios']
        
        if set(expected_farelo) == set(actual_obligatory):
            print("✅ Parâmetros obrigatórios para FARELO estão corretos!")
        else:
            print(f"❌ Parâmetros obrigatórios incorretos para FARELO")
            print(f"   Esperado: {expected_farelo}")
            print(f"   Atual: {actual_obligatory}")
    else:
        print(f"❌ Formulário inválido para farelo: {form_farelo.errors}")
    
    print()
    
    # Teste 2: Relatório com lote de ÓLEO
    print("=== TESTE 2: LOTE DE ÓLEO ===")
    form_data_oleo = {
        'usar_cliente_cadastrado': True,
        'cliente': cliente.id,
        'usar_contrato_cadastrado': False,
        'contrato_nome_manual': 'Contrato Teste Óleo',
        'contrato_numero_manual': 'CTO001',
        'lotes': [lote_oleo.id],
        'parametros_incluidos': ['fibra', 'cinza'],  # Parâmetros adicionais
        'data_inicial': date(2025, 7, 1),
        'data_final': date(2025, 7, 31),
        'formato': 'PDF',
        'observacoes_manuais': 'Teste de relatório com lote de óleo'
    }
    
    form_oleo = RelatorioExpedicaoForm(data=form_data_oleo)
    form_oleo.fields['lotes'].queryset = Lote.objects.filter(cliente=cliente)
    
    if form_oleo.is_valid():
        cleaned_data = form_oleo.cleaned_data
        print(f"✓ Parâmetros obrigatórios: {cleaned_data['parametros_obrigatorios']}")
        print(f"✓ Parâmetros incluídos: {cleaned_data['parametros_incluidos']}")
        
        # Verificar se os parâmetros corretos estão incluídos para óleo
        expected_oleo = ['umidade', 'acidez', 'indice_sabao', 'silica', 'fosforo', 'urase']
        actual_obligatory = cleaned_data['parametros_obrigatorios']
        
        if set(expected_oleo) == set(actual_obligatory):
            print("✅ Parâmetros obrigatórios para ÓLEO estão corretos!")
        else:
            print(f"❌ Parâmetros obrigatórios incorretos para ÓLEO")
            print(f"   Esperado: {expected_oleo}")
            print(f"   Atual: {actual_obligatory}")
    else:
        print(f"❌ Formulário inválido para óleo: {form_oleo.errors}")
    
    print()
    
    # Teste 3: Relatório misto (farelo + óleo)
    print("=== TESTE 3: LOTES MISTOS (FARELO + ÓLEO) ===")
    form_data_misto = {
        'usar_cliente_cadastrado': True,
        'cliente': cliente.id,
        'usar_contrato_cadastrado': False,
        'contrato_nome_manual': 'Contrato Teste Misto',
        'contrato_numero_manual': 'CTM001',
        'lotes': [lote_farelo.id, lote_oleo.id],
        'parametros_incluidos': ['fibra'],  # Parâmetro adicional
        'data_inicial': date(2025, 7, 1),
        'data_final': date(2025, 7, 31),
        'formato': 'PDF',
        'observacoes_manuais': 'Teste de relatório com lotes mistos'
    }
    
    form_misto = RelatorioExpedicaoForm(data=form_data_misto)
    form_misto.fields['lotes'].queryset = Lote.objects.filter(cliente=cliente)
    
    if form_misto.is_valid():
        cleaned_data = form_misto.cleaned_data
        print(f"✓ Parâmetros obrigatórios: {cleaned_data['parametros_obrigatorios']}")
        print(f"✓ Parâmetros incluídos: {cleaned_data['parametros_incluidos']}")
        
        # Para lotes mistos, deve priorizar farelo (se houver farelo, usa parâmetros de farelo)
        expected_misto = ['umidade', 'proteina', 'teor_oleo']  # Parâmetros de farelo
        actual_obligatory = cleaned_data['parametros_obrigatorios']
        
        if set(expected_misto) == set(actual_obligatory):
            print("✅ Parâmetros obrigatórios para LOTES MISTOS estão corretos!")
            print("   (Prioriza parâmetros de farelo quando há lotes mistos)")
        else:
            print(f"❌ Parâmetros obrigatórios incorretos para LOTES MISTOS")
            print(f"   Esperado: {expected_misto}")
            print(f"   Atual: {actual_obligatory}")
    else:
        print(f"❌ Formulário inválido para lotes mistos: {form_misto.errors}")

def verificar_analises_disponiveis():
    print("\n=== VERIFICAÇÃO DE ANÁLISES DISPONÍVEIS ===")
    from analises.models import (
        AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado,
        AnaliseFosforo, AnaliseTeorOleo, AnaliseFibra, AnaliseCinza,
        AnaliseUrase, AnaliseSilica
    )
    
    data_teste = date(2025, 7, 13)
    print(f"📅 Data de teste: {data_teste}")
    print()
    
    analises_info = [
        ('Umidade', AnaliseUmidade),
        ('Proteína', AnaliseProteina),
        ('Óleo Degomado', AnaliseOleoDegomado),
        ('Fósforo', AnaliseFosforo),
        ('Teor Óleo', AnaliseTeorOleo),
        ('Fibra', AnaliseFibra),
        ('Cinza', AnaliseCinza),
        ('Urase', AnaliseUrase),
        ('Sílica', AnaliseSilica),
    ]
    
    for nome, model in analises_info:
        count = model.objects.filter(data=data_teste).count()
        status = "✅" if count > 0 else "❌"
        print(f"{status} {nome}: {count} análise(s)")

def main():
    print("🧪 TESTE DE PARÂMETROS OBRIGATÓRIOS - RELATÓRIO DE EXPEDIÇÃO")
    print("=" * 70)
    
    verificar_analises_disponiveis()
    test_parametros_obrigatorios()
    
    print("\n" + "=" * 70)
    print("🎯 RESUMO DOS TESTES:")
    print("• Parâmetros para FARELO: umidade, proteína, teor_oleo")
    print("• Parâmetros para ÓLEO: umidade, acidez, indice_sabao, silica, fosforo, urase")
    print("• Lotes mistos: prioriza parâmetros de farelo")
    print("\n✨ Execute este script para verificar se a implementação está correta!")

if __name__ == "__main__":
    main()
