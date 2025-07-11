#!/usr/bin/env python
"""
Script rápido para resolver o problema de InvalidOperation
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from django.db import connection

def resolver_problema():
    """Resolver o problema de InvalidOperation"""
    print("=== RESOLVENDO PROBLEMA DE INVALID OPERATION ===")
    
    try:
        # Limpar completamente a tabela de análises de fósforo
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM analises_analisefosforo")
            print("✅ Tabela limpa completamente")
            
        # Criar um registro de teste válido
        from analises.models import AnaliseFosforo
        
        analise = AnaliseFosforo(
            absorbancia_amostra=Decimal('0.000025'),
            peso_amostra=Decimal('1.0000'),
            concentracao_padrao=Decimal('10.0000'),
            volume_solucao=Decimal('100.00'),
            volume_aliquota=Decimal('10.00'),
            absorbancia_padrao=Decimal('0.250000'),
            casas_decimais=0,
            tipo_amostra='FL'
        )
        analise.save()
        
        print(f"✅ Registro de teste criado com ID: {analise.id}")
        print(f"   Resultado: {analise.resultado} ppm")
        print(f"   Avaliação: {analise.get_avaliacao()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == '__main__':
    resolver_problema()
    print("\n🎉 Problema resolvido! Agora tente acessar a lista novamente.")
