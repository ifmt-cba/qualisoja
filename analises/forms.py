import datetime
from django import forms
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado
from django.utils import timezone  # Use o timezone do Django, não o datetime padrão
from django.core.exceptions import ValidationError
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
    
    #impede que o usuario acesse datas posteriores a de hoje 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = localdate()  # Usa o fuso horário configurado no Django
        self.fields['data'].widget.attrs['min'] = today.isoformat()


    
    #metodo que impede de adicionar datas diferentes da de hj
    def clean_data(self):
            data = self.cleaned_data.get('data')
            hoje = timezone.localdate()
            if data and data < hoje:
                raise ValidationError('A data não pode ser anterior/posterior à data HOJE.')
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
                self.add_error('peso_amostra', 'Para análise de umidade, o peso da amostra deve estar entre 5 e 5,5.')
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
    
    