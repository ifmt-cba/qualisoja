# QualiSoja - Módulo de Visualização de Dados

## Visão Geral

Este módulo é responsável pela visualização de dados de análises de proteína e umidade no sistema QualiSoja. 
Ele fornece gráficos interativos e estatísticas para auxiliar na interpretação dos resultados.

## Funcionalidades

- Visualização de dados de proteína e umidade em gráficos temporais
- Visualização de dados por tipo de amostra
- Exibição de estatísticas (média, mediana, mínimo, máximo, desvio padrão)
- Agrupamento automático de dados por data e tipo
- Tratamento de erros e validação de dados

## Estrutura do Código

O código JavaScript está organizado nas seguintes seções:

1. **Configurações e Inicialização**
   - Configuração global do Chart.js
   - Inicialização dos gráficos

2. **Funções Utilitárias**
   - `formatarPercentual`: Formata valores numéricos para percentuais
   - `calcularEstatisticas`: Calcula estatísticas básicas para um conjunto de valores
   - `mostrarErroGrafico`: Exibe mensagens de erro na interface

3. **Funções de Agrupamento de Dados**
   - `_groupData`: Função base para agrupamento de dados
   - `groupByDate`: Agrupa dados por data
   - `groupByTipo`: Agrupa dados por tipo de amostra

4. **Funções de Renderização**
   - `renderProteinaCharts`: Renderiza gráficos de proteína
   - `renderProteinaStats`: Renderiza estatísticas de proteína
   - `renderProteinaTimeChart`: Renderiza gráfico temporal de proteína
   - `renderProteinaTipoChart`: Renderiza gráfico por tipo de proteína
   - Funções equivalentes para dados de umidade

## Testes

O módulo possui testes automatizados utilizando Jest. Para executar os testes:

1. Certifique-se de ter o Node.js instalado
2. Execute `npm install` para instalar as dependências
3. Execute `npm test` para rodar os testes

### Cobertura de Testes

Os testes abrangem:
- Funções utilitárias
- Funções de agrupamento de dados
- Funções de renderização
- Testes de integração
- Testes de desempenho

## Melhorias Implementadas

1. **Estrutura de Código Melhorada**
   - Organização em funções específicas para cada responsabilidade
   - Melhor gerenciamento de instâncias de gráficos

2. **Tratamento de Erros Aprimorado**
   - Validação adequada de dados JSON
   - Mensagens de erro mais informativas
   - Exibição visual de erros na interface

3. **Funções Utilitárias Robustas**
   - Formatação consistente de percentuais
   - Cálculo de estatísticas com tratamento de valores inválidos
   - Funções de agrupamento com validação

4. **Testes Abrangentes**
   - Testes unitários para cada função
   - Testes de integração entre componentes
   - Testes de desempenho para grandes conjuntos de dados
   - Testes de casos de borda e valores extremos

## Desenvolvido por

Equipe QualiSoja - 2025
