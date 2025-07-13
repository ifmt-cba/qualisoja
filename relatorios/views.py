from urllib.parse import urlencode
from django.views.generic import TemplateView, View, FormView
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.db.models import Avg, Max, Min, Count
from django.urls import reverse
from datetime import timedelta
import io
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Importar models e forms do app analises
from analises.models import (
    AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado,
    AnaliseUrase, AnaliseCinza, AnaliseTeorOleo, 
    AnaliseFibra, AnaliseFosforo, AnaliseSilica
)
from .forms import RelatorioFiltroForm


class RelatorioGerarClassicoView(FormView):
    """View clássica para selecionar parâmetros e gerar relatórios (BACKUP)"""
    template_name = 'relatorios/gerar_relatorio_classico.html'
    form_class = RelatorioFiltroForm

    def get_initial(self):
        """Pré-configura as datas para os últimos 7 dias"""
        initial = super().get_initial()
        tipo = self.request.GET.get('tipo', 'completo')
        data_final = timezone.localdate()
        data_inicial = data_final - timedelta(days=7)
        
        initial.update({
            'data_inicial': data_inicial,
            'data_final': data_final,
            'tipo_relatorio': tipo
        })
        return initial
    
    def form_valid(self, form):
        """Processa o formulário válido e gera o relatório"""
        # Obter dados do formulário
        tipo_relatorio = form.cleaned_data['tipo_relatorio']
        data_inicial = form.cleaned_data['data_inicial']
        data_final = form.cleaned_data['data_final']
        tipo_amostra_umidade = form.cleaned_data.get('tipo_amostra_umidade', '')
        tipo_amostra_proteina = form.cleaned_data.get('tipo_amostra_proteina', '')
        formato_saida = form.cleaned_data.get('formato_saida', 'HTML')
        
        # Construir a URL de redirecionamento com query parameters
        query_params = {
            'tipo': tipo_relatorio,
            'inicio': data_inicial.strftime('%Y-%m-%d'),
            'fim': data_final.strftime('%Y-%m-%d'),
            'formato': formato_saida,
        }
        
        if tipo_amostra_umidade:
            query_params['umidade_tipo'] = tipo_amostra_umidade
        
        if tipo_amostra_proteina:
            query_params['proteina_tipo'] = tipo_amostra_proteina
        
        # Construir a URL com os parâmetros
        url = reverse('relatorios:visualizar')
        url = f"{url}?{urlencode(query_params)}"
        
        # Logs para depuração
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Redirecionando para URL: {url}")
        
        # Redirecionar para a visualização do relatório
        return redirect(url)


class RelatorioGerarView(FormView):
    """View moderna para selecionar parâmetros e gerar relatórios"""
    template_name = 'relatorios/gerar_relatorio.html'
    form_class = RelatorioFiltroForm

    def get_initial(self):
        """Pré-configura as datas para os últimos 7 dias"""
        initial = super().get_initial()
        tipo = self.request.GET.get('tipo', 'completo')
        data_final = timezone.localdate()
        data_inicial = data_final - timedelta(days=7)
        
        initial.update({
            'data_inicial': data_inicial,
            'data_final': data_final,
            'tipo_relatorio': tipo
        })
        return initial
    
    def form_valid(self, form):
        """Processa o formulário válido e gera o relatório"""
        # Obter dados do formulário
        tipo_relatorio = form.cleaned_data['tipo_relatorio']
        data_inicial = form.cleaned_data['data_inicial']
        data_final = form.cleaned_data['data_final']
        tipo_amostra_umidade = form.cleaned_data.get('tipo_amostra_umidade', '')
        tipo_amostra_proteina = form.cleaned_data.get('tipo_amostra_proteina', '')
        formato_saida = form.cleaned_data.get('formato_saida', 'HTML')
        
        # Construir a URL de redirecionamento com query parameters
        query_params = {
            'tipo': tipo_relatorio,
            'inicio': data_inicial.strftime('%Y-%m-%d'),
            'fim': data_final.strftime('%Y-%m-%d'),
            'formato': formato_saida,
        }
        
        if tipo_amostra_umidade:
            query_params['umidade_tipo'] = tipo_amostra_umidade
        
        if tipo_amostra_proteina:
            query_params['proteina_tipo'] = tipo_amostra_proteina
        
        # Construir a URL com os parâmetros
        url = reverse('relatorios:visualizar')
        url = f"{url}?{urlencode(query_params)}"
        
        # Logs para depuração
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Redirecionando para URL: {url}")
        
        # Redirecionar para a visualização do relatório
        return redirect(url)


