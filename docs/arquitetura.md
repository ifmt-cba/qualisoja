# Arquitetura do Sistema QualiSoja

## Visão Geral

O QualiSoja é um sistema web baseado em Django que segue o padrão arquitetural MVC (Model-View-Controller), embora no Django esse padrão seja frequentemente referido como MTV (Model-Template-View). Este documento descreve a arquitetura geral do sistema, seus componentes principais e como eles interagem.

## Componentes do Sistema

![Arquitetura QualiSoja](./arquitetura_qualisoja.png)

### 1. Camada de Modelo (Models)

Responsável pela definição da estrutura de dados e regras de negócio.

- **Aplicações principais:**
  - `analises`: Modelos para registro e processamento de análises de qualidade
  - `users`: Gerenciamento de usuários e perfis

- **Modelos principais:**
  - `BaseModel`: Classe abstrata com campos comuns (criado_em, atualizado_em)
  - `AnaliseUmidade`: Registro de análises de umidade
  - `AnaliseProteina`: Registro de análises de proteína
  - `ConfiguracaoRelatorio`: Configurações para geração de relatórios
  - `Profile`: Perfil de usuário estendido

### 2. Camada de Visão (Templates)

Responsável pela apresentação dos dados aos usuários.

- **Templates principais:**
  - Templates base: `base.html`, `baseLogin.html`
  - Templates de aplicação: em `analises/templates/app/`
  - Templates de autenticação: em `users/templates/`

- **Recursos estáticos:**
  - JavaScript: `templates/static/geral/js/`
  - CSS: `templates/static/geral/css/`
  - Imagens: `templates/static/image/`

### 3. Camada de Controle (Views)

Responsável pela lógica de controle e processamento.

- **Views principais:**
  - Views de análise: Cadastro e listagem de análises
  - Views de relatório: Geração e visualização de relatórios
  - Views de exportação: Exportação para Excel e PDF
  - Views de autenticação: Login e gerenciamento de usuários

### 4. URLs e Roteamento

- `qualisoja/urls.py`: URLs globais do projeto
- `analises/urls.py`: URLs específicas do módulo de análises
- `users/urls.py`: URLs relacionadas a usuários

### 5. Componente de Visualização de Dados

- **Frontend:**
  - Chart.js para visualizações gráficas
  - JavaScript para interatividade
  - Bootstrap para interface responsiva

- **Backend de visualização:**
  - `matplotlib_views.py`: Geração de gráficos no servidor
  - `relatorio_charts.js`: Renderização de gráficos no cliente

## Fluxo de Dados

1. **Cadastro de Análise:**
   - Usuário submete formulário → View processa dados → Modelo salva no banco → Redireciona para listagem

2. **Geração de Relatório:**
   - Usuário seleciona parâmetros → View consulta banco → Dados processados → Template renderiza com gráficos

3. **Exportação de Dados:**
   - Usuário solicita exportação → View gera arquivo (Excel/PDF) → Arquivo enviado ao navegador

## Banco de Dados

- **Desenvolvimento:** SQLite
- **Produção:** PostgreSQL (recomendado)

### Esquema simplificado:

```
+-------------------+      +-------------------+
| AnaliseUmidade    |      | AnaliseProteina   |
+-------------------+      +-------------------+
| id                |      | id                |
| criado_em         |      | criado_em         |
| atualizado_em     |      | atualizado_em     |
| data              |      | data              |
| horario           |      | horario           |
| tipo_amostra      |      | tipo_amostra      |
| peso_amostra      |      | peso_amostra      |
| resultado         |      | resultado         |
| ...               |      | ...               |
+-------------------+      +-------------------+
         
+-------------------+      +-------------------+
| User              |      | Profile           |
+-------------------+      +-------------------+
| id                |      | id                |
| username          |      | user (FK)         |
| email             |      | cargo             |
| ...               |      | ...               |
+-------------------+      +-------------------+
```

## Padrões de Design

1. **Class-Based Views:** Uso de views baseadas em classes para reúso de código e clareza
2. **Template Inheritance:** Herança de templates para consistência visual
3. **Abstract Base Models:** Modelos base abstratos para compartilhar campos comuns
4. **Service Layer:** Funções utilitárias para lógica de negócios complexa

## Segurança

- Autenticação de usuários via sistema Django
- Controle de acesso baseado em permissões
- Proteção contra CSRF em formulários
- Validação de dados de entrada

## Testes

- **Testes Python:** Usando o framework de testes do Django
- **Testes JavaScript:** Usando Jest para testes de componentes frontend

## Implantação

Recomendações para implantação em produção:

1. Usar PostgreSQL como banco de dados
2. Configurar servidor web (Nginx/Apache) com WSGI
3. Implementar HTTPS para segurança
4. Configurar backup regular do banco de dados

## Possíveis Evoluções

1. **API REST completa:** Para integração com outros sistemas
2. **Sistema de notificações:** Alertas sobre resultados fora de parâmetros
3. **Dashboard avançado:** Com mais visualizações e insights
4. **App mobile:** Para registro de análises em campo
