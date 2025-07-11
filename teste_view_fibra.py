#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qualisoja.settings")
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from analises.views import FibraListView
from analises.models import AnaliseFibra

print("=== Teste da View FibraListView ===")

# Verificar dados na tabela
count = AnaliseFibra.objects.count()
print(f"Total de registros na tabela: {count}")

# Testar a view diretamente
try:
    # Criar uma requisição fake
    factory = RequestFactory()
    request = factory.get('/analises/fibra/')
    request.user = AnonymousUser()
    
    # Instanciar a view
    view = FibraListView.as_view()
    response = view(request)
    
    print(f"✅ View executou com sucesso!")
    print(f"   Status code: {response.status_code}")
    print(f"   Template usado: {getattr(response, 'template_name', 'N/A')}")
    
    # Verificar context
    if hasattr(response, 'context_data'):
        context = response.context_data
        analises = context.get('analises', [])
        object_list = context.get('object_list', [])
        print(f"   Contexto 'analises': {len(analises) if analises else 0} itens")
        print(f"   Contexto 'object_list': {len(object_list) if object_list else 0} itens")
    
except Exception as e:
    print(f"❌ Erro na view: {e}")
    import traceback
    traceback.print_exc()

# Testar com Client (simulação mais completa)
print("\n=== Teste com Django Client ===")
try:
    client = Client()
    response = client.get('/analises/fibra/')
    print(f"✅ Client request executado!")
    print(f"   Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"   Página carregou com sucesso!")
    else:
        print(f"   Erro na página: {response.content.decode()[:200]}...")
        
except Exception as e:
    print(f"❌ Erro no client: {e}")
    import traceback
    traceback.print_exc()
