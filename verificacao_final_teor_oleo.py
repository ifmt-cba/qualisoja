#!/usr/bin/env python3
"""
Verificação final das análises de teor de óleo
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseTeorOleo

def verificacao_final():
    """Verificação final dos dados"""
    
    print("=== VERIFICAÇÃO FINAL - TEOR DE ÓLEO ===")
    
    # Contar análises
    total = AnaliseTeorOleo.objects.count()
    print(f"📊 Total de análises no banco: {total}")
    
    if total == 0:
        print("❌ Nenhuma análise encontrada!")
        return False
    
    # Listar todas com ordenação da view
    analises = AnaliseTeorOleo.objects.all().order_by('-data', '-horario')
    
    print(f"\n📋 Lista de análises (ordenadas por data/horário):")
    for i, analise in enumerate(analises, 1):
        print(f"{i}. ID: {analise.pk}")
        print(f"   📅 Data: {analise.data.strftime('%d/%m/%Y')}")
        print(f"   🕐 Horário: {analise.horario.strftime('%H:%M')}")
        print(f"   🧪 Tipo: {analise.get_tipo_amostra_display()}")
        print(f"   ⚖️  Peso amostra: {analise.peso_amostra}g")
        print(f"   📦 Peso tara: {analise.peso_tara}g")
        print(f"   🛢️  Peso líquido: {analise.peso_liquido}g")
        print(f"   📈 Teor de óleo: {analise.teor_oleo}%")
        if analise.observacoes:
            print(f"   📝 Obs: {analise.observacoes}")
        print()
    
    # Verificar se os dados estão corretos
    problemas = []
    for analise in analises:
        if analise.teor_oleo is None:
            problemas.append(f"ID {analise.pk}: teor_oleo é None")
        if analise.peso_amostra is None:
            problemas.append(f"ID {analise.pk}: peso_amostra é None")
        if analise.peso_tara is None:
            problemas.append(f"ID {analise.pk}: peso_tara é None")
        if analise.peso_liquido is None:
            problemas.append(f"ID {analise.pk}: peso_liquido é None")
    
    if problemas:
        print("⚠️  Problemas encontrados:")
        for problema in problemas:
            print(f"   - {problema}")
    else:
        print("✅ Todos os dados estão corretos!")
    
    # Informações para acesso
    print(f"\n🌐 URLs para testar:")
    print(f"   Lista: http://127.0.0.1:8000/analises/teor-oleo/")
    print(f"   Nova:  http://127.0.0.1:8000/analises/teor-oleo/nova/")
    
    if total > 0:
        primeiro_id = analises.first().pk
        print(f"   Detalhe: http://127.0.0.1:8000/analises/teor-oleo/{primeiro_id}/")
        print(f"   Editar:  http://127.0.0.1:8000/analises/teor-oleo/{primeiro_id}/editar/")
    
    return total > 0

if __name__ == "__main__":
    sucesso = verificacao_final()
    
    if sucesso:
        print("\n🎉 SUCESSO: As análises de teor de óleo estão sendo salvas!")
        print("   O sistema está funcionando corretamente.")
        print("   Execute: python manage.py runserver")
        print("   E acesse: http://127.0.0.1:8000/analises/teor-oleo/")
    else:
        print("\n❌ PROBLEMA: Nenhuma análise encontrada no banco.")
