from django.urls import path
from .views import (
    AnaliseHomeView,
    UmidadeCreateView, ProteinaCreateView, OleoDegomadoCreateView, UraseCreateView,
    CinzaCreateView, TeorOleoCreateView, FibraCreateView, FosforoCreateView, SilicaCreateView,
    UraseListView, UmidadeListView, ProteinaListView, OleoDegomadoListView,
    CinzaListView, TeorOleoListView, FibraListView, FosforoListView, SilicaListView,
    TeorOleoDetailView, TeorOleoUpdateView, TeorOleoDeleteView,
    ProteinaDetailView, ProteinaUpdateView, ProteinaDeleteView,
    UmidadeDetailView, UmidadeUpdateView, UmidadeDeleteView,
    OleoDegomadoDetailView, OleoDegomadoUpdateView, OleoDegomadoDeleteView,
    UraseDetailView, UraseUpdateView, UraseDeleteView,
    CinzaDetailView, CinzaUpdateView, CinzaDeleteView,
    FibraDetailView, FibraUpdateView, FibraDeleteView,
    FosforoDetailView, FosforoUpdateView, FosforoDeleteView,
    SilicaDetailView, SilicaUpdateView, SilicaDeleteView
)

app_name = 'analises'

urlpatterns = [
    path('home/', AnaliseHomeView.as_view(), name='home'),
    path('umidade/nova/', UmidadeCreateView.as_view(), name='umidade_create'),
    path('proteina/nova/', ProteinaCreateView.as_view(), name='proteina_create'),
    path('oleo/nova/', OleoDegomadoCreateView.as_view(), name='oleo_create'),
    path('urase/cadastro/', UraseCreateView.as_view(), name='urase_create'),
    path('cinza/nova/', CinzaCreateView.as_view(), name='cinza_create'),
    path('silica/nova/', SilicaCreateView.as_view(), name='silica_create'),
    path('fibra/nova/', FibraCreateView.as_view(), name='fibra_create'),
    path('teor-oleo/nova/', TeorOleoCreateView.as_view(), name='teor_oleo_create'),
    path('fosforo/nova/', FosforoCreateView.as_view(), name='cadastro_fosforo'),
    path('umidade/', UmidadeListView.as_view(), name='umidade_list'),
    path('proteina/', ProteinaListView.as_view(), name='proteina_list'),
    path('oleo/', OleoDegomadoListView.as_view(), name='oleo_list'),
    path('urase/', UraseListView.as_view(), name='urase_list'),
    path('cinza/', CinzaListView.as_view(), name='cinza_list'),
    path('silica/', SilicaListView.as_view(), name='silica_list'),
    path('fibra/', FibraListView.as_view(), name='fibra_list'),
    path('teor-oleo/', TeorOleoListView.as_view(), name='teor_oleo_list'),
    path('fosforo/', FosforoListView.as_view(), name='lista_fosforo'),
    path('silica/nova/', SilicaCreateView.as_view(), name='silica_create'),
    path('silica/', SilicaListView.as_view(), name='silica_list'),

    # URLs CRUD completo para Teor de Óleo
    path('teor-oleo/<int:pk>/', TeorOleoDetailView.as_view(),
         name='teor_oleo_detail'),
    path('teor-oleo/<int:pk>/editar/',
         TeorOleoUpdateView.as_view(), name='teor_oleo_update'),
    path('teor-oleo/<int:pk>/excluir/',
         TeorOleoDeleteView.as_view(), name='teor_oleo_delete'),

    # URLs CRUD completo para Umidade
    path('umidade/<int:pk>/', UmidadeDetailView.as_view(), name='umidade_detail'),
    path('umidade/<int:pk>/editar/',
         UmidadeUpdateView.as_view(), name='umidade_update'),
    path('umidade/<int:pk>/excluir/',
         UmidadeDeleteView.as_view(), name='umidade_delete'),

    # URLs CRUD completo para Proteína
    path('proteina/<int:pk>/', ProteinaDetailView.as_view(), name='proteina_detail'),
    path('proteina/<int:pk>/editar/',
         ProteinaUpdateView.as_view(), name='proteina_update'),
    path('proteina/<int:pk>/excluir/',
         ProteinaDeleteView.as_view(), name='proteina_delete'),

    # URLs CRUD completo para Urase
    path('urase/<int:pk>/', UraseDetailView.as_view(), name='urase_detail'),
    path('urase/<int:pk>/editar/', UraseUpdateView.as_view(), name='urase_update'),
    path('urase/<int:pk>/excluir/', UraseDeleteView.as_view(), name='urase_delete'),

    # URLs CRUD completo para Cinza
    path('cinza/<int:pk>/', CinzaDetailView.as_view(), name='cinza_detail'),
    path('cinza/<int:pk>/editar/', CinzaUpdateView.as_view(), name='cinza_update'),
    path('cinza/<int:pk>/excluir/', CinzaDeleteView.as_view(), name='cinza_delete'),

    # URLs CRUD completo para Fibra
    path('fibra/<int:pk>/', FibraDetailView.as_view(), name='fibra_detail'),
    path('fibra/<int:pk>/editar/', FibraUpdateView.as_view(), name='fibra_update'),
    path('fibra/<int:pk>/excluir/', FibraDeleteView.as_view(), name='fibra_delete'),

    # URLs CRUD completo para Fósforo
    path('fosforo/<int:pk>/', FosforoDetailView.as_view(), name='fosforo_detail'),
    path('fosforo/<int:pk>/editar/',
         FosforoUpdateView.as_view(), name='fosforo_update'),
    path('fosforo/<int:pk>/excluir/',
         FosforoDeleteView.as_view(), name='fosforo_delete'),

    # URLs CRUD completo para Óleo Degomado
    path('oleo/<int:pk>/', OleoDegomadoDetailView.as_view(), name='oleo_detail'),
    path('oleo/<int:pk>/editar/',
         OleoDegomadoUpdateView.as_view(), name='oleo_update'),
    path('oleo/<int:pk>/excluir/',
         OleoDegomadoDeleteView.as_view(), name='oleo_delete'),

    # URLs CRUD completo para Silica
    path('silica/<int:pk>/', SilicaDetailView.as_view(), name='silica_detail'),
    path('silica/<int:pk>/editar/',
         SilicaUpdateView.as_view(), name='silica_update'),
    path('silica/<int:pk>/excluir/',
         SilicaDeleteView.as_view(), name='silica_delete'),
]
