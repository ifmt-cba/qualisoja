from django import forms
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, AnaliseUrase
from django.utils import timezone
from django.core.exceptions import ValidationError


class AnaliseUmidadeForm(forms.ModelForm):
    class Meta:
        model = AnaliseUmidade
        fields = "__all__"
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "horario": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        resultado = cleaned_data.get("resultado")
        if resultado is not None and (resultado < 0 or resultado > 100):
            self.add_error(
                "resultado", "O valor da umidade deve estar entre 0% e 100%."
            )
        return cleaned_data


class AnaliseProteinaForm(forms.ModelForm):
    class Meta:
        model = AnaliseProteina
        exclude = ["resultado", "resultado_corrigido"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "horario": forms.TimeInput(attrs={"type": "time"}),
        }
        help_texts = {
            "peso_amostra": "Informe o peso da amostra em gramas (ex: 0.5 para 0,5g ou 1.00 para 1g)",
            "ml_gasto": "Informe o volume de titulante gasto em mL",
            "ml_branco": "Informe o valor do branco em mL (entre 0 e 0,5)",
            "normalidade": "O valor máximo de normalidade é 0.3 N.",
        }

    def __init__(self, *args, **kwargs):
        """
        Torna os campos de análise não obrigatórios no nível do formulário.
        A obrigatoriedade será validada no método clean() dependendo do tipo_amostra.
        """
        super().__init__(*args, **kwargs)
        self.fields["peso_amostra"].required = False
        self.fields["ml_gasto"].required = False
        self.fields["ml_branco"].required = False
        self.fields["normalidade"].required = False

    def clean(self):
        from decimal import Decimal

        cleaned_data = super().clean()
        tipo_amostra = cleaned_data.get("tipo_amostra")

        # Se for um caso especial, não há mais validações a fazer.
        if tipo_amostra in ["FP", "SA"]:
            return cleaned_data

        # Para análises normais, os campos são obrigatórios.
        peso_amostra = cleaned_data.get("peso_amostra")
        ml_gasto = cleaned_data.get("ml_gasto")
        ml_branco = cleaned_data.get("ml_branco")
        normalidade = cleaned_data.get("normalidade")

        # Validação de obrigatoriedade
        if not peso_amostra:
            self.add_error("peso_amostra", "Este campo é obrigatório.")
        if not ml_gasto:
            self.add_error("ml_gasto", "Este campo é obrigatório.")
        if not ml_branco:
            self.add_error("ml_branco", "Este campo é obrigatório.")
        if not normalidade:
            self.add_error("normalidade", "Este campo é obrigatório.")

        # Se algum campo obrigatório estiver faltando, não continue com as outras validações.
        if self.errors:
            return cleaned_data

        # Validação de faixas de valores
        if normalidade <= 0:
            self.add_error("normalidade", "A normalidade deve ser um valor positivo.")
        elif normalidade > Decimal("0.3"):
            self.add_error("normalidade", "O valor máximo para a normalidade é 0.3 N.")
        if peso_amostra <= 0 or peso_amostra > 100:
            self.add_error(
                "peso_amostra", "O peso da amostra deve estar entre 0,01g e 100g."
            )
        if ml_gasto <= 0 or ml_gasto > 100:
            self.add_error(
                "ml_gasto", "O volume da amostra deve estar entre 0,01mL e 100mL."
            )
        if ml_branco < 0 or ml_branco > 0.5:
            self.add_error(
                "ml_branco", "O valor do branco deve estar entre 0 e 0,5 mL."
            )
        return cleaned_data


