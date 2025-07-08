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
            # Busca a umidade da mesma data e tipo de amostra, a mais recente por horário
            umidade_obj = (
                AnaliseUmidade.objects.filter(
                    data=proteina.data, tipo_amostra=proteina.tipo_amostra
                )
                .order_by("-horario")
                .first()
            )

            umidade_valor = umidade_obj.resultado if umidade_obj else None

            proteina.calcular_proteina(umidade_valor)
        else:
            # Garante que os resultados sejam nulos para "Fábrica parada" e "Sem amostra"
            proteina.resultado = None
            proteina.resultado_corrigido = None

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
        titulacao = form.cleaned_data["titulacao"]
        fator_correcao = form.cleaned_data["fator_correcao"]
        peso_amostra = form.cleaned_data["peso_amostra"]
        tipo_analise = form.cleaned_data["tipo_analise"]  # corrigido typo aqui
        tara = form.cleaned_data["tara"]
        liquido = form.cleaned_data["liquido"]

        if tipo_analise == "UMI":
            if tara and fator_correcao and peso_amostra:
                resultado = ((tara + peso_amostra) - liquido) / peso_amostra * 100

        elif tipo_analise == "ACI":
            if titulacao and fator_correcao and peso_amostra:
                resultado = (
                    titulacao * fator_correcao * Decimal("28.2") * Decimal("100")
                ) / peso_amostra

        elif tipo_analise == "SAB":
            if titulacao and fator_correcao and peso_amostra:
                resultado = (
                    titulacao * fator_correcao * Decimal("300.4") * Decimal("100")
                ) / peso_amostra
        else:
            resultado = None

        form.instance.resultado = resultado
        return super().form_valid(form)


class UmidadeListView(ListView):
    model = AnaliseUmidade
    template_name = "app/lista_umidade.html"


class ProteinaListView(ListView):
    model = AnaliseProteina
    template_name = "app/lista_proteina.html"

    def get_queryset(self):
        from django.db.models import OuterRef, Subquery

        umidade_subquery = (
            AnaliseUmidade.objects.filter(
                data=OuterRef("data"), tipo_amostra=OuterRef("tipo_amostra")
            )
            .order_by("-horario")
            .values("resultado")[:1]
        )

        return AnaliseProteina.objects.annotate(
            umidade=Subquery(umidade_subquery)
        ).order_by("-data", "-horario")


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
