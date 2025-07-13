import datetime
from django import forms
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, AnaliseUrase, AnaliseCinza, AnaliseTeorOleo, AnaliseFibra, AnaliseFosforo, AnaliseSilica
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localdate


class AnaliseUmidadeForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de umidade.
    """
    class Meta:
        model = AnaliseUmidade
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        """Validação específica do formulário de umidade"""
        cleaned_data = super().clean()

        # Verificar se resultado está dentro de limites razoáveis
        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 100):
            self.add_error(
                'resultado', 'O valor da umidade deve estar entre 0% e 100%.')

        return cleaned_data


class AnaliseProteinaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de proteína.
    """
    class Meta:
        model = AnaliseProteina
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        """Validação específica do formulário de proteína"""
        cleaned_data = super().clean()

        # Verificar se resultado está dentro de limites razoáveis
        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 100):
            self.add_error(
                'resultado', 'O valor da proteína deve estar entre 0% e 100%.')

        # Verificar se resultado_corrigido está dentro de limites razoáveis
        resultado_corrigido = cleaned_data.get('resultado_corrigido')
        if resultado_corrigido is not None and (resultado_corrigido < 0 or resultado_corrigido > 100):
            self.add_error(
                'resultado_corrigido', 'O valor corrigido da proteína deve estar entre 0% e 100%.')

        return cleaned_data

# class AnaliseOleoDegomadoForm(forms.ModelForm):
#     """
#     Formulário para cadastro e edição de análises de óleo degomado.
#     """
#     class Meta:
#         model = AnaliseOleoDegomado
#         fields = '__all__'
#         widgets = {
#             'data': forms.DateInput(attrs={'type': 'date'}),
#             'horario': forms.TimeInput(attrs={'type': 'time'}),
#             # 'observacoes': forms.Textarea(attrs={'rows': 3}),
#         }

#     def clean(self):
#         """Validação específica do formulário de óleo degomado"""
#         cleaned_data = super().clean()

#         tipo_analise = cleaned_data.get('tipo_analise')
#         peso_amostra = cleaned_data.get('peso_amostra')
#         if tipo_analise == "UMI":
#             if peso_amostra is not None and not (7 <= peso_amostra <= 7.5):
#                 self.add_error('peso_amostra', 'Para análise de umidade, o peso da amostra deve estar entre 7 e 7,5.')
#             # if peso_amostra is not None and (7 <= peso_amostra <= 7.5):
#             #      self.add_error('peso_amostra', 'Para análise de umidade, o peso da amostra deve estar entre 7 e 7,5.')


#         # Verificar se resultado está dentro de limites razoáveis
#         resultado = cleaned_data.get('resultado')
#         if resultado is not None and (resultado < 0 or resultado > 100):
#             self.add_error('resultado', 'O valor do resultado deve estar entre 0% e 100%.')

#         # Verificar acidez
#         acidez = cleaned_data.get('acidez')
#         if acidez is not None and acidez < 0:
#             self.add_error('acidez', 'A acidez não pode ser negativa.')

#         return cleaned_data


class AnaliseOleoDegomadoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de óleo degomado.
    """
    class Meta:
        model = AnaliseOleoDegomado
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = localdate()  # Usa o fuso horário configurado no Django
        self.fields['data'].widget.attrs['min'] = today.isoformat()

    def clean_data(self):
        data = self.cleaned_data.get('data')
        hoje = timezone.localdate()  # Usa o fuso horário correto
        if data and data < hoje:
            raise ValidationError('A data não pode ser anterior à data atual.')
        return data

    def clean(self):
        """Validação específica do formulário de óleo degomado"""
        cleaned_data = super().clean()

        tipo_analise = cleaned_data.get('tipo_analise')
        peso_amostra = cleaned_data.get('peso_amostra')
        liquido = cleaned_data.get('liquido')
        resultado = cleaned_data.get('resultado')
        # acidez = cleaned_data.get('acidez')
        titulacao = cleaned_data.get('titulacao')
        fator_correcao = cleaned_data.get('fator_correcao')

        if tipo_analise == "UMI":
            if peso_amostra is not None and not (5 <= peso_amostra <= 5.5):
                self.add_error(
                    'peso_amostra', 'Para análise de umidade, o peso da amostra deve estar entre 5 e 5,5.')
            if liquido is not None and not (0 <= liquido <= 100):
                self.add_error(
                    'liquido', 'Para análise de umidade, o valor do líquido deve estar entre 0 e 100.')
            # if titulacao is not None and not (0 <= titulacao <= 100):
            #     self.add_error('titulacao', 'Para análise de umidade, o valor da Titulação deve estar entre 0 e 100.')

        if tipo_analise == 'ACI':
            if peso_amostra is not None and not (7 <= peso_amostra <= 7.5):
                self.add_error(
                    'peso_amostra', 'Para análise de Acidez, o peso da amostra deve estar entre 7 e 7,5.')
            if titulacao is not None and not (0 <= titulacao <= 100):
                self.add_error(
                    'titulacao', 'Para análise de Acidez, o valor da Titulação deve estar entre 0 e 100.')
            if fator_correcao is not None and not (0 < fator_correcao <= 1):
                self.add_error(
                    'fator_correcao', 'Para análise de Acidez, o valor de Fator de Correção deve estar entre 0,1 à 1,0.')

        if tipo_analise == 'SAB':
            if peso_amostra is not None and not (10 <= peso_amostra <= 10.5):
                self.add_error(
                    'peso_amostra', 'Para análise de Sabões, o peso da amostra deve estar entre 10 à 10,5.')
            if titulacao is not None and not (0 <= titulacao <= 100):
                self.add_error(
                    'titulacao', 'Para análise de Sabões, o valor da Titulação deve estar entre 0 e 100.')
            if fator_correcao is not None and not (0.01 < fator_correcao <= 0.1):
                self.add_error(
                    'fator_correcao', 'Para análise de Sabões, o valor de Fator de Correção deve estar entre 0,01 à 0,1.')

        if resultado is not None and not (0 <= resultado <= 100):
            self.add_error(
                'resultado', 'O valor do resultado deve estar entre 0% e 100%.')

        # if acidez is not None and acidez < 0:
        #     self.add_error('acidez', 'A acidez não pode ser negativa.')

        return cleaned_data


class AnaliseUraseForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de urase.
    """
    class Meta:
        model = AnaliseUrase
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'amostra_1': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Digite o valor da Amostra 1'
            }),
            'amostra_2': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Digite o valor da Amostra 2'
            }),
        }

    def clean(self):
        """Validação específica do formulário de urase"""
        cleaned_data = super().clean()

        amostra_1 = cleaned_data.get('amostra_1')
        amostra_2 = cleaned_data.get('amostra_2')

        # Validar se ambas as amostras foram fornecidas
        if amostra_1 is None or amostra_2 is None:
            raise forms.ValidationError('Ambas as amostras são obrigatórias.')

        # Validar se os valores são positivos
        if amostra_1 < 0:
            self.add_error(
                'amostra_1', 'O valor da Amostra 1 não pode ser negativo.')

        if amostra_2 < 0:
            self.add_error(
                'amostra_2', 'O valor da Amostra 2 não pode ser negativo.')

        # Validar se os valores são razoáveis
        if amostra_1 > 1000:
            self.add_error(
                'amostra_1', 'O valor da Amostra 1 parece muito alto.')

        if amostra_2 > 1000:
            self.add_error(
                'amostra_2', 'O valor da Amostra 2 parece muito alto.')

        return cleaned_data


class AnaliseCinzaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de cinza.
    """
    class Meta:
        model = AnaliseCinza
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        """Validação específica do formulário de cinza"""
        cleaned_data = super().clean()

        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 10):
            self.add_error(
                'resultado', 'O teor de cinza deve estar entre 0% e 10%.')

        return cleaned_data


class AnaliseTeorOleoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de teor de óleo.
    """
    class Meta:
        model = AnaliseTeorOleo
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'peso_amostra': forms.NumberInput(attrs={
                'step': '0.001',
                'min': '2.000',
                'max': '2.500',
                'placeholder': 'Entre 2,000 e 2,500 g'
            }),
            'peso_tara': forms.NumberInput(attrs={
                'step': '0.001',
                'placeholder': 'Peso da tara (recipiente vazio)'
            }),
            'peso_liquido': forms.NumberInput(attrs={
                'step': '0.001',
                'placeholder': 'Peso líquido de óleo'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Observações adicionais sobre a análise...'
            }),
        }

    def clean(self):
        """Validação específica do formulário de teor de óleo"""
        cleaned_data = super().clean()

        peso_amostra = cleaned_data.get('peso_amostra')
        peso_tara = cleaned_data.get('peso_tara')
        peso_liquido = cleaned_data.get('peso_liquido')
        teor_oleo = cleaned_data.get('teor_oleo')

        # Validar peso da amostra
        if peso_amostra is not None:
            if not (2.000 <= float(peso_amostra) <= 2.500):
                self.add_error(
                    'peso_amostra', 'O peso da amostra deve estar entre 2,000 g e 2,500 g.')

        # Validar peso da tara
        if peso_tara is not None:
            if peso_tara <= 0:
                self.add_error(
                    'peso_tara', 'O peso da tara deve ser positivo.')

        # Validar peso líquido
        if peso_liquido is not None:
            if peso_liquido <= 0:
                self.add_error(
                    'peso_liquido', 'O peso líquido deve ser positivo.')
            if peso_tara is not None and peso_liquido < peso_tara:
                self.add_error(
                    'peso_liquido', 'O peso líquido (tara + óleo) deve ser maior que o peso da tara vazia.')

        # Validar teor de óleo (se fornecido manualmente)
        if teor_oleo is not None and (teor_oleo < 0 or teor_oleo > 30):
            self.add_error(
                'teor_oleo', 'O teor de óleo deve estar entre 0% e 30%.')

        return cleaned_data


class AnaliseFibraForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de fibra.
    """
    class Meta:
        model = AnaliseFibra
        fields = ['data', 'horario', 'tipo_amostra', 'peso_amostra',
                  'peso_tara', 'peso_fibra', 'peso_branco', 'resultado']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'peso_amostra': forms.NumberInput(attrs={
                'step': '0.0001',
                'placeholder': 'Peso da amostra'
            }),
            'peso_tara': forms.NumberInput(attrs={
                'step': '0.0001',
                'placeholder': 'Peso da tara (recipiente vazio)'
            }),
            'peso_fibra': forms.NumberInput(attrs={
                'step': '0.0001',
                'placeholder': 'Peso da fibra'
            }),
            'peso_branco': forms.NumberInput(attrs={
                'step': '0.0001',
                'placeholder': 'Peso do branco'
            }),
        }

    def clean(self):
        """Validação específica do formulário de fibra"""
        cleaned_data = super().clean()

        peso_amostra = cleaned_data.get('peso_amostra')
        peso_tara = cleaned_data.get('peso_tara')
        peso_fibra = cleaned_data.get('peso_fibra')
        peso_branco = cleaned_data.get('peso_branco')

        # Validações lógicas para análise de fibra
        # O peso da fibra não pode ser maior que o peso da tara
        if peso_fibra is not None and peso_tara is not None:
            if peso_fibra > peso_tara:
                self.add_error(
                    'peso_fibra', 'O peso da fibra não pode ser maior que o peso da tara.')

        # O peso do branco não pode ser maior que o peso da tara
        if peso_branco is not None and peso_tara is not None:
            if peso_branco > peso_tara:
                self.add_error(
                    'peso_branco', 'O peso do branco não pode ser maior que o peso da tara.')

        # A soma de peso_fibra + peso_branco não pode ser maior que peso_tara
        if peso_fibra is not None and peso_branco is not None and peso_tara is not None:
            if (peso_fibra + peso_branco) > peso_tara:
                self.add_error(
                    'peso_fibra', 'A soma do peso da fibra e peso do branco não pode ser maior que o peso da tara.')

        # Validar se o resultado calculado é razoável (entre 0% e 50%)
        if all([peso_amostra, peso_tara, peso_fibra, peso_branco]):
            resultado_calc = (
                (peso_tara - peso_fibra - peso_branco) / peso_amostra) * 100
            if resultado_calc < 0:
                self.add_error(
                    'peso_tara', 'Os valores informados resultam em um teor de fibra negativo. Verifique os pesos.')
            elif resultado_calc > 50:
                self.add_error(
                    'resultado', 'O teor de fibra calculado é muito alto (>50%). Verifique os valores.')

        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 50):
            self.add_error(
                'resultado', 'O teor de fibra deve estar entre 0% e 50%.')

        return cleaned_data


class AnaliseFosforoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de fósforo.
    Focado na absorbância da amostra, com valores padrão para outros campos.
    """
    class Meta:
        model = AnaliseFosforo
        fields = ['data', 'horario', 'tipo_amostra', 'absorbancia_amostra',
                  'casas_decimais', 'peso_amostra', 'concentracao_padrao', 'volume_solucao',
                  'volume_aliquota', 'absorbancia_padrao']
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'horario': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'tipo_amostra': forms.Select(attrs={
                'class': 'form-select'
            }),
            'absorbancia_amostra': forms.NumberInput(attrs={
                'class': 'form-control campo-principal',
                'step': '0.000001',
                'min': '0.000001',
                'placeholder': 'Ex: 0.125000',
                'style': 'font-size: 1.1rem; font-weight: 600; border: 2px solid #0d6efd;'
            }),
            'casas_decimais': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6',
                'step': '1',
                'style': 'width: 80px;'
            }),
            'peso_amostra': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0001',
                'placeholder': '1.0000'
            }),
            'concentracao_padrao': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0001',
                'placeholder': '10.0000'
            }),
            'volume_solucao': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '100.00'
            }),
            'volume_aliquota': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '10.00'
            }),
            'absorbancia_padrao': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'min': '0.000001',
                'placeholder': '0.250000'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar o campo principal como obrigatório
        self.fields['absorbancia_amostra'].required = True

        # Adicionar classes de destaque
        self.fields['absorbancia_amostra'].widget.attrs.update({
            'autofocus': True,
            'title': 'Campo principal - Digite apenas o valor da absorbância'
        })

    def clean(self):
        """Validação específica do formulário de fósforo"""
        cleaned_data = super().clean()

        # Validar que a absorbância da amostra foi informada
        absorbancia_amostra = cleaned_data.get('absorbancia_amostra')
        if not absorbancia_amostra or absorbancia_amostra <= 0:
            self.add_error(
                'absorbancia_amostra', 'A absorbância da amostra é obrigatória e deve ser maior que zero.')

        return cleaned_data


class AnaliseSilicaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de sílica.
    """
    class Meta:
        model = AnaliseSilica
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'resultado_silica': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Ex: 1.25',
                'class': 'form-control'
            }),
            'analise_cinza': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir hora atual como padrão
        if not self.instance.pk:
            self.fields['horario'].initial = timezone.localtime().time()

        # Filtrar análises de cinza recentes para facilitar seleção
        self.fields['analise_cinza'].queryset = AnaliseCinza.objects.filter(
            data__gte=timezone.now().date() - datetime.timedelta(days=30)
        ).order_by('-data', '-horario')
        self.fields['analise_cinza'].empty_label = "Selecione uma análise de cinza"

    def clean(self):
        """Validação específica do formulário de sílica"""
        cleaned_data = super().clean()

        resultado_silica = cleaned_data.get('resultado_silica')
        analise_cinza = cleaned_data.get('analise_cinza')

        # Validar se o resultado da sílica é positivo
        if resultado_silica and resultado_silica <= 0:
            self.add_error('resultado_silica',
                           'O resultado da sílica deve ser maior que zero.')

        # Validar se a análise de cinza foi selecionada
        if not analise_cinza:
            self.add_error('analise_cinza', 'Selecione uma análise de cinza.')

        return cleaned_data
