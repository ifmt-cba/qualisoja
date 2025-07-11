#!/usr/bin/env python
"""
Teste completo da listagem de fósforo
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo
from decimal import Decimal
from django.db import connection

def teste_completo():
    """Teste completo da funcionalidade"""
    print("=== TESTE COMPLETO FÓSFORO ===")
    
    try:
        # Limpar dados antigos
        AnaliseFosforo.objects.all().delete()
        print("✅ Dados limpos")
        
        # Criar registros de teste com diferentes resultados
        registros = [
            {
                'absorbancia_amostra': Decimal('0.050'),  # Resultado baixo (ótimo)
                'peso_amostra': Decimal('1.0000'),
                'concentracao_padrao': Decimal('10.0'),
                'volume_solucao': Decimal('100.0'),
                'volume_aliquota': Decimal('10.0'),
                'absorbancia_padrao': Decimal('0.200'),
                'casas_decimais': 0,
                'tipo_amostra': 'FL'
            },
            {
                'absorbancia_amostra': Decimal('0.100'),  # Resultado médio (bom)
                'peso_amostra': Decimal('1.0000'),
                'concentracao_padrao': Decimal('10.0'),
                'volume_solucao': Decimal('100.0'),
                'volume_aliquota': Decimal('10.0'),
                'absorbancia_padrao': Decimal('0.200'),
                'casas_decimais': 0,
                'tipo_amostra': 'FL'
            },
            {
                'absorbancia_amostra': Decimal('0.200'),  # Resultado alto (ruim)
                'peso_amostra': Decimal('1.0000'),
                'concentracao_padrao': Decimal('10.0'),
                'volume_solucao': Decimal('100.0'),
                'volume_aliquota': Decimal('10.0'),
                'absorbancia_padrao': Decimal('0.200'),
                'casas_decimais': 0,
                'tipo_amostra': 'FL'
            }
        ]
        
        for i, dados in enumerate(registros):
            analise = AnaliseFosforo(**dados)
            analise.save()
            print(f"✅ Registro {i+1} criado: ID {analise.id}")
            print(f"   Resultado: {analise.resultado}")
            print(f"   Formatado: {analise.get_resultado_formatado()}")
            print(f"   Avaliação: {analise.get_avaliacao()}")
            print()
        
        # Verificar total de registros
        total = AnaliseFosforo.objects.count()
        print(f"✅ Total de registros: {total}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if teste_completo():
        print("\n🎉 Teste completo concluído!")
        print("A listagem deve funcionar agora com dados de teste.")
        print("Acesse: http://127.0.0.1:8000/analises/fosforo/")
    else:
        print("\n❌ Falha no teste completo")
