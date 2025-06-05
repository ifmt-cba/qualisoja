# Interface Moderna do Gerador de Relatórios QualiSoja

## 📋 Visão Geral

A nova interface moderna do gerador de relatórios agora é a interface padrão do sistema, substituindo a interface clássica anterior. Ela está disponível em `/relatorios/gerar/` e oferece uma experiência completamente renovada, com a interface clássica preservada como backup em `/relatorios/gerar-classico/`.

## ✨ Principais Funcionalidades

### 🎨 Design Moderno
- **Interface visual atualizada** com cores da marca QualiSoja
- **Design responsivo** que funciona em desktop, tablet e mobile
- **Animações suaves** e feedback visual intuitivo
- **Tema verde corporativo** consistente com a identidade visual

### 🚀 Wizard de 3 Etapas
1. **Seleção do Tipo de Relatório**
   - Cartões interativos para escolha rápida
   - Opções: Umidade, Proteína, Completo
   
2. **Período e Filtros Avançados**
   - Botões de seleção rápida (7, 15, 30, 90 dias)
   - Date picker personalizado com localização PT-BR
   - Filtros por tipo de amostra dinâmicos
   
3. **Formato e Geração**
   - Seleção visual do formato de saída
   - Opções: HTML (online), PDF, Excel

### ⚡ Funcionalidades Avançadas

#### Atalhos de Teclado
- `Ctrl + Enter`: Gerar relatório diretamente
- `Ctrl + P`: Pré-visualizar dados
- `Ctrl + S`: Salvar configuração
- `Ctrl + /`: Mostrar/ocultar painel de atalhos

#### Auto-Save Inteligente
- **Persistência automática** das configurações no localStorage
- **Restauração automática** ao recarregar a página
- **Expiração inteligente** (7 dias) para configurações antigas

#### Pré-visualização de Dados
- **Estatísticas em tempo real** do período selecionado
- **Estimativa de análises** disponíveis
- **Validação prévia** antes da geração

### 🔧 Melhorias Técnicas

#### Validação Robusta
- Validação de campos obrigatórios
- Verificação de intervalos de data válidos
- Limite máximo de 1 ano para consultas
- Feedback visual de erros em tempo real

#### Acessibilidade
- **Navegação por teclado** completa
- **ARIA labels** para leitores de tela
- **Foco visual** bem definido
- **Contraste adequado** para diferentes necessidades

#### Notificações Toast
- **Feedback visual** para ações do usuário
- **Tipos diferentes**: sucesso, erro, informação
- **Auto-remoção** após tempo determinado

## 🎯 Como Usar

### Acesso
Navegue para `/relatorios/gerar/` no sistema QualiSoja (interface padrão) ou `/relatorios/gerar-classico/` para a interface clássica.

### Fluxo Básico
1. **Selecione o tipo** de relatório clicando no cartão desejado
2. **Configure o período** usando os botões rápidos ou datas personalizadas
3. **Escolha o formato** de saída (HTML, PDF ou Excel)
4. **Clique em "Gerar Relatório"** ou use `Ctrl + Enter`

### Dicas de Uso
- Use `Ctrl + P` para **pré-visualizar** os dados antes de gerar
- **Salve configurações** frequentes com `Ctrl + S`
- Use `Ctrl + /` para ver todos os **atalhos disponíveis**
- A **navegação por etapas** permite voltar e alterar configurações facilmente

## 🔄 Compatibilidade

### Interface Clássica (Backup)
A interface clássica original foi preservada e permanece disponível em `/relatorios/gerar-classico/` para usuários que preferem a versão tradicional.

### Funcionalidades Backend
- **Mesma lógica de negócio** da interface original
- **Compatibilidade total** com os models existentes
- **Mesma geração de relatórios** (views e processamento)

## 🚀 Benefícios

### Para Usuários
- **Experiência mais intuitiva** e moderna
- **Navegação mais rápida** com atalhos
- **Feedback visual** melhorado
- **Configurações persistentes**

### Para Desenvolvedores
- **Código JavaScript modular** e bem organizado
- **CSS com variáveis** para fácil manutenção
- **Estrutura escalável** para futuras funcionalidades
- **Documentação inline** completa

## 🔧 Manutenção

### Configurações CSS
As cores e estilos principais estão definidos como variáveis CSS no início do arquivo:
```css
:root {
    --primary-green: #065f46;
    --light-green: #d1fae5;
    --accent-green: #059669;
    /* ... outras variáveis */
}
```

### JavaScript
O código JavaScript está modularizado em funções específicas:
- `initializePage()`: Configuração inicial
- `setupEventListeners()`: Eventos e interações
- `validateForm()`: Validação de dados
- `updateSummary()`: Atualização do resumo
- E outras funções utilitárias

## 📱 Responsividade

A interface é totalmente responsiva e se adapta a:
- **Desktop** (1200px+): Layout completo com sidebar
- **Tablet** (768px-1199px): Layout adaptado
- **Mobile** (< 768px): Layout empilhado e otimizado para toque

---

**Versão**: 1.0
**Data**: Maio 2025
**Compatibilidade**: Django 4.x, Bootstrap 5.x, JavaScript ES6+
