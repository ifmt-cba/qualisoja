#!/usr/bin/env python
"""
Script para criar dados de teste incluindo lotes de farelo
para testar a funcionalidade de parâmetros obrigatórios na expedição.
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from relatorios.models import Cliente, Lote

def criar_lotes_teste():
    """Cria lotes de teste incluindo lotes de farelo."""
    
    print("🔄 Criando lotes de teste para expedição...")
    
    # Buscar cliente existente ou criar um novo
    cliente, created = Cliente.objects.get_or_create(
        codigo='CLI_TESTE',
        defaults={
            'nome': 'Cliente Teste Farelo',
            'email': 'teste@exemplo.com',
            'ativo': True
        }
    )
    
    if created:
        print(f"✅ Cliente criado: {cliente.nome}")
    else:
        print(f"ℹ️ Cliente existente: {cliente.nome}")
    
    # Dados dos lotes de teste
    lotes_dados = [
        {
            'codigo': 'LOTE_OLEO_001',
            'observacoes': 'Lote de óleo de soja refinado',
            'quantidade_kg': 25000.00
        },
        {
            'codigo': 'LOTE_OLEO_002', 
            'observacoes': 'Lote de óleo degomado',
            'quantidade_kg': 30000.00
        },
        {
            'codigo': 'LOTE_FARELO_001',
            'observacoes': 'Lote de farelo de soja',
            'quantidade_kg': 20000.00
        },
        {
            'codigo': 'LOTE_FARELO_002',
            'observacoes': 'Farelo peletizado',
            'quantidade_kg': 18000.00
        },
        {
            'codigo': 'SOJ_FARELO_003',
            'observacoes': 'Subproduto farelo fino',
            'quantidade_kg': 15000.00
        }
    ]
    
    lotes_criados = 0
    
    for lote_data in lotes_dados:
        # Verificar se o lote já existe
        if not Lote.objects.filter(codigo=lote_data['codigo']).exists():
            lote = Lote.objects.create(
                codigo=lote_data['codigo'],
                cliente=cliente,
                data_producao=date.today() - timedelta(days=1),
                quantidade_kg=lote_data['quantidade_kg'],
                observacoes=lote_data['observacoes'],
                status='APROVADO'
            )
            
            # Determinar tipo baseado no código/observações
            is_farelo = ('farelo' in lote.codigo.lower() or 
                        (lote.observacoes and 'farelo' in lote.observacoes.lower()))
            tipo = 'FARELO' if is_farelo else 'ÓLEO'
            
            print(f"✅ Lote criado: {lote.codigo} - Tipo: {tipo}")
            lotes_criados += 1
        else:
            print(f"ℹ️ Lote já existe: {lote_data['codigo']}")
    
    print(f"\n🎉 Criação concluída!")
    print(f"📈 Total de lotes criados: {lotes_criados}")
    
    # Listar todos os lotes do cliente
    print(f"\n📋 Lotes do cliente {cliente.nome}:")
    for lote in Lote.objects.filter(cliente=cliente).order_by('codigo'):
        is_farelo = ('farelo' in lote.codigo.lower() or 
                    (lote.observacoes and 'farelo' in lote.observacoes.lower()))
        tipo = 'FARELO' if is_farelo else 'ÓLEO'
        print(f"🔹 {lote.codigo} - {tipo} - {lote.quantidade_kg}kg")

if __name__ == "__main__":
    criar_lotes_teste()
