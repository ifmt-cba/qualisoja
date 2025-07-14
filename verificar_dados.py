#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from relatorios.models import RelatorioExpedicao
from analises.models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado

print("=== Verificando Relatório de Expedição ===")
try:
    relatorio = RelatorioExpedicao.objects.get(id=5)
    print(f"Relatório ID: {relatorio.id}")
    print(f"Código: {relatorio.codigo}")
    print(f"Cliente: {relatorio.get_cliente_nome()}")
    print(f"Data de geração: {relatorio.data_geracao}")
    print(f"Data inicial: {relatorio.data_inicial}")
    print(f"Data final: {relatorio.data_final}")
    print(f"Tipo de análise: {relatorio.tipo_analise}")
    print(f"Análises selecionadas: {relatorio.analises_selecionadas}")
    
    # Verificar se há análises no período
    from datetime import datetime, timedelta
    
    data_fim = datetime.now().date()
    data_inicio = data_fim - timedelta(days=30)  # últimos 30 dias
    
    print("\n=== Análises disponíveis nos últimos 30 dias ===")
    
    # Análises de Umidade
    umidade = AnaliseUmidade.objects.filter(
        criado_em__date__gte=data_inicio,
        criado_em__date__lte=data_fim
    ).count()
    print(f"Análises de Umidade: {umidade}")
    
    # Análises de Proteína
    proteina = AnaliseProteina.objects.filter(
        criado_em__date__gte=data_inicio,
        criado_em__date__lte=data_fim
    ).count()
    print(f"Análises de Proteína: {proteina}")
    
    # Análises de Óleo Degomado
    oleo = AnaliseOleoDegomado.objects.filter(
        criado_em__date__gte=data_inicio,
        criado_em__date__lte=data_fim
    ).count()
    print(f"Análises de Óleo Degomado: {oleo}")
    
    # Mostrar algumas análises recentes
    print("\n=== Últimas 5 análises de cada tipo ===")
    
    print("\nÚltimas análises de Umidade:")
    for analise in AnaliseUmidade.objects.all().order_by('-criado_em')[:5]:
        print(f"  ID: {analise.id}, Data: {analise.criado_em}, Resultado: {analise.resultado}%")
    
    print("\nÚltimas análises de Proteína:")
    for analise in AnaliseProteina.objects.all().order_by('-criado_em')[:5]:
        print(f"  ID: {analise.id}, Data: {analise.criado_em}, Resultado: {analise.resultado}%")
    
    print("\nÚltimas análises de Óleo Degomado:")
    for analise in AnaliseOleoDegomado.objects.all().order_by('-criado_em')[:5]:
        print(f"  ID: {analise.id}, Data: {analise.criado_em}, Resultado: {analise.resultado}%")

except RelatorioExpedicao.DoesNotExist:
    print("Relatório ID 5 não encontrado!")
except Exception as e:
    print(f"Erro: {e}")
