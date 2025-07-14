from django.contrib import admin
from .models import (
    ConfiguracaoRelatorio, Cliente, EspecificacaoContrato, 
    Lote, RelatorioExpedicao, RelatorioAnalise, HistoricoEnvioRelatorio
)

@admin.register(ConfiguracaoRelatorio)
class ConfiguracaoRelatorioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_relatorio', 'periodo_padrao', 'ativo']
    list_filter = ['tipo_relatorio', 'ativo']
    search_fields = ['nome']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'email', 'telefone', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'codigo', 'email']
    ordering = ['nome']

@admin.register(EspecificacaoContrato)
class EspecificacaoContratoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'nome_contrato', 'codigo_contrato', 'data_inicio', 'data_fim', 'ativo']
    list_filter = ['ativo', 'data_inicio', 'data_fim']
    search_fields = ['cliente__nome', 'nome_contrato', 'codigo_contrato']
    raw_id_fields = ['cliente']
    date_hierarchy = 'data_inicio'

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'cliente', 'data_producao', 'quantidade_kg', 'status']
    list_filter = ['status', 'data_producao', 'cliente']
    search_fields = ['codigo', 'cliente__nome']
    raw_id_fields = ['cliente', 'contrato']
    date_hierarchy = 'data_producao'

@admin.register(RelatorioExpedicao)
class RelatorioExpedicaoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'cliente', 'tipo_analise', 'data_inicial', 'data_final', 'status', 'certificacao_conformidade', 'data_geracao']
    list_filter = ['status', 'tipo_analise', 'certificacao_conformidade', 'data_geracao', 'cliente']
    search_fields = ['codigo', 'cliente__nome']
    raw_id_fields = ['cliente', 'contrato', 'usuario_responsavel']
    readonly_fields = ['codigo', 'data_geracao', 'certificacao_conformidade']
    date_hierarchy = 'data_geracao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'cliente', 'contrato', 'usuario_responsavel')
        }),
        ('Período e Configuração', {
            'fields': ('tipo_analise', 'data_inicial', 'data_final', 'parametros_incluidos')
        }),
        ('Configurações', {
            'fields': ('formato', 'status', 'certificacao_conformidade')
        }),
        ('Observações', {
            'fields': ('observacoes_automaticas', 'observacoes_manuais')
        }),
        ('Arquivo', {
            'fields': ('arquivo_gerado',)
        })
    )

@admin.register(HistoricoEnvioRelatorio)
class HistoricoEnvioRelatorioAdmin(admin.ModelAdmin):
    list_display = ['relatorio', 'destinatario', 'data_envio', 'usuario_responsavel', 'versao_relatorio', 'sucesso_envio']
    list_filter = ['sucesso_envio', 'data_envio']
    search_fields = ['relatorio__codigo', 'destinatario', 'assunto']
    raw_id_fields = ['relatorio', 'usuario_responsavel']
    readonly_fields = ['data_envio']
    date_hierarchy = 'data_envio'

@admin.register(RelatorioAnalise)
class RelatorioAnaliseAdmin(admin.ModelAdmin):
    list_display = ['relatorio', 'tipo_analise', 'data_analise', 'resultado', 'unidade', 'conforme']
    list_filter = ['tipo_analise', 'conforme', 'data_analise', 'relatorio__status']
    search_fields = ['relatorio__codigo', 'tipo_analise']
    raw_id_fields = ['relatorio']
    readonly_fields = ['content_type', 'object_id']
    date_hierarchy = 'data_analise'
    
    fieldsets = (
        ('Vinculação', {
            'fields': ('relatorio', 'content_type', 'object_id')
        }),
        ('Dados da Análise', {
            'fields': ('tipo_analise', 'data_analise', 'resultado', 'unidade')
        }),
        ('Conformidade', {
            'fields': ('conforme', 'observacao_conformidade')
        })
    )
