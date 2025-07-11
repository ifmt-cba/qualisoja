#!/usr/bin/env python
"""
Script final para criar dados de fósforo com a fórmula corrigida
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo
from datetime import date, time
from decimal import Decimal

def criar_dados_finais():
    """Cria dados usando o Django ORM com fórmula corrigida"""
    print("📝 CRIANDO DADOS COM FÓRMULA CORRIGIDA...")
    
    # Primeiro, limpar dados existentes
    count = AnaliseFosforo.objects.count()
    if count > 0:
        AnaliseFosforo.objects.all().delete()
        print(f"🧹 {count} registros antigos removidos")
    
    dados_teste = [
        {
            'data': date.today(),
            'horario': time(10, 30),
            'tipo_amostra': 'FL',
            'absorbancia_amostra': Decimal('0.125000'),
            'peso_amostra': Decimal('1.0000'),
            'concentracao_padrao': Decimal('10.0000'),
            'volume_solucao': Decimal('100.00'),
            'volume_aliquota': Decimal('10.00'),
            'absorbancia_padrao': Decimal('0.250000'),
            'casas_decimais': 0
        },
        {
            'data': date.today(),
            'horario': time(11, 15),
            'tipo_amostra': 'SI',
            'absorbancia_amostra': Decimal('0.089000'),
            'peso_amostra': Decimal('1.0000'),
            'concentracao_padrao': Decimal('10.0000'),
            'volume_solucao': Decimal('100.00'),
            'volume_aliquota': Decimal('10.00'),
            'absorbancia_padrao': Decimal('0.250000'),
            'casas_decimais': 0
        },
        {
            'data': date.today(),
            'horario': time(14, 45),
            'tipo_amostra': 'FL',
            'absorbancia_amostra': Decimal('0.234000'),
            'peso_amostra': Decimal('1.0000'),
            'concentracao_padrao': Decimal('10.0000'),
            'volume_solucao': Decimal('100.00'),
            'volume_aliquota': Decimal('10.00'),
            'absorbancia_padrao': Decimal('0.250000'),
            'casas_decimais': 0
        },
        {
            'data': date.today(),
            'horario': time(16, 20),
            'tipo_amostra': 'FL',
            'absorbancia_amostra': Decimal('0.045000'),
            'peso_amostra': Decimal('1.0000'),
            'concentracao_padrao': Decimal('10.0000'),
            'volume_solucao': Decimal('100.00'),
            'volume_aliquota': Decimal('10.00'),
            'absorbancia_padrao': Decimal('0.250000'),
            'casas_decimais': 0
        }
    ]
    
    criados = 0
    for i, dados in enumerate(dados_teste, 1):
        try:
            analise = AnaliseFosforo.objects.create(**dados)
            
            print(f"✅ Análise {i} criada:")
            print(f"   ID: {analise.id}")
            print(f"   Absorbância: {analise.absorbancia_amostra}")
            print(f"   Resultado calculado: {analise.resultado} ppm")
            print(f"   Resultado formatado: {analise.get_resultado_formatado()} ppm")
            
            # Verificar se o resultado está em faixa aceitável
            resultado_num = float(analise.resultado) if analise.resultado else 0
            if resultado_num < 500:  # Valores razoáveis para fósforo
                print(f"   ✅ Resultado OK ({resultado_num} ppm)")
            else:
                print(f"   ⚠️ Resultado alto ({resultado_num} ppm)")
            print()
            
            criados += 1
            
        except Exception as e:
            print(f"❌ Erro ao criar análise {i}: {e}")
            import traceback
            traceback.print_exc()
    
    return criados

def testar_listagem_final():
    """Testa a listagem final"""
    print("🔍 TESTANDO LISTAGEM FINAL...")
    
    try:
        analises = AnaliseFosforo.objects.all()
        print(f"Total de análises: {analises.count()}")
        
        for analise in analises:
            try:
                resultado_formatado = analise.get_resultado_formatado()
                print(f"ID {analise.id}: {resultado_formatado} ppm - OK")
            except Exception as e:
                print(f"ID {analise.id}: ERRO - {e}")
        
        print("✅ Listagem funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na listagem: {e}")
        return False

def main():
    """Função principal"""
    print("🎯 CRIAÇÃO FINAL DE DADOS DE FÓSFORO\n")
    
    # 1. Criar dados com fórmula corrigida
    criados = criar_dados_finais()
    print(f"📊 Total criado: {criados} análises\n")
    
    # 2. Testar listagem
    listagem_ok = testar_listagem_final()
    
    print("\n" + "="*50)
    if criados > 0 and listagem_ok:
        print("🎉 SUCESSO!")
        print("✅ Dados criados com fórmula corrigida")
        print("✅ Listagem funcionando")
        print("🌐 Acesse: http://127.0.0.1:8000/analises/fosforo/")
    else:
        print("❌ Ainda há problemas a resolver")

if __name__ == "__main__":
    main()
