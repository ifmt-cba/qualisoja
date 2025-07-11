#!/usr/bin/env python
"""
Script para limpar dados de fósforo e recriar tabela
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from django.db import connection
from decimal import Decimal

def resetar_tabela():
    """Reset completo da tabela de fósforo"""
    print("=== RESETANDO TABELA DE FÓSFORO ===")
    
    try:
        with connection.cursor() as cursor:
            # Limpar completamente a tabela
            cursor.execute("DELETE FROM analises_analisefosforo")
            print("✅ Tabela limpa")
            
            # Reset do auto increment
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='analises_analisefosforo'")
            print("✅ Auto increment resetado")
        
        # Criar um registro de teste
        from analises.models import AnaliseFosforo
        
        analise = AnaliseFosforo.objects.create(
            absorbancia_amostra=Decimal('0.000100'),
            peso_amostra=Decimal('1.0000'),
            concentracao_padrao=Decimal('10.0000'),
            volume_solucao=Decimal('100.00'),
            volume_aliquota=Decimal('10.00'),
            absorbancia_padrao=Decimal('0.250000'),
            casas_decimais=0,
            tipo_amostra='FL'
        )
        
        print(f"✅ Registro criado: ID {analise.id}")
        print(f"   Resultado: {analise.resultado}")
        print(f"   Formatado: {analise.get_resultado_formatado()}")
        
        # Verificar se a listagem funciona
        total = AnaliseFosforo.objects.count()
        print(f"✅ Total de registros: {total}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if resetar_tabela():
        print("\n🎉 Tabela resetada com sucesso!")
        print("Agora tente acessar: http://127.0.0.1:8000/analises/fosforo/")
    else:
        print("\n❌ Falha ao resetar tabela")
