from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import AnaliseUmidade, AnaliseProteina
from .forms import AnaliseUmidadeForm, AnaliseProteinaForm
from django.views.generic import TemplateView, View, FormView
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Avg, Max, Min, Count
from datetime import timedelta
import io
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from .forms import RelatorioFiltroForm
class UmidadeCreateView(CreateView):
    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = 'app/cadastro_umidade.html'
    success_url = reverse_lazy('umidade_list')

class ProteinaCreateView(CreateView):
    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = 'app/cadastro_proteina.html'
    success_url = reverse_lazy('proteina_list')

class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = 'app/lista_umidade.html'

class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = 'app/lista_proteina.html'

class RelatorioDashboardView(TemplateView):
    """Dashboard principal de relatórios"""
    template_name = 'app/relatorios_dashboard.html'


class RelatorioGerarView(FormView):
    """View para selecionar parâmetros e gerar relatórios"""
    template_name = 'app/gerar_relatorio.html'
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
        
        # Obter dados para o relatório
        dados = self.obter_dados_relatorio(
            tipo_relatorio, 
            data_inicial, 
            data_final, 
            tipo_amostra_umidade, 
            tipo_amostra_proteina
        )
        
        # Gerar relatório no formato desejado
        if formato_saida == 'PDF':
            return self.gerar_pdf_relatorio(dados, tipo_relatorio, data_inicial, data_final)
        elif formato_saida == 'EXCEL':
            return self.gerar_excel_relatorio(dados, tipo_relatorio, data_inicial, data_final)
        else:  # HTML
            contexto = {
                'dados': dados,
                'tipo_relatorio': tipo_relatorio,
                'data_inicial': data_inicial,
                'data_final': data_final,
                'filtros': form.cleaned_data,
                'form': form
            }
            return render(self.request, 'app/visualizar_relatorio.html', contexto)
    
    def obter_dados_relatorio(self, tipo_relatorio, data_inicial, data_final, tipo_amostra_umidade='', tipo_amostra_proteina=''):
        """Obtém dados para o relatório com base nos parâmetros"""
        dados = {}
        
        if tipo_relatorio in ['umidade', 'completo']:
            queryset = AnaliseUmidade.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_umidade:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_umidade)
            
            dados['umidade'] = queryset.order_by('data', 'horario')
            
            # Cálculo de estatísticas
            if queryset.exists():
                dados['estatisticas_umidade'] = {
                    'media': queryset.aggregate(media=Avg('resultado'))['media'],
                    'minimo': queryset.aggregate(min=Min('resultado'))['min'],
                    'maximo': queryset.aggregate(max=Max('resultado'))['max'],
                    'total': queryset.count(),
                }
        
        if tipo_relatorio in ['proteina', 'completo']:
            queryset = AnaliseProteina.objects.filter(
                data__gte=data_inicial,
                data__lte=data_final
            )
            
            if tipo_amostra_proteina:
                queryset = queryset.filter(tipo_amostra=tipo_amostra_proteina)
            
            dados['proteina'] = queryset.order_by('data', 'horario')
            
            # Cálculo de estatísticas
            if queryset.exists():
                dados['estatisticas_proteina'] = {
                    'media': queryset.aggregate(media=Avg('resultado'))['media'],
                    'minimo': queryset.aggregate(min=Min('resultado'))['min'],
                    'maximo': queryset.aggregate(max=Max('resultado'))['max'],
                    'total': queryset.count(),
                }
        
        return dados
    
    def gerar_pdf_relatorio(self, dados, tipo_relatorio, data_inicial, data_final):
        """Gera um relatório em formato PDF"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{tipo_relatorio}_{data_inicial}_a_{data_final}.pdf"'
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Título do relatório
        styles = getSampleStyleSheet()
        if tipo_relatorio == 'umidade':
            titulo = "Relatório de Umidade"
        elif tipo_relatorio == 'proteina':
            titulo = "Relatório de Proteína"
        else:
            titulo = "Relatório Completo"
            
        elements.append(Paragraph(f"{titulo} - {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}", styles['Title']))
        
        # Criação das tabelas com os dados
        if 'umidade' in dados and dados['umidade'].exists():
            elements.append(Paragraph("Dados de Umidade:", styles['Heading2']))
            
            # Cabeçalho da tabela
            data = [["Data", "Hora", "Tipo de Amostra", "Peso da Amostra", "Resultado (%)"]]
            
            # Dados
            for item in dados['umidade']:
                data.append([
                    item.data.strftime('%d/%m/%Y'),
                    item.horario.strftime('%H:%M'),
                    item.get_tipo_amostra_display(),
                    f"{item.peso_amostra:.2f}",
                    f"{item.resultado:.2f}" if item.resultado else "-"
                ])
            
            # Adicionar tabela ao documento
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            
            # Adicionar estatísticas
            if 'estatisticas_umidade' in dados:
                elements.append(Paragraph("Estatísticas de Umidade:", styles['Heading3']))
                estat_data = [
                    ["Média", "Mínimo", "Máximo", "Total de Amostras"],
                    [
                        f"{dados['estatisticas_umidade']['media']:.2f}%",
                        f"{dados['estatisticas_umidade']['minimo']:.2f}%",
                        f"{dados['estatisticas_umidade']['maximo']:.2f}%",
                        f"{dados['estatisticas_umidade']['total']}"
                    ]
                ]
                
                estat_table = Table(estat_data)
                estat_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(estat_table)
        
        if 'proteina' in dados and dados['proteina'].exists():
            elements.append(Paragraph("Dados de Proteína:", styles['Heading2']))
            
            # Cabeçalho da tabela
            data = [["Data", "Hora", "Tipo de Amostra", "Peso da Amostra", "ML Gastos", "Resultado (%)", "Resultado Corrigido (%)"]]
            
            # Dados
            for item in dados['proteina']:
                data.append([
                    item.data.strftime('%d/%m/%Y'),
                    item.horario.strftime('%H:%M'),
                    item.get_tipo_amostra_display(),
                    f"{item.peso_amostra:.2f}",
                    f"{item.ml_gasto:.2f}" if item.ml_gasto else "-",
                    f"{item.resultado:.2f}" if item.resultado else "-",
                    f"{item.resultado_corrigido:.2f}" if item.resultado_corrigido else "-"
                ])
            
            # Adicionar tabela ao documento
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            
            # Adicionar estatísticas
            if 'estatisticas_proteina' in dados:
                elements.append(Paragraph("Estatísticas de Proteína:", styles['Heading3']))
                estat_data = [
                    ["Média", "Mínimo", "Máximo", "Total de Amostras"],
                    [
                        f"{dados['estatisticas_proteina']['media']:.2f}%",
                        f"{dados['estatisticas_proteina']['minimo']:.2f}%",
                        f"{dados['estatisticas_proteina']['maximo']:.2f}%",
                        f"{dados['estatisticas_proteina']['total']}"
                    ]
                ]
                
                estat_table = Table(estat_data)
                estat_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(estat_table)
        
        # Construir o PDF e retorná-lo
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    def gerar_excel_relatorio(self, dados, tipo_relatorio, data_inicial, data_final):
        """Gera um relatório em formato Excel"""
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{tipo_relatorio}_{data_inicial}_a_{data_final}.xlsx"'
        
        workbook = xlsxwriter.Workbook(response)
        
        # Formato para cabeçalhos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        # Formato para células de dados
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        if 'umidade' in dados and dados['umidade'].exists():
            # Criar planilha para umidade
            ws_umidade = workbook.add_worksheet('Umidade')
            
            # Cabeçalhos
            headers = ['Data', 'Horário', 'Tipo de Amostra', 'Peso (g)', 'Resultado (%)', 'Fator Correção']
            for col, header in enumerate(headers):
                ws_umidade.write(0, col, header, header_format)
            
            # Dados
            for row, item in enumerate(dados['umidade'], start=1):
                ws_umidade.write(row, 0, item.data.strftime('%d/%m/%Y'), cell_format)
                ws_umidade.write(row, 1, item.horario.strftime('%H:%M'), cell_format)
                ws_umidade.write(row, 2, item.get_tipo_amostra_display(), cell_format)
                ws_umidade.write(row, 3, float(item.peso_amostra), cell_format)
                ws_umidade.write(row, 4, float(item.resultado) if item.resultado else 0, cell_format)
                ws_umidade.write(row, 5, float(item.fator_correcao) if item.fator_correcao else 0, cell_format)
                
            # Adicionar estatísticas
            if 'estatisticas_umidade' in dados:
                ws_umidade.write(len(dados['umidade']) + 2, 0, "Estatísticas", header_format)
                
                estat_row = len(dados['umidade']) + 3
                ws_umidade.write(estat_row, 0, "Média", cell_format)
                ws_umidade.write(estat_row, 1, float(dados['estatisticas_umidade']['media']), cell_format)
                
                ws_umidade.write(estat_row + 1, 0, "Mínimo", cell_format)
                ws_umidade.write(estat_row + 1, 1, float(dados['estatisticas_umidade']['minimo']), cell_format)
                
                ws_umidade.write(estat_row + 2, 0, "Máximo", cell_format)
                ws_umidade.write(estat_row + 2, 1, float(dados['estatisticas_umidade']['maximo']), cell_format)
                
                ws_umidade.write(estat_row + 3, 0, "Total de Amostras", cell_format)
                ws_umidade.write(estat_row + 3, 1, int(dados['estatisticas_umidade']['total']), cell_format)
        
        if 'proteina' in dados and dados['proteina'].exists():
            # Criar planilha para proteína
            ws_proteina = workbook.add_worksheet('Proteína')
            
            # Cabeçalhos
            headers = ['Data', 'Horário', 'Tipo de Amostra', 'Peso (g)', 'ML Gastos', 'Resultado (%)', 'Resultado Corrigido (%)']
            for col, header in enumerate(headers):
                ws_proteina.write(0, col, header, header_format)
            
            # Dados
            for row, item in enumerate(dados['proteina'], start=1):
                ws_proteina.write(row, 0, item.data.strftime('%d/%m/%Y'), cell_format)
                ws_proteina.write(row, 1, item.horario.strftime('%H:%M'), cell_format)
                ws_proteina.write(row, 2, item.get_tipo_amostra_display(), cell_format)
                ws_proteina.write(row, 3, float(item.peso_amostra), cell_format)
                ws_proteina.write(row, 4, float(item.ml_gasto) if item.ml_gasto else 0, cell_format)
                ws_proteina.write(row, 5, float(item.resultado) if item.resultado else 0, cell_format)
                ws_proteina.write(row, 6, float(item.resultado_corrigido) if item.resultado_corrigido else 0, cell_format)
                
            # Adicionar estatísticas
            if 'estatisticas_proteina' in dados:
                ws_proteina.write(len(dados['proteina']) + 2, 0, "Estatísticas", header_format)
                
                estat_row = len(dados['proteina']) + 3
                ws_proteina.write(estat_row, 0, "Média", cell_format)
                ws_proteina.write(estat_row, 1, float(dados['estatisticas_proteina']['media']), cell_format)
                
                ws_proteina.write(estat_row + 1, 0, "Mínimo", cell_format)
                ws_proteina.write(estat_row + 1, 1, float(dados['estatisticas_proteina']['minimo']), cell_format)
                
                ws_proteina.write(estat_row + 2, 0, "Máximo", cell_format)
                ws_proteina.write(estat_row + 2, 1, float(dados['estatisticas_proteina']['maximo']), cell_format)
                
                ws_proteina.write(estat_row + 3, 0, "Total de Amostras", cell_format)
                ws_proteina.write(estat_row + 3, 1, int(dados['estatisticas_proteina']['total']), cell_format)
        
        workbook.close()
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginaAtiva'] = 'relatorios'  # Se estiver usando isso no template
        return context