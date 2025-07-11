#!/usr/bin/env python
"""
Teste rápido para verificar se o template está correto
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from django.template import Template, Context
from django.template.loader import get_template
from analises.models import AnaliseFosforo

def testar_template():
    """Teste do template lista_fosforo.html"""
    print("=== TESTE DE TEMPLATE ===")
    
    try:
        # Carregar o template
        template = get_template('app/lista_fosforo.html')
        print("✅ Template carregado com sucesso!")
        
        # Criar contexto vazio para teste
        context = Context({
            'object_list': [],
            'messages': []
        })
        
        # Renderizar template
        html = template.render(context)
        print("✅ Template renderizado com sucesso!")
        print("✅ Problema de sintaxe corrigido!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no template: {e}")
        return False

if __name__ == '__main__':
    testar_template()
