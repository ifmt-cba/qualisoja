# Módulo de Análises - QualiSoja

## Visão Geral

O módulo de análises é o componente central do sistema QualiSoja, responsável pelo registro, processamento e gerenciamento das análises de qualidade de soja e seus derivados. Este documento descreve a estrutura, funcionalidades e uso deste módulo.

## Modelos de Dados

### BaseModel

Classe abstrata que fornece campos comuns para todos os modelos:

- `criado_em`: Data e hora de criação do registro
- `atualizado_em`: Data e hora da última atualização

### AnaliseUmidade

Registra análises de umidade em diferentes tipos de amostras:

- **Campos principais:**
  - `data`: Data da análise
  - `horario`: Horário da análise
  - `tipo_amostra`: Tipo de amostra (Farelo Grosso, Farelo Fino, Soja Industrializada, Peletizado)
  - `tara`: Tara do recipiente
  - `liquido`: Peso líquido
  - `peso_amostra`: Peso da amostra
  - `resultado`: Resultado da análise
  - `fator_correcao`: Fator de correção aplicado (se houver)

### AnaliseProteina

Registra análises de proteína em diferentes tipos de amostras:

- **Campos principais:**
  - `data`: Data da análise
  - `horario`: Horário da análise
  - `tipo_amostra`: Tipo de amostra (Farelo, Soja Industrializada)
  - `peso_amostra`: Peso da amostra em gramas
  - `ml_gasto`: Mililitros gastos na titulação
  - `resultado`: Percentual de proteína (%)
  - `resultado_corrigido`: Percentual de proteína corrigido (%)
  - `eh_media_24h`: Indica se o registro é uma média de 24 horas

### ConfiguracaoRelatorio

Armazena configurações para geração de relatórios:

- **Campos principais:**
  - `nome`: Nome do relatório
  - `tipo_relatorio`: Tipo de relatório (Umidade, Proteína, Combinado)
  - `periodo_padrao`: Período padrão em dias
  - `ativo`: Indica se a configuração está ativa

## Funcionalidades

### Registro de Análises

- Cadastro de análises de umidade
- Cadastro de análises de proteína
- Validação de dados de entrada
- Cálculo automático de resultados

### Visualização de Dados

- Listagem de análises
- Filtros por data, tipo de amostra
- Exportação para Excel e PDF

### Relatórios

- Geração de relatórios customizáveis
- Visualizações gráficas usando Chart.js
- Estatísticas e análises de tendências

## API e Views

### Views principais

1. `UmidadeCreateView` e `ProteinaCreateView`: Para criação de análises
2. `UmidadeListView` e `ProteinaListView`: Para listagem de análises
3. `RelatorioGerarView`: Para geração de relatórios
4. `RelatorioVisualizarView`: Para visualização de relatórios

### Endpoints para geração de relatórios

- `/relatorios/gerar/`: Formulário para seleção de parâmetros
- `/relatorios/visualizar/`: Visualização do relatório gerado
- `/relatorios/exportar/excel/`: Exportação para Excel
- `/relatorios/exportar/pdf/`: Exportação para PDF

## Fluxo de Trabalho

1. **Registro de Análise:**
   - Usuário acessa formulário de cadastro
   - Preenche dados da análise
   - Sistema valida e salva os dados

2. **Geração de Relatório:**
   - Usuário seleciona parâmetros (período, tipo)
   - Sistema processa dados e gera visualizações
   - Usuário pode exportar ou imprimir resultados

## Uso Programático

### Exemplo: Obtenção de dados para relatório

```python
from analises.views import obter_dados_relatorio
from datetime import date, timedelta

# Definir período
data_final = date.today()
data_inicial = data_final - timedelta(days=7)

# Obter dados
dados = obter_dados_relatorio(
    tipo_relatorio='completo',
    data_inicial=data_inicial,
    data_final=data_final,
    tipo_amostra_umidade='FG',
    tipo_amostra_proteina='FL'
)

# Acessar estatísticas
media_proteina = dados['estatisticas_proteina']['media']
```

## Extensões e Personalizações

O módulo de análises pode ser estendido para incluir novos tipos de análises. Para isso:

1. Crie uma nova classe de modelo que herda de `BaseModel`
2. Adicione os campos específicos da análise
3. Crie views para cadastro e listagem
4. Atualize os métodos de geração de relatórios

## Resolução de Problemas

### Problemas comuns

1. **Erro: "no such column: analises_analiseproteina.criado_em"**
   - Execute as migrações: `python manage.py migrate`
   - Verifique se os campos temporais estão corretos: 
     ```sql
     UPDATE analises_analiseproteina SET criado_em = datetime('now'), atualizado_em = datetime('now');
     UPDATE analises_analiseumidade SET criado_em = datetime('now'), atualizado_em = datetime('now');
     ```

2. **Gráficos não aparecem corretamente**
   - Verifique se os dados estão no formato correto
   - Abra o console do navegador para verificar erros JavaScript
