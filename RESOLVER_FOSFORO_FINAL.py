#!/usr/bin/env python
"""
SCRIPT FINAL - Execute este arquivo para resolver definitivamente
"""
import os
import sys
import django
from datetime import datetime, time
from decimal import Decimal

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo

def criar_dados_teste():
    """Criar dados de teste válidos"""
    print("🧹 Limpando dados antigos...")
    AnaliseFosforo.objects.all().delete()
    
    print("✨ Criando novos dados...")
    
    # Dados simples e válidos
    dados = [
        {'abs': '0.020', 'hora': '14:00', 'desc': 'ÓTIMO (< 80 ppm)'},
        {'abs': '0.030', 'hora': '15:00', 'desc': 'BOM (80-180 ppm)'},
        {'abs': '0.050', 'hora': '16:00', 'desc': 'RUIM (> 180 ppm)'},
    ]
    
    for i, dado in enumerate(dados, 1):
        analise = AnaliseFosforo(
            data=datetime.now().date(),
            horario=time(int(dado['hora'][:2]), 0),
            tipo_amostra='FL',
            peso_amostra=Decimal('1.0000'),
            absorbancia_amostra=Decimal(dado['abs']),
            concentracao_padrao=Decimal('10.0000'),
            volume_solucao=Decimal('100.00'),
            volume_aliquota=Decimal('10.00'),
            absorbancia_padrao=Decimal('0.250000'),
            casas_decimais=0
        )
        analise.save()
        
        print(f"✅ Registro {i}: ID {analise.id}")
        print(f"   Absorbância: {analise.absorbancia_amostra}")
        print(f"   Resultado: {analise.resultado} ppm")
        print(f"   Formatado: {analise.get_resultado_formatado()} ppm")
        print(f"   Avaliação: {analise.get_avaliacao()}")
        print(f"   Descrição: {dado['desc']}")
        print()
    
    total = AnaliseFosforo.objects.count()
    print(f"🎯 Total de registros criados: {total}")
    
    return total > 0

if __name__ == '__main__':
    print("=" * 50)
    print("RESOLUÇÃO DEFINITIVA - LISTA DE FÓSFORO")
    print("=" * 50)
    
    try:
        if criar_dados_teste():
            print("🎉 SUCESSO!")
            print()
            print("Agora:")
            print("1. Inicie o servidor: python manage.py runserver")
            print("2. Acesse: http://127.0.0.1:8000/analises/fosforo/")
            print("3. Você deve ver 3 análises na lista!")
        else:
            print("❌ FALHA na criação dos dados")
            
    except Exception as e:
        print(f"💥 ERRO: {e}")
        import traceback
        traceback.print_exc()
        
    print()
    print("=" * 50)
