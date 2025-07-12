from django.contrib import admin
from .models import LogPersonalizado

@admin.register(LogPersonalizado)
class LogAdmin(admin.ModelAdmin):
    list_display = ('data', 'usuario', 'acao_html')
    list_filter = ('usuario', 'data')
    search_fields = ('acao',)
    readonly_fields = ('data', 'usuario', 'acao')

    def acao_html(self, obj):
        from django.utils.html import format_html
        return format_html(obj.acao)
    acao_html.short_description = 'Ação'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('usuario')

    def view_on_site(self, obj):
        # Não exibe link externo
        return None

    def user_logs(self, obj):
        # Mostra todos os logs do usuário na página de detalhe
        logs = LogPersonalizado.objects.filter(usuario=obj.usuario).order_by('-data')
        from django.utils.html import format_html, format_html_join
        return format_html('<ul>{}</ul>', format_html_join('', '<li>{} - {}</li>', ((l.data.strftime('%d/%m/%Y %H:%M'), l.acao) for l in logs)))
    user_logs.short_description = 'Atividades do Usuário'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context['user_logs'] = self.user_logs(obj) if obj else ''
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# Register your models here.
