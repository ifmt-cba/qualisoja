#!/usr/bin/env python
"""
Script para limpar e recriar dados de fósforo com proteção contra InvalidOperation
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
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def limpar_dados():
    """Remove todos os dados de fósforo"""
    print("🧹 Limpando dados existentes...")
    
    try:
        count = AnaliseFosforo.objects.count()
        AnaliseFosforo.objects.all().delete()
        print(f"✅ {count} análises removidas")
        return True
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")
        return False

def criar_dados_limpos():
    """Cria dados de teste com valores seguros"""
    print("📝 Criando dados de teste...")
    
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
            analise = AnaliseFosforo(**dados)
            analise.save()  # Isso vai calcular o resultado automaticamente
            
            print(f"✅ Análise {i} criada:")
            print(f"   ID: {analise.id}")
            print(f"   Absorbância: {analise.absorbancia_amostra}")
            print(f"   Resultado: {analise.resultado}")
            print(f"   Formatado: {analise.get_resultado_formatado()} ppm")
            print()
            
            criados += 1
            
        except Exception as e:
            print(f"❌ Erro ao criar análise {i}: {e}")
            import traceback
            traceback.print_exc()
    
    return criados

def testar_listagem():
    """Testa a listagem"""
    print("🔍 Testando listagem...")
    
    try:
        analises = AnaliseFosforo.objects.all().order_by('-id')
        print(f"✅ {analises.count()} análises encontradas")
        
        for analise in analises:
            try:
                resultado = analise.get_resultado_formatado()
                print(f"   ID {analise.id}: {resultado} ppm")
            except Exception as e:
                print(f"   ID {analise.id}: ERRO - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na listagem: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 LIMPEZA E RECRIAÇÃO DE DADOS DE FÓSFORO\n")
    
    # 1. Limpar dados existentes
    if not limpar_dados():
        return
    
    print()
    
    # 2. Criar dados seguros
    criados = criar_dados_limpos()
    print(f"📊 Total criado: {criados} análises\n")
    
    # 3. Testar listagem
    testar_listagem()
    
    print("\n" + "="*50)
    print("🎯 PROCESSO CONCLUÍDO!")
    print("✅ Agora acesse: http://127.0.0.1:8000/analises/fosforo/")
    print("💡 Os dados devem aparecer na lista sem erros.")

if __name__ == "__main__":
    main()
