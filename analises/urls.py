from django.urls import path
from .views import (
    AnaliseHomeView,
    UmidadeCreateView, ProteinaCreateView, OleoDegomadoCreateView, UraseCreateView,
    CinzaCreateView, FibraCreateView, TeorOleoCreateView, FosforoCreateView,
    UraseListView, UmidadeListView, ProteinaListView, OleoDegomadoListView,
    CinzaListView, FibraListView, TeorOleoListView, FosforoListView
)

app_name = 'analises'

urlpatterns = [
    path('home/', AnaliseHomeView.as_view(), name='home'),
    path('umidade/nova/', UmidadeCreateView.as_view(), name='umidade_create'),
    path('proteina/nova/', ProteinaCreateView.as_view(), name='proteina_create'),
    path('oleo/nova/', OleoDegomadoCreateView.as_view(), name='oleo_create'),
    path('urase/cadastro/', UraseCreateView.as_view(), name='urase_create'),
    path('cinza/nova/', CinzaCreateView.as_view(), name='cinza_create'),
    path('fibra/nova/', FibraCreateView.as_view(), name='fibra_create'),
    path('teor-oleo/nova/', TeorOleoCreateView.as_view(), name='teor_oleo_create'),
    path('fosforo/nova/', FosforoCreateView.as_view(), name='fosforo_create'),
    path('umidade/', UmidadeListView.as_view(), name='umidade_list'),
    path('proteina/', ProteinaListView.as_view(), name='proteina_list'),
    path('oleo/', OleoDegomadoListView.as_view(), name='oleo_list'),
    path('urase/', UraseListView.as_view(), name='urase_list'),
    path('cinza/', CinzaListView.as_view(), name='cinza_list'),
    path('fibra/', FibraListView.as_view(), name='fibra_list'),
    path('teor-oleo/', TeorOleoListView.as_view(), name='teor_oleo_list'),
    path('fosforo/', FosforoListView.as_view(), name='fosforo_list'),
]