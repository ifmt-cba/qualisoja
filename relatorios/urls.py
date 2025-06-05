from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'relatorios'

def dashboard_redirect(request):
    """Redirect da URL antiga do dashboard para a nova interface de geração"""
    return redirect('relatorios:gerar')

urlpatterns = [
    # Redirect da URL antiga para manter compatibilidade
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('gerar/', views.RelatorioGerarView.as_view(), name='gerar'),
    path('gerar-classico/', views.RelatorioGerarModernoView.as_view(), name='gerar_classico'),
    path('visualizar/', views.RelatorioVisualizarView.as_view(), name='visualizar'),
]
