#!/usr/bin/env python
"""
Script para testar o template de fósforo e identificar onde está o erro
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo
from django.template import Template, Context
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

def testar_modelo():
    """Testa o modelo e métodos"""
    print("🔍 TESTANDO MODELO...")
    
    try:
        analises = AnaliseFosforo.objects.all()
        print(f"Total de análises: {analises.count()}")
        
        for analise in analises[:3]:
            print(f"\nAnálise ID: {analise.id}")
            print(f"  Data: {analise.data}")
            print(f"  Resultado raw: {analise.resultado}")
            print(f"  Tipo do resultado: {type(analise.resultado)}")
            
            # Testar método get_resultado_formatado
            try:
                formatado = analise.get_resultado_formatado()
                print(f"  Resultado formatado: {formatado}")
            except Exception as e:
                print(f"  ERRO no formatado: {e}")
                import traceback
                traceback.print_exc()
            
            # Testar floatformat diretamente
            try:
                from django.template.defaultfilters import floatformat
                float_formatted = floatformat(analise.resultado, 0)
                print(f"  Floatformat: {float_formatted}")
            except Exception as e:
                print(f"  ERRO no floatformat: {e}")
                import traceback
                traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no modelo: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_template():
    """Testa o template"""
    print("\n🎨 TESTANDO TEMPLATE...")
    
    try:
        # Criar request fake
        factory = RequestFactory()
        request = factory.get('/analises/fosforo/')
        request.user = AnonymousUser()
        
        # Buscar dados
        analises = AnaliseFosforo.objects.all()[:3]
        
        # Template mínimo para teste
        template_content = """
        <h1>Teste Template</h1>
        <p>Total: {{ object_list|length }}</p>
        {% for analise in object_list %}
        <div>
            ID: {{ analise.id }} - 
            Resultado: {{ analise.resultado }} - 
            Formatado: {{ analise.resultado|floatformat:0 }}
        </div>
        {% endfor %}
        """
        
        template = Template(template_content)
        context = Context({
            'object_list': analises,
            'request': request
        })
        
        rendered = template.render(context)
        print("✅ Template renderizado com sucesso!")
        print("Resultado:")
        print(rendered)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no template: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_view():
    """Testa a view"""
    print("\n🔧 TESTANDO VIEW...")
    
    try:
        from analises.views import FosforoListView
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/analises/fosforo/')
        request.user = AnonymousUser()
        
        view = FosforoListView()
        view.request = request
        view.setup(request)
        
        # Testar get_queryset
        queryset = view.get_queryset()
        print(f"Queryset count: {queryset.count()}")
        
        # Testar get_context_data
        context = view.get_context_data()
        print(f"Context object_list count: {len(context.get('object_list', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na view: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🐛 DIAGNÓSTICO DETALHADO DE FÓSFORO\n")
    
    # 1. Testar modelo
    modelo_ok = testar_modelo()
    
    # 2. Testar template
    template_ok = testar_template()
    
    # 3. Testar view
    view_ok = testar_view()
    
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES:")
    print(f"  Modelo: {'✅' if modelo_ok else '❌'}")
    print(f"  Template: {'✅' if template_ok else '❌'}")
    print(f"  View: {'✅' if view_ok else '❌'}")
    
    if all([modelo_ok, template_ok, view_ok]):
        print("\n🎯 Tudo funcionando! O problema pode ser no servidor ou navegador.")
    else:
        print("\n🔍 Identifique e corrija os erros acima.")

if __name__ == "__main__":
    main()
