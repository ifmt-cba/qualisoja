import datetime
from django import forms
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, AnaliseUrase, AnaliseCinza, AnaliseTeorOleo, AnaliseFibra, AnaliseFosforo
from django.utils import timezone  # Use o timezone do Django, não o datetime padrão

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
            self.add_error('resultado', 'O valor da umidade deve estar entre 0% e 100%.')
        
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
            self.add_error('resultado', 'O valor da proteína deve estar entre 0% e 100%.')
        
        # Verificar se resultado_corrigido está dentro de limites razoáveis
        resultado_corrigido = cleaned_data.get('resultado_corrigido')
        if resultado_corrigido is not None and (resultado_corrigido < 0 or resultado_corrigido > 100):
            self.add_error('resultado_corrigido', 'O valor corrigido da proteína deve estar entre 0% e 100%.')
        
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
            if peso_amostra is not None and not (7 <= peso_amostra <= 7.5):
                self.add_error('peso_amostra', 'Para análise de umidade, o peso da amostra deve estar entre 7 e 7,5.')
            if liquido is not None and not (0 <= liquido <= 100):
                self.add_error('liquido', 'Para análise de umidade, o valor do líquido deve estar entre 0 e 100.')
            if titulacao is not None and not (0 <= titulacao <= 100):    
                self.add_error('titulacao', 'Para análise de umidade, o valor da Titulação deve estar entre 0 e 100.')
        
        if tipo_analise == 'ACI':
            if peso_amostra is not None and not (7 <= peso_amostra <= 7.5):
                self.add_error('peso_amostra', 'Para análise de Acidez, o peso da amostra deve estar entre 7 e 7,5.')
            if titulacao is not None and not (0 <= titulacao <= 100):    
                self.add_error('titulacao', 'Para análise de Acidez, o valor da Titulação deve estar entre 0 e 100.')
            if fator_correcao is not None and not (0 < fator_correcao <= 1):
                self.add_error('fator_correcao', 'Para análise de Acidez, o valor de Fator de Correção deve estar entre 0,1 à 1,0.')


        if tipo_analise == 'SAB':
            if peso_amostra is not None and not (10 <= peso_amostra <= 10.5):
                self.add_error('peso_amostra', 'Para análise de Sabões, o peso da amostra deve estar entre 10 à 10,5.')
            if titulacao is not None and not (0 <= titulacao <= 100):    
                self.add_error('titulacao', 'Para análise de Sabões, o valor da Titulação deve estar entre 0 e 100.')
            if fator_correcao is not None and not (0.01 < fator_correcao <= 0.1):
                self.add_error('fator_correcao', 'Para análise de Sabões, o valor de Fator de Correção deve estar entre 0,01 à 0,1.')
        
        if resultado is not None and not (0 <= resultado <= 100):
            self.add_error('resultado', 'O valor do resultado deve estar entre 0% e 100%.')
        
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
            self.add_error('amostra_1', 'O valor da Amostra 1 não pode ser negativo.')
        
        if amostra_2 < 0:
            self.add_error('amostra_2', 'O valor da Amostra 2 não pode ser negativo.')
        
        # Validar se os valores são razoáveis
        if amostra_1 > 1000:
            self.add_error('amostra_1', 'O valor da Amostra 1 parece muito alto.')
        
        if amostra_2 > 1000:
            self.add_error('amostra_2', 'O valor da Amostra 2 parece muito alto.')
        
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
            self.add_error('resultado', 'O teor de cinza deve estar entre 0% e 10%.')
        
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
        peso_liquido = cleaned_data.get('peso_liquido')
        teor_oleo = cleaned_data.get('teor_oleo')
        
        # Validar peso da amostra
        if peso_amostra is not None:
            if not (2.000 <= float(peso_amostra) <= 2.500):
                self.add_error('peso_amostra', 'O peso da amostra deve estar entre 2,000 g e 2,500 g.')
        
        # Validar peso líquido
        if peso_liquido is not None and peso_amostra is not None:
            if peso_liquido > peso_amostra:
                self.add_error('peso_liquido', 'O peso líquido não pode ser maior que o peso da amostra.')
            if peso_liquido < 0:
                self.add_error('peso_liquido', 'O peso líquido não pode ser negativo.')
        
        # Validar teor de óleo (se fornecido manualmente)
        if teor_oleo is not None and (teor_oleo < -100 or teor_oleo > 25):
            self.add_error('teor_oleo', 'O teor de óleo deve estar entre -100% e 25%.')
        
        return cleaned_data


class AnaliseFibraForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de fibra.
    """
    class Meta:
        model = AnaliseFibra
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        """Validação específica do formulário de fibra"""
        cleaned_data = super().clean()
        
        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 15):
            self.add_error('resultado', 'O teor de fibra deve estar entre 0% e 15%.')
        
        return cleaned_data


class AnaliseFosforoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de análises de fósforo.
    """
    class Meta:
        model = AnaliseFosforo
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        """Validação específica do formulário de fósforo"""
        cleaned_data = super().clean()
        
        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 2):
            self.add_error('resultado', 'O teor de fósforo deve estar entre 0% e 2%.')
        
        return cleaned_data