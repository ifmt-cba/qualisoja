#!/usr/bin/env python
"""
Script para verificar e resolver problemas com análises de fósforo
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

def verificar_dados():
    """Verifica os dados existentes"""
    print("=== VERIFICAÇÃO DE DADOS DE FÓSFORO ===")
    
    # Contar total
    total = AnaliseFosforo.objects.count()
    print(f"Total de análises: {total}")
    
    if total == 0:
        print("❌ Nenhuma análise encontrada!")
        return False
    
    # Listar algumas análises
    print("\n📋 Análises existentes:")
    for i, analise in enumerate(AnaliseFosforo.objects.all().order_by('-id')[:10], 1):
        print(f"{i}. ID: {analise.id}")
        print(f"   Data: {analise.data}")
        print(f"   Tipo: {analise.get_tipo_amostra_display()}")
        print(f"   Absorbância: {analise.absorbancia_amostra}")
        print(f"   Resultado: {analise.resultado}")
        print(f"   Formatado: {analise.get_resultado_formatado()}")
        print()
    
    return True

def criar_dados_teste():
    """Cria dados de teste se não existirem"""
    print("=== CRIANDO DADOS DE TESTE ===")
    
    dados_teste = [
        {
            'data': date.today(),
            'horario': time(10, 30),
            'tipo_amostra': 'FL',
            'absorbancia_amostra': Decimal('0.125000'),
            'casas_decimais': 0
        },
        {
            'data': date.today(),
            'horario': time(11, 15),
            'tipo_amostra': 'SI',
            'absorbancia_amostra': Decimal('0.089000'),
            'casas_decimais': 0
        },
        {
            'data': date.today(),
            'horario': time(14, 45),
            'tipo_amostra': 'FL',
            'absorbancia_amostra': Decimal('0.234000'),
            'casas_decimais': 0
        }
    ]
    
    criados = 0
    for dados in dados_teste:
        try:
            analise = AnaliseFosforo.objects.create(**dados)
            print(f"✅ Criada análise ID: {analise.id} - Resultado: {analise.get_resultado_formatado()} ppm")
            criados += 1
        except Exception as e:
            print(f"❌ Erro ao criar análise: {e}")
    
    print(f"\n📊 Total de análises criadas: {criados}")
    return criados > 0

def testar_view():
    """Testa se a view está funcionando"""
    print("=== TESTE DA VIEW ===")
    
    try:
        from analises.views import FosforoListView
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/analises/fosforo/')
        
        view = FosforoListView()
        view.request = request
        
        queryset = view.get_queryset()
        context = view.get_context_data()
        
        print(f"✅ View funcionando")
        print(f"   Queryset count: {queryset.count()}")
        print(f"   Context object_list: {len(context.get('object_list', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na view: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🔍 DIAGNÓSTICO DE ANÁLISES DE FÓSFORO\n")
    
    # 1. Verificar dados existentes
    tem_dados = verificar_dados()
    
    # 2. Criar dados se não existirem
    if not tem_dados:
        criar_dados_teste()
        print("\n" + "="*50)
        verificar_dados()
    
    # 3. Testar a view
    print("\n" + "="*50)
    testar_view()
    
    print("\n" + "="*50)
    print("🎯 DIAGNÓSTICO CONCLUÍDO!")
    print("✅ Acesse: http://127.0.0.1:8000/analises/fosforo/")

if __name__ == "__main__":
    main()
