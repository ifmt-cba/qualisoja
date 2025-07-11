from django.contrib import admin
from .models import (
    AnaliseUmidade, 
    AnaliseProteina, 
    AnaliseOleoDegomado, 
    AnaliseUrase, 
    AnaliseCinza, 
    AnaliseTeorOleo, 
    AnaliseFibra, 
    AnaliseFosforo,
    AnaliseSilica
)


@admin.register(AnaliseUmidade)
class AnaliseUmidadeAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "peso_amostra", "resultado"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]


@admin.register(AnaliseProteina)
class AnaliseProteinaAdmin(admin.ModelAdmin):
    list_display = [
        "data",
        "horario",
        "tipo_amostra",
        "peso_amostra",
        "ml_gasto",
        "resultado",
        "resultado_corrigido",
        "eh_media_24h",
    ]
    list_filter = ["tipo_amostra", "eh_media_24h", "data"]
    search_fields = ["tipo_amostra", "data"]


@admin.register(AnaliseOleoDegomado)
class AnaliseOleoDegomadoAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "tipo_analise", "peso_amostra", "resultado"]
    list_filter = ["tipo_amostra", "tipo_analise", "data"]
    search_fields = ["tipo_amostra", "tipo_analise"]
    readonly_fields = ["resultado"]


@admin.register(AnaliseUrase)
class AnaliseUraseAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "amostra_1", "amostra_2", "resultado"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]
    readonly_fields = ["resultado"]


@admin.register(AnaliseCinza)
class AnaliseCinzaAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "peso_amostra", "peso_cadinho", "peso_cinza", "resultado"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]
    readonly_fields = ["resultado"]


@admin.register(AnaliseTeorOleo)
class AnaliseTeorOleoAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "peso_amostra", "peso_tara", "peso_liquido", "teor_oleo"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]
    readonly_fields = ["teor_oleo"]


@admin.register(AnaliseFibra)
class AnaliseFibraAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "peso_amostra", "peso_tara", "peso_fibra", "resultado"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]
    readonly_fields = ["resultado"]


@admin.register(AnaliseFosforo)
class AnaliseFosforoAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "absorbancia_amostra", "peso_amostra", "resultado", "casas_decimais"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]
    readonly_fields = ["resultado"]


@admin.register(AnaliseSilica)
class AnaliseSilicaAdmin(admin.ModelAdmin):
    list_display = ["data", "horario", "tipo_amostra", "resultado_silica", "resultado_final", "analise_cinza"]
    list_filter = ["tipo_amostra", "data"]
    search_fields = ["tipo_amostra"]
    readonly_fields = ["resultado_final"]
    autocomplete_fields = ["analise_cinza"]
