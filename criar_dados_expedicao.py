#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo para relatórios de expedição.
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from relatorios.models import Cliente, EspecificacaoContrato, Lote
from django.contrib.auth.models import User

def criar_dados_exemplo():
    """Cria dados de exemplo para testes."""
    print("🌱 Criando dados de exemplo para Relatórios de Expedição...")
    
    # Obter ou criar usuário admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@qualisoja.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Usuário admin criado: {admin_user.username}")
    else:
        print(f"ℹ️ Usuário admin já existe: {admin_user.username}")
    
    # Criar clientes de exemplo
    clientes_data = [
        {
            'nome': 'Agroindústria Santos Ltda',
            'codigo': 'AGR001',
            'email': 'qualidade@agrosantos.com.br',
            'telefone': '(11) 3456-7890',
            'endereco': 'Rua das Indústrias, 123 - São Paulo, SP'
        },
        {
            'nome': 'Cooperativa Agrícola Vale Verde',
            'codigo': 'COOP002',
            'email': 'expedicao@valeverde.coop.br',
            'telefone': '(45) 2345-6789',
            'endereco': 'Av. Principal, 456 - Cascavel, PR'
        },
        {
            'nome': 'Exportadora Grãos do Brasil',
            'codigo': 'EXP003',
            'email': 'comercial@graosdobrasil.com',
            'telefone': '(67) 3456-7890',
            'endereco': 'Rod. BR-163, Km 85 - Campo Grande, MS'
        }
    ]
    
    clientes = []
    for cliente_data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            codigo=cliente_data['codigo'],
            defaults=cliente_data
        )
        clientes.append(cliente)
        if created:
            print(f"✅ Cliente criado: {cliente.nome}")
        else:
            print(f"ℹ️ Cliente já existe: {cliente.nome}")
    
    # Criar especificações de contrato
    contratos_data = [
        {
            'cliente': clientes[0],
            'nome_contrato': 'Contrato Farelo Premium 2025',
            'codigo_contrato': 'FP-2025-001',
            'umidade_max': Decimal('12.5'),
            'proteina_min': Decimal('44.0'),
            'proteina_max': Decimal('48.0'),
            'oleo_min': Decimal('0.5'),
            'oleo_max': Decimal('2.0'),
            'fibra_max': Decimal('7.0'),
            'cinza_max': Decimal('6.5'),
            'fosforo_min': Decimal('0.6'),
            'fosforo_max': Decimal('0.9'),
            'data_inicio': date.today() - timedelta(days=60),
            'data_fim': date.today() + timedelta(days=300)
        },
        {
            'cliente': clientes[1],
            'nome_contrato': 'Fornecimento Cooperativa 2025',
            'codigo_contrato': 'COOP-2025-002',
            'umidade_max': Decimal('13.0'),
            'proteina_min': Decimal('43.5'),
            'proteina_max': Decimal('47.5'),
            'oleo_min': Decimal('0.8'),
            'oleo_max': Decimal('2.5'),
            'fibra_max': Decimal('7.5'),
            'cinza_max': Decimal('7.0'),
            'fosforo_min': Decimal('0.5'),
            'fosforo_max': Decimal('0.8'),
            'data_inicio': date.today() - timedelta(days=45),
            'data_fim': date.today() + timedelta(days=315)
        },
        {
            'cliente': clientes[2],
            'nome_contrato': 'Exportação Premium Quality',
            'codigo_contrato': 'EXP-2025-003',
            'umidade_max': Decimal('12.0'),
            'proteina_min': Decimal('45.0'),
            'proteina_max': Decimal('49.0'),
            'oleo_min': Decimal('0.3'),
            'oleo_max': Decimal('1.5'),
            'fibra_max': Decimal('6.5'),
            'cinza_max': Decimal('6.0'),
            'fosforo_min': Decimal('0.7'),
            'fosforo_max': Decimal('1.0'),
            'data_inicio': date.today() - timedelta(days=30),
            'data_fim': date.today() + timedelta(days=335)
        }
    ]
    
    contratos = []
    for contrato_data in contratos_data:
        contrato, created = EspecificacaoContrato.objects.get_or_create(
            codigo_contrato=contrato_data['codigo_contrato'],
            defaults=contrato_data
        )
        contratos.append(contrato)
        if created:
            print(f"✅ Contrato criado: {contrato.nome_contrato}")
        else:
            print(f"ℹ️ Contrato já existe: {contrato.nome_contrato}")
    
    # Criar lotes de exemplo
    lotes_data = []
    for i, cliente in enumerate(clientes):
        for j in range(5):  # 5 lotes por cliente
            lotes_data.append({
                'codigo': f'LT{(i+1):02d}{(j+1):03d}',
                'cliente': cliente,
                'contrato': contratos[i],
                'data_producao': date.today() - timedelta(days=30-j*5),
                'quantidade_kg': Decimal(f'{20000 + j*1000}.00'),
                'observacoes': f'Lote de produção {j+1} - Cliente {cliente.nome}',
                'status': 'APROVADO' if j < 4 else 'ANALISE'
            })
    
    lotes = []
    for lote_data in lotes_data:
        lote, created = Lote.objects.get_or_create(
            codigo=lote_data['codigo'],
            defaults=lote_data
        )
        lotes.append(lote)
        if created:
            print(f"✅ Lote criado: {lote.codigo}")
        else:
            print(f"ℹ️ Lote já existe: {lote.codigo}")
    
    print(f"\n🎉 Dados de exemplo criados com sucesso!")
    print(f"📊 Resumo:")
    print(f"   - {len(clientes)} clientes")
    print(f"   - {len(contratos)} contratos")
    print(f"   - {len(lotes)} lotes")
    print(f"\n🔗 Acesse: http://127.0.0.1:8000/relatorios/expedicao/")

if __name__ == '__main__':
    criar_dados_exemplo()
