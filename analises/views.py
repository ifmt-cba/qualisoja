from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decimal import Decimal
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (
    AnaliseUmidade,
    AnaliseProteina,
    AnaliseOleoDegomado,
    AnaliseUrase,
    AnaliseCinza,
    AnaliseTeorOleo,
    AnaliseFibra,
    AnaliseFosforo,
    AnaliseSilica,
)
from .forms import (
    AnaliseUmidadeForm,
    AnaliseProteinaForm,
    AnaliseOleoDegomadoForm,
    AnaliseUraseForm,
    AnaliseCinzaForm,
    AnaliseTeorOleoForm,
    AnaliseFibraForm,
    AnaliseFosforoForm,
    AnaliseSilicaForm,
)
from logs.utils import registrar_log


@method_decorator(login_required, name="dispatch")
class AnaliseHomeView(TemplateView):
    """View para a página inicial do módulo de análises"""

    template_name = "app/home_analises.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from datetime import date
        from django.db.models import Count
        
        try:
            # Contar total de análises por tipo
            context['total_umidade'] = AnaliseUmidade.objects.count()
            context['total_proteina'] = AnaliseProteina.objects.count()
            context['total_oleo'] = AnaliseOleoDegomado.objects.count()
            context['total_urase'] = AnaliseUrase.objects.count()
            context['total_cinza'] = AnaliseCinza.objects.count()
            context['total_fibra'] = AnaliseFibra.objects.count()
            context['total_fosforo'] = AnaliseFosforo.objects.count()
            context['total_teor_oleo'] = AnaliseTeorOleo.objects.count()
            
            # Total geral de análises
            context['total_analises'] = (
                context['total_umidade'] + context['total_proteina'] + 
                context['total_oleo'] + context['total_urase'] + 
                context['total_cinza'] + context['total_fibra'] + 
                context['total_fosforo'] + context['total_teor_oleo']
            )
            
            # Análises de hoje
            hoje = date.today()
            analises_hoje = 0
            try:
                analises_hoje += AnaliseUmidade.objects.filter(data=hoje).count()
                analises_hoje += AnaliseProteina.objects.filter(data=hoje).count()
                analises_hoje += AnaliseOleoDegomado.objects.filter(data=hoje).count()
                analises_hoje += AnaliseUrase.objects.filter(data=hoje).count()
                analises_hoje += AnaliseCinza.objects.filter(data=hoje).count()
                analises_hoje += AnaliseFibra.objects.filter(data=hoje).count()
                analises_hoje += AnaliseFosforo.objects.filter(data=hoje).count()
                analises_hoje += AnaliseTeorOleo.objects.filter(data=hoje).count()
            except Exception as e:
                print(f"Erro ao contar análises de hoje: {e}")
                analises_hoje = 0
            
            context['analises_hoje'] = analises_hoje
            
            # Última análise
            context['ultima_analise'] = None
            try:
                # Buscar a análise mais recente de todos os tipos
                from datetime import datetime
                ultima_data = None
                ultima_analise = None
                
                modelos = [
                    (AnaliseUmidade, 'Umidade'),
                    (AnaliseProteina, 'Proteína'),
                    (AnaliseOleoDegomado, 'Óleo Degomado'),
                    (AnaliseUrase, 'Urase'),
                    (AnaliseCinza, 'Cinza'),
                    (AnaliseFibra, 'Fibra'),
                    (AnaliseFosforo, 'Fósforo'),
                    (AnaliseTeorOleo, 'Teor de Óleo'),
                ]
                
                for modelo, nome in modelos:
                    try:
                        analise_recente = modelo.objects.order_by('-data', '-criado_em').first()
                        if analise_recente and (not ultima_data or analise_recente.data > ultima_data):
                            ultima_data = analise_recente.data
                            ultima_analise = {
                                'tipo': nome,
                                'data': analise_recente.data,
                                'horario': getattr(analise_recente, 'horario', None)
                            }
                    except Exception as e:
                        print(f"Erro ao buscar última análise de {nome}: {e}")
                        continue
                
                context['ultima_analise'] = ultima_analise
                
            except Exception as e:
                print(f"Erro ao buscar última análise: {e}")
            
        except Exception as e:
            print(f"Erro ao preparar contexto do dashboard: {e}")
            # Valores padrão em caso de erro
            context.update({
                'total_umidade': 0,
                'total_proteina': 0,
                'total_oleo': 0,
                'total_urase': 0,
                'total_cinza': 0,
                'total_fibra': 0,
                'total_fosforo': 0,
                'total_teor_oleo': 0,
                'total_analises': 0,
                'analises_hoje': 0,
                'ultima_analise': None
            })
        
        return context


