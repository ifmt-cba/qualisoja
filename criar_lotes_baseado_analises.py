#!/usr/bin/env python
"""
Script para criar lotes baseados nas análises existentes.
Segue o mesmo padrão que o sistema de relatórios usa para buscar dados.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import *
from relatorios.models import Cliente, EspecificacaoContrato, Lote
from django.contrib.auth.models import User

def criar_cliente_padrao():
    """Cria cliente padrão se não existir."""
    cliente, created = Cliente.objects.get_or_create(
        codigo='CLI001',
        defaults={
            'nome': 'Cliente Teste QualiSoja',
            'email': 'teste@qualisoja.com',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua Teste, 123 - São Paulo/SP',
            'ativo': True
        }
    )
    if created:
        print(f"✓ Cliente criado: {cliente.nome}")
    else:
        print(f"✓ Cliente já existe: {cliente.nome}")
    return cliente

def criar_contrato_padrao(cliente):
    """Cria contrato padrão se não existir."""
    from datetime import date
    contrato, created = EspecificacaoContrato.objects.get_or_create(
        cliente=cliente,
        codigo_contrato='CONT001',
        defaults={
            'nome_contrato': 'Contrato Padrão QualiSoja',
            'umidade_min': 12.0,
            'umidade_max': 14.0,
            'proteina_min': 45.0,
            'proteina_max': 50.0,
            'oleo_min': 18.0,
            'oleo_max': 22.0,
            'data_inicio': date(2025, 1, 1),
            'data_fim': date(2025, 12, 31),
            'ativo': True
        }
    )
    if created:
        print(f"✓ Contrato criado: {contrato.nome_contrato}")
    else:
        print(f"✓ Contrato já existe: {contrato.nome_contrato}")
    return contrato

def obter_datas_analises():
    """Obtém todas as datas únicas onde existem análises."""
    datas = set()
    
    # Buscar datas de todas as análises
    for model in [AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, 
                  AnaliseFosforo, AnaliseTeorOleo, AnaliseFibra, 
                  AnaliseCinza, AnaliseUrase, AnaliseSilica]:
        if model.objects.exists():
            datas_model = model.objects.values_list('data', flat=True).distinct()
            datas.update(datas_model)
    
    return sorted(list(datas))

def determinar_tipo_produto(data):
    """
    Determina o tipo de produto baseado nas análises disponíveis na data.
    Se há análise de proteína e teor de óleo, é farelo.
    Se há análise de óleo degomado, acidez, etc., é óleo.
    """
    # Verificar se há análises típicas de farelo
    tem_proteina = AnaliseProteina.objects.filter(data=data).exists()
    tem_teor_oleo = AnaliseTeorOleo.objects.filter(data=data).exists()
    
    # Verificar se há análises típicas de óleo
    tem_oleo_degomado = AnaliseOleoDegomado.objects.filter(data=data).exists()
    tem_urase = AnaliseUrase.objects.filter(data=data).exists()
    tem_silica = AnaliseSilica.objects.filter(data=data).exists()
    
    if tem_proteina and tem_teor_oleo:
        return 'farelo'
    elif tem_oleo_degomado or tem_urase or tem_silica:
        return 'oleo'
    else:
        # Se não está claro, usar umidade como critério
        # Se há mais de uma análise de umidade, pode ser farelo
        count_umidade = AnaliseUmidade.objects.filter(data=data).count()
        return 'farelo' if count_umidade > 1 else 'oleo'

def criar_lote_para_data(cliente, contrato, data, tipo_produto, numero_sequencial):
    """Cria um lote para uma data específica baseado no tipo de produto."""
    
    if tipo_produto == 'farelo':
        codigo_lote = f"FAR{data.strftime('%y%m%d')}-{numero_sequencial:02d}"
        observacoes = "Lote de farelo de soja - criado automaticamente baseado nas análises"
        quantidade = 15000.0  # 15 toneladas
    else:
        codigo_lote = f"OLE{data.strftime('%y%m%d')}-{numero_sequencial:02d}"
        observacoes = "Lote de óleo de soja - criado automaticamente baseado nas análises"
        quantidade = 8000.0   # 8 toneladas
    
    # Verificar se já existe
    if Lote.objects.filter(codigo=codigo_lote).exists():
        print(f"⚠ Lote {codigo_lote} já existe, pulando...")
        return None
    
    lote = Lote.objects.create(
        codigo=codigo_lote,
        cliente=cliente,
        contrato=contrato,
        data_producao=data,
        quantidade_kg=quantidade,
        observacoes=observacoes,
        status='APROVADO'
    )
    
    print(f"✓ Lote criado: {codigo_lote} ({tipo_produto}) - {data}")
    return lote

def main():
    print("=== CRIAÇÃO DE LOTES BASEADOS NAS ANÁLISES EXISTENTES ===")
    print()
    
    # Verificar se há análises
    total_analises = sum([
        AnaliseUmidade.objects.count(),
        AnaliseProteina.objects.count(),
        AnaliseOleoDegomado.objects.count(),
        AnaliseFosforo.objects.count(),
        AnaliseTeorOleo.objects.count(),
        AnaliseFibra.objects.count(),
        AnaliseCinza.objects.count(),
        AnaliseUrase.objects.count(),
        AnaliseSilica.objects.count()
    ])
    
    if total_analises == 0:
        print("❌ Nenhuma análise encontrada no sistema!")
        print("Execute primeiro os scripts de criação de dados de análises.")
        return
    
    print(f"📊 Total de análises encontradas: {total_analises}")
    
    # Criar cliente e contrato padrão
    cliente = criar_cliente_padrao()
    contrato = criar_contrato_padrao(cliente)
    print()
    
    # Obter datas das análises
    datas_analises = obter_datas_analises()
    print(f"📅 Datas com análises encontradas: {len(datas_analises)}")
    for data in datas_analises:
        print(f"   - {data}")
    print()
    
    # Criar lotes para cada data
    lotes_criados = 0
    for i, data in enumerate(datas_analises, 1):
        tipo_produto = determinar_tipo_produto(data)
        print(f"📦 Data {data}: Tipo determinado = {tipo_produto}")
        
        # Criar lote principal
        lote = criar_lote_para_data(cliente, contrato, data, tipo_produto, 1)
        if lote:
            lotes_criados += 1
        
        # Se há muitas análises na mesma data, criar um lote adicional
        total_analises_data = sum([
            AnaliseUmidade.objects.filter(data=data).count(),
            AnaliseProteina.objects.filter(data=data).count(),
            AnaliseOleoDegomado.objects.filter(data=data).count(),
        ])
        
        if total_analises_data > 3:  # Se há muitas análises, criar lote adicional
            tipo_adicional = 'oleo' if tipo_produto == 'farelo' else 'farelo'
            lote_adicional = criar_lote_para_data(cliente, contrato, data, tipo_adicional, 2)
            if lote_adicional:
                lotes_criados += 1
    
    print()
    print("=== RESUMO ===")
    print(f"✓ Lotes criados: {lotes_criados}")
    print(f"✓ Total de lotes no sistema: {Lote.objects.count()}")
    print()
    
    # Mostrar lotes criados
    print("📋 Lotes disponíveis:")
    for lote in Lote.objects.all().order_by('-data_producao'):
        tipo = "FARELO" if 'farelo' in lote.observacoes.lower() else "ÓLEO"
        print(f"   - {lote.codigo} ({tipo}) - {lote.data_producao} - {lote.cliente.nome}")
    
    print()
    print("🎉 Agora você pode criar relatórios de expedição usando esses lotes!")
    print("   Os lotes foram criados baseados nas análises existentes no sistema.")

if __name__ == "__main__":
    main()
