from django.conf import settings
from django.http import HttpResponse
import json
import statistics
from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Avg, Min, Max, StdDev
from django.db.models.functions import Extract
from analises.models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import time


def convert_decimal_to_float(stats_dict):
    """Converte valores Decimal para float em um dicionário de estatísticas"""
    converted = {}
    for key, value in stats_dict.items():
        if isinstance(value, Decimal):
            converted[key] = float(value)
        elif value is None:
            converted[key] = None
        else:
            converted[key] = value
    return converted


def home(request):
    """View para a página inicial - Painel de Controle do dia atual"""
    # Data de hoje
    hoje = timezone.localdate()

    # Buscar análises de hoje
    analises_umidade_hoje = AnaliseUmidade.objects.filter(
        data=hoje).order_by('-horario')
    analises_proteina_hoje = AnaliseProteina.objects.filter(
        data=hoje).order_by('-horario')
    analises_oleo_hoje = AnaliseOleoDegomado.objects.filter(
        data=hoje).order_by('-horario')

    # Calcular estatísticas do dia
    total_analises_hoje = analises_umidade_hoje.count(
    ) + analises_proteina_hoje.count() + analises_oleo_hoje.count()

    # Estatísticas de umidade do dia
    stats_umidade_hoje = {}
    if analises_umidade_hoje.exists():
        stats_umidade_hoje = analises_umidade_hoje.aggregate(
            media=Avg('resultado'),
            minimo=Min('resultado'),
            maximo=Max('resultado'),
            total=Count('id')
        )
        stats_umidade_hoje = convert_decimal_to_float(stats_umidade_hoje)
    else:
        stats_umidade_hoje = {'media': 0, 'minimo': 0, 'maximo': 0, 'total': 0}

    # Estatísticas de proteína do dia
    stats_proteina_hoje = {}
    if analises_proteina_hoje.exists():
        stats_proteina_hoje = analises_proteina_hoje.aggregate(
            media=Avg('resultado_corrigido'),
            minimo=Min('resultado_corrigido'),
            maximo=Max('resultado_corrigido'),
            total=Count('id')
        )
        stats_proteina_hoje = convert_decimal_to_float(stats_proteina_hoje)
    else:
        stats_proteina_hoje = {'media': 0,
                               'minimo': 0, 'maximo': 0, 'total': 0}

    # Estatísticas de óleo do dia
    stats_oleo_hoje = {}
    if analises_oleo_hoje.exists():
        stats_oleo_hoje = analises_oleo_hoje.aggregate(
            media=Avg('acidez'),
            minimo=Min('acidez'),
            maximo=Max('acidez'),
            total=Count('id')
        )
        stats_oleo_hoje = convert_decimal_to_float(stats_oleo_hoje)
    else:
        stats_oleo_hoje = {'media': 0, 'minimo': 0, 'maximo': 0, 'total': 0}

    # Últimas análises do dia (últimas 5 de cada tipo)
    ultimas_umidade = analises_umidade_hoje[:5]
    ultimas_proteina = analises_proteina_hoje[:5]
    ultimas_oleo = analises_oleo_hoje[:5]

    # Estatísticas gerais (últimos 30 dias para comparação)
    data_30_dias = hoje - timedelta(days=30)
    total_30_dias = (
        AnaliseUmidade.objects.filter(data__gte=data_30_dias).count() +
        AnaliseProteina.objects.filter(data__gte=data_30_dias).count() +
        AnaliseOleoDegomado.objects.filter(data__gte=data_30_dias).count()
    )

    context = {
        'hoje': hoje,
        'total_analises_hoje': total_analises_hoje,
        'total_30_dias': total_30_dias,

        # Estatísticas do dia
        'stats_umidade_hoje': stats_umidade_hoje,
        'stats_proteina_hoje': stats_proteina_hoje,
        'stats_oleo_hoje': stats_oleo_hoje,

        # Últimas análises do dia
        'ultimas_umidade': ultimas_umidade,
        'ultimas_proteina': ultimas_proteina,
        'ultimas_oleo': ultimas_oleo,

        # Informações do sistema
        'versao_sistema': '2.0',
        'data_ultima_atualizacao': '29/05/2025',
    }

    return render(request, 'home.html', context)


def home_simple(request):
    """View para a página inicial simples/dashboard do QualiSoja"""
    return render(request, 'home_simple.html')


def health_check(request):
    """
    Endpoint de verificação de saúde da aplicação
    """
    start_time = time.time()
    status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'checks': {}
    }

    # Verificar conexão com banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['checks']['database'] = 'healthy'
    except Exception as e:
        status['checks']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'

    # Verificar cache (Redis/memcache)
    try:
        cache.set('health_check', 'ok', 10)
        cache_value = cache.get('health_check')
        if cache_value == 'ok':
            status['checks']['cache'] = 'healthy'
        else:
            status['checks']['cache'] = 'unhealthy: cache not working'
            status['status'] = 'degraded'
    except Exception as e:
        status['checks']['cache'] = f'unhealthy: {str(e)}'
        status['status'] = 'degraded'

    # Tempo de resposta
    response_time = time.time() - start_time
    status['response_time'] = round(response_time * 1000, 2)  # em ms

    # Status code baseado na saúde geral
    if status['status'] == 'healthy':
        status_code = 200
    elif status['status'] == 'degraded':
        status_code = 200  # Ainda funcional, mas com problemas
    else:
        status_code = 503  # Service Unavailable

    return JsonResponse(status, status=status_code)


def teste_acesso(request):
    from django.shortcuts import render
    return render(request, 'teste_acesso.html')


def test_connection(request):
    """View simples para testar a conexão HTTP"""
    return render(request, 'test_connection.html', {
        'debug': settings.DEBUG,
        'https_redirect': getattr(settings, 'SECURE_SSL_REDIRECT', False),
        'codespaces': getattr(settings, 'CODESPACES', False),
    })
