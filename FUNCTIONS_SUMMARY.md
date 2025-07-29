# Resumo das Funções

## `analises/views.py`
- **get_context_data(self, **kwargs)**: Recupera dados de contexto para uma visualização.
- **form_valid(self, form)**: Lida com envios de formulário válidos.
- **form_invalid(self, form)**: Lida com envios de formulário inválidos.
- **delete(self, request, *args, **kwargs)**: Exclui um objeto.
- **get_queryset(self)**: Recupera o queryset para uma visualização.

## `relatorios/views.py`
- **get_initial(self)**: Recupera dados iniciais para um formulário.
- **form_valid(self, form)**: Lida com envios de formulário válidos.
- **form_invalid(self, form)**: Lida com envios de formulário inválidos.
- **obter_dados_relatorio(tipo_relatorio, data_inicial, data_final, ...)**: Busca dados do relatório com base em parâmetros.
- **gerar_pdf_relatorio(dados, tipo_relatorio, data_inicial, data_final)**: Gera um relatório em PDF.
- **gerar_excel_relatorio(dados, tipo_relatorio, data_inicial, data_final)**: Gera um relatório Excel.
- **_parse_date_params(self, request)**: analisa parâmetros de data de uma solicitação.
- **_obter_analises_disponiveis(self)**: Recupera análises disponíveis.
- **_adicionar_analises_automaticamente(self, relatorio, clean_data)**: Adiciona automaticamente análises a um relatório.

## `qualisoja/views.py`
- **convert_decimal_to_float(stats_dict)**: Converte valores decimais para float em um dicionário.
- **home(request)**: Renderiza a página inicial.
- **home_simple(request)**: Renderiza uma página inicial simplificada.
- **health_check(request)**: Executa uma verificação de integridade.
- **teste_acesso(request)**: Testa as permissões de acesso.
- **test_connection(request)**: Testa as conexões com o banco de dados ou serviço.