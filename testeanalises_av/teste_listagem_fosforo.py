#!/usr/bin/env python
"""
Teste da listagem de fósforo
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo
from analises.views import FosforoListView

def testar_listagem():
    """Testar se a listagem funciona"""
    print("=== TESTANDO LISTAGEM DE FÓSFORO ===")
    
    try:
        # Verificar registros no banco
        registros = AnaliseFosforo.objects.all()
        print(f"Total de registros: {registros.count()}")
        
        # Testar cada registro
        for analise in registros:
            print(f"\nTeste registro ID {analise.id}:")
            try:
                resultado = analise.resultado
                print(f"  Resultado: {resultado}")
                
                formatado = analise.get_resultado_formatado()
                print(f"  Formatado: {formatado}")
                
                avaliacao = analise.get_avaliacao()
                print(f"  Avaliação: {avaliacao}")
                
                print(f"  ✅ Registro OK")
                
            except Exception as e:
                print(f"  ❌ Erro no registro: {e}")
        
        # Testar view
        view = FosforoListView()
        view.model = AnaliseFosforo
        
        queryset = view.get_queryset()
        print(f"\nQueryset da view: {queryset.count()} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na listagem: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if testar_listagem():
        print("\n🎉 Listagem funcionando corretamente!")
    else:
        print("\n❌ Problema na listagem")
