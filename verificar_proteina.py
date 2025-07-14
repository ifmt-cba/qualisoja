#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from django.db import connection
from analises.models import AnaliseProteina

print("=== Verificando estrutura da tabela AnaliseProteina ===")

# Verificar campos do modelo Django
print("\nCampos do modelo Django:")
for field in AnaliseProteina._meta.fields:
    print(f"  {field.name}: {field.__class__.__name__}")

# Verificar estrutura real da tabela no banco
with connection.cursor() as cursor:
    # Obter nome da tabela
    table_name = AnaliseProteina._meta.db_table
    print(f"\nNome da tabela: {table_name}")
    
    # Verificar estrutura da tabela
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print("\nColunas na tabela do banco:")
    for col in columns:
        print(f"  {col[1]}: {col[2]}")
    
    # Tentar buscar algumas análises usando apenas campos básicos
    print("\n=== Testando consulta simples ===")
    try:
        # Usar apenas campos que certamente existem
        cursor.execute(f"SELECT id, data, tipo_amostra FROM {table_name} LIMIT 5")
        resultados = cursor.fetchall()
        print(f"Análises encontradas (consulta direta): {len(resultados)}")
        for resultado in resultados:
            print(f"  ID: {resultado[0]}, Data: {resultado[1]}, Tipo: {resultado[2]}")
    except Exception as e:
        print(f"Erro na consulta direta: {e}")
    
    # Tentar através do ORM sem usar campos problemáticos
    print("\n=== Testando consulta ORM simples ===")
    try:
        analises = AnaliseProteina.objects.values('id', 'data', 'tipo_amostra')[:5]
        print(f"Análises encontradas (ORM básico): {analises.count()}")
        for analise in analises:
            print(f"  {analise}")
    except Exception as e:
        print(f"Erro na consulta ORM básica: {e}")
    
    # Tentar buscar especificamente o campo ml_branco
    print("\n=== Testando campo ml_branco ===")
    try:
        cursor.execute(f"SELECT id, ml_branco FROM {table_name} LIMIT 3")
        resultados = cursor.fetchall()
        print(f"Campo ml_branco existe e funcionando")
        for resultado in resultados:
            print(f"  ID: {resultado[0]}, ml_branco: {resultado[1]}")
    except Exception as e:
        print(f"Erro ao acessar ml_branco: {e}")
