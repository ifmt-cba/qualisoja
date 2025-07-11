#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qualisoja.settings")
django.setup()

from analises.models import AnaliseFibra
from decimal import Decimal
from datetime import date, time

print("=== Teste de Criação de Análise de Fibra ===")

# Verificar registros existentes
count_inicial = AnaliseFibra.objects.count()
print(f"Registros existentes: {count_inicial}")

# Criar nova análise
try:
    nova_analise = AnaliseFibra(
        data=date.today(),
        horario=time(15, 30),
        tipo_amostra='FL',  # Farelo
        peso_amostra=Decimal('2.0000'),
        peso_tara=Decimal('1.5000'),
        peso_fibra=Decimal('0.8000'),
        peso_branco=Decimal('0.2000')
    )
    
    # Salvar (vai calcular automaticamente o resultado)
    nova_analise.save()
    
    print(f"✅ Análise criada com sucesso!")
    print(f"   ID: {nova_analise.id}")
    print(f"   Data: {nova_analise.data}")
    print(f"   Tipo: {nova_analise.get_tipo_amostra_display()}")
    print(f"   Peso amostra: {nova_analise.peso_amostra}g")
    print(f"   Peso tara: {nova_analise.peso_tara}g")
    print(f"   Peso fibra: {nova_analise.peso_fibra}g")
    print(f"   Peso branco: {nova_analise.peso_branco}g")
    print(f"   Resultado calculado: {nova_analise.resultado}%")
    
    # Verificar se foi salvo
    count_final = AnaliseFibra.objects.count()
    print(f"Total de registros agora: {count_final}")
    
    # Listar todos os registros
    print("\n=== Todos os Registros ===")
    for analise in AnaliseFibra.objects.all().order_by('-data', '-horario'):
        print(f"- {analise.data} {analise.horario} | {analise.get_tipo_amostra_display()} | Resultado: {analise.resultado}%")

except Exception as e:
    print(f"❌ Erro ao criar análise: {e}")
    import traceback
    traceback.print_exc()
