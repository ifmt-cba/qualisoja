from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, home_simple, test_connection
from . import views

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('simple/', home_simple, name='home_simple'),
    path('test-connection/', test_connection, name='test_connection'),
    path('admin/', admin.site.urls),
    path('analises/', include('analises.urls', namespace='analises')),
    path('relatorios/', include('relatorios.urls', namespace='relatorios')),
    path('health/', views.health_check, name='health_check'),
    path('teste/', views.teste_acesso, name='teste_acesso'),
]

# Importar e adicionar URLs opcionais de debug e CSRF
try:
    from .debug_views import debug_dashboard_data
    urlpatterns.append(path('debug/dashboard/', debug_dashboard_data, name='debug_dashboard'))
except ImportError:
    pass

try:
    from test_csrf_view import test_csrf_view
    urlpatterns.append(path('test-csrf/', test_csrf_view, name='test_csrf'))
except ImportError:
    pass

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
