from django.contrib import admin
from django.urls import path, include
from .views import home, home_simple

# Importar view de debug
try:
    from debug_views import debug_dashboard_data
    debug_available = True
except ImportError:
    debug_available = False

urlpatterns = [
    path('', home, name='home'),
    path('simple/', home_simple, name='home_simple'),
    path('admin/', admin.site.urls),
    path('cadastro/',include('users.urls', namespace='users')),
    path('analises/',include('analises.urls', namespace='analises')),
    path('relatorios/',include('relatorios_app.urls', namespace='relatorios'))
]

# Adicionar URL de debug se disponível
if debug_available:
    urlpatterns.append(path('debug/dashboard/', debug_dashboard_data, name='debug_dashboard'))
