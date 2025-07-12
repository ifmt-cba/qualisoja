from django.contrib import admin
from .models import LogPersonalizado
from django.urls import reverse
from django.utils.html import format_html

@admin.register(LogPersonalizado)
class LogAdmin(admin.ModelAdmin):
    list_display = ('data', 'usuario', 'acao_link')
    list_filter = ('usuario', 'data')
    search_fields = ('acao',)
    readonly_fields = ('data', 'usuario', 'acao', 'content_type', 'object_id')

    def acao_link(self, obj):
        if obj.content_object:
            ct = obj.content_type
            url = reverse(f'admin:{ct.app_label}_{ct.model}_change', args=[obj.object_id])
            link = format_html('<a href="{}">{}</a>', url, ct.model_class()._meta.verbose_name.title())
            return format_html('{} ({})', obj.acao, link)
        return obj.acao
    acao_link.short_description = 'Ação'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('usuario', 'content_type')

    def user_logs(self, obj):
        logs = LogPersonalizado.objects.filter(usuario=obj.usuario).order_by('-data')
        items = []
        for l in logs:
            if l.content_object:
                ct = l.content_type
                url = reverse(f'admin:{ct.app_label}_{ct.model}_change', args=[l.object_id])
                link = format_html('<a href="{}">{}</a>', url, ct.model_class()._meta.verbose_name.title())
                acao = format_html('{} ({})', l.acao, link)
            else:
                acao = l.acao
            items.append(f"<li>{l.data.strftime('%d/%m/%Y %H:%M')} - {acao}</li>")
        return format_html('<ul>{}</ul>', format_html(''.join(items)))
    user_logs.short_description = 'Atividades do Usuário'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context['user_logs'] = self.user_logs(obj) if obj else ''
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
