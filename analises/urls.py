from django.urls import path
from analises import views

urlpatterns = [
    path('cadastrarAnalise/', views.cadastrarAnalise, name="CadastrarAnalise"),
    path('historicoAnalises/',views.historicoAnalises, name="historicoAnalises"),
    path('relatorios/',views.relatorios, name="relatorios")
]