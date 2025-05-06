from django.urls import path
from users import views
urlpatterns = [
path('cadastro/', views.cadastro, name="cadastro"),
]