def obter_dados_relatorio(tipo_relatorio, data_inicial, data_final, tipo_amostra_umidade='', tipo_amostra_proteina='', tipo_amostra_oleo_degomado='', tipo_amostra_urase='', tipo_amostra_cinza='', tipo_amostra_teor_oleo='', tipo_amostra_fibra='', tipo_amostra_fosforo='', tipo_amostra_silica=''):
    """
    Obtém dados para o relatório com base nos parâmetros
    
    Args:
        tipo_relatorio (str): Tipo de relatório ('umidade', 'proteina', 'oleo_degomado', 'urase', 'cinza', 'teor_oleo', 'fibra', 'fosforo', 'silica' ou 'completo')
        data_inicial (date): Data inicial para o relatório
        data_final (date): Data final para o relatório
        tipo_amostra_umidade (str, optional): Filtro de tipo de amostra para umidade
        tipo_amostra_proteina (str, optional): Filtro de tipo de amostra para proteína
        tipo_amostra_oleo_degomado (str, optional): Filtro de tipo de amostra para óleo degomado
        tipo_amostra_urase (str, optional): Filtro de tipo de amostra para urase
        tipo_amostra_cinza (str, optional): Filtro de tipo de amostra para cinza
        tipo_amostra_teor_oleo (str, optional): Filtro de tipo de amostra para teor de óleo
        tipo_amostra_fibra (str, optional): Filtro de tipo de amostra para fibra
        tipo_amostra_fosforo (str, optional): Filtro de tipo de amostra para fósforo
        tipo_amostra_silica (str, optional): Filtro de tipo de amostra para sílica
        
    Returns:
        dict: Dicionário com os dados do relatório
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Validação de parâmetros
    if not tipo_relatorio or not data_inicial or not data_final:
        logger.error("Parâmetros obrigatórios não fornecidos para o relatório")
        raise ValueError("Parâmetros obrigatórios não fornecidos")
        
    if data_inicial > data_final:
        logger.error(f"Data inicial ({data_inicial}) posterior à data final ({data_final})")
        raise ValueError("Data inicial não pode ser posterior à data final")
    
    dados = {}
    
    if tipo_relatorio in ['umidade', 'completo']:
        try:
            # Consulta para análises de umidade
            queryset = AnaliseUmidade.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_umidade:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_umidade)
            
            dados['analises_umidade'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos de umidade
            import json
            umidade_data = []
            
            for analise in queryset:
                umidade_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'peso_amostra': float(analise.peso_amostra) if analise.peso_amostra else 0,
                    'tara': float(analise.tara) if hasattr(analise, 'tara') and analise.tara else 0,
                    'liquido': float(analise.liquido) if hasattr(analise, 'liquido') and analise.liquido else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0,
                    'fator_correcao': float(analise.fator_correcao) if hasattr(analise, 'fator_correcao') and analise.fator_correcao else 0
                })
                
            dados['analises_umidade_json'] = json.dumps(umidade_data)
            
            # Cálculo de estatísticas - usando 'resultado'
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_umidade'] = {
                    'media': queryset.aggregate(Avg('resultado'))['resultado__avg'],
                    'minimo': queryset.aggregate(Min('resultado'))['resultado__min'],
                    'maximo': queryset.aggregate(Max('resultado'))['resultado__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de umidade: {str(e)}")
            dados['erro_umidade'] = str(e)
    
    if tipo_relatorio in ['proteina', 'completo']:
        try:
            # Consulta para análises de proteína
            queryset = AnaliseProteina.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_proteina:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_proteina)
            
            dados['analises_proteina'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            proteina_data = []
            
            for analise in queryset:
                proteina_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'peso_amostra': float(analise.peso_amostra),
                    'ml_gasto': float(analise.ml_gasto) if analise.ml_gasto else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0,
                    'resultado_corrigido': float(analise.resultado_corrigido) if analise.resultado_corrigido else 0
                })
                
            dados['analises_proteina_json'] = json.dumps(proteina_data)
            
            # Cálculo de estatísticas - usando 'resultado' e 'resultado_corrigido' se disponíveis
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                estatisticas = {
                    'total': queryset.count(),
                }
                
                # Verificar se o campo resultado existe
                estatisticas['media'] = queryset.aggregate(Avg('resultado'))['resultado__avg']
                estatisticas['minimo'] = queryset.aggregate(Min('resultado'))['resultado__min']
                estatisticas['maximo'] = queryset.aggregate(Max('resultado'))['resultado__max']
                
                # Verificar se resultado_corrigido existe e usá-lo se disponível
                try:
                    estatisticas['media_corrigida'] = queryset.aggregate(Avg('resultado_corrigido'))['resultado_corrigido__avg']
                    estatisticas['minimo_corrigido'] = queryset.aggregate(Min('resultado_corrigido'))['resultado_corrigido__min']
                    estatisticas['maximo_corrigido'] = queryset.aggregate(Max('resultado_corrigido'))['resultado_corrigido__max']
                except:
                    pass  # Ignorar se o campo não existir
                    
                dados['estatisticas_proteina'] = estatisticas
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de proteína: {str(e)}")
            dados['erro_proteina'] = str(e)
    
    if tipo_relatorio in ['oleo_degomado', 'completo']:
        try:
            # Consulta para análises de óleo degomado
            queryset = AnaliseOleoDegomado.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_oleo_degomado:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_oleo_degomado)
            
            dados['analises_oleo_degomado'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            oleo_degomado_data = []
            
            for analise in queryset:
                oleo_degomado_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'tipo_analise': analise.get_tipo_analise_display(),
                    'tara': float(analise.tara) if analise.tara else 0,
                    'liquido': float(analise.liquido) if analise.liquido else 0,
                    'peso_amostra': float(analise.peso_amostra) if analise.peso_amostra else 0,
                    'titulacao': float(analise.titulacao) if analise.titulacao else 0,
                    'fator_correcao': float(analise.fator_correcao) if analise.fator_correcao else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0
                })
                
            dados['analises_oleo_degomado_json'] = json.dumps(oleo_degomado_data)
            
            # Cálculo de estatísticas - usando 'resultado'
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                estatisticas = {
                    'total': queryset.count(),
                }
                
                # Estatísticas baseadas no resultado
                estatisticas['media'] = queryset.aggregate(Avg('resultado'))['resultado__avg']
                estatisticas['minimo'] = queryset.aggregate(Min('resultado'))['resultado__min']
                estatisticas['maximo'] = queryset.aggregate(Max('resultado'))['resultado__max']
                
                # Estatísticas específicas do óleo degomado (campos que realmente existem)
                try:
                    estatisticas['titulacao_media'] = queryset.aggregate(Avg('titulacao'))['titulacao__avg']
                    estatisticas['titulacao_min'] = queryset.aggregate(Min('titulacao'))['titulacao__min']
                    estatisticas['titulacao_max'] = queryset.aggregate(Max('titulacao'))['titulacao__max']
                    
                    estatisticas['peso_amostra_media'] = queryset.aggregate(Avg('peso_amostra'))['peso_amostra__avg']
                    estatisticas['fator_correcao_media'] = queryset.aggregate(Avg('fator_correcao'))['fator_correcao__avg']
                except:
                    pass  # Ignorar se os campos não existirem
                    
                dados['estatisticas_oleo_degomado'] = estatisticas
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de óleo degomado: {str(e)}")
            dados['erro_oleo_degomado'] = str(e)
    
    # Análise de Urase
    if tipo_relatorio in ['urase', 'completo']:
        try:
            queryset = AnaliseUrase.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_urase:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_urase)
            
            dados['analises_urase'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            urase_data = []
            
            for analise in queryset:
                urase_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'amostra_1': float(analise.amostra_1) if analise.amostra_1 else 0,
                    'amostra_2': float(analise.amostra_2) if analise.amostra_2 else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0,
                })
                
            dados['analises_urase_json'] = json.dumps(urase_data)
            
            # Cálculo de estatísticas
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_urase'] = {
                    'media': queryset.aggregate(Avg('resultado'))['resultado__avg'],
                    'minimo': queryset.aggregate(Min('resultado'))['resultado__min'],
                    'maximo': queryset.aggregate(Max('resultado'))['resultado__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de urase: {str(e)}")
            dados['erro_urase'] = str(e)
    
    # Análise de Cinza
    if tipo_relatorio in ['cinza', 'completo']:
        try:
            queryset = AnaliseCinza.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_cinza:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_cinza)
            
            dados['analises_cinza'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            cinza_data = []
            
            for analise in queryset:
                cinza_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'peso_amostra': float(analise.peso_amostra) if analise.peso_amostra else 0,
                    'peso_cadinho': float(analise.peso_cadinho) if analise.peso_cadinho else 0,
                    'peso_cinza': float(analise.peso_cinza) if analise.peso_cinza else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0,
                })
                
            dados['analises_cinza_json'] = json.dumps(cinza_data)
            
            # Cálculo de estatísticas
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_cinza'] = {
                    'media': queryset.aggregate(Avg('resultado'))['resultado__avg'],
                    'minimo': queryset.aggregate(Min('resultado'))['resultado__min'],
                    'maximo': queryset.aggregate(Max('resultado'))['resultado__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de cinza: {str(e)}")
            dados['erro_cinza'] = str(e)
    
    # Análise de Teor de Óleo
    if tipo_relatorio in ['teor_oleo', 'completo']:
        try:
            queryset = AnaliseTeorOleo.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_teor_oleo:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_teor_oleo)
            
            dados['analises_teor_oleo'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            teor_oleo_data = []
            
            for analise in queryset:
                teor_oleo_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'peso_amostra': float(analise.peso_amostra) if analise.peso_amostra else 0,
                    'peso_tara': float(analise.peso_tara) if analise.peso_tara else 0,
                    'peso_liquido': float(analise.peso_liquido) if analise.peso_liquido else 0,
                    'teor_oleo': float(analise.teor_oleo) if analise.teor_oleo else 0,
                })
                
            dados['analises_teor_oleo_json'] = json.dumps(teor_oleo_data)
            
            # Cálculo de estatísticas
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_teor_oleo'] = {
                    'media': queryset.aggregate(Avg('teor_oleo'))['teor_oleo__avg'],
                    'minimo': queryset.aggregate(Min('teor_oleo'))['teor_oleo__min'],
                    'maximo': queryset.aggregate(Max('teor_oleo'))['teor_oleo__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de teor de óleo: {str(e)}")
            dados['erro_teor_oleo'] = str(e)
    
    # Análise de Fibra
    if tipo_relatorio in ['fibra', 'completo']:
        try:
            queryset = AnaliseFibra.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_fibra:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_fibra)
            
            dados['analises_fibra'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            fibra_data = []
            
            for analise in queryset:
                fibra_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'peso_amostra': float(analise.peso_amostra) if analise.peso_amostra else 0,
                    'peso_tara': float(analise.peso_tara) if analise.peso_tara else 0,
                    'peso_fibra': float(analise.peso_fibra) if analise.peso_fibra else 0,
                    'peso_branco': float(analise.peso_branco) if analise.peso_branco else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0,
                })
                
            dados['analises_fibra_json'] = json.dumps(fibra_data)
            
            # Cálculo de estatísticas
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_fibra'] = {
                    'media': queryset.aggregate(Avg('resultado'))['resultado__avg'],
                    'minimo': queryset.aggregate(Min('resultado'))['resultado__min'],
                    'maximo': queryset.aggregate(Max('resultado'))['resultado__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de fibra: {str(e)}")
            dados['erro_fibra'] = str(e)
    
    # Análise de Fósforo
    if tipo_relatorio in ['fosforo', 'completo']:
        try:
            queryset = AnaliseFosforo.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_fosforo:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_fosforo)
            
            dados['analises_fosforo'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            fosforo_data = []
            
            for analise in queryset:
                fosforo_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'absorbancia_amostra': float(analise.absorbancia_amostra) if analise.absorbancia_amostra else 0,
                    'peso_amostra': float(analise.peso_amostra) if analise.peso_amostra else 0,
                    'concentracao_padrao': float(analise.concentracao_padrao) if analise.concentracao_padrao else 0,
                    'volume_solucao': float(analise.volume_solucao) if analise.volume_solucao else 0,
                    'volume_aliquota': float(analise.volume_aliquota) if analise.volume_aliquota else 0,
                    'absorbancia_padrao': float(analise.absorbancia_padrao) if analise.absorbancia_padrao else 0,
                    'resultado': float(analise.resultado) if analise.resultado else 0,
                })
                
            dados['analises_fosforo_json'] = json.dumps(fosforo_data)
            
            # Cálculo de estatísticas
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_fosforo'] = {
                    'media': queryset.aggregate(Avg('resultado'))['resultado__avg'],
                    'minimo': queryset.aggregate(Min('resultado'))['resultado__min'],
                    'maximo': queryset.aggregate(Max('resultado'))['resultado__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de fósforo: {str(e)}")
            dados['erro_fosforo'] = str(e)
    
    # Análise de Sílica
    if tipo_relatorio in ['silica', 'completo']:
        try:
            queryset = AnaliseSilica.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_silica:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_silica)
            
            dados['analises_silica'] = queryset.order_by('-data', '-horario')
            
            # Preparar dados em JSON para os gráficos
            import json
            silica_data = []
            
            for analise in queryset:
                silica_data.append({
                    'data': analise.data.strftime('%Y-%m-%d'),
                    'horario': analise.horario.strftime('%H:%M'),
                    'tipo': analise.get_tipo_amostra_display(),
                    'tipo_code': analise.tipo_amostra,
                    'analise_cinza_id': analise.analise_cinza.id if analise.analise_cinza else None,
                    'analise_cinza_resultado': float(analise.analise_cinza.resultado) if analise.analise_cinza and analise.analise_cinza.resultado else 0,
                    'resultado_silica': float(analise.resultado_silica) if analise.resultado_silica else 0,
                    'resultado_final': float(analise.resultado_final) if analise.resultado_final else 0,
                })
                
            dados['analises_silica_json'] = json.dumps(silica_data)
            
            # Cálculo de estatísticas
            if queryset.exists():
                from django.db.models import Avg, Min, Max
                dados['estatisticas_silica'] = {
                    'media': queryset.aggregate(Avg('resultado_final'))['resultado_final__avg'],
                    'minimo': queryset.aggregate(Min('resultado_final'))['resultado_final__min'],
                    'maximo': queryset.aggregate(Max('resultado_final'))['resultado_final__max'],
                    'total': queryset.count(),
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao processar dados de sílica: {str(e)}")
            dados['erro_silica'] = str(e)
    
    return dados


def gerar_pdf_relatorio(dados, tipo_relatorio, data_inicial, data_final):
    """Gera um relatório em formato PDF"""
    from io import BytesIO
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{tipo_relatorio}_{data_inicial}_a_{data_final}.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos e título
    styles = getSampleStyleSheet()
    titulo_texto = {
        'umidade': "Relatório de Umidade",
        'proteina': "Relatório de Proteína", 
        'oleo_degomado': "Relatório de Óleo Degomado",
        'urase': "Relatório de Urase",
        'cinza': "Relatório de Cinza",
        'teor_oleo': "Relatório de Teor de Óleo",
        'fibra': "Relatório de Fibra",
        'fosforo': "Relatório de Fósforo",
        'silica': "Relatório de Sílica",
        'completo': "Relatório Completo"
    }.get(tipo_relatorio, "Relatório Completo")
    
    elements.append(Paragraph(f"{titulo_texto}: {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}", styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Seção de Proteínas
    if 'analises_proteina' in dados and dados['analises_proteina'].exists():
        elements.append(Paragraph("Análises de Proteína", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        # Cabeçalho da tabela
        data = [["Data", "Hora", "Tipo", "Peso (g)", "ML Gasto", "Result (%)", "Corrigido (%)", "Média 24h"]]
        
        # Dados da tabela
        for analise in dados['analises_proteina']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.peso_amostra:.2f}",
                f"{analise.ml_gasto:.2f}" if analise.ml_gasto else "-",
                f"{analise.resultado:.2f}" if analise.resultado else "-",
                f"{analise.resultado_corrigido:.2f}" if analise.resultado_corrigido else "-",
                "Sim" if analise.eh_media_24h else "Não"  # Proteína tem eh_media_24h
            ])
        
        # Criar e estilizar a tabela
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Adicionar estatísticas se disponíveis
        if 'estatisticas_proteina' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_proteina']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}%" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}%" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}%" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Seção de Umidade (similar à seção de Proteínas)
    if 'analises_umidade' in dados and dados['analises_umidade'].exists():
        elements.append(Paragraph("Análises de Umidade", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        # Cabeçalho e dados da tabela
        data = [["Data", "Hora", "Tipo", "Tara (g)", "Líquido (g)", "Peso (g)", "Resultado (%)", "Fator", "Média 24h"]]
        
        for analise in dados['analises_umidade']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.tara:.2f}" if hasattr(analise, 'tara') and analise.tara else "-",
                f"{analise.liquido:.2f}" if hasattr(analise, 'liquido') and analise.liquido else "-",
                f"{analise.peso_amostra:.2f}",
                f"{analise.resultado:.2f}" if hasattr(analise, 'resultado') and analise.resultado else "-",  # Corrigido
                f"{analise.fator_correcao:.2f}" if hasattr(analise, 'fator_correcao') and analise.fator_correcao else "-",
                "Não"  # AnaliseUmidade não tem o campo eh_media_24h
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de umidade
        if 'estatisticas_umidade' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_umidade']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}%" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}%" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}%" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
    
    # Seção de Óleo Degomado
    if 'analises_oleo_degomado' in dados and dados['analises_oleo_degomado'].exists():
        elements.append(Paragraph("Análises de Óleo Degomado", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        # Cabeçalho e dados da tabela
        data = [["Data", "Hora", "Tipo", "Tara", "Líquido", "Peso Amostra", "Titulação", "Fator Correção", "Resultado"]]
        
        for analise in dados['analises_oleo_degomado']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.tara:.2f}" if analise.tara else "-",
                f"{analise.liquido:.2f}" if analise.liquido else "-",
                f"{analise.peso_amostra:.2f}" if analise.peso_amostra else "-",
                f"{analise.titulacao:.2f}" if analise.titulacao else "-",
                f"{analise.fator_correcao:.2f}" if analise.fator_correcao else "-",
                f"{analise.resultado:.2f}" if analise.resultado else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
    
    # Seção de Urase
    if 'analises_urase' in dados and dados['analises_urase'].exists():
        elements.append(Paragraph("Análises de Urase", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        data = [["Data", "Hora", "Tipo", "Amostra 1", "Amostra 2", "Resultado"]]
        
        for analise in dados['analises_urase']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.amostra_1:.2f}" if analise.amostra_1 else "-",
                f"{analise.amostra_2:.2f}" if analise.amostra_2 else "-",
                f"{analise.resultado:.2f}" if analise.resultado else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de urase
        if 'estatisticas_urase' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_urase']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Seção de Cinza
    if 'analises_cinza' in dados and dados['analises_cinza'].exists():
        elements.append(Paragraph("Análises de Cinza", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        data = [["Data", "Hora", "Tipo", "Peso Amostra", "Peso Cadinho", "Peso Cinza", "Resultado (%)"]]
        
        for analise in dados['analises_cinza']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.peso_amostra:.4f}" if analise.peso_amostra else "-",
                f"{analise.peso_cadinho:.4f}" if analise.peso_cadinho else "-",
                f"{analise.peso_cinza:.4f}" if analise.peso_cinza else "-",
                f"{analise.resultado:.2f}" if analise.resultado else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de cinza
        if 'estatisticas_cinza' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_cinza']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}%" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}%" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}%" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Seção de Teor de Óleo
    if 'analises_teor_oleo' in dados and dados['analises_teor_oleo'].exists():
        elements.append(Paragraph("Análises de Teor de Óleo", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        data = [["Data", "Hora", "Tipo", "Peso Amostra", "Peso Tara", "Peso Líquido", "Teor Óleo (%)"]]
        
        for analise in dados['analises_teor_oleo']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.peso_amostra:.3f}" if analise.peso_amostra else "-",
                f"{analise.peso_tara:.3f}" if analise.peso_tara else "-",
                f"{analise.peso_liquido:.3f}" if analise.peso_liquido else "-",
                f"{analise.teor_oleo:.2f}" if analise.teor_oleo else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de teor de óleo
        if 'estatisticas_teor_oleo' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_teor_oleo']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}%" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}%" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}%" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Seção de Fibra
    if 'analises_fibra' in dados and dados['analises_fibra'].exists():
        elements.append(Paragraph("Análises de Fibra", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        data = [["Data", "Hora", "Tipo", "Peso Amostra", "Peso Tara", "Peso Fibra", "Peso Branco", "Resultado (%)"]]
        
        for analise in dados['analises_fibra']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.peso_amostra:.4f}" if analise.peso_amostra else "-",
                f"{analise.peso_tara:.4f}" if analise.peso_tara else "-",
                f"{analise.peso_fibra:.4f}" if analise.peso_fibra else "-",
                f"{analise.peso_branco:.4f}" if analise.peso_branco else "-",
                f"{analise.resultado:.2f}" if analise.resultado else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de fibra
        if 'estatisticas_fibra' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_fibra']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}%" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}%" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}%" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Seção de Fósforo
    if 'analises_fosforo' in dados and dados['analises_fosforo'].exists():
        elements.append(Paragraph("Análises de Fósforo", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        data = [["Data", "Hora", "Tipo", "Absorbância", "Peso Amostra", "Resultado (ppm)"]]
        
        for analise in dados['analises_fosforo']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.absorbancia_amostra:.6f}" if analise.absorbancia_amostra else "-",
                f"{analise.peso_amostra:.4f}" if analise.peso_amostra else "-",
                f"{analise.resultado:.0f}" if analise.resultado else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de fósforo
        if 'estatisticas_fosforo' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_fosforo']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.0f} ppm" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.0f} ppm" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.0f} ppm" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Seção de Sílica
    if 'analises_silica' in dados and dados['analises_silica'].exists():
        elements.append(Paragraph("Análises de Sílica", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        data = [["Data", "Hora", "Tipo", "Análise Cinza", "Resultado Sílica", "Resultado Final"]]
        
        for analise in dados['analises_silica']:
            data.append([
                analise.data.strftime('%d/%m/%Y'),
                analise.horario.strftime('%H:%M'),
                analise.get_tipo_amostra_display(),
                f"{analise.analise_cinza.resultado:.2f}%" if analise.analise_cinza and analise.analise_cinza.resultado else "-",
                f"{analise.resultado_silica:.2f}%" if analise.resultado_silica else "-",
                f"{analise.resultado_final:.2f}%" if analise.resultado_final else "-"
            ])
        
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.silver),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Estatísticas de sílica
        if 'estatisticas_silica' in dados:
            elements.append(Paragraph("Estatísticas:", styles['Heading3']))
            estat = dados['estatisticas_silica']
            estat_data = [
                ["Média", "Mínimo", "Máximo", "Total de Análises"],
                [
                    f"{estat['media']:.2f}%" if estat['media'] is not None else "-",
                    f"{estat['minimo']:.2f}%" if estat['minimo'] is not None else "-",
                    f"{estat['maximo']:.2f}%" if estat['maximo'] is not None else "-",
                    str(estat['total'])
                ]
            ]
            t = Table(estat_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 30))
    
    # Construir o PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response.write(pdf)
    return response


def gerar_excel_relatorio(dados, tipo_relatorio, data_inicial, data_final):
    """Gera um relatório em formato Excel"""
    import xlsxwriter
    from io import BytesIO
    
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    
    # Formatos
    header_format = workbook.add_format({
        'bold': True, 
        'bg_color': '#4472C4', 
        'color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    cell_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    number_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'num_format': '0.00'
    })
    
    # Planilha para Proteína
    if 'analises_proteina' in dados and dados['analises_proteina'].exists():
        worksheet = workbook.add_worksheet('Proteína')
        
        # Adicionar cabeçalho
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Peso da Amostra (g)', 
                  'ML Gasto', 'Resultado (%)', 'Resultado Corrigido (%)', 'Média 24h']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)  # Largura da coluna
        
        # Adicionar dados
        for row, analise in enumerate(dados['analises_proteina'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.peso_amostra, number_format)
            worksheet.write(row, 4, analise.ml_gasto if analise.ml_gasto else 0, number_format)
            worksheet.write(row, 5, analise.resultado if analise.resultado else 0, number_format)
            worksheet.write(row, 6, analise.resultado_corrigido if analise.resultado_corrigido else 0, number_format)
            worksheet.write(row, 7, "Sim" if analise.eh_media_24h else "Não", cell_format)  # Proteína tem eh_media_24h
        
        # Adicionar estatísticas
        if 'estatisticas_proteina' in dados:
            row_start = len(dados['analises_proteina']) + 3
            estat = dados['estatisticas_proteina']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (%)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (%)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo (%)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Umidade
    if 'analises_umidade' in dados and dados['analises_umidade'].exists():
        worksheet = workbook.add_worksheet('Umidade')
        
        # Adicionar cabeçalho
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Tara', 'Líquido', 
                  'Peso da Amostra (g)', 'Resultado (%)', 'Fator de Correção', 'Média 24h']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)  # Largura da coluna
        
        # Adicionar dados
        for row, analise in enumerate(dados['analises_umidade'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.tara if hasattr(analise, 'tara') and analise.tara else 0, number_format)
            worksheet.write(row, 4, analise.liquido if hasattr(analise, 'liquido') and analise.liquido else 0, number_format)
            worksheet.write(row, 5, analise.peso_amostra, number_format)
            worksheet.write(row, 6, analise.resultado if hasattr(analise, 'resultado') else 0, number_format)  # Corrigido
            worksheet.write(row, 7, analise.fator_correcao if hasattr(analise, 'fator_correcao') else 0, number_format)
            worksheet.write(row, 8, "Não", cell_format)  # AnaliseUmidade não tem eh_media_24h
        
        # Adicionar estatísticas
        if 'estatisticas_umidade' in dados:
            row_start = len(dados['analises_umidade']) + 3
            estat = dados['estatisticas_umidade']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (%)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (%)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo (%)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Óleo Degomado
    if 'analises_oleo_degomado' in dados and dados['analises_oleo_degomado'].exists():
        worksheet = workbook.add_worksheet('Óleo Degomado')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Tara', 'Líquido', 
                  'Peso Amostra', 'Titulação', 'Fator Correção', 'Resultado']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_oleo_degomado'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.tara if analise.tara else 0, number_format)
            worksheet.write(row, 4, analise.liquido if analise.liquido else 0, number_format)
            worksheet.write(row, 5, analise.peso_amostra if analise.peso_amostra else 0, number_format)
            worksheet.write(row, 6, analise.titulacao if analise.titulacao else 0, number_format)
            worksheet.write(row, 7, analise.fator_correcao if analise.fator_correcao else 0, number_format)
            worksheet.write(row, 8, analise.resultado if analise.resultado else 0, number_format)
    
    # Planilha para Urase
    if 'analises_urase' in dados and dados['analises_urase'].exists():
        worksheet = workbook.add_worksheet('Urase')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Amostra 1', 'Amostra 2', 'Resultado']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_urase'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.amostra_1 if analise.amostra_1 else 0, number_format)
            worksheet.write(row, 4, analise.amostra_2 if analise.amostra_2 else 0, number_format)
            worksheet.write(row, 5, analise.resultado if analise.resultado else 0, number_format)
        
        # Estatísticas de urase
        if 'estatisticas_urase' in dados:
            row_start = len(dados['analises_urase']) + 3
            estat = dados['estatisticas_urase']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Cinza
    if 'analises_cinza' in dados and dados['analises_cinza'].exists():
        worksheet = workbook.add_worksheet('Cinza')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Peso Amostra (g)', 
                  'Peso Cadinho (g)', 'Peso Cinza (g)', 'Resultado (%)']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_cinza'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.peso_amostra if analise.peso_amostra else 0, number_format)
            worksheet.write(row, 4, analise.peso_cadinho if analise.peso_cadinho else 0, number_format)
            worksheet.write(row, 5, analise.peso_cinza if analise.peso_cinza else 0, number_format)
            worksheet.write(row, 6, analise.resultado if analise.resultado else 0, number_format)
        
        # Estatísticas de cinza
        if 'estatisticas_cinza' in dados:
            row_start = len(dados['analises_cinza']) + 3
            estat = dados['estatisticas_cinza']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (%)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (%)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo (%)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Teor de Óleo
    if 'analises_teor_oleo' in dados and dados['analises_teor_oleo'].exists():
        worksheet = workbook.add_worksheet('Teor de Óleo')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Peso Amostra (g)', 
                  'Peso Tara (g)', 'Peso Líquido (g)', 'Teor Óleo (%)']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_teor_oleo'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.peso_amostra if analise.peso_amostra else 0, number_format)
            worksheet.write(row, 4, analise.peso_tara if analise.peso_tara else 0, number_format)
            worksheet.write(row, 5, analise.peso_liquido if analise.peso_liquido else 0, number_format)
            worksheet.write(row, 6, analise.teor_oleo if analise.teor_oleo else 0, number_format)
        
        # Estatísticas de teor de óleo
        if 'estatisticas_teor_oleo' in dados:
            row_start = len(dados['analises_teor_oleo']) + 3
            estat = dados['estatisticas_teor_oleo']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (%)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (%)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start +  3, 0, "Máximo (%)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Fibra
    if 'analises_fibra' in dados and dados['analises_fibra'].exists():
        worksheet = workbook.add_worksheet('Fibra')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Peso Amostra (g)', 
                  'Peso Tara (g)', 'Peso Fibra (g)', 'Peso Branco (g)', 'Resultado (%)']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_fibra'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.peso_amostra if analise.peso_amostra else 0, number_format)
            worksheet.write(row, 4, analise.peso_tara if analise.peso_tara else 0, number_format)
            worksheet.write(row, 5, analise.peso_fibra if analise.peso_fibra else 0, number_format)
            worksheet.write(row, 6, analise.peso_branco if analise.peso_branco else 0, number_format)
            worksheet.write(row, 7, analise.resultado if analise.resultado else 0, number_format)
        
        # Estatísticas de fibra
        if 'estatisticas_fibra' in dados:
            row_start = len(dados['analises_fibra']) + 3
            estat = dados['estatisticas_fibra']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (%)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (%)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo (%)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Fósforo
    if 'analises_fosforo' in dados and dados['analises_fosforo'].exists():
        worksheet = workbook.add_worksheet('Fósforo')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Absorbância Amostra', 
                  'Peso Amostra (g)', 'Concentração Padrão', 'Volume Solução', 
                  'Volume Alíquota', 'Absorbância Padrão', 'Resultado (ppm)']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_fosforo'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.absorbancia_amostra if analise.absorbancia_amostra else 0, number_format)
            worksheet.write(row, 4, analise.peso_amostra if analise.peso_amostra else 0, number_format)
            worksheet.write(row, 5, analise.concentracao_padrao if analise.concentracao_padrao else 0, number_format)
            worksheet.write(row, 6, analise.volume_solucao if analise.volume_solucao else 0, number_format)
            worksheet.write(row, 7, analise.volume_aliquota if analise.volume_aliquota else 0, number_format)
            worksheet.write(row, 8, analise.absorbancia_padrao if analise.absorbancia_padrao else 0, number_format)
            worksheet.write(row, 9, analise.resultado if analise.resultado else 0, number_format)
        
        # Estatísticas de fósforo
        if 'estatisticas_fosforo' in dados:
            row_start = len(dados['analises_fosforo']) + 3
            estat = dados['estatisticas_fosforo']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (ppm)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (ppm)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo (ppm)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Planilha para Sílica
    if 'analises_silica' in dados and dados['analises_silica'].exists():
        worksheet = workbook.add_worksheet('Sílica')
        
        headers = ['Data', 'Horário', 'Tipo de Amostra', 'Análise Cinza ID', 
                  'Resultado Cinza (%)', 'Resultado Sílica (%)', 'Resultado Final (%)']
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)
        
        for row, analise in enumerate(dados['analises_silica'], start=1):
            worksheet.write(row, 0, analise.data.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 1, analise.horario.strftime('%H:%M'), cell_format)
            worksheet.write(row, 2, analise.get_tipo_amostra_display(), cell_format)
            worksheet.write(row, 3, analise.analise_cinza.id if analise.analise_cinza else "", cell_format)
            worksheet.write(row, 4, analise.analise_cinza.resultado if analise.analise_cinza and analise.analise_cinza.resultado else 0, number_format)
            worksheet.write(row, 5, analise.resultado_silica if analise.resultado_silica else 0, number_format)
            worksheet.write(row, 6, analise.resultado_final if analise.resultado_final else 0, number_format)
        
        # Estatísticas de sílica
        if 'estatisticas_silica' in dados:
            row_start = len(dados['analises_silica']) + 3
            estat = dados['estatisticas_silica']
            
            worksheet.write(row_start, 0, "Estatísticas", header_format)
            worksheet.write(row_start + 1, 0, "Média (%)", cell_format)
            worksheet.write(row_start + 1, 1, estat['media'], number_format)
            worksheet.write(row_start + 2, 0, "Mínimo (%)", cell_format)
            worksheet.write(row_start + 2, 1, estat['minimo'], number_format)
            worksheet.write(row_start + 3, 0, "Máximo (%)", cell_format)
            worksheet.write(row_start + 3, 1, estat['maximo'], number_format)
            worksheet.write(row_start + 4, 0, "Total de Análises", cell_format)
            worksheet.write(row_start + 4, 1, estat['total'], cell_format)
    
    # Finalizar e retornar o arquivo Excel
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=relatorio_{tipo_relatorio}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}.xlsx'
    
    return response


class RelatorioVisualizarView(TemplateView):
    """View para visualizar relatórios gerados"""
    template_name = 'relatorios/visualizar_relatorio.html'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import logging
        self.logger = logging.getLogger(__name__)
    
    def _parse_date_params(self, request):
        """
        Processa os parâmetros de data da requisição.
        
        Returns:
            tuple: (tipo_relatorio, data_inicial, data_final, formato, tipo_amostra_umidade, tipo_amostra_proteina, tipo_amostra_oleo_degomado, tipo_amostra_urase, tipo_amostra_cinza, tipo_amostra_teor_oleo, tipo_amostra_fibra, tipo_amostra_fosforo, tipo_amostra_silica)
            ou None se ocorrer um erro.
        """
        try:
            from datetime import datetime
            
            tipo_relatorio = request.GET.get('tipo', 'completo')
            data_inicial_str = request.GET.get('inicio') or request.GET.get('data_inicial')
            data_final_str = request.GET.get('fim') or request.GET.get('data_final')
            formato = request.GET.get('formato', 'HTML')
            tipo_amostra_umidade = request.GET.get('umidade_tipo', '')
            tipo_amostra_proteina = request.GET.get('proteina_tipo', '')
            tipo_amostra_oleo_degomado = request.GET.get('oleo_degomado_tipo', '')
            tipo_amostra_urase = request.GET.get('urase_tipo', '')
            tipo_amostra_cinza = request.GET.get('cinza_tipo', '')
            tipo_amostra_teor_oleo = request.GET.get('teor_oleo_tipo', '')
            tipo_amostra_fibra = request.GET.get('fibra_tipo', '')
            tipo_amostra_fosforo = request.GET.get('fosforo_tipo', '')
            tipo_amostra_silica = request.GET.get('silica_tipo', '')
            
            # Validar parâmetros
            if not data_inicial_str or not data_final_str:
                raise ValueError("Datas inicial e final são obrigatórias")
                
            # Converter strings para datas
            data_inicial = datetime.strptime(data_inicial_str, '%Y-%m-%d').date()
            data_final = datetime.strptime(data_final_str, '%Y-%m-%d').date()
            
            if data_inicial > data_final:
                raise ValueError("A data inicial não pode ser posterior à data final")
                
            return (
                tipo_relatorio, 
                data_inicial, 
                data_final, 
                formato,
                tipo_amostra_umidade,
                tipo_amostra_proteina,
                tipo_amostra_oleo_degomado,
                tipo_amostra_urase,
                tipo_amostra_cinza,
                tipo_amostra_teor_oleo,
                tipo_amostra_fibra,
                tipo_amostra_fosforo,
                tipo_amostra_silica
            )
        except ValueError as e:
            self.logger.error(f"Erro ao processar parâmetros de data: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Erro inesperado ao processar parâmetros: {str(e)}")
            return None
    
    def get(self, request, *args, **kwargs):
        """Sobrescrever o método get para lidar com formatos especiais"""
        params = self._parse_date_params(request)
        
        if not params:
            # Se houver erro nos parâmetros, exibir mensagem de erro na página HTML
            return super().get(request, *args, **kwargs)
            
        tipo_relatorio, data_inicial, data_final, formato, tipo_amostra_umidade, tipo_amostra_proteina, tipo_amostra_oleo_degomado, tipo_amostra_urase, tipo_amostra_cinza, tipo_amostra_teor_oleo, tipo_amostra_fibra, tipo_amostra_fosforo, tipo_amostra_silica = params
            
        # Para formatos de arquivo, gera o arquivo diretamente
        if formato in ['PDF', 'EXCEL']:
            try:
                # Obter dados para o relatório
                dados = obter_dados_relatorio(
                    tipo_relatorio, 
                    data_inicial, 
                    data_final, 
                    tipo_amostra_umidade, 
                    tipo_amostra_proteina,
                    tipo_amostra_oleo_degomado,
                    tipo_amostra_urase,
                    tipo_amostra_cinza,
                    tipo_amostra_teor_oleo,
                    tipo_amostra_fibra,
                    tipo_amostra_fosforo,
                    tipo_amostra_silica
                )
                
                # Gerar o arquivo apropriado
                if formato == 'PDF':
                    return gerar_pdf_relatorio(dados, tipo_relatorio, data_inicial, data_final)
                elif formato == 'EXCEL':
                    return gerar_excel_relatorio(dados, tipo_relatorio, data_inicial, data_final)
            
            except Exception as e:
                self.logger.error(f"Erro ao gerar relatório {formato}: {str(e)}")
                # Em caso de erro, continue para renderizar o template com a mensagem de erro
        
        # Para formato HTML ou em caso de erro, renderiza o template normalmente
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Prepara o contexto para renderização do template."""
        context = super().get_context_data(**kwargs)
        context['paginaAtiva'] = 'relatorios'
        
        params = self._parse_date_params(self.request)
        
        if not params:
            context['error'] = "Parâmetros de data inválidos. Verifique se as datas estão no formato correto."
            return context
            
        tipo_relatorio, data_inicial, data_final, formato, tipo_amostra_umidade, tipo_amostra_proteina, tipo_amostra_oleo_degomado, tipo_amostra_urase, tipo_amostra_cinza, tipo_amostra_teor_oleo, tipo_amostra_fibra, tipo_amostra_fosforo, tipo_amostra_silica = params
        
        try:
            # Obter dados para o relatório
            dados = obter_dados_relatorio(
                tipo_relatorio, 
                data_inicial, 
                data_final, 
                tipo_amostra_umidade, 
                tipo_amostra_proteina,
                tipo_amostra_oleo_degomado,
                tipo_amostra_urase,
                tipo_amostra_cinza,
                tipo_amostra_teor_oleo,
                tipo_amostra_fibra,
                tipo_amostra_fosforo,
                tipo_amostra_silica
            )
            
            # Adicionar todos os dados ao contexto
            context.update({
                'tipo_relatorio': tipo_relatorio,
                'data_inicial': data_inicial,
                'data_final': data_final,
                'formato': formato,
                'tipo_amostra_umidade': tipo_amostra_umidade,
                'tipo_amostra_proteina': tipo_amostra_proteina,
                'tipo_amostra_oleo_degomado': tipo_amostra_oleo_degomado,
                'tipo_amostra_urase': tipo_amostra_urase,
                'tipo_amostra_cinza': tipo_amostra_cinza,
                'tipo_amostra_teor_oleo': tipo_amostra_teor_oleo,
                'tipo_amostra_fibra': tipo_amostra_fibra,
                'tipo_amostra_fosforo': tipo_amostra_fosforo,
                'tipo_amostra_silica': tipo_amostra_silica,
                'query_string': self.request.META.get('QUERY_STRING', ''),
                **dados
            })
                
        except Exception as e:
            self.logger.error(f"Erro ao gerar dados para relatório HTML: {str(e)}")
            context['error'] = f"Erro ao gerar relatório: {str(e)}"
        
        return context


