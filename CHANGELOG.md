# Changelog do QualiSoja

Este arquivo documenta todas as mudanças significativas no projeto QualiSoja.

## [Não lançado]

### Adicionado
- Nova funcionalidade...

### Alterado
- Melhorias na interface...

## [1.1.0] - 2023-05-27

### Reestruturação da Arquitetura
- **Separação do módulo de relatórios**: Migração completa da funcionalidade de relatórios do app `analises` para um novo app dedicado `relatorios`
  - Criação do novo app `relatorios` com sua própria estrutura MVC
  - Movimentação de todas as views, templates, forms e URLs relacionadas a relatórios
  - Atualização de todas as referências de namespace para `relatorios:gerar`, etc.
  - Reorganização dos arquivos JavaScript específicos para relatórios
- **Simplificação da interface de relatórios**: Remoção do dashboard intermediário redundante
  - Acesso direto à interface de geração de relatórios
  - Eliminação de cliques desnecessários para o usuário
  - Interface mais limpa e eficiente

### Melhorias
- Organização mais clara do código com responsabilidades bem definidas
- Redução de conflitos de desenvolvimento entre equipes
- Melhor separação de responsabilidades entre os módulos

### Técnico
- Criação de novas migrações para o app `analises` removendo `ConfiguracaoRelatorio`
- Criação de migrações iniciais para o app `relatorios`
- Atualização dos caminhos de importação nos templates

## [1.0.0] - 2023-01-15

### Versão Inicial
- Sistema básico de registro de análises
- Relatórios com visualizações gráficas
- Exportação para PDF e Excel
