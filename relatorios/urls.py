from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('dashboard/', views.RelatorioDashboardView.as_view(), name='dashboard'),
    path('gerar/', views.RelatorioGerarView.as_view(), name='gerar'),
    path('visualizar/', views.RelatorioVisualizarView.as_view(), name='visualizar'),
]
