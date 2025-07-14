from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class BaseModel(models.Model):
    """
    Modelo base que contém campos e métodos comuns a todos os modelos.
    """
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação", null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização", null=True, blank=True)
    
    class Meta:
        abstract = True

class ConfiguracaoRelatorio(BaseModel):
    """
    Modelo para armazenar configurações de relatórios.
    Permite personalizar como os relatórios são gerados e exibidos.
    """
    TIPO_RELATORIO_CHOICES = [
        ('UMIDADE', 'Relatório de Umidade'),
        ('PROTEINA', 'Relatório de Proteína'),
        ('COMBINADO', 'Relatório Combinado'),
    ]
    
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome do Relatório"
    )
    tipo_relatorio = models.CharField(
        max_length=15,
        choices=TIPO_RELATORIO_CHOICES,
        verbose_name="Tipo de Relatório"
    )
    periodo_padrao = models.IntegerField(
        default=7,
        verbose_name="Período padrão em dias",
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    ativo = models.BooleanField(
        default=True, 
        verbose_name="Relatório Ativo"
    )
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_relatorio_display()})"
    
    class Meta:
        verbose_name = "Configuração de Relatório"
        verbose_name_plural = "Configurações de Relatórios"
        ordering = ['nome']

class Cliente(BaseModel):
    """
    Modelo para armazenar informações dos clientes.
    """
    nome = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código do Cliente")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    logo = models.ImageField(upload_to='clientes/logos/', blank=True, null=True, verbose_name="Logo do Cliente")
    ativo = models.BooleanField(default=True, verbose_name="Cliente Ativo")
    
    def __str__(self):
        return f"{self.nome} ({self.codigo})"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

