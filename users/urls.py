from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.loginViews, name='login'),
    path('login/', views.loginViews, name='login_explicit'),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logout/', views.logout, name="logout")
]
