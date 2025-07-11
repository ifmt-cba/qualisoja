#!/usr/bin/env python
"""
Adicionar mais registros de teste
"""
import sqlite3

def adicionar_registros():
    """Adicionar registros com diferentes valores"""
    print("=== ADICIONANDO MAIS REGISTROS ===")
    
    db_path = 'c:/Users/rodri/qualisoja/db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Registros com diferentes resultados
        registros = [
            # Registro ÓTIMO (resultado < 80)
            {
                'abs': 0.040000,
                'resultado': 64.000,
                'horario': '15:30:00'
            },
            # Registro BOM (80 <= resultado <= 180)
            {
                'abs': 0.080000,
                'resultado': 128.000,
                'horario': '16:30:00'
            },
            # Registro RUIM (resultado > 180)
            {
                'abs': 0.150000,
                'resultado': 240.000,
                'horario': '17:30:00'
            }
        ]
        
        for i, reg in enumerate(registros, 2):
            sql = f"""
            INSERT INTO analises_analisefosforo (
                data, horario, tipo_amostra, peso_amostra, 
                absorbancia_amostra, concentracao_padrao, 
                volume_solucao, volume_aliquota, absorbancia_padrao,
                resultado, casas_decimais, criado_em, atualizado_em
            ) VALUES (
                '2025-01-10', '{reg['horario']}', 'FL', 1.0000,
                {reg['abs']}, 10.0000, 100.00, 10.00, 0.250000,
                {reg['resultado']}, 0, datetime('now'), datetime('now')
            )
            """
            cursor.execute(sql)
            print(f"✅ Registro {i} adicionado: {reg['resultado']} ppm")
        
        conn.commit()
        
        # Verificar total
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
    if adicionar_registros():
        print("\n🎉 Registros adicionados!")
        print("Agora teste: http://127.0.0.1:8000/analises/fosforo/")
    else:
        print("\n❌ Falha ao adicionar registros")
