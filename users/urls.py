from django.urls import path
from users import views
urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/',views.loginViews, name="login"),
]