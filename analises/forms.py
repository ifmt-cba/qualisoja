import datetime
from django import forms
from .models import AnaliseUmidade, AnaliseProteina
from django.utils import timezone  # Use o timezone do Django, não o datetime padrão
import datetime  # Para usar timedelta

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

class RelatorioFiltroForm(forms.Form):
    """Formulário para filtrar relatórios"""
    
    TIPO_RELATORIO_CHOICES = [
        ('umidade', 'Relatório de Umidade'),
        ('proteina', 'Relatório de Proteína'),
        ('completo', 'Relatório Completo'),
    ]
    
    FORMATO_SAIDA_CHOICES = [
        ('HTML', 'Visualizar no navegador'),
        ('PDF', 'Exportar como PDF'),
        ('EXCEL', 'Exportar como Excel'),
    ]
    
    tipo_relatorio = forms.ChoiceField(
        choices=TIPO_RELATORIO_CHOICES,
        initial='completo',
        required=True,
        label='Tipo de Relatório'
    )
    
    formato_saida = forms.ChoiceField(
        choices=FORMATO_SAIDA_CHOICES,
        initial='HTML',
        required=True,
        label='Formato de Saída'
    )
    
    data_inicial = forms.DateField(
        required=True,
        label='Data Inicial',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today() - datetime.timedelta(days=7)
    )
    
    data_final = forms.DateField(
        required=True,
        label='Data Final',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today()
    )
    
    tipo_amostra_umidade = forms.CharField(
        required=False,
        label='Tipo de Amostra (Umidade)'
    )
    
    tipo_amostra_proteina = forms.CharField(
        required=False,
        label='Tipo de Amostra (Proteína)'
    )
    
    def clean(self):
        """Validar o formulário"""
        cleaned_data = super().clean()
        
        # Validar datas
        data_inicial = cleaned_data.get('data_inicial')
        data_final = cleaned_data.get('data_final')
        
        if data_inicial and data_final and data_inicial > data_final:
            raise forms.ValidationError(
                "A data inicial não pode ser posterior à data final!"
            )
        
        return cleaned_data