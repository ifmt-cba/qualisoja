#!/usr/bin/env python3
"""
Script para verificar se as análises de teor de óleo aparecem na lista
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

def verificar_lista():
    """Verifica se há análises no banco e se estão sendo listadas corretamente"""
    
    print("=== VERIFICAÇÃO DA LISTA DE TEOR DE ÓLEO ===")
    
    # Contar análises
    total = AnaliseTeorOleo.objects.count()
    print(f"Total de análises no banco: {total}")
    
    if total == 0:
        print("Criando análise de teste...")
        
        # Criar análise de teste
        analise = AnaliseTeorOleo.objects.create(
            data=date.today(),
            horario=time(14, 30),
            tipo_amostra='FL',
            peso_amostra=Decimal('2.250'),
            peso_tara=Decimal('20.000'),
            peso_liquido=Decimal('20.150'),
            observacoes='Análise de teste - lista'
        )
        
        print(f"Análise criada com ID: {analise.pk}")
        print(f"Teor de óleo calculado: {analise.teor_oleo}%")
        
        total = AnaliseTeorOleo.objects.count()
        print(f"Novo total: {total}")
    
    # Listar todas as análises ordenadas como na view
    analises = AnaliseTeorOleo.objects.all().order_by('-data', '-horario')
    print(f"\n=== LISTA ORDENADA ===")
    
    for i, analise in enumerate(analises, 1):
        print(f"{i}. ID: {analise.pk}")
        print(f"   Data: {analise.data}")
        print(f"   Horário: {analise.horario}")
        print(f"   Tipo: {analise.get_tipo_amostra_display()}")
        print(f"   Peso amostra: {analise.peso_amostra}g")
        print(f"   Peso tara: {analise.peso_tara}g")
        print(f"   Peso líquido: {analise.peso_liquido}g")
        print(f"   Teor de óleo: {analise.teor_oleo}%")
        print(f"   Observações: {analise.observacoes}")
        print()
    
    if analises.exists():
        print("✅ As análises estão no banco e devem aparecer na lista!")
    else:
        print("❌ Nenhuma análise encontrada no banco.")
    
    print(f"\nURL para acessar: http://127.0.0.1:8000/analises/teor-oleo/")

if __name__ == "__main__":
    verificar_lista()
