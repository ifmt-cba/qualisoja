#!/usr/bin/env python
"""
Teste simples para verificar se o modelo AnaliseFosforo está funcionando
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from decimal import Decimal
from analises.models import AnaliseFosforo

def teste_simples():
    print("=== TESTE SIMPLES MODELO FÓSFORO ===")
    
    try:
        # Criar uma análise simples
        analise = AnaliseFosforo(
            absorbancia_amostra=Decimal('0.000025'),
            casas_decimais=0
        )
        analise.save()
        
        print(f"✅ Análise criada com ID: {analise.id}")
        print(f"✅ Resultado: {analise.resultado}")
        print(f"✅ Resultado formatado: {analise.get_resultado_formatado()}")
        print(f"✅ Casas decimais: {analise.casas_decimais}")
        
        # Limpar
        analise.delete()
        print("✅ Análise removida")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if teste_simples():
        print("\n🎉 Modelo funcionando corretamente!")
    else:
        print("\n💥 Problema encontrado no modelo!")
