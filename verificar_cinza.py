#!/usr/bin/env python
"""
Script para verificar dados de análise de cinza
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseCinza
from decimal import Decimal

def verificar_cinza():
    """Verifica os dados de cinza"""
    print("🔍 VERIFICANDO ANÁLISES DE CINZA\n")
    
    total = AnaliseCinza.objects.count()
    print(f"📊 Total de análises: {total}")
    
    if total == 0:
        print("❌ Nenhuma análise encontrada!")
        print("💡 Vamos criar dados de teste...")
        criar_dados_teste()
        return
    
    print("\n📋 Dados encontrados:")
    for i, analise in enumerate(AnaliseCinza.objects.all().order_by('-id')[:5], 1):
        print(f"\n{i}. Análise ID: {analise.id}")
        print(f"   Data: {analise.data}")
        print(f"   Tipo: {analise.get_tipo_amostra_display()}")
        print(f"   Peso amostra: {analise.peso_amostra}g")
        print(f"   Peso cadinho: {analise.peso_cadinho}g")
        print(f"   Peso cinza: {analise.peso_cinza}g")
        print(f"   Resultado (campo): {analise.resultado}")
        
        # Verificar cálculo
        if all([analise.peso_amostra, analise.peso_cadinho, analise.peso_cinza]):
            try:
                resultado_calc = ((analise.peso_cinza - analise.peso_cadinho) / analise.peso_amostra) * 100
                print(f"   Resultado calculado: {resultado_calc:.2f}%")
                
                if analise.resultado is None:
                    print("   ⚠️ PROBLEMA: Campo resultado está NULL!")
                elif abs(float(analise.resultado) - float(resultado_calc)) > 0.01:
                    print(f"   ⚠️ PROBLEMA: Resultado no campo ({analise.resultado}) difere do calculado ({resultado_calc:.2f})")
                else:
                    print("   ✅ Cálculo correto")
            except Exception as e:
                print(f"   ❌ Erro no cálculo: {e}")
        else:
            print("   ❌ Dados incompletos para cálculo")

def criar_dados_teste():
    """Cria dados de teste para cinza"""
    print("\n📝 CRIANDO DADOS DE TESTE...")
    
    dados_teste = [
        {
            'tipo_amostra': 'FL',
            'peso_amostra': Decimal('2.0000'),
            'peso_cadinho': Decimal('15.2000'),
            'peso_cinza': Decimal('15.3000'),  # 0.1g de cinza = 5% 
        },
        {
            'tipo_amostra': 'SI', 
            'peso_amostra': Decimal('1.5000'),
            'peso_cadinho': Decimal('12.1000'),
            'peso_cinza': Decimal('12.1450'),  # 0.045g de cinza = 3%
        },
        {
            'tipo_amostra': 'FL',
            'peso_amostra': Decimal('2.5000'),
            'peso_cadinho': Decimal('18.0000'),
            'peso_cinza': Decimal('18.1750'),  # 0.175g de cinza = 7%
        }
    ]
    
    criados = 0
    for i, dados in enumerate(dados_teste, 1):
        try:
            analise = AnaliseCinza.objects.create(**dados)
            print(f"✅ Análise {i} criada:")
            print(f"   ID: {analise.id}")
            print(f"   Resultado: {analise.resultado}%")
            criados += 1
        except Exception as e:
            print(f"❌ Erro ao criar análise {i}: {e}")
    
    print(f"\n📊 {criados} análises criadas com sucesso!")

def main():
    """Função principal"""
    verificar_cinza()
    print("\n" + "="*50)
    print("🌐 Acesse: http://127.0.0.1:8000/analises/cinza/list/")

if __name__ == "__main__":
    main()
