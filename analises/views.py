from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import AnaliseUmidade, AnaliseProteina
from .forms import AnaliseUmidadeForm, AnaliseProteinaForm

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

class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = 'app/lista_umidade.html'

class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = 'app/lista_proteina.html'