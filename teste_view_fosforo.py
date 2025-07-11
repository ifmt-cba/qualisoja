#!/usr/bin/env python
"""
Testar view de listagem de fósforo
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
from django.test import RequestFactory

def testar_view():
    """Testar a view de listagem"""
    print("=== TESTANDO VIEW DE LISTAGEM ===")
    
    try:
        # Verificar dados no banco
        total = AnaliseFosforo.objects.count()
        print(f"Total de registros no banco: {total}")
        
        if total == 0:
            print("❌ Nenhum registro encontrado no banco!")
            return False
        
        # Listar alguns registros
        registros = AnaliseFosforo.objects.all()[:3]
        for reg in registros:
            print(f"Registro ID {reg.id}:")
            print(f"  Data: {reg.data}")
            print(f"  Horário: {reg.horario}")
            print(f"  Resultado: {reg.resultado}")
            print(f"  Formatado: {reg.get_resultado_formatado()}")
        
        # Testar a view
        factory = RequestFactory()
        request = factory.get('/analises/fosforo/')
        
        view = FosforoListView()
        view.request = request
        view.object_list = view.get_queryset()
        
        context = view.get_context_data()
        object_list = context['object_list']
        
        print(f"\nContext da view:")
        print(f"  object_list count: {len(object_list)}")
        print(f"  Primeiro objeto: {object_list[0] if object_list else 'Nenhum'}")
        
        return len(object_list) > 0
        
    except Exception as e:
        print(f"❌ Erro ao testar view: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if testar_view():
        print("\n✅ View funcionando corretamente!")
    else:
        print("\n❌ Problema na view")
