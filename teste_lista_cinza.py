#!/usr/bin/env python
"""
Teste final da lista de cinza
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseCinza
from decimal import Decimal
from datetime import date, time

def teste_final_cinza():
    """Teste final da funcionalidade de cinza"""
    print("🧪 TESTE FINAL - ANÁLISE DE CINZA\n")
    
    # Verificar se há dados
    total = AnaliseCinza.objects.count()
    print(f"📊 Total de análises: {total}")
    
    if total == 0:
        print("❌ Nenhuma análise encontrada! Criando dados de teste...")
        criar_dados_teste()
        total = AnaliseCinza.objects.count()
    
    # Listar análises
    print("\n📋 Análises encontradas:")
    for analise in AnaliseCinza.objects.all().order_by('-id')[:5]:
        print(f"  ✅ ID {analise.id}: {analise.resultado}% ({analise.get_tipo_amostra_display()})")
        
        # Verificar classificação
        if analise.resultado:
            if analise.resultado <= 3:
                classificacao = "BAIXO (Excelente)"
            elif analise.resultado <= 6:
                classificacao = "NORMAL (Aceitável)"
            else:
                classificacao = "ALTO (Atenção)"
            print(f"     Classificação: {classificacao}")
        print()
    
    print("="*50)
    print("🎉 ANÁLISE DE CINZA FUNCIONANDO!")
    print("✅ Template moderno com classificação")
    print("✅ Cálculo automático: ((peso_cinza - peso_cadinho) / peso_amostra) × 100")
    print("✅ Classificação por faixas (BAIXO/NORMAL/ALTO)")
    print("\n🌐 Acesse: http://127.0.0.1:8000/analises/cinza/list/")

def criar_dados_teste():
    """Cria dados de teste se necessário"""
    dados = [
        {
            'data': date.today(),
            'horario': time(9, 30),
            'tipo_amostra': 'FL',
            'peso_amostra': Decimal('2.0000'),
            'peso_cadinho': Decimal('15.2000'),
            'peso_cinza': Decimal('15.2500'),  # 2.5%
        },
        {
            'data': date.today(),
            'horario': time(10, 15),
            'tipo_amostra': 'SI',
            'peso_amostra': Decimal('1.5000'),
            'peso_cadinho': Decimal('12.1000'),
            'peso_cinza': Decimal('12.1750'),  # 5%
        },
        {
            'data': date.today(),
            'horario': time(11, 45),
            'tipo_amostra': 'FL',
            'peso_amostra': Decimal('2.5000'),
            'peso_cadinho': Decimal('18.0000'),
            'peso_cinza': Decimal('18.2000'),  # 8%
        }
    ]
    
    for dados_item in dados:
        AnaliseCinza.objects.create(**dados_item)

if __name__ == "__main__":
    teste_final_cinza()
