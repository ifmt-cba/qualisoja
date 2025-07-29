"""
Módulo para envio de emails com relatórios.
Contém funcionalidades para enviar relatórios por email com anexos.
"""

import os
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from io import BytesIO
import mimetypes

logger = logging.getLogger(__name__)

class EmailRelatorioService:
    """Serviço para envio de relatórios por email."""
    
    def __init__(self):
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.from_name = getattr(settings, 'RELATORIOS_EMAIL_SETTINGS', {}).get('FROM_NAME', 'QualiSoja')
        self.reply_to = getattr(settings, 'RELATORIOS_EMAIL_SETTINGS', {}).get('REPLY_TO', self.from_email)
        self.max_attachment_size = getattr(settings, 'RELATORIOS_EMAIL_SETTINGS', {}).get('MAX_ATTACHMENTS_SIZE', 25 * 1024 * 1024)
    
    def enviar_relatorio(self, relatorio, destinatarios, assunto=None, mensagem_personalizada=None, incluir_anexos=True):
        """
        Envia um relatório por email.
        
        Args:
            relatorio: Instância do RelatorioExpedicao
            destinatarios: Lista de emails dos destinatários
            assunto: Assunto personalizado (opcional)
            mensagem_personalizada: Mensagem adicional (opcional)
            incluir_anexos: Se deve incluir os arquivos do relatório
        
        Returns:
            dict: Resultado do envio com sucesso/erro
        """
        try:
            # Validar destinatários
            if not destinatarios or not isinstance(destinatarios, list):
                return {
                    'sucesso': False,
                    'erro': 'Lista de destinatários inválida ou vazia'
                }
            
            # Gerar assunto padrão se não fornecido
            if not assunto:
                assunto = f"Relatório de Expedição {relatorio.codigo} - {relatorio.get_cliente_nome()}"
            
            # Preparar contexto para o template de email
            contexto = {
                'relatorio': relatorio,
                'cliente_nome': relatorio.get_cliente_nome(),
                'contrato_info': relatorio.get_contrato_info(),
                'data_envio': timezone.now(),
                'mensagem_personalizada': mensagem_personalizada,
                'logo_url': getattr(settings, 'RELATORIOS_EMAIL_SETTINGS', {}).get('TEMPLATE_LOGO_URL', ''),
                'sistema_nome': 'QualiSoja'
            }
            
            # Renderizar templates HTML e texto
            html_content = render_to_string('relatorios/email/relatorio_envio.html', contexto)
            text_content = render_to_string('relatorios/email/relatorio_envio.txt', contexto)
            
            # Criar email
            email = EmailMultiAlternatives(
                subject=assunto,
                body=text_content,
                from_email=f"{self.from_name} <{self.from_email}>",
                to=destinatarios,
                reply_to=[self.reply_to]
            )
            
            # Adicionar versão HTML
            email.attach_alternative(html_content, "text/html")
            
            # Adicionar anexos se solicitado
            if incluir_anexos:
                anexos_resultado = self._adicionar_anexos(email, relatorio)
                if not anexos_resultado['sucesso']:
                    logger.warning(f"Problemas com anexos: {anexos_resultado['erro']}")
            
            # Enviar email
            email.send()
            
            logger.info(f"Email do relatório {relatorio.codigo} enviado com sucesso para {len(destinatarios)} destinatários")
            
            return {
                'sucesso': True,
                'mensagem': f'Relatório enviado com sucesso para {len(destinatarios)} destinatário(s)'
            }
            
        except Exception as e:
            logger.error(f"Erro ao enviar email do relatório {relatorio.codigo}: {str(e)}")
            return {
                'sucesso': False,
                'erro': f'Erro ao enviar email: {str(e)}'
            }
    
    def _adicionar_anexos(self, email, relatorio):
        """Adiciona anexos do relatório ao email."""
        try:
            anexos_adicionados = []
            
            # Verificar se há arquivo gerado
            if relatorio.arquivo_gerado and os.path.exists(relatorio.arquivo_gerado.path):
                file_path = relatorio.arquivo_gerado.path
                file_name = os.path.basename(file_path)
                
                # Verificar tamanho do arquivo
                file_size = os.path.getsize(file_path)
                if file_size > self.max_attachment_size:
                    return {
                        'sucesso': False,
                        'erro': f'Arquivo muito grande ({file_size / (1024*1024):.1f}MB). Máximo permitido: {self.max_attachment_size / (1024*1024):.1f}MB'
                    }
                
                # Determinar tipo MIME
                content_type, encoding = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                # Ler arquivo e anexar
                with open(file_path, 'rb') as f:
                    email.attach(file_name, f.read(), content_type)
                
                anexos_adicionados.append(file_name)
                logger.info(f"Anexo adicionado: {file_name} ({file_size / 1024:.1f}KB)")
            
            # Gerar PDFs/Excel em memória se não há arquivo salvo
            else:
                # Gerar PDF em memória
                pdf_content = self._gerar_pdf_relatorio(relatorio)
                if pdf_content:
                    email.attach(
                        f"relatorio_{relatorio.codigo}.pdf",
                        pdf_content,
                        'application/pdf'
                    )
                    anexos_adicionados.append(f"relatorio_{relatorio.codigo}.pdf")
                
                # Gerar Excel em memória se requisitado
                if relatorio.formato in ['EXCEL', 'ambos']:
                    excel_content = self._gerar_excel_relatorio(relatorio)
                    if excel_content:
                        email.attach(
                            f"relatorio_{relatorio.codigo}.xlsx",
                            excel_content,
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                        anexos_adicionados.append(f"relatorio_{relatorio.codigo}.xlsx")
            
            return {
                'sucesso': True,
                'anexos': anexos_adicionados
            }
            
        except Exception as e:
            logger.error(f"Erro ao adicionar anexos: {str(e)}")
            return {
                'sucesso': False,
                'erro': f'Erro ao processar anexos: {str(e)}'
            }
    
    def _gerar_pdf_relatorio(self, relatorio):
        """Gera PDF do relatório em memória."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph(f"Relatório de Expedição - {relatorio.codigo}", title_style))
            
            # Informações do cliente
            cliente_info = [
                ['Cliente:', relatorio.get_cliente_nome()],
                ['Contrato:', relatorio.get_contrato_info()['nome']],
                ['Período:', f"{relatorio.data_inicial.strftime('%d/%m/%Y')} a {relatorio.data_final.strftime('%d/%m/%Y')}"],
                ['Data de Geração:', relatorio.data_geracao.strftime('%d/%m/%Y %H:%M')],
                ['Status:', relatorio.get_status_display()],
            ]
            
            cliente_table = Table(cliente_info, colWidths=[2*inch, 4*inch])
            cliente_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(cliente_table)
            story.append(Spacer(1, 20))
            
            # Análises (se disponíveis)
            analises = relatorio.get_analises_relacionadas()
            if analises.exists():
                story.append(Paragraph("Análises Realizadas", styles['Heading2']))
                
                analises_data = [['Data', 'Tipo', 'Resultado', 'Conformidade']]
                for analise in analises:
                    conformidade = "Conforme" if analise.conforme else "Não Conforme" if analise.conforme is False else "N/A"
                    resultado = f"{analise.resultado}%" if analise.resultado else "N/A"
                    analises_data.append([
                        analise.data_analise.strftime('%d/%m/%Y'),
                        analise.tipo_analise.title(),
                        resultado,
                        conformidade
                    ])
                
                analises_table = Table(analises_data)
                analises_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(analises_table)
            
            # Observações
            if relatorio.observacoes_automaticas or relatorio.observacoes_manuais:
                story.append(Spacer(1, 20))
                story.append(Paragraph("Observações", styles['Heading2']))
                
                if relatorio.observacoes_automaticas:
                    story.append(Paragraph(f"Automáticas: {relatorio.observacoes_automaticas}", styles['Normal']))
                
                if relatorio.observacoes_manuais:
                    story.append(Paragraph(f"Manuais: {relatorio.observacoes_manuais}", styles['Normal']))
            
            # Gerar PDF
            doc.build(story)
            pdf_content = buffer.getvalue()
            buffer.close()
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {str(e)}")
            return None
    
    def _gerar_excel_relatorio(self, relatorio):
        """Gera arquivo Excel do relatório em memória."""
        try:
            import xlsxwriter
            
            buffer = BytesIO()
            workbook = xlsxwriter.Workbook(buffer)
            worksheet = workbook.add_worksheet('Relatório')
            
            # Formatos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D7E4BD',
                'border': 1
            })
            
            data_format = workbook.add_format({
                'border': 1
            })
            
            # Cabeçalho
            row = 0
            worksheet.write(row, 0, 'Relatório de Expedição', header_format)
            worksheet.write(row, 1, relatorio.codigo, data_format)
            
            row += 1
            worksheet.write(row, 0, 'Cliente', header_format)
            worksheet.write(row, 1, relatorio.get_cliente_nome(), data_format)
            
            row += 1
            worksheet.write(row, 0, 'Período', header_format)
            worksheet.write(row, 1, f"{relatorio.data_inicial.strftime('%d/%m/%Y')} a {relatorio.data_final.strftime('%d/%m/%Y')}", data_format)
            
            row += 2
            
            # Análises
            analises = relatorio.get_analises_relacionadas()
            if analises.exists():
                # Cabeçalhos das análises
                headers = ['Data', 'Tipo de Análise', 'Resultado', 'Unidade', 'Conformidade']
                for col, header in enumerate(headers):
                    worksheet.write(row, col, header, header_format)
                
                row += 1
                
                # Dados das análises
                for analise in analises:
                    worksheet.write(row, 0, analise.data_analise.strftime('%d/%m/%Y'), data_format)
                    worksheet.write(row, 1, analise.tipo_analise.title(), data_format)
                    worksheet.write(row, 2, analise.resultado if analise.resultado else 'N/A', data_format)
                    worksheet.write(row, 3, analise.unidade or '%', data_format)
                    conformidade = "Conforme" if analise.conforme else "Não Conforme" if analise.conforme is False else "N/A"
                    worksheet.write(row, 4, conformidade, data_format)
                    row += 1
            
            # Ajustar largura das colunas
            worksheet.set_column('A:E', 15)
            
            workbook.close()
            excel_content = buffer.getvalue()
            buffer.close()
            
            return excel_content
            
        except Exception as e:
            logger.error(f"Erro ao gerar Excel: {str(e)}")
            return None
    
    def testar_configuracao(self):
        """Testa a configuração de email."""
        try:
            from django.core.mail import get_connection
            
            connection = get_connection()
            connection.open()
            connection.close()
            
            return {
                'sucesso': True,
                'mensagem': 'Configuração de email OK'
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
