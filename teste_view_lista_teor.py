#!/usr/bin/env python3
"""
Teste direto da view de lista de teor de óleo
"""

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from analises.views import TeorOleoListView
from analises.models import AnaliseTeorOleo
import os
import sys
import django
from decimal import Decimal
from datetime import date, time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()


def teste_view_lista():
    """Testa a view de lista diretamente"""

    print("=== TESTE DA VIEW DE LISTA ===")

    # Verificar quantas análises existem
    total = AnaliseTeorOleo.objects.count()
    print(f"Total de análises no banco: {total}")

    if total == 0:
        print("Criando análise de teste...")
        AnaliseTeorOleo.objects.create(
            data=date.today(),
            horario=time(18, 0),
            tipo_amostra='FL',
            peso_amostra=Decimal('2.200'),
            peso_tara=Decimal('20.000'),
            peso_liquido=Decimal('20.150'),
            observacoes='Teste para verificar lista'
        )
        total = AnaliseTeorOleo.objects.count()
        print(f"Nova análise criada. Total: {total}")

    # Criar request simulado
    request = HttpRequest()
    request.user = AnonymousUser()
    request.method = 'GET'

    # Instanciar a view
    view = TeorOleoListView()
    view.setup(request)

    # Obter queryset
    queryset = view.get_queryset()
    print(f"Queryset retornou {queryset.count()} análises")

    # Obter context
    context = view.get_context_data()
    analises = context.get('analises') or context.get('object_list')

    if analises:
        print(f"Context retornou {len(analises)} análises:")
        for a in analises:
            print(f"  - ID: {a.pk}, Data: {a.data}, Teor: {a.teor_oleo}%")
    else:
        print("❌ Context não retornou análises!")

    # Testar template context
    print(f"\nContext keys: {list(context.keys())}")

    return queryset.count() > 0


if __name__ == "__main__":
    sucesso = teste_view_lista()
    if sucesso:
        print("\n✅ A view de lista está funcionando corretamente!")
        print("🌐 Acesse: http://127.0.0.1:8000/analises/teor-oleo/")
    else:
        print("\n❌ Problema encontrado na view de lista!")
