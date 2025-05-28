# Módulo de Relatórios - QualiSoja

## Visão Geral

O módulo de relatórios é um componente independente do sistema QualiSoja, responsável pela geração, visualização e exportação de relatórios baseados nos dados de análises. Este módulo foi separado do módulo de análises para melhorar a organização do código, facilitar a manutenção e permitir o desenvolvimento paralelo por diferentes equipes.

## Estrutura do Módulo

### Modelos de Dados

O módulo de relatórios não possui modelos próprios, mas utiliza os dados dos seguintes modelos do módulo de análises:

- `AnaliseUmidade`: Para relatórios de análises de umidade
- `AnaliseProteina`: Para relatórios de análises de proteína

### Views

- **RelatorioDashboardView**: Dashboard principal para navegação entre os tipos de relatórios
- **RelatorioGerarView**: Interface para seleção de parâmetros e geração de relatórios
- **RelatorioVisualizarView**: Exibição do relatório gerado com gráficos e tabelas

### Funções Auxiliares

- **obter_dados_relatorio()**: Consulta ao banco de dados e preparação dos dados
- **gerar_pdf_relatorio()**: Exportação de relatórios para PDF
- **gerar_excel_relatorio()**: Exportação de relatórios para Excel

## Templates

- **relatorios_dashboard.html**: Dashboard com opções de relatórios
- **gerar_relatorio.html**: Formulário para seleção de parâmetros
- **visualizar_relatorio.html**: Visualização de relatórios com gráficos e tabelas

## Arquivos Estáticos

- **relatorio_charts.js**: Implementação dos gráficos usando Chart.js

## URLs

- `/relatorios/dashboard/`: Dashboard principal de relatórios
- `/relatorios/gerar/`: Formulário para seleção de parâmetros
- `/relatorios/visualizar/`: Visualização do relatório gerado

## Funcionalidades

### Tipos de Relatórios

1. **Relatórios de Umidade**:
   - Análise temporal de resultados
   - Comparação por tipo de amostra
   - Estatísticas (média, mínimo, máximo)

2. **Relatórios de Proteína**:
   - Análise temporal de resultados
   - Comparação por tipo de amostra
   - Estatísticas (média, mínimo, máximo)

3. **Relatórios Completos**:
   - Combinação de dados de umidade e proteína
   - Correlações entre diferentes métricas
   - Visão geral da qualidade da produção

### Opções de Filtragem

- **Intervalo de datas**: Personalização do período analisado
- **Tipo de amostra**: Filtragem por categoria de amostra
- **Formato de saída**: HTML, PDF ou Excel

### Visualizações Gráficas

- **Gráficos de linha**: Para análise de tendências ao longo do tempo
- **Gráficos de barra**: Para comparação entre diferentes tipos de amostras
- **Tabelas resumo**: Com estatísticas e dados detalhados

## Integração com o Sistema

O módulo de relatórios se integra com o resto do sistema das seguintes formas:

1. **Acesso a dados**: Consulta direta aos modelos do módulo de análises
2. **Navegação**: Links no menu principal e no dashboard
3. **Exportação**: Geração de arquivos PDF e Excel para uso externo

## Fluxo de Trabalho

1. O usuário acessa o dashboard de relatórios
2. Seleciona o tipo de relatório desejado
3. Configura os parâmetros (datas, tipos de amostra, etc.)
4. Gera o relatório
5. Visualiza o relatório na interface web
6. Opcionalmente, exporta para PDF ou Excel

## Desenvolvimento e Manutenção

O código do módulo de relatórios está localizado no diretório `relatorios/` e segue a estrutura padrão de aplicações Django:

```
relatorios/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── views.py
├── static/
│   └── relatorios/
│       └── js/
│           └── relatorio_charts.js
└── templates/
    └── relatorios/
        ├── relatorios_dashboard.html
        ├── gerar_relatorio.html
        └── visualizar_relatorio.html
```

Para adicionar novos tipos de relatórios ou funcionalidades, modifique os arquivos relevantes seguindo o padrão existente.