class EspecificacaoContrato(BaseModel):
    """
    Modelo para armazenar especificações de qualidade por contrato/cliente.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    nome_contrato = models.CharField(max_length=100, verbose_name="Nome do Contrato")
    codigo_contrato = models.CharField(max_length=50, verbose_name="Código do Contrato")
    
    # Especificações de Umidade
    umidade_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Umidade Mínima (%)")
    umidade_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Umidade Máxima (%)")
    
    # Especificações de Proteína
    proteina_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Proteína Mínima (%)")
    proteina_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Proteína Máxima (%)")
    
    # Especificações de Óleo
    oleo_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Óleo Mínimo (%)")
    oleo_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Óleo Máximo (%)")
    
    # Especificações de Fibra
    fibra_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Fibra Mínima (%)")
    fibra_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Fibra Máxima (%)")
    
    # Especificações de Cinza
    cinza_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Cinza Mínima (%)")
    cinza_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Cinza Máxima (%)")
    
    # Especificações de Fósforo
    fosforo_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Fósforo Mínimo (%)")
    fosforo_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Fósforo Máximo (%)")
    
    data_inicio = models.DateField(verbose_name="Data de Início do Contrato")
    data_fim = models.DateField(verbose_name="Data de Fim do Contrato")
    ativo = models.BooleanField(default=True, verbose_name="Contrato Ativo")
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.nome_contrato}"
    
    class Meta:
        verbose_name = "Especificação de Contrato"
        verbose_name_plural = "Especificações de Contratos"
        ordering = ['-data_inicio']

class Lote(BaseModel):
    """
    Modelo para armazenar informações dos lotes de produto.
    """
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código do Lote")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    contrato = models.ForeignKey(EspecificacaoContrato, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Contrato")
    data_producao = models.DateField(verbose_name="Data de Produção")
    quantidade_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade (kg)")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    status = models.CharField(
        max_length=20,
        choices=[
            ('PRODUCAO', 'Em Produção'),
            ('ANALISE', 'Em Análise'),
            ('APROVADO', 'Aprovado'),
            ('REPROVADO', 'Reprovado'),
            ('EXPEDIDO', 'Expedido'),
        ],
        default='PRODUCAO',
        verbose_name="Status"
    )
    
    def __str__(self):
        return f"Lote {self.codigo} - {self.cliente.nome}"
    
    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ['-data_producao']

class RelatorioExpedicao(BaseModel):
    """
    Modelo para armazenar relatórios de expedição gerados.
    """
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('GERADO', 'Gerado'),
        ('ENVIADO', 'Enviado'),
        ('VISUALIZADO', 'Visualizado'),
    ]
    
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('HTML', 'HTML'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código do Relatório")
    
    # Cliente e Contrato podem ser selecionados ou digitados manualmente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cliente")
    cliente_nome_manual = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome do Cliente (Manual)")
    
    contrato = models.ForeignKey(EspecificacaoContrato, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Contrato")
    contrato_nome_manual = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do Contrato (Manual)")
    contrato_numero_manual = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número do Contrato (Manual)")
    
    # Substituir lotes por análises específicas
    # lotes = models.ManyToManyField(Lote, verbose_name="Lotes")  # Deprecated - usar RelatorioAnalise
    
    data_inicial = models.DateField(verbose_name="Data Inicial")
    data_final = models.DateField(verbose_name="Data Final")
    
    # Novo campo para definir o tipo de análise do relatório
    TIPO_ANALISE_CHOICES = [
        ('auto', 'Detectar automaticamente'),
        ('oleo', 'Análise de Óleo'),
        ('farelo', 'Análise de Farelo'),
        ('ambos', 'Ambos os tipos'),
        ('personalizado', 'Seleção personalizada'),
    ]
    
    tipo_analise = models.CharField(
        max_length=15,
        choices=TIPO_ANALISE_CHOICES,
        default='auto',
        verbose_name="Tipo de Análise"
    )
    
    parametros_incluidos = models.JSONField(
        default=list,
        verbose_name="Parâmetros Incluídos",
        help_text="Lista de parâmetros incluídos no relatório"
    )
    
    # Parâmetros obrigatórios na expedição
    parametros_obrigatorios = models.JSONField(
        default=list,
        verbose_name="Parâmetros Obrigatórios",
        help_text="Lista de parâmetros obrigatórios na expedição (sempre incluídos)"
    )
    
    # Análises específicas selecionadas pelo usuário
    analises_selecionadas = models.JSONField(
        default=list,
        verbose_name="Análises Selecionadas",
        help_text="Lista de análises específicas selecionadas pelo usuário"
    )
    
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Responsável")
    data_geracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")
    
    observacoes_automaticas = models.TextField(blank=True, null=True, verbose_name="Observações Automáticas")
    observacoes_manuais = models.TextField(blank=True, null=True, verbose_name="Observações Manuais")
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='RASCUNHO', verbose_name="Status")
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES, default='PDF', verbose_name="Formato")
    
    certificacao_conformidade = models.BooleanField(default=False, verbose_name="Certificação de Conformidade")
    incluir_graficos = models.BooleanField(default=False, verbose_name="Incluir Gráficos Comparativos")
    arquivo_gerado = models.FileField(upload_to='relatorios/expedicao/', blank=True, null=True, verbose_name="Arquivo Gerado")
    
    def __str__(self):
        return f"Relatório {self.codigo} - {self.get_cliente_nome()}"
    
    def get_cliente_nome(self):
        """Retorna o nome do cliente (selecionado ou manual)."""
        if self.cliente:
            return self.cliente.nome
        return self.cliente_nome_manual or "Cliente não informado"
    
    def get_contrato_info(self):
        """Retorna informações do contrato (selecionado ou manual)."""
        if self.contrato:
            return {
                'nome': self.contrato.nome_contrato,
                'numero': self.contrato.codigo_contrato
            }
        return {
            'nome': self.contrato_nome_manual or "Contrato não informado",
            'numero': self.contrato_numero_manual or "N/A"
        }
    
    def get_parametros_completos(self):
        """Retorna todos os parâmetros (obrigatórios + incluídos)."""
        parametros = set(self.parametros_obrigatorios or [])
        parametros.update(self.parametros_incluidos or [])
        return list(parametros)
    
    def get_analises_relacionadas(self):
        """Retorna todas as análises relacionadas a este relatório."""
        return RelatorioAnalise.objects.filter(relatorio=self).order_by('data_analise', 'tipo_analise')
    
    def get_analises_por_tipo(self, tipo_analise):
        """Retorna análises de um tipo específico."""
        return self.get_analises_relacionadas().filter(tipo_analise=tipo_analise)
    
    def adicionar_analise(self, analise_obj, tipo_analise, resultado=None, unidade=None):
        """Adiciona uma análise ao relatório."""
        from django.contrib.contenttypes.models import ContentType
        
        content_type = ContentType.objects.get_for_model(analise_obj)
        
        # Extrair dados da análise
        data_analise = analise_obj.data
        if resultado is None:
            # Tentar obter resultado de diferentes campos possíveis
            resultado = getattr(analise_obj, 'resultado', None) or getattr(analise_obj, 'teor_oleo', None)
        
        relatorio_analise, created = RelatorioAnalise.objects.get_or_create(
            relatorio=self,
            content_type=content_type,
            object_id=analise_obj.id,
            defaults={
                'data_analise': data_analise,
                'tipo_analise': tipo_analise,
                'resultado': resultado,
                'unidade': unidade or '%',
            }
        )
        
        return relatorio_analise
    
    def remover_analise(self, analise_obj):
        """Remove uma análise do relatório."""
        from django.contrib.contenttypes.models import ContentType
        
        content_type = ContentType.objects.get_for_model(analise_obj)
        RelatorioAnalise.objects.filter(
            relatorio=self,
            content_type=content_type,
            object_id=analise_obj.id
        ).delete()
    
    def get_resumo_analises(self):
        """Retorna um resumo das análises incluídas no relatório."""
        analises = self.get_analises_relacionadas()
        resumo = {}
        
        for analise in analises:
            tipo = analise.tipo_analise
            if tipo not in resumo:
                resumo[tipo] = {
                    'count': 0,
                    'resultados': [],
                    'conformes': 0,
                    'nao_conformes': 0
                }
            
            resumo[tipo]['count'] += 1
            if analise.resultado is not None:
                resumo[tipo]['resultados'].append(analise.resultado)
            
            if analise.conforme is True:
                resumo[tipo]['conformes'] += 1
            elif analise.conforme is False:
                resumo[tipo]['nao_conformes'] += 1
        
        return resumo
    
    def calcular_medias_por_tipo(self):
        """Calcula médias dos resultados por tipo de análise."""
        from django.db.models import Avg
        
        analises = self.get_analises_relacionadas()
        medias = {}
        
        tipos_analise = analises.values_list('tipo_analise', flat=True).distinct()
        
        for tipo in tipos_analise:
            analises_tipo = analises.filter(tipo_analise=tipo, resultado__isnull=False)
            if analises_tipo.exists():
                media = analises_tipo.aggregate(media=Avg('resultado'))['media']
                medias[tipo] = round(float(media), 2) if media else None
        
        return medias
    
    def verificar_conformidade_analises(self):
        """Verifica conformidade de todas as análises com base no contrato."""
        if not self.contrato:
            return {'total': 0, 'conformes': 0, 'nao_conformes': 0, 'sem_especificacao': 0}
        
        analises = self.get_analises_relacionadas()
        total = analises.count()
        conformes = 0
        nao_conformes = 0
        sem_especificacao = 0
        
        for analise in analises:
            if analise.conforme is True:
                conformes += 1
            elif analise.conforme is False:
                nao_conformes += 1
            else:
                sem_especificacao += 1
        
        return {
            'total': total,
            'conformes': conformes,
            'nao_conformes': nao_conformes,
            'sem_especificacao': sem_especificacao,
            'percentual_conformidade': round((conformes / total * 100), 2) if total > 0 else 0
        }
    
    def verificar_conformidade(self):
        """Verifica se todas as análises estão em conformidade com o contrato."""
        if not self.contrato:
            return False
        
        resultado_conformidade = self.verificar_conformidade_analises()
        
        # Considerar conforme se pelo menos 80% das análises estão conformes
        if resultado_conformidade['total'] == 0:
            return False
        
        percentual_minimo_conformidade = 80  # Pode ser configurável
        return resultado_conformidade['percentual_conformidade'] >= percentual_minimo_conformidade
    
    class Meta:
        verbose_name = "Relatório de Expedição"
        verbose_name_plural = "Relatórios de Expedição"
        ordering = ['-data_geracao']

class HistoricoEnvioRelatorio(BaseModel):
    """
    Modelo para armazenar histórico de envios de relatórios.
    """
    relatorio = models.ForeignKey(RelatorioExpedicao, on_delete=models.CASCADE, verbose_name="Relatório")
    destinatario = models.EmailField(verbose_name="Destinatário")
    assunto = models.CharField(max_length=200, verbose_name="Assunto")
    mensagem = models.TextField(blank=True, null=True, verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Responsável pelo Envio")
    versao_relatorio = models.CharField(max_length=10, default="1.0", verbose_name="Versão do Relatório")
    sucesso_envio = models.BooleanField(default=False, verbose_name="Envio Bem-sucedido")
    erro_envio = models.TextField(blank=True, null=True, verbose_name="Erro no Envio")
    
    def __str__(self):
        return f"Envio {self.relatorio.codigo} para {self.destinatario}"
    
    class Meta:
        verbose_name = "Histórico de Envio"
        verbose_name_plural = "Histórico de Envios"
        ordering = ['-data_envio']

class RelatorioAnalise(BaseModel):
    """
    Modelo para relacionar relatórios com análises específicas usando Generic Foreign Key.
    Isso permite que um relatório seja associado a diferentes tipos de análises.
    """
    relatorio = models.ForeignKey('RelatorioExpedicao', on_delete=models.CASCADE, verbose_name="Relatório")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Tipo de Análise")
    object_id = models.PositiveIntegerField(verbose_name="ID da Análise")
    analise = GenericForeignKey('content_type', 'object_id')
    
    # Metadados da análise no momento da inclusão no relatório
    data_analise = models.DateField(verbose_name="Data da Análise")
    tipo_analise = models.CharField(max_length=50, verbose_name="Tipo de Análise")
    resultado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Resultado")
    unidade = models.CharField(max_length=10, null=True, blank=True, verbose_name="Unidade")
    
    # Status de conformidade específico desta análise no contexto do relatório
    conforme = models.BooleanField(null=True, blank=True, verbose_name="Conforme")
    observacao_conformidade = models.TextField(blank=True, null=True, verbose_name="Observação de Conformidade")
    
    def __str__(self):
        return f"{self.relatorio.codigo} - {self.tipo_analise} ({self.data_analise})"
    
    class Meta:
        verbose_name = "Análise do Relatório"
        verbose_name_plural = "Análises do Relatório"
        ordering = ['data_analise', 'tipo_analise']
        unique_together = [['relatorio', 'content_type', 'object_id']]  # Evita duplicatas
