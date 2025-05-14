from django import forms
from .models import AnaliseUmidade, AnaliseProteina

class AnaliseUmidadeForm(forms.ModelForm):
    class Meta:
        model = AnaliseUmidade
        fields = '__all__'

class AnaliseProteinaForm(forms.ModelForm):
    class Meta:
        model = AnaliseProteina
        fields = '__all__'
