#!/usr/bin/env python
"""
Script para forçar dados válidos
"""
import os
import sys
import django
import sqlite3

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

def limpar_e_criar():
    """Limpar tabela via SQL direto e criar dados válidos"""
    print("=== LIMPEZA FORÇADA ===")
    
    # Conectar diretamente ao SQLite
    db_path = 'c:/Users/rodri/qualisoja/db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Limpar tabela completamente
        cursor.execute("DELETE FROM analises_analisefosforo")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='analises_analisefosforo'")
        conn.commit()
        print("✅ Tabela limpa via SQL direto")
        
        # Inserir dados via SQL direto
        sql = """
        INSERT INTO analises_analisefosforo (
            data, horario, tipo_amostra, peso_amostra, 
            absorbancia_amostra, concentracao_padrao, 
            volume_solucao, volume_aliquota, absorbancia_padrao,
            resultado, casas_decimais, criado_em, atualizado_em
        ) VALUES (
            '2025-01-10', '14:30:00', 'FL', 1.0000,
            0.100000, 10.0000, 100.00, 10.00, 0.250000,
            200.000, 0, datetime('now'), datetime('now')
        )
        """
        
        cursor.execute(sql)
        conn.commit()
        print("✅ Registro inserido via SQL direto")
        
        # Verificar se foi inserido
        cursor.execute("SELECT COUNT(*) FROM analises_analisefosforo")
        count = cursor.fetchone()[0]
        print(f"✅ Total de registros: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    if limpar_e_criar():
        print("\n🎉 Dados criados via SQL direto!")
        print("Agora teste: http://127.0.0.1:8000/analises/fosforo/")
    else:
        print("\n❌ Falha na criação")
