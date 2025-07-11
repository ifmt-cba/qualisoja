from decimal import Decimal
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, AnaliseUrase, AnaliseCinza, AnaliseTeorOleo, AnaliseFibra, AnaliseFosforo, AnaliseSilica
from .forms import AnaliseUmidadeForm, AnaliseProteinaForm, AnaliseOleoDegomadoForm, AnaliseUraseForm, AnaliseCinzaForm, AnaliseTeorOleoForm, AnaliseFibraForm, AnaliseFosforoForm, AnaliseSilicaForm
from logs.utils import registrar_log


class AnaliseHomeView(TemplateView):
    """View para a página inicial do módulo de análises"""
    template_name = 'app/home_analises.html'

class UmidadeCreateView(CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Umidade", obj=self.object)
        return response
    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = 'app/cadastro_umidade.html'
    success_url = reverse_lazy('analises:umidade_list')

class UmidadeUpdateView(UpdateView):
    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = 'app/cadastro_umidade.html'
    success_url = reverse_lazy('analises:umidade_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Umidade", obj=self.object)
        messages.success(self.request, 'Análise de umidade atualizada com sucesso!')
        return response

class UmidadeDetailView(DetailView):
    model = AnaliseUmidade
    template_name = 'app/detalhe_umidade.html'
    context_object_name = 'analise'

class UmidadeDeleteView(DeleteView):
    model = AnaliseUmidade
    template_name = 'app/confirmar_exclusao_umidade.html'
    success_url = reverse_lazy('analises:umidade_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Umidade", obj=obj)
        messages.success(request, 'Análise de umidade excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class ProteinaCreateView(CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Proteína", obj=self.object)
        return response
    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = 'app/cadastro_proteina.html'
    success_url = reverse_lazy('analises:proteina_list')

class OleoDegomadoCreateView(CreateView):
    model = AnaliseOleoDegomado
    form_class = AnaliseOleoDegomadoForm
    template_name = 'app/cadastro_oleo.html'
    success_url = reverse_lazy('analises:oleo_list')

    # def form_valid(self, form):
    #     titulacao = form.cleaned_data['titulacao']
    #     fator_correcao = form.cleaned_data['fator_correcao']
    #     peso_amostra = form.cleaned_data['peso_amostra']
    #     tipo_analise = form.cleaned_data['tipo_analise']
    #     tara = form.cleaned_data['tara']
    #     liquido = form.cleaned_data['liquido']
        
    #     resultado = None  # <- ✅ isso evita o erro

    #     if tipo_analise == 'UMI':
    #         if tara and fator_correcao and peso_amostra:
    #             resultado = ((tara + peso_amostra) - (liquido))/peso_amostra*100
    #             # form.instance.resultado = resultado.quantize(Decimal('0.01'))  # arredonda para 2 casas decimais

    #     elif tipo_analise == 'ACI':
    #         if titulacao and fator_correcao and peso_amostra:
    #             # Use Decimal para valores numéricos literais
    #             resultado = (titulacao * fator_correcao * Decimal('28.2') * Decimal('100')) / peso_amostra
    #             # form.instance.resultado = resultado.quantize(Decimal('0.01'))  # arredonda para 2 casas decimais

    #     elif tipo_analise == 'SAB':
    #         if titulacao and fator_correcao and peso_amostra:
    #             resultado = (titulacao * fator_correcao * Decimal('300.4') * Decimal('100')) / peso_amostra
    #             # form.instance.resultado = resultado.quantize(Decimal('0.01'))  # arredonda para 2 casas decimais
    #     else:
    #         resultado = None
    #     form.instance.resultado = resultado        
    #     return super().form_valid(form)
    def form_valid(self, form):
        titulacao = form.cleaned_data['titulacao']
        fator_correcao = form.cleaned_data['fator_correcao']
        peso_amostra = form.cleaned_data['peso_amostra']
        tipo_analise = form.cleaned_data['tipo_analise']
        tara = form.cleaned_data['tara']
        liquido = form.cleaned_data['liquido']

        resultado = None  # evita erro se nenhum cálculo for feito

        if tipo_analise == 'UMI':
            if tara is not None and liquido is not None and peso_amostra is not None:
                resultado = (((tara + peso_amostra) - liquido) / peso_amostra) * 100

        elif tipo_analise == 'ACI':
            if titulacao is not None and fator_correcao is not None and peso_amostra is not None:
                resultado = (titulacao * fator_correcao * Decimal('28.2') * Decimal('100')) / peso_amostra

        elif tipo_analise == 'SAB':
            if titulacao is not None and fator_correcao is not None and peso_amostra is not None:
                resultado = (titulacao * fator_correcao * Decimal('300.4') * Decimal('100')) / peso_amostra

        form.instance.resultado = resultado
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Óleo Degomado", obj=self.object)
        return response


class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = 'app/lista_umidade.html'

class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = 'app/lista_proteina.html'

class ProteinaUpdateView(UpdateView):
    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = 'app/cadastro_proteina.html'
    success_url = reverse_lazy('analises:proteina_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Proteína", obj=self.object)
        messages.success(self.request, 'Análise de proteína atualizada com sucesso!')
        return response

class ProteinaDetailView(DetailView):
    model = AnaliseProteina
    template_name = 'app/detalhe_proteina.html'
    context_object_name = 'analise'

class ProteinaDeleteView(DeleteView):
    model = AnaliseProteina
    template_name = 'app/confirmar_exclusao_proteina.html'
    success_url = reverse_lazy('analises:proteina_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Proteína", obj=obj)
        messages.success(request, 'Análise de proteína excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class OleoDegomadoListView(ListView):
    model = AnaliseOleoDegomado
    template_name = 'app/lista_oleo.html'
    
# Adicione estas classes no seu views.py

class UraseCreateView(CreateView):
    model = AnaliseUrase
    form_class = AnaliseUraseForm
    template_name = 'app/cadastro_urase.html'
    success_url = reverse_lazy('analises:urase_list')

    def form_valid(self, form):
        """
        O cálculo é feito automaticamente no método save() do modelo,
        mas você pode adicionar validações extras aqui se necessário.
        """
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Urase", obj=self.object)
        messages.success(self.request, 'Análise de urase criada com sucesso!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a análise. Verifique os dados informados.')
        return super().form_invalid(form)

class UraseListView(ListView):
    model = AnaliseUrase
    template_name = 'app/lista_urase.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_farelo'] = self.get_queryset().filter(tipo_amostra='FL').count()
        return context

    def get_queryset(self):
        """
        Retorna as análises ordenadas por data e horário mais recentes.
        """
        return AnaliseUrase.objects.all().order_by('-data', '-horario')

class UraseDetailView(DetailView):
    model = AnaliseUrase
    template_name = 'app/detalhe_urase.html'
    context_object_name = 'analise'

class UraseUpdateView(UpdateView):
    model = AnaliseUrase
    form_class = AnaliseUraseForm
    template_name = 'app/cadastro_urase.html'
    success_url = reverse_lazy('analises:urase_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Urase", obj=self.object)
        messages.success(self.request, 'Análise de urase atualizada com sucesso!')
        return response

class UraseDeleteView(DeleteView):
    model = AnaliseUrase
    template_name = 'app/confirmar_exclusao_urase.html'
    success_url = reverse_lazy('analises:urase_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Urase", obj=obj)
        messages.success(request, 'Análise de urase excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Importar as novas análises
from .models import AnaliseCinza, AnaliseTeorOleo, AnaliseFibra, AnaliseFosforo
from .forms import AnaliseCinzaForm, AnaliseTeorOleoForm, AnaliseFibraForm, AnaliseFosforoForm

# Views para Análise de Cinza
class CinzaCreateView(CreateView):
    model = AnaliseCinza
    form_class = AnaliseCinzaForm
    template_name = 'app/cadastro_cinza.html'
    success_url = reverse_lazy('analises:cinza_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Cinza", obj=self.object)
        messages.success(self.request, 'Análise de cinza criada com sucesso!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a análise. Verifique os dados informados.')
        return super().form_invalid(form)

class CinzaListView(ListView):
    model = AnaliseCinza
    template_name = 'app/lista_cinza.html'
    context_object_name = 'object_list'
    ordering = ['-data', '-horario']
    paginate_by = 10

class CinzaDetailView(DetailView):
    model = AnaliseCinza
    template_name = 'app/detalhe_cinza.html'
    context_object_name = 'analise'

class CinzaUpdateView(UpdateView):
    model = AnaliseCinza
    form_class = AnaliseCinzaForm
    template_name = 'app/cadastro_cinza.html'
    success_url = reverse_lazy('analises:cinza_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Cinza", obj=self.object)
        messages.success(self.request, 'Análise de cinza atualizada com sucesso!')
        return response

class CinzaDeleteView(DeleteView):
    model = AnaliseCinza
    template_name = 'app/confirmar_exclusao_cinza.html'
    success_url = reverse_lazy('analises:cinza_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Cinza", obj=obj)
        messages.success(request, 'Análise de cinza excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Análise de Teor de Óleo
class TeorOleoCreateView(CreateView):
    model = AnaliseTeorOleo
    form_class = AnaliseTeorOleoForm
    template_name = 'app/cadastro_teor_oleo.html'
    success_url = reverse_lazy('analises:teor_oleo_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Teor de Óleo", obj=self.object)
        messages.success(self.request, 'Análise de teor de óleo criada com sucesso!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a análise. Verifique os dados informados.')
        return super().form_invalid(form)

class TeorOleoListView(ListView):
    model = AnaliseTeorOleo
    template_name = 'app/lista_teor_oleo.html'
    context_object_name = 'object_list'
    ordering = ['-data', '-horario']
    paginate_by = 10

class TeorOleoUpdateView(UpdateView):
    model = AnaliseTeorOleo
    form_class = AnaliseTeorOleoForm
    template_name = 'app/cadastro_teor_oleo.html'
    success_url = reverse_lazy('analises:teor_oleo_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Teor de Óleo", obj=self.object)
        messages.success(self.request, 'Análise de teor de óleo atualizada com sucesso!')
        return response

class TeorOleoDetailView(DetailView):
    model = AnaliseTeorOleo
    template_name = 'app/detalhe_teor_oleo.html'
    context_object_name = 'analise'

class TeorOleoDeleteView(DeleteView):
    model = AnaliseTeorOleo
    template_name = 'app/confirmar_exclusao_teor_oleo.html'
    success_url = reverse_lazy('analises:teor_oleo_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Teor de Óleo", obj=obj)
        messages.success(request, 'Análise de teor de óleo excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Análise de Fibra
class FibraCreateView(CreateView):
    model = AnaliseFibra
    form_class = AnaliseFibraForm
    template_name = 'app/cadastro_fibra.html'
    success_url = reverse_lazy('analises:fibra_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            if self.request.user.is_authenticated:
                registrar_log(self.request.user, "Criou uma nova análise de Fibra", obj=self.object)
            messages.success(self.request, 'Análise de fibra salva com sucesso!')
            return response
        except Exception as e:
            messages.error(self.request, f'Erro ao salvar análise: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """Processar formulário inválido"""
        messages.error(self.request, 'Erro no formulário. Verifique os dados e tente novamente.')
        return super().form_invalid(form)

class FibraListView(ListView):
    model = AnaliseFibra
    template_name = 'app/lista_fibra.html'
    context_object_name = 'object_list'
    ordering = ['-data', '-horario']
    paginate_by = 10

class FibraDetailView(DetailView):
    model = AnaliseFibra
    template_name = 'app/detalhe_fibra.html'
    context_object_name = 'analise'

class FibraUpdateView(UpdateView):
    model = AnaliseFibra
    form_class = AnaliseFibraForm
    template_name = 'app/cadastro_fibra.html'
    success_url = reverse_lazy('analises:fibra_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Fibra", obj=self.object)
        messages.success(self.request, 'Análise de fibra atualizada com sucesso!')
        return response

class FibraDeleteView(DeleteView):
    model = AnaliseFibra
    template_name = 'app/confirmar_exclusao_fibra.html'
    success_url = reverse_lazy('analises:fibra_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Fibra", obj=obj)
        messages.success(request, 'Análise de fibra excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Análise de Fósforo
class FosforoCreateView(CreateView):
    model = AnaliseFosforo
    form_class = AnaliseFosforoForm
    template_name = 'app/cadastro_fosforo.html'
    success_url = reverse_lazy('analises:lista_fosforo')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Fósforo", obj=self.object)
        messages.success(self.request, 'Análise de fósforo salva com sucesso!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar análise. Verifique os dados informados.')
        return super().form_invalid(form)

class FosforoListView(ListView):
    model = AnaliseFosforo
    template_name = 'app/lista_fosforo.html'
    context_object_name = 'object_list'
    ordering = ['-id']
    paginate_by = 100
    
    def get_queryset(self):
        """Retorna todos os registros de forma simples"""
        return AnaliseFosforo.objects.all().order_by('-id')

class FosforoDetailView(DetailView):
    model = AnaliseFosforo
    template_name = 'app/detalhe_fosforo.html'
    context_object_name = 'analise'

class FosforoUpdateView(UpdateView):
    model = AnaliseFosforo
    form_class = AnaliseFosforoForm
    template_name = 'app/cadastro_fosforo.html'
    success_url = reverse_lazy('analises:lista_fosforo')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Fósforo", obj=self.object)
        messages.success(self.request, 'Análise de fósforo atualizada com sucesso!')
        return response

class FosforoDeleteView(DeleteView):
    model = AnaliseFosforo
    template_name = 'app/confirmar_exclusao_fosforo.html'
    success_url = reverse_lazy('analises:lista_fosforo')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Fósforo", obj=obj)
        messages.success(request, 'Análise de fósforo excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class OleoDegomadoUpdateView(UpdateView):
    model = AnaliseOleoDegomado
    form_class = AnaliseOleoDegomadoForm
    template_name = 'app/cadastro_oleo.html'
    success_url = reverse_lazy('analises:oleo_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Óleo Degomado", obj=self.object)
        messages.success(self.request, 'Análise de óleo degomado atualizada com sucesso!')
        return response

class OleoDegomadoDetailView(DetailView):
    model = AnaliseOleoDegomado
    template_name = 'app/detalhe_oleo.html'
    context_object_name = 'analise'

class OleoDegomadoDeleteView(DeleteView):
    model = AnaliseOleoDegomado
    template_name = 'app/confirmar_exclusao_oleo.html'
    success_url = reverse_lazy('analises:oleo_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Óleo Degomado", obj=obj)
        messages.success(request, 'Análise de óleo degomado excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Análise de Sílica
class SilicaCreateView(CreateView):
    model = AnaliseSilica
    form_class = AnaliseSilicaForm
    template_name = 'app/cadastro_silica.html'
    success_url = reverse_lazy('analises:silica_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Criou uma nova análise de Sílica", obj=self.object)
        messages.success(self.request, 'Análise de Sílica cadastrada com sucesso!')
        return response

class SilicaListView(ListView):
    model = AnaliseSilica
    template_name = 'app/lista_silica.html'
    context_object_name = 'analises'
    paginate_by = 10
    ordering = ['-data', '-horario']

class SilicaUpdateView(UpdateView):
    model = AnaliseSilica
    form_class = AnaliseSilicaForm
    template_name = 'app/cadastro_silica.html'
    success_url = reverse_lazy('analises:silica_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(self.request.user, "Editou uma análise de Sílica", obj=self.object)
        messages.success(self.request, 'Análise de Sílica atualizada com sucesso!')
        return response

class SilicaDetailView(DetailView):
    model = AnaliseSilica
    template_name = 'app/detalhe_silica.html'
    context_object_name = 'analise'

class SilicaDeleteView(DeleteView):
    model = AnaliseSilica
    template_name = 'app/confirmar_exclusao_silica.html'
    success_url = reverse_lazy('analises:silica_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Sílica", obj=obj)
        messages.success(request, 'Análise de Sílica excluída com sucesso!')
        return super().delete(request, *args, **kwargs)