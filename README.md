# 🌱 QualiSoja

<div align="center">

![QualiSoja Logo](https://img.shields.io/badge/QualiSoja-Sistema%20de%20Qualidade-green?style=for-the-badge)

**Sistema Avançado de Controle de Qualidade da Soja**

*Desenvolvido pelo Instituto Federal de Mato Grosso - Campus Cuiabá*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green?style=flat-square&logo=django)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE.md)

</div>

---

O **QualiSoja** é uma solução completa para controle de qualidade na cadeia produtiva da soja, permitindo o gerenciamento de análises laboratoriais (como umidade, proteína, óleo e urase), geração de relatórios e rastreabilidade das atividades realizadas por diferentes perfis de usuários (analistas e equipe de produção). O sistema garante registros auditáveis, segurança por níveis de acesso e geração de relatórios técnicos exportáveis.projetado especificamente para atender às necessidades de:

-  **Indústrias de Processamento**
-  **Laboratórios de Análise**
-  **Cooperativas Agrícolas**
-  **Centros de Pesquisa**
---
## Sumário

1. [Visão do Produto](#visão-do-produto)
2. [Funcionalidades Principais](#funcionalidades-principais)
3. [Principais Diferenciais](#principais-diferenciais)
4. [Perfis de Usuário](#perfis-de-usuário)
5. [Formulário de Análise](formulário-de-análise)
6. [Módulos de Análise](módulo-de-análise)
7. [Funcionalidades Especiais](funcionalidades-especiais)
8. [Tecnologias Utilizadas](#tecnologias-utilizadas)
9. [Estrutura do Projeto](#estrutura-do-projeto)
10. [Como Usar](#como-usar)
11. [Documentação](#documentação)

---
## Visão do Produto

#### O QualiSoja foi projetado para digitalizar e automatizar os processos de análise de qualidade na indústria  de soja. Desenvolvido com foco em simplicidade, segurança e rastreabilidade, o sistema permite que diferentes perfis de usuários operem com eficiência, reduzindo erros operacionais e agilizando a geração de relatórios. Com uma interface clara e recursos específicos para cada tipo de análise laboratorial, o sistema assegura o controle dos resultados, facilita a auditoria de dados e padroniza os registros técnicos do processo produtivo.
---
## Funcionalidades Principais 

- Cadastro de análises laboratoriais
   - Umidade, proteína, óleo degomado e urase
   - Cálculo automático de resultados com base nas fórmulas padrão do laboratório
- Controle de acesso por grupo
  - Usuários do grupo Analista podem cadastrar, consultar análises e gerar relatórios
  - Usuários do grupo Produção podem apenas visualizar e exportar  relatórios
  - Administradores têm acesso total ao sistema via /admin
- Geração e exportação de relatórios
  - Relatórios personalizados por tipo de análise e intervalo de datas
  - Filtros por tipo de amostra e formato de saída (web, PDF e excel.)
- Registro de atividades
   - Log automático de login de usuários
   - Registro de criação de análises e geração de relatórios
   - Rastreabilidade das atividades que acontecem dentro do sistema via /admin
 - Navegação adaptada por perfil de acesso
   - Menus e páginas exibidos de acordo com o grupo do usuário logado
 - Gestão via painel administrativo Django
   - Gerenciamento avançado de usuários, permissões e grupos
   - Visualização dos registros de atividade diretamente no admin
     
---


###  Principais Diferenciais

- **Interface Intuitiva**: Design responsivo e fácil navegação
- **Análises Abrangentes**: Suporte a 7 tipos de análises físico-químicas
- **Relatórios Inteligentes**: Geração automatizada de relatórios profissionais
- **Casos Especiais**: Tratamento automático para situações como "Fábrica Parada" e "Sem Amostra"
- **Visualizações Avançadas**: Dashboards interativos com gráficos dinâmicos
--

---
### Perfis de Usuário

| **Perfil**         | **Permissões Principais**                                                                 |
|--------------------|--------------------------------------------------------------------------------------------|
| **Administrador**  | Acesso total ao sistema, gerencia usuários, grupos, análises e visualiza logs do sistema. |
| **Analista**       | Realiza o cadastro, edição e consulta de análises laboratoriais (umidade, proteína etc.). |
| **Produção**       | Visualiza e gera relatórios de análises. Não possui permissão de edição ou cadastro.      |

---

###  Formulário de Análise

```
╭─────────────────────────────────────────────────────────────────╮
│  🔬 Nova Análise de Proteína                                    │
├─────────────────────────────────────────────────────────────────┤
│   Data: [14/07/2025]      Horário: [10:30]                 │
│   Tipo: [▼ Farelo     ]   Usuário: [admin    ]             │
│                                                                 │
│  ⚠ Caso Especial Detectado!                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 🏭 FÁBRICA PARADA                                          │ │
│  │ Não há necessidade de inserir dados de análise.           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [ Salvar] [ Cancelar]                                      │
╰─────────────────────────────────────────────────────────────────╯
```

</div>

## Módulos de Análise

###  Análises Disponíveis

| Tipo de Análise | Parâmetros Medidos | Casos Especiais |
|------------------|-------------------|------------------|
| ** Umidade** | Tara, Líquido, Peso da Amostra |  
| ** Proteína** | ML Gasto, ML Branco, Normalidade |  FP/SA |
| ** Urase** | Amostra 1, Amostra 2 |  FP/SA |
| ** Cinza** | Peso Amostra, Cadinho, Cinza | FP/SA |
| ** Teor de Óleo** | Peso Amostra, Tara, Líquido |  FP/SA |
| ** Fibra** | Peso Amostra, Tara, Fibra, Branco |  FP/SA |
| ** Fósforo** | Absorbância da Amostra |  FP/SA |
| ** Sílica** | Análise de Cinza, Resultado Sílica |  FP/SA |

---

### Funcionalidades Especiais

- **Cálculos Automáticos**: Fórmulas específicas para cada tipo de análise
- **Validação Inteligente**: Verificação automática de dados de entrada
- **Precisão Configurável**: Controle de casas decimais por análise
- **Histórico Completo**: Rastreabilidade total dos registros

---

##  Tecnologias Utilizadas

<div align="center">

### Backend
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

### DevOps & Ferramentas
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

</div>

##  Estrutura do Projeto

```
qualisoja/
├──  analises/              # Módulo principal de análises
│   ├── models.py            # Modelos de dados (7 tipos de análises)
│   ├── views.py             # Lógica de negócio
│   ├── forms.py             # Formulários de entrada
│   └── templates/app/       # Templates específicos
├──  relatorios/           # Sistema de relatórios
│   ├── views.py            # Geração de relatórios
│   └── templates/          # Templates de relatórios
├──  users/               # Gerenciamento de usuários
├──  templates/           # Templates globais
├──  staticfiles/         # Arquivos estáticos
├──  qualisoja/           # Configurações do Django
├──  devops/             # Configurações de deploy
└──  docs/               # Documentação técnica
```

> 📖 **Documentação Detalhada**: Consulte [docs/arquitetura.md](docs/arquitetura.md) para informações técnicas completas

##  Instalação Rápida

###  Pré-requisitos

-  **Python 3.10+**
-  **pip** (gerenciador de pacotes Python)
-  **Git** (controle de versão)

###  Instalação em 3 Passos

```bash
# Clone o repositório
git clone https://github.com/ifmt-cba/qualisoja.git
cd qualisoja

# Configure o ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências e execute
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Acesso ao Sistema

- **URL Local**: `http://127.0.0.1:8000/`
- **Usuário Admin**: `admin`
- **Senha**: `admin123`

> 📝 **Nota**: Para configuração avançada e deploy em produção, consulte [SETUP.md](SETUP.md)

##  Como Usar

###  **Registro de Análises**
- Acesse o módulo desejado (Umidade, Proteína, etc.)
- Preencha os dados da amostra
- O sistema calcula automaticamente os resultados
- Para casos especiais (FP/SA), apenas selecione o tipo

###  **Visualização de Dados**
- Navegue até a seção de relatórios
- Escolha filtros por data, tipo ou período
- Exporte em PDF, Excel ou visualize gráficos

### **Gerenciamento**
- Configure usuários e permissões
- Personalize parâmetros de análise
- Monitore logs e auditoria

##  Documentação

### Guias Disponíveis

-  **[Guia de Instalação](SETUP.md)** - Configuração detalhada
-  **[Arquitetura do Sistema](docs/arquitetura.md)** - Visão técnica
-  **[Módulo de Análises](docs/modulo_analises.md)** - Funcionalidades principais
-  **[Sistema de Relatórios](docs/modulo_relatorios.md)** - Geração de relatórios
-  **[Changelog](CHANGELOG.md)** - Histórico de versões

###  Últimas Atualizações

-  **Funcionalidade FP/SA**: Tratamento automático para casos especiais
-  **Análise de Umidade**: Precisão de 4 casas decimais
-  **Interface Melhorada**: Design responsivo e intuitivo
-  **Validações Avançadas**: Verificação automática de dados


###  Sugerir Melhorias

- Abra uma [Issue](https://github.com/ifmt-cba/qualisoja/issues) com a tag `enhancement`
- Descreva sua ideia claramente
- Explique o benefício para os usuários

##  Equipe

<div align="center">

###  Coordenação Acadêmica
**Prof. Dr. João Paulo Delgado Preti**  
*Instituto Federal de Mato Grosso - Campus Cuiabá*

###  Desenvolvimento
**Equipe de Engenharia de Software IFMT**  
*Estudantes e Pesquisadores*

</div>

## Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

##  Agradecimentos

-  **IFMT Campus Cuiabá** - Suporte institucional
-  **Setor Agrícola do MT** - Feedback e validação
-  **Comunidade Open Source** - Ferramentas e bibliotecas

---

<div align="center">

** Se este projeto foi útil para você, considere dar uma estrela!**

[![GitHub stars](https://img.shields.io/github/stars/ifmt-cba/qualisoja?style=social)](https://github.com/ifmt-cba/qualisoja/stargazers)

</div>
