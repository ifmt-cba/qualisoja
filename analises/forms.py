import datetime
from django import forms
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado
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
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        """Validação específica do formulário de óleo degomado"""
        cleaned_data = super().clean()
        
        # Verificar se resultado está dentro de limites razoáveis
        resultado = cleaned_data.get('resultado')
        if resultado is not None and (resultado < 0 or resultado > 100):
            self.add_error('resultado', 'O valor do resultado deve estar entre 0% e 100%.')
        
        # Verificar acidez
        acidez = cleaned_data.get('acidez')
        if acidez is not None and acidez < 0:
            self.add_error('acidez', 'A acidez não pode ser negativa.')
        
        return cleaned_data