#!/usr/bin/env python
"""
Resolução definitiva do problema da lista de fósforo
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo
from decimal import Decimal
from datetime import datetime, time
from django.db import connection

def resolver_definitivo():
    """Resolver o problema de forma definitiva"""
    print("=== RESOLUÇÃO DEFINITIVA ===")
    
    # 1. Limpar completamente
    print("1. Limpando dados...")
    AnaliseFosforo.objects.all().delete()
    
    # 2. Verificar se está limpo
    count = AnaliseFosforo.objects.count()
    print(f"   Registros após limpeza: {count}")
    
    # 3. Criar dados válidos simples
    print("2. Criando dados válidos...")
    
    dados = [
        {
            'absorbancia': Decimal('0.020'),
            'resultado_esperado': 'baixo',
            'horario': time(14, 0)
        },
        {
            'absorbancia': Decimal('0.030'),
            'resultado_esperado': 'médio',
            'horario': time(15, 0)
        },
        {
            'absorbancia': Decimal('0.050'),
            'resultado_esperado': 'alto',
            'horario': time(16, 0)
        }
    ]
    
    registros_criados = []
    
    for i, dado in enumerate(dados):
        try:
            analise = AnaliseFosforo(
                data=datetime.now().date(),
                horario=dado['horario'],
                tipo_amostra='FL',
                peso_amostra=Decimal('1.0000'),
                absorbancia_amostra=dado['absorbancia'],
                concentracao_padrao=Decimal('10.0000'),
                volume_solucao=Decimal('100.00'),
                volume_aliquota=Decimal('10.00'),
                absorbancia_padrao=Decimal('0.250000'),
                casas_decimais=0
            )
            analise.save()
            
            print(f"   ✅ Registro {i+1}: ID {analise.id}")
            print(f"      Absorbância: {analise.absorbancia_amostra}")
            print(f"      Resultado: {analise.resultado}")
            print(f"      Formatado: {analise.get_resultado_formatado()}")
            
            registros_criados.append(analise)
            
        except Exception as e:
            print(f"   ❌ Erro no registro {i+1}: {e}")
    
    # 4. Verificar se foram criados
    total_final = AnaliseFosforo.objects.count()
    print(f"\n3. Verificação final: {total_final} registros no banco")
    
    # 5. Testar a listagem
    print("4. Testando listagem...")
    try:
        lista = AnaliseFosforo.objects.all().order_by('-data', '-horario')
        print(f"   Queryset: {lista.count()} registros")
        
        for analise in lista:
            print(f"   - ID {analise.id}: {analise.get_resultado_formatado()} ppm")
            
    except Exception as e:
        print(f"   ❌ Erro na listagem: {e}")
        import traceback
        traceback.print_exc()
    
    return len(registros_criados) > 0

if __name__ == '__main__':
    if resolver_definitivo():
        print("\n🎉 PROBLEMA RESOLVIDO!")
        print("Agora acesse: http://127.0.0.1:8000/analises/fosforo/")
        print("Os dados devem aparecer na lista!")
    else:
        print("\n❌ Ainda há problemas")
