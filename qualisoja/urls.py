from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/',include('users.urls')),
    path('analises/',include('analises.urls'))

]