@method_decorator(login_required, name="dispatch")
class UmidadeCreateView(CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Criou uma nova análise de Umidade", obj=self.object
            )
        return response

    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = "app/cadastro_umidade.html"
    success_url = reverse_lazy("analises:umidade_list")


@method_decorator(login_required, name="dispatch")
class UmidadeUpdateView(UpdateView):
    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = "app/cadastro_umidade.html"
    success_url = reverse_lazy("analises:umidade_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Umidade", obj=self.object
            )
        messages.success(self.request, "Análise de umidade atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class UmidadeDetailView(DetailView):
    model = AnaliseUmidade
    template_name = "app/detalhe_umidade.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class UmidadeDeleteView(DeleteView):
    model = AnaliseUmidade
    template_name = "app/confirmar_exclusao_umidade.html"
    success_url = reverse_lazy("analises:umidade_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Umidade", obj=obj)
        messages.success(request, "Análise de umidade excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class ProteinaCreateView(CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Criou uma nova análise de Proteína", obj=self.object
            )
        return response

    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = "app/cadastro_proteina.html"
    success_url = reverse_lazy("analises:proteina_list")


@method_decorator(login_required, name="dispatch")
class OleoDegomadoCreateView(CreateView):
    model = AnaliseOleoDegomado
    form_class = AnaliseOleoDegomadoForm
    template_name = "app/cadastro_oleo.html"
    success_url = reverse_lazy("analises:oleo_list")

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
        titulacao = form.cleaned_data["titulacao"]
        fator_correcao = form.cleaned_data["fator_correcao"]
        peso_amostra = form.cleaned_data["peso_amostra"]
        tipo_analise = form.cleaned_data["tipo_analise"]
        tara = form.cleaned_data["tara"]
        liquido = form.cleaned_data["liquido"]

        resultado = None  # evita erro se nenhum cálculo for feito

        if tipo_analise == "UMI":
            if tara is not None and liquido is not None and peso_amostra is not None:
                resultado = (((tara + peso_amostra) - liquido) / peso_amostra) * 100

        elif tipo_analise == "ACI":
            if (
                titulacao is not None
                and fator_correcao is not None
                and peso_amostra is not None
            ):
                resultado = (
                    titulacao * fator_correcao * Decimal("28.2") * Decimal("100")
                ) / peso_amostra

        elif tipo_analise == "SAB":
            if (
                titulacao is not None
                and fator_correcao is not None
                and peso_amostra is not None
            ):
                resultado = (
                    titulacao * fator_correcao * Decimal("300.4") * Decimal("100")
                ) / peso_amostra

        form.instance.resultado = resultado
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user,
                "Criou uma nova análise de Óleo Degomado",
                obj=self.object,
            )
        return response


@method_decorator(login_required, name="dispatch")
class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = "app/lista_umidade.html"


@method_decorator(login_required, name="dispatch")
class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = "app/lista_proteina.html"
    context_object_name = "analises"
    ordering = ["-data", "-horario"]