class AnaliseOleoDegomadoForm(forms.ModelForm):
    class Meta:
        model = AnaliseOleoDegomado
        fields = "__all__"
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "horario": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Melhora a experiência do usuário no frontend, restringindo o
        date-picker do navegador para apenas a data de hoje.
        """
        super().__init__(*args, **kwargs)
        today_iso = timezone.localdate().isoformat()
        # Restringe o calendário no frontend para não permitir seleção de datas passadas ou futuras
        self.fields["data"].widget.attrs["min"] = today_iso
        self.fields["data"].widget.attrs["max"] = today_iso

    def clean_data(self):
        """
        Validação de backend que garante que a data da análise seja exatamente a data de hoje.
        Isso complementa o validador do modelo, que já impede datas futuras.
        """
        data = self.cleaned_data.get("data")
        hoje = timezone.localdate()
        if data and data != hoje:
            raise ValidationError("A data da análise deve ser a data de hoje.")
        return data

    def clean(self):
        """
        Validações customizadas para o formulário de Óleo Degomado.
        O método anterior foi removido pois estava validando campos que não existem mais no modelo.
        As validações de MinValueValidator e MaxValueValidator nos campos do modelo
        já cuidam das faixas de valores básicos.
        """
        cleaned_data = super().clean()

        tipo_analise = cleaned_data.get("tipo_analise")
        peso_amostra = cleaned_data.get("peso_amostra")
        liquido = cleaned_data.get("liquido")
        resultado = cleaned_data.get("resultado")
        # acidez = cleaned_data.get('acidez')
        titulacao = cleaned_data.get("titulacao")
        fator_correcao = cleaned_data.get("fator_correcao")

        if tipo_analise == "UMI":
            if peso_amostra is not None and not (5 <= peso_amostra <= 5.5):
                self.add_error(
                    "peso_amostra",
                    "Para análise de umidade, o peso da amostra deve estar entre 5 e 5,5.",
                )
            if liquido is not None and not (0 <= liquido <= 100):
                self.add_error(
                    "liquido",
                    "Para análise de umidade, o valor do líquido deve estar entre 0 e 100.",
                )
            if titulacao is not None and not (0 <= titulacao <= 100):
                self.add_error(
                    "titulacao",
                    "Para análise de umidade, o valor da Titulação deve estar entre 0 e 100.",
                )

        if tipo_analise == "ACI":
            if peso_amostra is not None and not (7 <= peso_amostra <= 7.5):
                self.add_error(
                    "peso_amostra",
                    "Para análise de Acidez, o peso da amostra deve estar entre 7 e 7,5.",
                )
            if titulacao is not None and not (0 <= titulacao <= 100):
                self.add_error(
                    "titulacao",
                    "Para análise de Acidez, o valor da Titulação deve estar entre 0 e 100.",
                )
            if fator_correcao is not None and not (0 < fator_correcao <= 1):
                self.add_error(
                    "fator_correcao",
                    "Para análise de Acidez, o valor de Fator de Correção deve estar entre 0,1 à 1,0.",
                )

        if tipo_analise == "SAB":
            if peso_amostra is not None and not (10 <= peso_amostra <= 10.5):
                self.add_error(
                    "peso_amostra",
                    "Para análise de Sabões, o peso da amostra deve estar entre 10 à 10,5.",
                )
            if titulacao is not None and not (0 <= titulacao <= 100):
                self.add_error(
                    "titulacao",
                    "Para análise de Sabões, o valor da Titulação deve estar entre 0 e 100.",
                )
            if fator_correcao is not None and not (0.01 <= fator_correcao <= 0.1):
                self.add_error(
                    "fator_correcao",
                    "Para análise de Sabões, o valor de Fator de Correção deve estar entre 0,01 à 0,1.",
                )

        if resultado is not None and not (0 <= resultado <= 100):
            self.add_error(
                "resultado", "O valor do resultado deve estar entre 0% e 100%."
            )

        # if acidez is not None and acidez < 0:
        #     self.add_error('acidez', 'A acidez não pode ser negativa.')

        return cleaned_data


class AnaliseUraseForm(forms.ModelForm):
    class Meta:
        model = AnaliseUrase
        fields = "__all__"
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "horario": forms.TimeInput(attrs={"type": "time"}),
            "amostra_1": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Digite o valor da Amostra 1"}
            ),
            "amostra_2": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Digite o valor da Amostra 2"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        amostra_1 = cleaned_data.get("amostra_1")
        amostra_2 = cleaned_data.get("amostra_2")
        if amostra_1 is None or amostra_2 is None:
            raise forms.ValidationError("Ambas as amostras são obrigatórias.")
        if amostra_1 < 0:
            self.add_error("amostra_1", "O valor da Amostra 1 não pode ser negativo.")
        if amostra_2 < 0:
            self.add_error("amostra_2", "O valor da Amostra 2 não pode ser negativo.")
        if amostra_1 > 1000:
            self.add_error("amostra_1", "O valor da Amostra 1 parece muito alto.")
        if amostra_2 > 1000:
            self.add_error("amostra_2", "O valor da Amostra 2 parece muito alto.")

        return cleaned_data
