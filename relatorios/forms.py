import datetime
from django import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Cliente, EspecificacaoContrato, Lote, RelatorioExpedicao


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

class RelatorioExpedicaoForm(forms.ModelForm):
    """Formulário para gerar relatórios de expedição baseados em análises selecionadas."""
    
    PARAMETROS_CHOICES = [
        ('umidade', 'Umidade'),
        ('proteina', 'Proteína'),
        ('oleo', 'Óleo Degomado'),
        ('acidez', 'Acidez'),
        ('indice_sabao', 'Índice de Sabão'),
        ('silica', 'Sílica'),
        ('fosforo', 'Fósforo'),
        ('urase', 'Urase'),
        ('teor_oleo', 'Teor de Óleo'),
        ('fibra', 'Fibra'),
        ('cinza', 'Cinza'),
    ]
    
    # Parâmetros obrigatórios para cada tipo de análise
    PARAMETROS_OBRIGATORIOS_OLEO = ['umidade', 'acidez', 'indice_sabao', 'silica', 'fosforo', 'urase']
    PARAMETROS_OBRIGATORIOS_FARELO = ['umidade', 'proteina', 'teor_oleo']

    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('HTML', 'Visualização Online'),
    ]
    
    PERIODO_CHOICES = [
        ('7', 'Últimos 7 dias'),
        ('15', 'Últimos 15 dias'),
        ('30', 'Último mês'),
        ('custom', 'Período personalizado'),
    ]
    
    TIPO_ANALISE_CHOICES = [
        ('auto', 'Detectar automaticamente'),
        ('oleo', 'Análise de Óleo'),
        ('farelo', 'Análise de Farelo'),
        ('ambos', 'Ambos os tipos'),
    ]
    
    # Seleção de período
    periodo_predefinido = forms.ChoiceField(
        choices=PERIODO_CHOICES,
        initial='7',
        required=False,
        label="Período das Análises",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleCustomPeriod()'})
    )
    
    # Tipo de análise
    tipo_analise = forms.ChoiceField(
        choices=TIPO_ANALISE_CHOICES,
        initial='auto',
        required=True,
        label="Tipo de Análise",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'updateParametrosObrigatorios()'})
    )

    # Opção de usar cliente cadastrado ou digitar manualmente
    usar_cliente_cadastrado = forms.BooleanField(
        required=False,
        initial=True,
        label="Usar cliente cadastrado",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'onchange': 'toggleClienteFields()'})
    )
    
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(ativo=True),
        empty_label="Selecione um cliente",
        required=False,
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'updateContratos()'})
    )
    
    cliente_nome_manual = forms.CharField(
        max_length=200,
        required=False,
        label="Nome do Cliente",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do cliente'})
    )
    
    # Opção de usar contrato cadastrado ou digitar manualmente
    usar_contrato_cadastrado = forms.BooleanField(
        required=False,
        initial=False,
        label="Usar contrato cadastrado",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'onchange': 'toggleContratoFields()'})
    )
    
    contrato = forms.ModelChoiceField(
        queryset=EspecificacaoContrato.objects.none(),
        empty_label="Selecione um contrato",
        required=False,
        label="Contrato",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    contrato_nome_manual = forms.CharField(
        max_length=100,
        required=False,
        label="Nome do Contrato",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do contrato'})
    )
    
    contrato_numero_manual = forms.CharField(
        max_length=50,
        required=False,
        label="Número do Contrato",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número do contrato'})
    )
    
    parametros_incluidos = forms.MultipleChoiceField(
        choices=PARAMETROS_CHOICES,
        required=False,
        label="Parâmetros Adicionais (parâmetros obrigatórios são incluídos automaticamente)",
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text="Os parâmetros obrigatórios são determinados pelo tipo de análise (óleo ou farelo) e incluídos automaticamente"
    )
    
    data_inicial = forms.DateField(
        required=False,
        label="Data Inicial (apenas para período personalizado)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=datetime.date.today() - datetime.timedelta(days=7)
    )
    
    data_final = forms.DateField(
        required=False,
        label="Data Final (apenas para período personalizado)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=datetime.date.today()
    )
    
    formato = forms.ChoiceField(
        choices=FORMATO_CHOICES,
        initial='PDF',
        required=True,
        label="Formato de Saída",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    observacoes_manuais = forms.CharField(
        required=False,
        label="Observações Manuais",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Adicione observações específicas para este relatório...'
        })
    )
    
    incluir_graficos = forms.BooleanField(
        required=False,
        initial=True,
        label="Incluir Gráficos Comparativos",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    incluir_certificacao = forms.BooleanField(
        required=False,
        initial=True,
        label="Incluir Certificação de Conformidade (se aplicável)",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = RelatorioExpedicao
        fields = ['cliente', 'cliente_nome_manual', 'contrato', 'contrato_nome_manual', 
                 'contrato_numero_manual', 'tipo_analise', 'data_inicial', 'data_final', 
                 'parametros_incluidos', 'formato', 'observacoes_manuais']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se um cliente foi selecionado, filtrar contratos
        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['contrato'].queryset = EspecificacaoContrato.objects.filter(
                    cliente_id=cliente_id, ativo=True
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.cliente:
            self.fields['contrato'].queryset = EspecificacaoContrato.objects.filter(
                cliente=self.instance.cliente, ativo=True
            )
    
    def _obter_periodo_analises(self, periodo_predefinido, data_inicial, data_final):
        """Determina o período das análises baseado na seleção do usuário."""
        from datetime import date, timedelta
        
        if periodo_predefinido == 'custom':
            if not data_inicial or not data_final:
                raise forms.ValidationError("Para período personalizado, informe data inicial e final.")
            return data_inicial, data_final
        
        data_fim = date.today()
        if periodo_predefinido == '7':
            data_inicio = data_fim - timedelta(days=7)
        elif periodo_predefinido == '15':
            data_inicio = data_fim - timedelta(days=15)
        elif periodo_predefinido == '30':
            data_inicio = data_fim - timedelta(days=30)
        else:
            data_inicio = data_fim - timedelta(days=7)  # padrão
        
        return data_inicio, data_fim
    
    def _detectar_tipo_analise_automatico(self, data_inicial, data_final):
        """Detecta automaticamente o tipo de análise baseado nas análises disponíveis no período."""
        from analises.models import AnaliseProteina, AnaliseTeorOleo, AnaliseOleoDegomado, AnaliseUrase
        
        # Verificar análises típicas de farelo
        tem_proteina = AnaliseProteina.objects.filter(
            data__gte=data_inicial, data__lte=data_final
        ).exists()
        tem_teor_oleo = AnaliseTeorOleo.objects.filter(
            data__gte=data_inicial, data__lte=data_final
        ).exists()
        
        # Verificar análises típicas de óleo
        tem_oleo_degomado = AnaliseOleoDegomado.objects.filter(
            data__gte=data_inicial, data__lte=data_final
        ).exists()
        tem_urase = AnaliseUrase.objects.filter(
            data__gte=data_inicial, data__lte=data_final
        ).exists()
        
        if tem_proteina and tem_teor_oleo:
            return 'farelo'
        elif tem_oleo_degomado or tem_urase:
            return 'oleo'
        elif tem_proteina or tem_teor_oleo:
            return 'farelo'
        elif tem_oleo_degomado:
            return 'oleo'
        else:
            return 'oleo'  # padrão
    
    def _get_parametros_obrigatorios_por_tipo(self, tipo_analise):
        """Retorna os parâmetros obrigatórios baseados no tipo de análise."""
        if tipo_analise == 'farelo':
            return self.PARAMETROS_OBRIGATORIOS_FARELO
        elif tipo_analise == 'ambos':
            # Para ambos, usar união dos parâmetros
            return list(set(self.PARAMETROS_OBRIGATORIOS_OLEO + self.PARAMETROS_OBRIGATORIOS_FARELO))
        else:
            return self.PARAMETROS_OBRIGATORIOS_OLEO
    
    def clean(self):
        cleaned_data = super().clean()
        periodo_predefinido = cleaned_data.get('periodo_predefinido', '7')
        data_inicial = cleaned_data.get('data_inicial')
        data_final = cleaned_data.get('data_final')
        tipo_analise = cleaned_data.get('tipo_analise', 'auto')
        usar_cliente_cadastrado = cleaned_data.get('usar_cliente_cadastrado')
        cliente = cleaned_data.get('cliente')
        cliente_nome_manual = cleaned_data.get('cliente_nome_manual')
        
        # Determinar período das análises
        try:
            data_inicio, data_fim = self._obter_periodo_analises(periodo_predefinido, data_inicial, data_final)
            cleaned_data['data_inicial'] = data_inicio
            cleaned_data['data_final'] = data_fim
        except forms.ValidationError as e:
            raise e
        
        # Validar cliente
        if usar_cliente_cadastrado and not cliente:
            raise forms.ValidationError("Selecione um cliente cadastrado ou desmarque a opção.")
        
        if not usar_cliente_cadastrado and not cliente_nome_manual:
            raise forms.ValidationError("Digite o nome do cliente ou selecione um cliente cadastrado.")
        
        # Determinar tipo de análise
        if tipo_analise == 'auto':
            tipo_analise_final = self._detectar_tipo_analise_automatico(data_inicio, data_fim)
        else:
            tipo_analise_final = tipo_analise
        
        # Verificar se há análises no período
        from analises.models import (
            AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado,
            AnaliseFosforo, AnaliseTeorOleo, AnaliseFibra, AnaliseCinza,
            AnaliseUrase, AnaliseSilica
        )
        
        total_analises = sum([
            AnaliseUmidade.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseProteina.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseOleoDegomado.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseFosforo.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseTeorOleo.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseFibra.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseCinza.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseUrase.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
            AnaliseSilica.objects.filter(data__gte=data_inicio, data__lte=data_fim).count(),
        ])
        
        if total_analises == 0:
            raise forms.ValidationError(f"Nenhuma análise encontrada no período de {data_inicio} a {data_fim}.")
        
        # Determinar parâmetros obrigatórios
        parametros_obrigatorios = self._get_parametros_obrigatorios_por_tipo(tipo_analise_final)
        
        # Adicionar parâmetros obrigatórios automaticamente
        parametros_incluidos = cleaned_data.get('parametros_incluidos', [])
        parametros_completos = list(set(parametros_obrigatorios + parametros_incluidos))
        cleaned_data['parametros_incluidos'] = parametros_completos
        cleaned_data['parametros_obrigatorios'] = parametros_obrigatorios
        cleaned_data['tipo_analise_detectado'] = tipo_analise_final
        cleaned_data['total_analises_encontradas'] = total_analises
        
        return cleaned_data

class FiltroRelatorioExpedicaoForm(forms.Form):
    """Formulário simplificado para filtros rápidos de relatórios de expedição."""
    
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(ativo=True),
        empty_label="Todos os clientes",
        required=False,
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Todos os status')] + RelatorioExpedicao.STATUS_CHOICES,
        required=False,
        label="Status",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    data_inicial = forms.DateField(
        required=False,
        label="Data Inicial",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    data_final = forms.DateField(
        required=False,
        label="Data Final",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

class EnvioRelatorioForm(forms.Form):
    """Formulário para envio de relatórios por e-mail."""
    
    destinatarios = forms.CharField(
        required=True,
        label="Destinatários",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'email1@exemplo.com, email2@exemplo.com'
        }),
        help_text="Separe múltiplos e-mails por vírgula"
    )
    
    assunto = forms.CharField(
        required=True,
        label="Assunto",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    mensagem = forms.CharField(
        required=False,
        label="Mensagem",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Mensagem adicional (opcional)...'
        })
    )
    
    def clean_destinatarios(self):
        destinatarios = self.cleaned_data['destinatarios']
        emails = [email.strip() for email in destinatarios.split(',')]
        
        # Validar cada e-mail
        import re
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        emails_validos = []
        for email in emails:
            if email and email_regex.match(email):
                emails_validos.append(email)
            elif email:  # Se não está vazio mas é inválido
                raise forms.ValidationError(f"E-mail inválido: {email}")
        
        if not emails_validos:
            raise forms.ValidationError("Pelo menos um e-mail válido deve ser fornecido.")
        
        return emails_validos
