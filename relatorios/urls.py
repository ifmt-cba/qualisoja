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
    
    # URLs para Relatórios de Expedição
    path('expedicao/', views.RelatorioExpedicaoListView.as_view(), name='expedicao_lista'),
    path('expedicao/criar/', views.RelatorioExpedicaoCreateView.as_view(), name='expedicao_criar'),
    path('expedicao/<int:pk>/', views.RelatorioExpedicaoDetailView.as_view(), name='expedicao_detalhe'),
    path('expedicao/<int:pk>/pdf/', views.RelatorioExpedicaoPDFView.as_view(), name='expedicao_pdf'),
    path('expedicao/<int:pk>/formato/', views.RelatorioExpedicaoFormatoView.as_view(), name='expedicao_formato'),
    path('expedicao/<int:pk>/visualizar/', views.RelatorioExpedicaoDetailView.as_view(), name='expedicao_visualizar'),
    path('expedicao/<int:pk>/enviar/', views.RelatorioExpedicaoEnviarView.as_view(), name='expedicao_enviar'),
    path('expedicao/<int:pk>/download/', views.RelatorioExpedicaoDownloadView.as_view(), name='expedicao_download'),
    path('expedicao/<int:pk>/excel/', views.RelatorioExpedicaoExcelView.as_view(), name='expedicao_excel'),
    
    # API endpoints
    path('api/cliente/<int:cliente_id>/dados/', views.ClienteDadosAPIView.as_view(), name='api_cliente_dados'),
]
