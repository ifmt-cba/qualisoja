import datetime
from django import forms
from .models import AnaliseUmidade, AnaliseProteina
from django.utils import timezone  # Use o timezone do Django, não o datetime padrão
import datetime  # Para usar timedelta

class AnaliseUmidadeForm(forms.ModelForm):
    class Meta:
        model = AnaliseUmidade
        fields = '__all__'

class AnaliseProteinaForm(forms.ModelForm):
    class Meta:
        model = AnaliseProteina
        fields = '__all__'

class RelatorioFiltroForm(forms.Form):
    data_inicial = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.localdate  # Correto: usando timezone.localdate do Django
    )
    data_final = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.localdate  # Correto: usando timezone.localdate do Django
    )
    
    OPCOES_RELATORIO = [
        ('umidade', 'Relatório de Umidade'),
        ('proteina', 'Relatório de Proteína'),
        ('completo', 'Relatório Completo')
    ]
    
    tipo_relatorio = forms.ChoiceField(
        choices=OPCOES_RELATORIO,
        initial='completo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_amostra_umidade = forms.ChoiceField(
        choices=[('', 'Todos')] + list(AnaliseUmidade.TIPO_AMOSTRA_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_amostra_proteina = forms.ChoiceField(
        choices=[('', 'Todos')] + list(AnaliseProteina.TIPO_AMOSTRA_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Adicione estas opções para personalizar a exportação
    FORMATO_CHOICES = [
        ('HTML', 'Visualizar no navegador'),
        ('PDF', 'Exportar como PDF'),
        ('EXCEL', 'Exportar como Excel'),
    ]
    
    formato_saida = forms.ChoiceField(
        choices=FORMATO_CHOICES,
        required=True,
        initial='HTML',
        widget=forms.RadioSelect()
    )