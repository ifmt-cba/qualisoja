#!/usr/bin/env python3
"""
Script para testar a análise de teor de óleo com a fórmula corrigida
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseTeorOleo

def teste_teor_oleo():
    """Testa a análise de teor de óleo com dados de exemplo"""
    
    print("=== TESTE DE ANÁLISE DE TEOR DE ÓLEO ===")
    print("Fórmula: (peso_liquido - peso_tara) / peso_amostra * 100")
    print()
    
    # Dados de teste
    dados_teste = [
        {
            'peso_amostra': Decimal('2.000'),
            'peso_tara': Decimal('15.000'),      # Recipiente vazio
            'peso_liquido': Decimal('15.200'),   # Recipiente com óleo
            'esperado': Decimal('10.00')         # (15.200 - 15.000) / 2.000 * 100 = 10%
        },
        {
            'peso_amostra': Decimal('2.500'),
            'peso_tara': Decimal('20.000'),      # Recipiente vazio
            'peso_liquido': Decimal('20.125'),   # Recipiente com óleo
            'esperado': Decimal('5.00')          # (20.125 - 20.000) / 2.500 * 100 = 5%
        },
        {
            'peso_amostra': Decimal('2.250'),
            'peso_tara': Decimal('18.500'),      # Recipiente vazio
            'peso_liquido': Decimal('18.675'),   # Recipiente com óleo
            'esperado': Decimal('7.78')          # (18.675 - 18.500) / 2.250 * 100 = 7.78%
        }
    ]
    
    for i, dados in enumerate(dados_teste, 1):
        print(f"--- Teste {i} ---")
        print(f"Peso da amostra: {dados['peso_amostra']} g")
        print(f"Peso da tara (vazio): {dados['peso_tara']} g")
        print(f"Peso líquido (tara + óleo): {dados['peso_liquido']} g")
        print(f"Óleo extraído: {dados['peso_liquido'] - dados['peso_tara']} g")
        print(f"Teor esperado: {dados['esperado']}%")
        
        # Criar análise
        analise = AnaliseTeorOleo(
            tipo_amostra='FL',
            peso_amostra=dados['peso_amostra'],
            peso_tara=dados['peso_tara'],
            peso_liquido=dados['peso_liquido']
        )
        
        # Salvar (vai calcular automaticamente)
        analise.save()
        
        print(f"Teor calculado: {analise.teor_oleo}%")
        
        # Verificar se está correto
        if analise.teor_oleo == dados['esperado']:
            print("✅ CORRETO!")
        else:
            print(f"❌ ERRO! Esperado: {dados['esperado']}, Calculado: {analise.teor_oleo}")
        
        print()
        
        # Limpar teste
        analise.delete()
    
    print("=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    teste_teor_oleo()
