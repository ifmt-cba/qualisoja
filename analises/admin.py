from django.contrib import admin
from .models import (
    AnaliseUmidade, 
    AnaliseProteina, 
    AnaliseOleoDegomado, 
    AnaliseUrase, 
    AnaliseCinza, 
    AnaliseTeorOleo, 
    AnaliseFibra, 
    AnaliseFosforo
)

@admin.register(AnaliseUmidade)
class AnaliseUmidadeAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'peso_amostra', 'resultado']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']

@admin.register(AnaliseProteina)
class AnaliseProteinaAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'resultado', 'resultado_corrigido']
    list_filter = ['tipo_amostra', 'eh_media_24h']
    search_fields = ['tipo_amostra']

@admin.register(AnaliseOleoDegomado)
class AnaliseOleoDegomadoAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'peso_amostra', 'resultado']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']

@admin.register(AnaliseUrase)
class AnaliseUraseAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'amostra_1', 'amostra_2', 'resultado']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']
    readonly_fields = ['resultado']

@admin.register(AnaliseCinza)
class AnaliseCinzaAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'peso_amostra', 'peso_cadinho', 'peso_cinza', 'resultado']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']
    ordering = ['-data', '-horario']
    readonly_fields = ['resultado']

@admin.register(AnaliseTeorOleo)
class AnaliseTeorOleoAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'peso_amostra', 'peso_tara', 'peso_liquido', 'teor_oleo']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']
    ordering = ['-data', '-horario']
    readonly_fields = ['teor_oleo']

@admin.register(AnaliseFibra)
class AnaliseFibraAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'peso_amostra', 'peso_tara', 'peso_fibra', 'peso_branco', 'resultado']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']
    ordering = ['-data', '-horario']
    readonly_fields = ['resultado']

@admin.register(AnaliseFosforo)
class AnaliseFosforoAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'tipo_amostra', 'peso_amostra', 'absorbancia_amostra', 
                   'concentracao_padrao', 'volume_solucao', 'volume_aliquota', 
                   'absorbancia_padrao', 'resultado']
    list_filter = ['tipo_amostra', 'data']
    search_fields = ['tipo_amostra']
    ordering = ['-data', '-horario']
    readonly_fields = ['resultado']
    
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('data', 'horario', 'tipo_amostra')
        }),
        ('Dados da Amostra', {
            'fields': ('peso_amostra', 'absorbancia_amostra')
        }),
        ('Dados do Padrão', {
            'fields': ('concentracao_padrao', 'absorbancia_padrao')
        }),
        ('Volumes', {
            'fields': ('volume_solucao', 'volume_aliquota')
        }),
        ('Resultado', {
            'fields': ('resultado', 'casas_decimais'),
            'description': 'Resultado calculado automaticamente usando: (Aa × Cp × V × 1000 × 1000) / (P × VAl × Ap)'
        }),
    )
