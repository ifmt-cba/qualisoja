from django.urls import path
from .views import (
    UmidadeCreateView, ProteinaCreateView, UmidadeListView, ProteinaListView,
    RelatorioDashboardView, RelatorioGerarView
)

urlpatterns = [
    path('umidade/nova/', UmidadeCreateView.as_view(), name='umidade_create'),
    path('proteina/nova/', ProteinaCreateView.as_view(), name='proteina_create'),
    path('umidade/', UmidadeListView.as_view(), name='umidade_list'),
    path('proteina/', ProteinaListView.as_view(), name='proteina_list'),
    
    # Renomeado para 'listar_relatorios' para corresponder ao template
    path('relatorios/', RelatorioDashboardView.as_view(), name='listar_relatorios'),
    path('relatorios/gerar/', RelatorioGerarView.as_view(), name='gerar_relatorio'),
    
]