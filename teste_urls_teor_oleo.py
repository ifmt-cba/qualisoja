#!/usr/bin/env python3
"""
Script para testar as URLs e views de teor de óleo
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()


def teste_urls():
    """Testa se as URLs estão funcionando"""

    client = Client()

    print("=== TESTE DAS URLs ===")

    urls_teste = [
        ('analises:teor_oleo_list', 'Lista de Teor de Óleo'),
        ('analises:teor_oleo_create', 'Criar Teor de Óleo'),
    ]

    for url_name, descricao in urls_teste:
        try:
            url = reverse(url_name)
            print(f"{descricao}: {url}")

            response = client.get(url)
            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                print(f"  ✅ URL funcionando")
            else:
                print(f"  ❌ Erro na URL")

        except Exception as e:
            print(f"  ❌ Erro ao testar {url_name}: {e}")

        print()


if __name__ == "__main__":
    teste_urls()
