from decimal import Decimal
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.db.models import OuterRef, Subquery
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, AnaliseUrase
from .forms import (
    AnaliseUmidadeForm,
    AnaliseProteinaForm,
    AnaliseOleoDegomadoForm,
    AnaliseUraseForm,
)


class AnaliseHomeView(TemplateView):
    """View para a página inicial do módulo de análises"""

    template_name = "app/home_analises.html"


class UmidadeCreateView(CreateView):
    model = AnaliseUmidade
    form_class = AnaliseUmidadeForm
    template_name = "app/cadastro_umidade.html"
    success_url = reverse_lazy("analises:umidade_list")


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


class OleoDegomadoCreateView(CreateView):
    model = AnaliseOleoDegomado
    form_class = AnaliseOleoDegomadoForm
    template_name = "app/cadastro_oleo.html"
    success_url = reverse_lazy("analises:oleo_list")

    def form_valid(self, form):
        # O modelo AnaliseOleoDegomado não possui cálculos automáticos.
        # A view simplesmente salva os dados inseridos no formulário.
        self.object = form.save()
        return super().form_valid(form)


class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = "app/lista_umidade.html"


class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = "app/lista_proteina.html"
    context_object_name = "analises"
    paginate_by = 20

    def get_queryset(self):
        from django.db.models import Case, When, Subquery, OuterRef, Value, DecimalField

        # Subquery para buscar a umidade correspondente para 'Soja Industrializada'
        umidade_si_subquery = (
            AnaliseUmidade.objects.filter(data=OuterRef("data"), tipo_amostra="SI")
            .order_by("-horario")
            .values("resultado")[:1]
        )

        # Subquery para buscar a umidade correspondente para 'Farelo' (Grosso ou Fino)
        umidade_fl_subquery = (
            AnaliseUmidade.objects.filter(
                data=OuterRef("data"), tipo_amostra__in=["FG", "FF"]
            )
            .order_by("-horario")
            .values("resultado")[:1]
        )

        # Anota cada análise de proteína com a umidade correta usada no cálculo
        queryset = AnaliseProteina.objects.annotate(
            umidade_usada=Case(
                When(tipo_amostra="SI", then=Subquery(umidade_si_subquery)),
                When(tipo_amostra="FL", then=Subquery(umidade_fl_subquery)),
                default=Value(None, output_field=DecimalField()),
            )
        ).order_by("-data", "-horario")
        return queryset


class OleoDegomadoListView(ListView):
    model = AnaliseOleoDegomado
    template_name = "app/lista_oleo.html"


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
        return super().form_valid(form)


class UraseListView(ListView):
    model = AnaliseUrase
    template_name = "app/lista_urase.html"
    context_object_name = "analises"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_farelo"] = self.get_queryset().filter(tipo_amostra="FL").count()
        return context

    def get_queryset(self):
        return AnaliseUrase.objects.all().order_by("-data", "-horario")
