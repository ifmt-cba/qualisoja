import datetime
from django import forms


class RelatorioFiltroForm(forms.Form):
    """Formulário para filtrar relatórios"""
    
    TIPO_RELATORIO_CHOICES = [
        ('umidade', 'Relatório de Umidade'),
        ('proteina', 'Relatório de Proteína'),
        ('oleo_degomado', 'Análise do Óleo Degomado'),
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
    
    tipo_amostra_oleo_degomado = forms.CharField(
        required=False,
        label='Tipo de Amostra (Óleo Degomado)'
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
