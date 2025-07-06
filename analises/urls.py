from django.urls import path
from .views import (
    AnaliseHomeView,
    UmidadeCreateView, ProteinaCreateView, OleoDegomadoCreateView,UraseCreateView,
    UraseListView,UmidadeListView, ProteinaListView, OleoDegomadoListView
)

app_name = 'analises'

urlpatterns = [
    path('home/', AnaliseHomeView.as_view(), name='home'),
    path('umidade/nova/', UmidadeCreateView.as_view(), name='umidade_create'),
    path('proteina/nova/', ProteinaCreateView.as_view(), name='proteina_create'),
    path('oleo/nova/', OleoDegomadoCreateView.as_view(), name='oleo_create'),
    path('umidade/', UmidadeListView.as_view(), name='umidade_list'),
    path('proteina/', ProteinaListView.as_view(), name='proteina_list'),
    path('oleo/', OleoDegomadoListView.as_view(), name='oleo_list'),
    path('urase/cadastro/', UraseCreateView.as_view(), name='urase_create'),
    path('urase/', UraseListView.as_view(), name='urase_list'),
]