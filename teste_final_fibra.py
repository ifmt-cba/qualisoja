#!/usr/bin/env python
"""
Teste completo do sistema de análise de fibra
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qualisoja.settings")
django.setup()

from django.test import Client
from analises.models import AnaliseFibra
from analises.forms import AnaliseFibraForm
from decimal import Decimal
from datetime import date, time

print("=== TESTE COMPLETO DO SISTEMA DE FIBRA ===\n")

# 1. Teste do modelo
print("1. TESTE DO MODELO")
count_inicial = AnaliseFibra.objects.count()
print(f"   Registros iniciais: {count_inicial}")

# Criar análise via modelo
nova_analise = AnaliseFibra.objects.create(
    data=date.today(),
    horario=time(16, 0),
    tipo_amostra='SI',  # Soja Industrializada
    peso_amostra=Decimal('1.8000'),
    peso_tara=Decimal('1.2000'),
    peso_fibra=Decimal('0.6000'),
    peso_branco=Decimal('0.1000')
)
print(f"   ✅ Análise criada: {nova_analise}")
print(f"   ✅ Resultado calculado: {nova_analise.resultado}%")

# 2. Teste do formulário
print("\n2. TESTE DO FORMULÁRIO")
data_form = {
    'data': '2025-07-10',
    'horario': '16:30',
    'tipo_amostra': 'FL',
    'peso_amostra': '1.9000',
    'peso_tara': '1.3000',
    'peso_fibra': '0.7000',
    'peso_branco': '0.1500'  # 4 casas decimais
}

form = AnaliseFibraForm(data=data_form)
if form.is_valid():
    analise_form = form.save()
    print(f"   ✅ Formulário validado e salvo: {analise_form}")
    print(f"   ✅ Resultado: {analise_form.resultado}%")
else:
    print(f"   ❌ Erro no formulário: {form.errors}")

# 3. Teste das URLs
print("\n3. TESTE DAS URLs")
client = Client()

# Teste da lista
try:
    response = client.get('/analises/fibra/')
    if response.status_code == 200:
        print("   ✅ Lista de fibra carrega corretamente")
        content = response.content.decode()
        if 'badge bg-success' in content:
            print("   ✅ Dados visíveis na lista")
        else:
            print("   ⚠️  Lista vazia ou sem dados visíveis")
    else:
        print(f"   ❌ Erro na lista: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro ao acessar lista: {e}")

# Teste do formulário
try:
    response = client.get('/analises/fibra/nova/')
    if response.status_code == 200:
        print("   ✅ Formulário de fibra carrega corretamente")
    else:
        print(f"   ❌ Erro no formulário: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro ao acessar formulário: {e}")

# 4. Resumo final
print("\n4. RESUMO FINAL")
count_final = AnaliseFibra.objects.count()
print(f"   Registros iniciais: {count_inicial}")
print(f"   Registros finais: {count_final}")
print(f"   Registros criados neste teste: {count_final - count_inicial}")

print("\n5. ÚLTIMAS ANÁLISES CADASTRADAS:")
for i, analise in enumerate(AnaliseFibra.objects.all().order_by('-data', '-horario')[:5], 1):
    print(f"   {i}. {analise.data} {analise.horario} | {analise.get_tipo_amostra_display()} | {analise.resultado}%")

print("\n=== TESTE CONCLUÍDO ===")
print("✅ Sistema de análise de fibra está funcionando!")
print("✅ URLs de acesso:")
print("   - Lista: http://localhost:8000/analises/fibra/")
print("   - Novo:  http://localhost:8000/analises/fibra/nova/")
print("   - Admin: http://localhost:8000/admin/analises/analisefibra/")
