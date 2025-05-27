from django.urls import path
from .views import (
    UmidadeCreateView, ProteinaCreateView, UmidadeListView, ProteinaListView
)

app_name = 'analises'

urlpatterns = [
    path('umidade/nova/', UmidadeCreateView.as_view(), name='umidade_create'),
    path('proteina/nova/', ProteinaCreateView.as_view(), name='proteina_create'),
    path('umidade/', UmidadeListView.as_view(), name='umidade_list'),
    path('proteina/', ProteinaListView.as_view(), name='proteina_list'),
]