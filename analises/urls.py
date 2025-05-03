from django.urls import path
from analises import views

urlpatterns = [
    path('cadastrarAnalise/', views.cadastrarAnalise, name="CadastrarAnalise"),
    path('salvarAnalise/', views.cadastrarAnalise, name="salvarAnalise")
]