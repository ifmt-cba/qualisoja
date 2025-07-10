from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.loginViews, name='login'),
    path('cadastro/', views.cadastro, name="cadastro"),
    #path('login/',views.loginViews, name="login"),
    path('logout/', views.logout, name="logout")
]
