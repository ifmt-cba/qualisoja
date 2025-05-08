from django.contrib import admin
from .models import AnaliseUmidade, AnaliseProteina

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
