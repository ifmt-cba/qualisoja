#!/usr/bin/env python3
"""
Script para testar criação de análise de teor de óleo
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date, time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseTeorOleo

def criar_analise_teste():
    """Cria uma análise de teor de óleo para teste"""
    
    print("=== CRIANDO ANÁLISE DE TEOR DE ÓLEO ===")
    
    # Criar análise
    analise = AnaliseTeorOleo(
        data=date.today(),
        horario=time(14, 30),
        tipo_amostra='FL',
        peso_amostra=Decimal('2.000'),
        peso_tara=Decimal('15.000'),
        peso_liquido=Decimal('15.200'),
        observacoes='Teste de criação de análise'
    )
    
    print(f"Antes de salvar - Teor de óleo: {analise.teor_oleo}")
    
    # Salvar (vai calcular automaticamente)
    analise.save()
    
    print(f"Depois de salvar - Teor de óleo: {analise.teor_oleo}%")
    print(f"ID da análise: {analise.pk}")
    
    # Verificar se está no banco
    total = AnaliseTeorOleo.objects.count()
    print(f"Total de análises no banco: {total}")
    
    # Listar todas as análises
    analises = AnaliseTeorOleo.objects.all()
    print(f"Análises encontradas: {analises.count()}")
    
    for a in analises:
        print(f"- ID: {a.pk}, Data: {a.data}, Teor: {a.teor_oleo}%")
    
    return analise

if __name__ == "__main__":
    criar_analise_teste()
