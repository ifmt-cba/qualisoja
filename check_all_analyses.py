#!/usr/bin/env python
"""
Script para verificar e limpar dados inválidos em todas as tabelas de análises.
"""
import os
import sys
import django
from decimal import Decimal, InvalidOperation

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import (
    AnaliseUmidade, 
    AnaliseProteina, 
    AnaliseCinza, 
    AnaliseOleo, 
    AnaliseFibra, 
    AnaliseAcidez,
    AnaliseFosforo
)
from django.db import connection

def check_and_fix_model(model_class, table_name):
    """Verifica e corrige dados inválidos para um modelo específico."""
    print(f"\n=== Verificando {model_class.__name__} ===")
    
    try:
        count = model_class.objects.count()
        print(f"Total de registros: {count}")
        
        if count == 0:
            print("Nenhum registro encontrado.")
            return
            
    except Exception as e:
        print(f"Erro ao contar registros: {e}")
        return
    
    # Obter todos os IDs
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {table_name} ORDER BY id")
        ids = [row[0] for row in cursor.fetchall()]
        
        problematic_ids = []
        
        for record_id in ids:
            try:
                # Tentar acessar o registro via ORM
                record = model_class.objects.get(id=record_id)
                # Tentar acessar todos os campos para detectar problemas
                for field in record._meta.fields:
                    if hasattr(record, field.name):
                        _ = getattr(record, field.name)
                        
            except Exception as e:
                print(f"Erro no registro ID {record_id}: {e}")
                problematic_ids.append(record_id)
        
        # Remover registros problemáticos
        if problematic_ids:
            print(f"Encontrados {len(problematic_ids)} registros problemáticos: {problematic_ids}")
            for prob_id in problematic_ids:
                try:
                    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", [prob_id])
                    print(f"Registro ID {prob_id} removido com sucesso")
                except Exception as e:
                    print(f"Erro ao remover registro ID {prob_id}: {e}")
            
            # Fazer commit das mudanças
            connection.commit()
            print(f"{len(problematic_ids)} registros problemáticos removidos!")
        else:
            print("Nenhum dado problemático encontrado!")

def main():
    """Função principal para verificar todas as tabelas."""
    print("=== VERIFICAÇÃO COMPLETA DE DADOS INVÁLIDOS ===")
    
    # Lista de modelos e suas tabelas correspondentes
    models_to_check = [
        (AnaliseUmidade, 'analises_analiseumidade'),
        (AnaliseProteina, 'analises_analiseproteina'),
        (AnaliseCinza, 'analises_analisecinza'),
        (AnaliseOleo, 'analises_analiseoleo'),
        (AnaliseFibra, 'analises_analisefibra'),
        (AnaliseAcidez, 'analises_analiseacidez'),
        (AnaliseFosforo, 'analises_analisefosforo'),
    ]
    
    for model_class, table_name in models_to_check:
        try:
            check_and_fix_model(model_class, table_name)
        except Exception as e:
            print(f"Erro ao verificar {model_class.__name__}: {e}")
    
    print("\n=== VERIFICAÇÃO COMPLETA FINALIZADA ===")

if __name__ == "__main__":
    main()
