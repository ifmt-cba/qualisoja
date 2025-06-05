from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado
from .forms import AnaliseUmidadeForm, AnaliseProteinaForm, AnaliseOleoDegomadoForm

class AnaliseHomeView(TemplateView):
    """View para a página inicial do módulo de análises"""
    template_name = 'app/home_analises.html'

class UmidadeCreateView(CreateView):
    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = 'app/cadastro_umidade.html'
    success_url = reverse_lazy('analises:umidade_list')

class ProteinaCreateView(CreateView):
    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = 'app/cadastro_proteina.html'
    success_url = reverse_lazy('analises:proteina_list')

class OleoDegomadoCreateView(CreateView):
    model = AnaliseOleoDegomado
    form_class = AnaliseOleoDegomadoForm
    template_name = 'app/cadastro_oleo.html'
    success_url = reverse_lazy('analises:oleo_list')

class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = 'app/lista_umidade.html'

class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = 'app/lista_proteina.html'

class OleoDegomadoListView(ListView):
    model = AnaliseOleoDegomado
    template_name = 'app/lista_oleo.html'