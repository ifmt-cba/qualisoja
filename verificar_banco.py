#!/usr/bin/env python
"""
Script para verificar os dados no banco SQLite
"""
import sqlite3
import os

def verificar_banco():
    """Verifica os dados diretamente no banco SQLite"""
    print("🔍 VERIFICANDO BANCO DE DADOS...")
    
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Arquivo {db_path} não encontrado!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(analises_analisefosforo)")
        columns = cursor.fetchall()
        print("📋 Estrutura da tabela:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        print()
        
        # Verificar dados
        cursor.execute("SELECT id, resultado, absorbancia_amostra, casas_decimais FROM analises_analisefosforo")
        rows = cursor.fetchall()
        
        print(f"📊 Total de registros: {len(rows)}")
        print("🔢 Dados encontrados:")
        
        for row in rows:
            print(f"  ID: {row[0]}")
            print(f"    Resultado: {row[1]} (tipo: {type(row[1])})")
            print(f"    Absorbância: {row[2]}")
            print(f"    Casas decimais: {row[3]}")
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
        import traceback
        traceback.print_exc()

def limpar_banco():
    """Limpa a tabela de fósforo"""
    print("🧹 LIMPANDO TABELA...")
    
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM analises_analisefosforo")
        rows_deleted = cursor.rowcount
        conn.commit()
        
        print(f"✅ {rows_deleted} registros removidos")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao limpar banco: {e}")

def main():
    """Função principal"""
    print("🗄️ DIAGNÓSTICO DO BANCO DE DADOS\n")
    
    verificar_banco()
    
    print("\n" + "="*40)
    resposta = input("Deseja limpar a tabela? (s/N): ").strip().lower()
    
    if resposta == 's':
        limpar_banco()
        print("✅ Tabela limpa! Agora você pode recriar os dados.")
    else:
        print("ℹ️ Tabela mantida como está.")

if __name__ == "__main__":
    main()
