#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qualisoja.settings")
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from analises.models import AnaliseFibra
from decimal import Decimal
from datetime import date, time

print("=== Teste Completo da Lista de Fibra ===")

# 1. Verificar dados
count = AnaliseFibra.objects.count()
print(f"1. Registros na tabela: {count}")

# 2. Criar dados se não existir
if count == 0:
    print("2. Criando dados de teste...")
    AnaliseFibra.objects.create(
        data=date.today(),
        horario=time(14, 30),
        tipo_amostra='FL',
        peso_amostra=Decimal('2.0'),
        peso_tara=Decimal('1.5'),
        peso_fibra=Decimal('0.8'),
        peso_branco=Decimal('0.2')
    )
    print("   ✅ Dados criados!")

# 3. Testar a URL
print("3. Testando acesso à URL...")
client = Client()

try:
    # Teste da lista
    response = client.get('/analises/fibra/')
    print(f"   Status da lista: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode()
        if 'Nenhuma análise de fibra encontrada' in content:
            print("   ⚠️  Lista vazia (template mostra mensagem de vazio)")
        elif 'Análises de Fibra' in content:
            print("   ✅ Lista carregou corretamente!")
            # Verificar se há dados na tabela
            if 'badge bg-success' in content:
                print("   ✅ Dados sendo exibidos!")
            else:
                print("   ⚠️  Sem dados visíveis na tabela")
        else:
            print("   ❌ Problema no template")
    else:
        print(f"   ❌ Erro HTTP: {response.status_code}")
        print(f"      Conteúdo: {response.content.decode()[:200]}...")

    # Teste do formulário
    response_form = client.get('/analises/fibra/nova/')
    print(f"   Status do form: {response_form.status_code}")

except Exception as e:
    print(f"   ❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()

# 4. Verificar URLs
print("4. URLs disponíveis:")
print("   - Lista: http://localhost:8000/analises/fibra/")
print("   - Form:  http://localhost:8000/analises/fibra/nova/")
print("   - Admin: http://localhost:8000/admin/analises/analisefibra/")

print("\n=== Resumo ===")
final_count = AnaliseFibra.objects.count()
print(f"Total de registros: {final_count}")
for analise in AnaliseFibra.objects.all()[:3]:
    print(f"- {analise.data} | {analise.get_tipo_amostra_display()} | {analise.resultado}%")
