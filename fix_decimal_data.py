#!/usr/bin/env python
"""
Script para limpar dados inválidos de decimal no banco de dados.
"""
import os
import sys
import django
from decimal import Decimal, InvalidOperation

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseCinza
from django.db import connection

def fix_invalid_decimals():
    """Corrige valores decimais inválidos na tabela de cinza."""
    print("Verificando e corrigindo dados inválidos...")
    
    # Primeiro, tentar acessar todos os registros via ORM para identificar o problema
    try:
        count = AnaliseCinza.objects.count()
        print(f"Total de registros de cinza: {count}")
    except Exception as e:
        print(f"Erro ao contar registros: {e}")
    
    # Tentar acessar registros um por um para identificar o problemático
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM analises_analisecinza ORDER BY id")
        ids = [row[0] for row in cursor.fetchall()]
        
        print(f"IDs encontrados: {ids}")
        
        problematic_ids = []
        
        for record_id in ids:
            try:
                # Tentar acessar o registro via ORM
                record = AnaliseCinza.objects.get(id=record_id)
                # Tentar acessar cada campo decimal
                _ = record.peso_amostra
                _ = record.peso_cadinho  
                _ = record.peso_cinza
                _ = record.resultado
                print(f"Registro ID {record_id}: OK")
            except Exception as e:
                print(f"Erro no registro ID {record_id}: {e}")
                problematic_ids.append(record_id)
        
        # Remover registros problemáticos
        if problematic_ids:
            print(f"Removendo {len(problematic_ids)} registros problemáticos...")
            for prob_id in problematic_ids:
                try:
                    # Remover diretamente do banco
                    cursor.execute("DELETE FROM analises_analisecinza WHERE id = %s", [prob_id])
                    print(f"Registro ID {prob_id} removido com sucesso")
                except Exception as e:
                    print(f"Erro ao remover registro ID {prob_id}: {e}")
                    # Tentar com formato diferente para SQLite
                    try:
                        cursor.execute("DELETE FROM analises_analisecinza WHERE id = ?", [prob_id])
                        print(f"Registro ID {prob_id} removido com sucesso (tentativa 2)")
                    except Exception as e2:
                        print(f"Erro na segunda tentativa para ID {prob_id}: {e2}")
            
            # Fazer commit das mudanças
            connection.commit()
        else:
            print("Nenhum dado problemático encontrado!")
    
    print("Verificação e limpeza concluída!")

if __name__ == "__main__":
    fix_invalid_decimals()