@method_decorator(login_required, name="dispatch")
class ProteinaCreateView(CreateView):
    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = "app/cadastro_proteina.html"
    success_url = reverse_lazy("analises:proteina_list")

    def form_valid(self, form):
        proteina = form.save(commit=False)

        # Só calcula a proteína se for um tipo de amostra válido para análise
        if proteina.tipo_amostra not in ["FP", "SA"]:
            # Define os tipos de amostra de umidade correspondentes
            umidade_tipos_lookup = [proteina.tipo_amostra]
            if proteina.tipo_amostra == "FL":  # Farelo
                umidade_tipos_lookup = ["FG", "FF"]  # Farelo Grosso e Fino

            # Busca a umidade da mesma data e tipo de amostra, a mais recente por horário
            umidade_obj = (
                AnaliseUmidade.objects.filter(
                    data=proteina.data, tipo_amostra__in=umidade_tipos_lookup
                )
                .order_by("-horario")
                .first()
            )

            # Garante que um valor decimal seja passado, mesmo que a umidade não seja encontrada.
            umidade_valor = (
                umidade_obj.resultado
                if umidade_obj and umidade_obj.resultado is not None
                else Decimal("0.00")
            )

            proteina.calcular_proteina(umidade_valor)
        else:
            # Garante que os resultados sejam zero para casos especiais, evitando erros nos relatórios.
            proteina.resultado = Decimal("0.00")
            proteina.resultado_corrigido = Decimal("0.00")

        proteina.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM INVÁLIDO:", form.errors, form.non_field_errors())
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class ProteinaUpdateView(UpdateView):
    model = AnaliseProteina
    form_class = AnaliseProteinaForm
    template_name = "app/cadastro_proteina.html"
    success_url = reverse_lazy("analises:proteina_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Proteína", obj=self.object
            )
        messages.success(self.request, "Análise de proteína atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class ProteinaDetailView(DetailView):
    model = AnaliseProteina
    template_name = "app/detalhe_proteina.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class ProteinaDeleteView(DeleteView):
    model = AnaliseProteina
    template_name = "app/confirmar_exclusao_proteina.html"
    success_url = reverse_lazy("analises:proteina_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Proteína", obj=obj)
        messages.success(request, "Análise de proteína excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class OleoDegomadoListView(ListView):
    model = AnaliseOleoDegomado
    template_name = "app/lista_oleo.html"


# Adicione estas classes no seu views.py


@method_decorator(login_required, name="dispatch")
class UraseCreateView(CreateView):
    model = AnaliseUrase
    form_class = AnaliseUraseForm
    template_name = "app/cadastro_urase.html"
    success_url = reverse_lazy("analises:urase_list")

    def form_valid(self, form):
        """
        O cálculo é feito automaticamente no método save() do modelo,
        mas você pode adicionar validações extras aqui se necessário.
        """
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Criou uma nova análise de Urase", obj=self.object
            )
        messages.success(self.request, "Análise de urase criada com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao salvar a análise. Verifique os dados informados."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class UraseListView(ListView):
    model = AnaliseUrase
    template_name = "app/lista_urase.html"
    context_object_name = "object_list"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_farelo"] = self.get_queryset().filter(tipo_amostra="FL").count()
        return context

    def get_queryset(self):
        """
        Retorna as análises ordenadas por data e horário mais recentes.
        """
        return AnaliseUrase.objects.all().order_by("-data", "-horario")


@method_decorator(login_required, name="dispatch")
class UraseDetailView(DetailView):
    model = AnaliseUrase
    template_name = "app/detalhe_urase.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class UraseUpdateView(UpdateView):
    model = AnaliseUrase
    form_class = AnaliseUraseForm
    template_name = "app/cadastro_urase.html"
    success_url = reverse_lazy("analises:urase_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Urase", obj=self.object
            )
        messages.success(self.request, "Análise de urase atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class UraseDeleteView(DeleteView):
    model = AnaliseUrase
    template_name = "app/confirmar_exclusao_urase.html"
    success_url = reverse_lazy("analises:urase_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Urase", obj=obj)
        messages.success(request, "Análise de urase excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# Importar as novas análises
from .models import AnaliseCinza, AnaliseTeorOleo, AnaliseFibra, AnaliseFosforo
from .forms import (
    AnaliseCinzaForm,
    AnaliseTeorOleoForm,
    AnaliseFibraForm,
    AnaliseFosforoForm,
)


# Views para Análise de Cinza
@method_decorator(login_required, name="dispatch")
class CinzaCreateView(CreateView):
    model = AnaliseCinza
    form_class = AnaliseCinzaForm
    template_name = "app/cadastro_cinza.html"
    success_url = reverse_lazy("analises:cinza_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Criou uma nova análise de Cinza", obj=self.object
            )
        messages.success(self.request, "Análise de cinza criada com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao salvar a análise. Verifique os dados informados."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class CinzaListView(ListView):
    model = AnaliseCinza
    template_name = "app/lista_cinza.html"
    context_object_name = "object_list"
    ordering = ["-data", "-horario"]
    paginate_by = 10


@method_decorator(login_required, name="dispatch")
class CinzaDetailView(DetailView):
    model = AnaliseCinza
    template_name = "app/detalhe_cinza.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class CinzaUpdateView(UpdateView):
    model = AnaliseCinza
    form_class = AnaliseCinzaForm
    template_name = "app/cadastro_cinza.html"
    success_url = reverse_lazy("analises:cinza_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Cinza", obj=self.object
            )
        messages.success(self.request, "Análise de cinza atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class CinzaDeleteView(DeleteView):
    model = AnaliseCinza
    template_name = "app/confirmar_exclusao_cinza.html"
    success_url = reverse_lazy("analises:cinza_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Cinza", obj=obj)
        messages.success(request, "Análise de cinza excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# Views para Análise de Teor de Óleo
@method_decorator(login_required, name="dispatch")
class TeorOleoCreateView(CreateView):
    model = AnaliseTeorOleo
    form_class = AnaliseTeorOleoForm
    template_name = "app/cadastro_teor_oleo.html"
    success_url = reverse_lazy("analises:teor_oleo_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user,
                "Criou uma nova análise de Teor de Óleo",
                obj=self.object,
            )
        messages.success(self.request, "Análise de teor de óleo criada com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao salvar a análise. Verifique os dados informados."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class TeorOleoListView(ListView):
    model = AnaliseTeorOleo
    template_name = "app/lista_teor_oleo.html"
    context_object_name = "object_list"
    ordering = ["-data", "-horario"]
    paginate_by = 10


@method_decorator(login_required, name="dispatch")
class TeorOleoUpdateView(UpdateView):
    model = AnaliseTeorOleo
    form_class = AnaliseTeorOleoForm
    template_name = "app/cadastro_teor_oleo.html"
    success_url = reverse_lazy("analises:teor_oleo_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Teor de Óleo", obj=self.object
            )
        messages.success(
            self.request, "Análise de teor de óleo atualizada com sucesso!"
        )
        return response


@method_decorator(login_required, name="dispatch")
class TeorOleoDetailView(DetailView):
    model = AnaliseTeorOleo
    template_name = "app/detalhe_teor_oleo.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class TeorOleoDeleteView(DeleteView):
    model = AnaliseTeorOleo
    template_name = "app/confirmar_exclusao_teor_oleo.html"
    success_url = reverse_lazy("analises:teor_oleo_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Teor de Óleo", obj=obj)
        messages.success(request, "Análise de teor de óleo excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# Views para Análise de Fibra
@method_decorator(login_required, name="dispatch")
class FibraCreateView(CreateView):
    model = AnaliseFibra
    form_class = AnaliseFibraForm
    template_name = "app/cadastro_fibra.html"
    success_url = reverse_lazy("analises:fibra_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            if self.request.user.is_authenticated:
                registrar_log(
                    self.request.user,
                    "Criou uma nova análise de Fibra",
                    obj=self.object,
                )
            messages.success(self.request, "Análise de fibra salva com sucesso!")
            return response
        except Exception as e:
            messages.error(self.request, f"Erro ao salvar análise: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Processar formulário inválido"""
        messages.error(
            self.request, "Erro no formulário. Verifique os dados e tente novamente."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class FibraListView(ListView):
    model = AnaliseFibra
    template_name = "app/lista_fibra.html"
    context_object_name = "object_list"
    ordering = ["-data", "-horario"]
    paginate_by = 10


@method_decorator(login_required, name="dispatch")
class FibraDetailView(DetailView):
    model = AnaliseFibra
    template_name = "app/detalhe_fibra.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class FibraUpdateView(UpdateView):
    model = AnaliseFibra
    form_class = AnaliseFibraForm
    template_name = "app/cadastro_fibra.html"
    success_url = reverse_lazy("analises:fibra_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Fibra", obj=self.object
            )
        messages.success(self.request, "Análise de fibra atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class FibraDeleteView(DeleteView):
    model = AnaliseFibra
    template_name = "app/confirmar_exclusao_fibra.html"
    success_url = reverse_lazy("analises:fibra_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Fibra", obj=obj)
        messages.success(request, "Análise de fibra excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# Views para Análise de Fósforo
@method_decorator(login_required, name="dispatch")
class FosforoCreateView(CreateView):
    model = AnaliseFosforo
    form_class = AnaliseFosforoForm
    template_name = "app/cadastro_fosforo.html"
    success_url = reverse_lazy("analises:lista_fosforo")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Criou uma nova análise de Fósforo", obj=self.object
            )
        messages.success(self.request, "Análise de fósforo salva com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao salvar análise. Verifique os dados informados."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class FosforoListView(ListView):
    model = AnaliseFosforo
    template_name = "app/lista_fosforo.html"
    context_object_name = "object_list"
    ordering = ["-id"]
    paginate_by = 100

    def get_queryset(self):
        """Retorna todos os registros de forma simples"""
        return AnaliseFosforo.objects.all().order_by("-id")


@method_decorator(login_required, name="dispatch")
class FosforoDetailView(DetailView):
    model = AnaliseFosforo
    template_name = "app/detalhe_fosforo.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class FosforoUpdateView(UpdateView):
    model = AnaliseFosforo
    form_class = AnaliseFosforoForm
    template_name = "app/cadastro_fosforo.html"
    success_url = reverse_lazy("analises:lista_fosforo")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Fósforo", obj=self.object
            )
        messages.success(self.request, "Análise de fósforo atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class FosforoDeleteView(DeleteView):
    model = AnaliseFosforo
    template_name = "app/confirmar_exclusao_fosforo.html"
    success_url = reverse_lazy("analises:lista_fosforo")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Fósforo", obj=obj)
        messages.success(request, "Análise de fósforo excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class OleoDegomadoUpdateView(UpdateView):
    model = AnaliseOleoDegomado
    form_class = AnaliseOleoDegomadoForm
    template_name = "app/cadastro_oleo.html"
    success_url = reverse_lazy("analises:oleo_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user,
                "Editou uma análise de Óleo Degomado",
                obj=self.object,
            )
        messages.success(
            self.request, "Análise de óleo degomado atualizada com sucesso!"
        )
        return response


@method_decorator(login_required, name="dispatch")
class OleoDegomadoDetailView(DetailView):
    model = AnaliseOleoDegomado
    template_name = "app/detalhe_oleo.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class OleoDegomadoDeleteView(DeleteView):
    model = AnaliseOleoDegomado
    template_name = "app/confirmar_exclusao_oleo.html"
    success_url = reverse_lazy("analises:oleo_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Óleo Degomado", obj=obj)
        messages.success(request, "Análise de óleo degomado excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# Views para Análise de Sílica
@method_decorator(login_required, name="dispatch")
class SilicaCreateView(CreateView):
    model = AnaliseSilica
    form_class = AnaliseSilicaForm
    template_name = "app/cadastro_silica.html"
    success_url = reverse_lazy("analises:silica_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Criou uma nova análise de Sílica", obj=self.object
            )
        messages.success(self.request, "Análise de Sílica cadastrada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class SilicaListView(ListView):
    model = AnaliseSilica
    template_name = "app/lista_silica.html"
    context_object_name = "analises"
    paginate_by = 10
    ordering = ["-data", "-horario"]


@method_decorator(login_required, name="dispatch")
class SilicaUpdateView(UpdateView):
    model = AnaliseSilica
    form_class = AnaliseSilicaForm
    template_name = "app/cadastro_silica.html"
    success_url = reverse_lazy("analises:silica_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            registrar_log(
                self.request.user, "Editou uma análise de Sílica", obj=self.object
            )
        messages.success(self.request, "Análise de Sílica atualizada com sucesso!")
        return response


@method_decorator(login_required, name="dispatch")
class SilicaDetailView(DetailView):
    model = AnaliseSilica
    template_name = "app/detalhe_silica.html"
    context_object_name = "analise"


@method_decorator(login_required, name="dispatch")
class SilicaDeleteView(DeleteView):
    model = AnaliseSilica
    template_name = "app/confirmar_exclusao_silica.html"
    success_url = reverse_lazy("analises:silica_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated:
            registrar_log(request.user, "Excluiu uma análise de Sílica", obj=obj)
        messages.success(request, "Análise de Sílica excluída com sucesso!")
        return super().delete(request, *args, **kwargs)
