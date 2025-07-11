#!/usr/bin/env python
"""
Script para criar dados de teste de cinza
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

def criar_dados_cinza():
    """Cria dados de teste para análise de cinza"""
    print("📝 CRIANDO DADOS DE TESTE DE CINZA...")
    
    # Limpar dados existentes
    count_old = AnaliseCinza.objects.count()
    if count_old > 0:
        AnaliseCinza.objects.all().delete()
        print(f"🧹 {count_old} registros antigos removidos")
    
    dados_teste = [
        {
            'data': date.today(),
            'horario': time(9, 30),
            'tipo_amostra': 'FL',
            'peso_amostra': Decimal('2.0000'),
            'peso_cadinho': Decimal('15.2000'),
            'peso_cinza': Decimal('15.3000'),  # Diferença: 0.1g = 5%
        },
        {
            'data': date.today(),
            'horario': time(10, 15),
            'tipo_amostra': 'SI', 
            'peso_amostra': Decimal('1.5000'),
            'peso_cadinho': Decimal('12.1000'),
            'peso_cinza': Decimal('12.1450'),  # Diferença: 0.045g = 3%
        },
        {
            'data': date.today(),
            'horario': time(11, 45),
            'tipo_amostra': 'FL',
            'peso_amostra': Decimal('2.5000'),
            'peso_cadinho': Decimal('18.0000'),
            'peso_cinza': Decimal('18.1750'),  # Diferença: 0.175g = 7%
        },
        {
            'data': date.today(),
            'horario': time(14, 20),
            'tipo_amostra': 'SI',
            'peso_amostra': Decimal('1.8000'),
            'peso_cadinho': Decimal('16.5000'),
            'peso_cinza': Decimal('16.5720'),  # Diferença: 0.072g = 4%
        }
    ]
    
    criados = 0
    for i, dados in enumerate(dados_teste, 1):
        try:
            analise = AnaliseCinza.objects.create(**dados)
            
            print(f"✅ Análise {i} criada:")
            print(f"   ID: {analise.id}")
            print(f"   Tipo: {analise.get_tipo_amostra_display()}")
            print(f"   Peso amostra: {analise.peso_amostra}g")
            print(f"   Peso cadinho: {analise.peso_cadinho}g")
            print(f"   Peso cinza: {analise.peso_cinza}g")
            print(f"   Resultado: {analise.resultado}%")
            
            # Verificar cálculo manual
            resultado_manual = ((analise.peso_cinza - analise.peso_cadinho) / analise.peso_amostra) * 100
            print(f"   Cálculo manual: {resultado_manual:.2f}%")
            print()
            
            criados += 1
            
        except Exception as e:
            print(f"❌ Erro ao criar análise {i}: {e}")
            import traceback
            traceback.print_exc()
    
    return criados

def testar_listagem():
    """Testa a listagem de cinza"""
    print("🔍 TESTANDO LISTAGEM...")
    
    try:
        analises = AnaliseCinza.objects.all()
        print(f"Total na listagem: {analises.count()}")
        
        for analise in analises:
            print(f"ID {analise.id}: Resultado = {analise.resultado}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na listagem: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 CRIAÇÃO DE DADOS DE TESTE - ANÁLISE DE CINZA\n")
    
    # 1. Criar dados
    criados = criar_dados_cinza()
    print(f"📊 Total criado: {criados} análises\n")
    
    # 2. Testar listagem
    listagem_ok = testar_listagem()
    
    print("\n" + "="*50)
    if criados > 0 and listagem_ok:
        print("🎉 DADOS CRIADOS COM SUCESSO!")
        print("✅ Resultados calculados automaticamente")
        print("🌐 Acesse: http://127.0.0.1:8000/analises/cinza/list/")
    else:
        print("❌ Houve problemas na criação dos dados")

if __name__ == "__main__":
    main()
