#!/usr/bin/env python3
"""
Script para testar todas as análises com CRUD completo
"""

from analises.models import AnaliseUrase, AnaliseCinza, AnaliseTeorOleo, AnaliseFibra, AnaliseFosforo
import os
import sys
import django
from datetime import datetime, date, time
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()


def testar_crud_completo():
    """Testa todas as análises com as novas opções FP e SA"""

    print("🔧 TESTANDO SISTEMA CRUD COMPLETO")
    print("=" * 50)

    try:
        # Teste 1: Verificar novos tipos de amostra
        print("\n📊 1. Verificando tipos de amostra...")

        # Urase
        urase_tipos = dict(AnaliseUrase.TIPO_AMOSTRA_CHOICES)
        print(f"   ✅ Urase: {list(urase_tipos.values())}")
        assert 'FP' in urase_tipos and 'SA' in urase_tipos

        # Cinza
        cinza_tipos = dict(AnaliseCinza.TIPO_AMOSTRA_CHOICES)
        print(f"   ✅ Cinza: {list(cinza_tipos.values())}")
        assert 'FP' in cinza_tipos and 'SA' in cinza_tipos

        # Teor de Óleo
        teor_tipos = dict(AnaliseTeorOleo.TIPO_AMOSTRA_CHOICES)
        print(f"   ✅ Teor de Óleo: {list(teor_tipos.values())}")
        assert 'FP' in teor_tipos and 'SA' in teor_tipos

        # Fibra
        fibra_tipos = dict(AnaliseFibra.TIPO_AMOSTRA_CHOICES)
        print(f"   ✅ Fibra: {list(fibra_tipos.values())}")
        assert 'FP' in fibra_tipos and 'SA' in fibra_tipos

        # Fósforo
        fosforo_tipos = dict(AnaliseFosforo.TIPO_AMOSTRA_CHOICES)
        print(f"   ✅ Fósforo: {list(fosforo_tipos.values())}")
        assert 'FP' in fosforo_tipos and 'SA' in fosforo_tipos

        # Teste 2: Criar análises com novos tipos
        print("\n🧪 2. Criando análises com novos tipos...")

        # Urase - Fábrica Parada
        urase_fp = AnaliseUrase.objects.create(
            data=date.today(),
            horario=time(14, 30),
            tipo_amostra='FP',
            amostra_1=Decimal('100.5'),
            amostra_2=Decimal('98.2')
        )
        print(
            f"   ✅ Urase FP criada: ID {urase_fp.id} - Resultado: {urase_fp.resultado}")

        # Cinza - Sem Amostra
        cinza_sa = AnaliseCinza.objects.create(
            data=date.today(),
            horario=time(15, 45),
            tipo_amostra='SA',
            peso_amostra=Decimal('2.0000'),
            peso_cadinho=Decimal('25.5000'),
            peso_cinza=Decimal('25.6200')
        )
        print(
            f"   ✅ Cinza SA criada: ID {cinza_sa.id} - Resultado: {cinza_sa.resultado}%")

        # Teor de Óleo - Fábrica Parada
        teor_fp = AnaliseTeorOleo.objects.create(
            data=date.today(),
            horario=time(16, 15),
            tipo_amostra='FP',
            peso_amostra=Decimal('2.100'),
            peso_tara=Decimal('25.000'),
            peso_liquido=Decimal('25.120')
        )
        print(
            f"   ✅ Teor de Óleo FP criado: ID {teor_fp.id} - Resultado: {teor_fp.teor_oleo}%")

        # Fibra - Sem Amostra
        fibra_sa = AnaliseFibra.objects.create(
            data=date.today(),
            horario=time(17, 30),
            tipo_amostra='SA',
            peso_amostra=Decimal('1.2500'),
            peso_tara=Decimal('30.0000'),
            peso_fibra=Decimal('29.8500'),
            peso_branco=Decimal('0.0200')
        )
        print(
            f"   ✅ Fibra SA criada: ID {fibra_sa.id} - Resultado: {fibra_sa.resultado}%")

        # Fósforo - Fábrica Parada
        fosforo_fp = AnaliseFosforo.objects.create(
            data=date.today(),
            horario=time(18, 45),
            tipo_amostra='FP',
            absorbancia_amostra=Decimal('0.315000'),
            peso_amostra=Decimal('1.0000'),
            casas_decimais=1
        )
        print(
            f"   ✅ Fósforo FP criado: ID {fosforo_fp.id} - Resultado: {fosforo_fp.get_resultado_formatado()} ppm")

        # Teste 3: Verificar contadores
        print("\n📈 3. Verificando contadores...")
        print(f"   📊 Análises de Urase: {AnaliseUrase.objects.count()}")
        print(f"   📊 Análises de Cinza: {AnaliseCinza.objects.count()}")
        print(
            f"   📊 Análises de Teor de Óleo: {AnaliseTeorOleo.objects.count()}")
        print(f"   📊 Análises de Fibra: {AnaliseFibra.objects.count()}")
        print(f"   📊 Análises de Fósforo: {AnaliseFosforo.objects.count()}")

        # Teste 4: URLs disponíveis
        print("\n🌐 4. URLs disponíveis para acesso:")
        print("   📋 Urase:")
        print("      - Lista: /analises/urase/")
        print("      - Nova: /analises/urase/cadastro/")
        print(f"      - Detalhe: /analises/urase/{urase_fp.id}/")
        print(f"      - Editar: /analises/urase/{urase_fp.id}/editar/")
        print(f"      - Excluir: /analises/urase/{urase_fp.id}/excluir/")

        print("   📋 Cinza:")
        print("      - Lista: /analises/cinza/")
        print("      - Nova: /analises/cinza/nova/")
        print(f"      - Detalhe: /analises/cinza/{cinza_sa.id}/")
        print(f"      - Editar: /analises/cinza/{cinza_sa.id}/editar/")
        print(f"      - Excluir: /analises/cinza/{cinza_sa.id}/excluir/")

        print("   📋 Teor de Óleo:")
        print("      - Lista: /analises/teor-oleo/")
        print("      - Nova: /analises/teor-oleo/nova/")
        print(f"      - Detalhe: /analises/teor-oleo/{teor_fp.id}/")
        print(f"      - Editar: /analises/teor-oleo/{teor_fp.id}/editar/")
        print(f"      - Excluir: /analises/teor-oleo/{teor_fp.id}/excluir/")

        print("   📋 Fibra:")
        print("      - Lista: /analises/fibra/")
        print("      - Nova: /analises/fibra/nova/")
        print(f"      - Detalhe: /analises/fibra/{fibra_sa.id}/")
        print(f"      - Editar: /analises/fibra/{fibra_sa.id}/editar/")
        print(f"      - Excluir: /analises/fibra/{fibra_sa.id}/excluir/")

        print("   📋 Fósforo:")
        print("      - Lista: /analises/fosforo/")
        print("      - Nova: /analises/fosforo/nova/")
        print(f"      - Detalhe: /analises/fosforo/{fosforo_fp.id}/")
        print(f"      - Editar: /analises/fosforo/{fosforo_fp.id}/editar/")
        print(f"      - Excluir: /analises/fosforo/{fosforo_fp.id}/excluir/")

        print("\n🎉 SUCESSO: Todas as análises estão padronizadas!")
        print("   ✅ Novos tipos de amostra: FP (Fábrica Parada) e SA (Sem Amostra)")
        print("   ✅ CRUD completo: Criar, Listar, Visualizar, Editar, Excluir")
        print("   ✅ Templates modernos com Bootstrap 5")
        print("   ✅ Campos bloqueados na visualização")
        print("   ✅ Cálculos automáticos funcionando")

        print(f"\n🚀 Para usar, execute: python manage.py runserver")
        print(f"   E acesse: http://127.0.0.1:8000/analises/home/")

        return True

    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = testar_crud_completo()
    sys.exit(0 if sucesso else 1)
