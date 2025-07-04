from django.contrib import admin
from django.urls import path, include
from .views import home, home_simple

# Importar view de debug
try:
    from debug_views import debug_dashboard_data
    debug_available = True
except ImportError:
    debug_available = False

# Importar view de teste CSRF
try:
    from test_csrf_view import test_csrf_view
    csrf_test_available = True
except ImportError:
    csrf_test_available = False

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    #path('analises/', home, name='home'),
    path('simple/', home_simple, name='home_simple'),
    path('admin/', admin.site.urls),
    path('analises/',include('analises.urls', namespace='analises')),
    path('relatorios/',include('relatorios.urls', namespace='relatorios'))
]

# Adicionar URL de teste CSRF se disponível
if csrf_test_available:
    urlpatterns.append(path('test-csrf/', test_csrf_view, name='test_csrf'))
if debug_available:
    urlpatterns.append(path('debug/dashboard/', debug_dashboard_data, name='debug_dashboard'))