class RelatorioGerarModernoView(FormView):
    """View que aponta para a interface clássica (backup)"""
    template_name = 'relatorios/gerar_relatorio_classico.html'
    form_class = RelatorioFiltroForm

    def get_initial(self):
        """Pré-configura as datas para os últimos 7 dias"""
        initial = super().get_initial()
        tipo = self.request.GET.get('tipo', 'completo')
        data_final = timezone.localdate()
        data_inicial = data_final - timedelta(days=7)
        
        initial.update({
            'data_inicial': data_inicial,
            'data_final': data_final,
            'tipo_relatorio': tipo
        })
        return initial
    
    def form_valid(self, form):
        """Processa o formulário válido e gera o relatório"""
        # Obter dados do formulário
        tipo_relatorio = form.cleaned_data['tipo_relatorio']
        data_inicial = form.cleaned_data['data_inicial']
        data_final = form.cleaned_data['data_final']
        tipo_amostra_umidade = form.cleaned_data.get('tipo_amostra_umidade', '')
        tipo_amostra_proteina = form.cleaned_data.get('tipo_amostra_proteina', '')
        formato_saida = form.cleaned_data.get('formato_saida', 'HTML')
        
        # Construir a URL de redirecionamento com query parameters
        query_params = {
            'tipo': tipo_relatorio,
            'inicio': data_inicial.strftime('%Y-%m-%d'),
            'fim': data_final.strftime('%Y-%m-%d'),
            'formato': formato_saida,
        }
        
        if tipo_amostra_umidade:
            query_params['umidade_tipo'] = tipo_amostra_umidade
        
        if tipo_amostra_proteina:
            query_params['proteina_tipo'] = tipo_amostra_proteina
        
        # Construir a URL com os parâmetros
        url = reverse('relatorios:visualizar')
        url = f"{url}?{urlencode(query_params)}"
        
        # Logs para depuração
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Redirecionando para URL: {url}")
        
        # Redirecionar para a visualização do relatório
        return redirect(url)
