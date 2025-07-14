
# 🌱 QualiSoja

<div align="center">

![QualiSoja Logo](https://img.shields.io/badge/QualiSoja-Sistema%20de%20Qualidade-green?style=for-the-badge)

**Sistema Avançado de Controle de Qualidade da Soja**

*Desenvolvido pelo Instituto Federal de Mato Grosso - Campus Cuiabá*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green?style=flat-square&logo=django)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE.md)

[📊 Demo](#demo) • [🚀 Instalação](#instalação) • [📚 Documentação](#documentação) • [🤝 Contribuir](#contribuição)

</div>

---

## 🎯 Sobre o Projeto

O **QualiSoja** é uma solução completa para controle de qualidade na cadeia produtiva da soja, projetado especificamente para atender às necessidades de:

- 🏭 **Indústrias de Processamento**
- 🧪 **Laboratórios de Análise**
- 🌾 **Cooperativas Agrícolas**
- 📊 **Centros de Pesquisa**

### ✨ Principais Diferenciais

- **Interface Intuitiva**: Design responsivo e fácil navegação
- **Análises Abrangentes**: Suporte a 7 tipos de análises físico-químicas
- **Relatórios Inteligentes**: Geração automatizada de relatórios profissionais
- **Casos Especiais**: Tratamento automático para situações como "Fábrica Parada" e "Sem Amostra"
- **Visualizações Avançadas**: Dashboards interativos com gráficos dinâmicos

## 🔬 Módulos de Análise

### 📈 Análises Disponíveis

| Tipo de Análise | Parâmetros Medidos | Casos Especiais |
|------------------|-------------------|------------------|
| **🌊 Umidade** | Tara, Líquido, Peso da Amostra | ❌ |
| **🥩 Proteína** | ML Gasto, ML Branco, Normalidade | ✅ FP/SA |
| **🔥 Urase** | Amostra 1, Amostra 2 | ✅ FP/SA |
| **🔥 Cinza** | Peso Amostra, Cadinho, Cinza | ✅ FP/SA |
| **🛢️ Teor de Óleo** | Peso Amostra, Tara, Líquido | ✅ FP/SA |
| **🌾 Fibra** | Peso Amostra, Tara, Fibra, Branco | ✅ FP/SA |
| **⚗️ Fósforo** | Absorbância da Amostra | ✅ FP/SA |
| **🔬 Sílica** | Análise de Cinza, Resultado Sílica | ✅ FP/SA |

### 🎛️ Funcionalidades Especiais

- **Cálculos Automáticos**: Fórmulas específicas para cada tipo de análise
- **Validação Inteligente**: Verificação automática de dados de entrada
- **Precisão Configurável**: Controle de casas decimais por análise
- **Histórico Completo**: Rastreabilidade total dos registros

## 🚀 Tecnologias Utilizadas

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

## 📊 Estrutura do Projeto

```
qualisoja/
├── 📱 analises/              # Módulo principal de análises
│   ├── models.py            # Modelos de dados (7 tipos de análises)
│   ├── views.py             # Lógica de negócio
│   ├── forms.py             # Formulários de entrada
│   └── templates/app/       # Templates específicos
├── 📈 relatorios/           # Sistema de relatórios
│   ├── views.py            # Geração de relatórios
│   └── templates/          # Templates de relatórios
├── 👥 users/               # Gerenciamento de usuários
├── 🎨 templates/           # Templates globais
├── 📁 staticfiles/         # Arquivos estáticos
├── ⚙️ qualisoja/           # Configurações do Django
├── 🐳 devops/             # Configurações de deploy
└── 📚 docs/               # Documentação técnica
```

## ⚡ Instalação Rápida

### 📋 Pré-requisitos

- 🐍 **Python 3.10+**
- 📦 **pip** (gerenciador de pacotes Python)
- 🔧 **Git** (controle de versão)

### 🎯 Instalação em 3 Passos

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/ifmt-cba/qualisoja.git
cd qualisoja

# 2️⃣ Configure o ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3️⃣ Instale as dependências e execute
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🌐 Acesso ao Sistema

- **URL Local**: `http://127.0.0.1:8000/`
- **Usuário Admin**: `admin`
- **Senha**: `admin123`

> 📝 **Nota**: Para configuração avançada e deploy em produção, consulte [SETUP.md](SETUP.md)

## 🎮 Como Usar

### 1️⃣ **Registro de Análises**
- Acesse o módulo desejado (Umidade, Proteína, etc.)
- Preencha os dados da amostra
- O sistema calcula automaticamente os resultados
- Para casos especiais (FP/SA), apenas selecione o tipo

### 2️⃣ **Visualização de Dados**
- Navegue até a seção de relatórios
- Escolha filtros por data, tipo ou período
- Exporte em PDF, Excel ou visualize gráficos

### 3️⃣ **Gerenciamento**
- Configure usuários e permissões
- Personalize parâmetros de análise
- Monitore logs e auditoria

## 📚 Documentação

### 📖 Guias Disponíveis

- 🚀 **[Guia de Instalação](SETUP.md)** - Configuração detalhada
- 🏗️ **[Arquitetura do Sistema](docs/arquitetura.md)** - Visão técnica
- 🔬 **[Módulo de Análises](docs/modulo_analises.md)** - Funcionalidades principais
- 📊 **[Sistema de Relatórios](docs/modulo_relatorios.md)** - Geração de relatórios
- 🔄 **[Changelog](CHANGELOG.md)** - Histórico de versões

### 🆕 Últimas Atualizações

- ✅ **Funcionalidade FP/SA**: Tratamento automático para casos especiais
- ✅ **Análise de Umidade**: Precisão de 4 casas decimais
- ✅ **Interface Melhorada**: Design responsivo e intuitivo
- ✅ **Validações Avançadas**: Verificação automática de dados

## 🤝 Contribuição

Contribuições são sempre bem-vindas! Veja como você pode ajudar:

### 🛠️ Como Contribuir

1. **Fork** o repositório
2. **Clone** sua fork: `git clone https://github.com/seu-usuario/qualisoja.git`
3. **Crie** uma branch: `git checkout -b feature/nova-funcionalidade`
4. **Commit** suas mudanças: `git commit -m 'feat: adiciona nova funcionalidade'`
5. **Push** para a branch: `git push origin feature/nova-funcionalidade`
6. **Abra** um Pull Request

### 🐛 Reportar Bugs

- Use o [GitHub Issues](https://github.com/ifmt-cba/qualisoja/issues)
- Descreva o problema detalhadamente
- Inclua capturas de tela se necessário

### 💡 Sugerir Melhorias

- Abra uma [Issue](https://github.com/ifmt-cba/qualisoja/issues) com a tag `enhancement`
- Descreva sua ideia claramente
- Explique o benefício para os usuários

## 👥 Equipe

<div align="center">

### 🎓 Coordenação Acadêmica
**Prof. Dr. João Paulo Delgado Preti**  
*Instituto Federal de Mato Grosso - Campus Cuiabá*

### 👨‍💻 Desenvolvimento
**Equipe de Engenharia de Software IFMT**  
*Estudantes e Pesquisadores*

</div>

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## 🏆 Agradecimentos

- 🏫 **IFMT Campus Cuiabá** - Suporte institucional
- 🌾 **Setor Agrícola do MT** - Feedback e validação
- 💻 **Comunidade Open Source** - Ferramentas e bibliotecas

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**

[![GitHub stars](https://img.shields.io/github/stars/ifmt-cba/qualisoja?style=social)](https://github.com/ifmt-cba/qualisoja/stargazers)

*Desenvolvido com ❤️ para a agricultura brasileira*

</div>
