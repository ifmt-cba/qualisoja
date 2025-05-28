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
from analises.models import AnaliseUmidade, AnaliseProteina
from .forms import RelatorioFiltroForm


class RelatorioDashboardView(TemplateView):
    """Dashboard principal de relatórios"""
    template_name = 'relatorios/relatorios_dashboard.html'


class RelatorioGerarView(FormView):
    """View para selecionar parâmetros e gerar relatórios"""
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


def obter_dados_relatorio(tipo_relatorio, data_inicial, data_final, tipo_amostra_umidade='', tipo_amostra_proteina=''):
    """
    Obtém dados para o relatório com base nos parâmetros
    
    Args:
        tipo_relatorio (str): Tipo de relatório ('umidade', 'proteina' ou 'completo')
        data_inicial (date): Data inicial para o relatório
        data_final (date): Data final para o relatório
        tipo_amostra_umidade (str, optional): Filtro de tipo de amostra para umidade
        tipo_amostra_proteina (str, optional): Filtro de tipo de amostra para proteína
        
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
    
    return dados


def gerar_pdf_relatorio(dados, tipo_relatorio, data_inicial, data_final):
    """Gera um relatório em formato PDF"""
    from io import BytesIO
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocDocument, Paragraph, Spacer, Table, TableStyle
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
        'completo': "Relatório Completo"
    }[tipo_relatorio]
    
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
                    f"{estat['media']:.2f}%",
                    f"{estat['minimo']:.2f}%",
                    f"{estat['maximo']:.2f}%",
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
                    f"{estat['media']:.2f}%",
                    f"{estat['minimo']:.2f}%",
                    f"{estat['maximo']:.2f}%",
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
            tuple: (tipo_relatorio, data_inicial, data_final, formato, tipo_amostra_umidade, tipo_amostra_proteina)
            ou None se ocorrer um erro.
        """
        try:
            from datetime import datetime
            
            tipo_relatorio = request.GET.get('tipo', 'completo')
            data_inicial_str = request.GET.get('inicio')
            data_final_str = request.GET.get('fim')
            formato = request.GET.get('formato', 'HTML')
            tipo_amostra_umidade = request.GET.get('umidade_tipo', '')
            tipo_amostra_proteina = request.GET.get('proteina_tipo', '')
            
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
                tipo_amostra_proteina
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
            
        tipo_relatorio, data_inicial, data_final, formato, tipo_amostra_umidade, tipo_amostra_proteina = params
            
        # Para formatos de arquivo, gera o arquivo diretamente
        if formato in ['PDF', 'EXCEL']:
            try:
                # Obter dados para o relatório
                dados = obter_dados_relatorio(
                    tipo_relatorio, 
                    data_inicial, 
                    data_final, 
                    tipo_amostra_umidade, 
                    tipo_amostra_proteina
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
            
        tipo_relatorio, data_inicial, data_final, formato, tipo_amostra_umidade, tipo_amostra_proteina = params
        
        try:
            # Obter dados para o relatório
            dados = obter_dados_relatorio(
                tipo_relatorio, 
                data_inicial, 
                data_final, 
                tipo_amostra_umidade, 
                tipo_amostra_proteina
            )
            
            # Adicionar todos os dados ao contexto
            context.update({
                'tipo_relatorio': tipo_relatorio,
                'data_inicial': data_inicial,
                'data_final': data_final,
                'formato': formato,
                'tipo_amostra_umidade': tipo_amostra_umidade,
                'tipo_amostra_proteina': tipo_amostra_proteina,
                'query_string': self.request.META.get('QUERY_STRING', ''),
                **dados
            })
                
        except Exception as e:
            self.logger.error(f"Erro ao gerar dados para relatório HTML: {str(e)}")
            context['error'] = f"Erro ao gerar relatório: {str(e)}"
        
        return context
