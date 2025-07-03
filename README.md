
<p align="center">
  <b>QualiSoja</b><br>
  <b>Sistema de Registro da Análise da Qualidade da Soja</b><br>
  Desenvolvido pelo <a href="https://cba.ifmt.edu.br/">IFMT Campus Cuiabá</a>
</p>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#uso">Uso</a> •
  <a href="#contribuição">Contribuição</a> •
  <a href="#licença">Licença</a>
</p>

---

## Sobre

O QualiSoja é um sistema desenvolvido para registrar, monitorar e analisar parâmetros de qualidade da soja e seus derivados. Voltado para laboratórios, indústrias de processamento e cooperativas agrícolas, o sistema facilita o controle de qualidade através de uma interface intuitiva e de fácil utilização.

Desenvolvido como projeto de pesquisa e extensão do Instituto Federal de Mato Grosso - Campus Cuiabá, o QualiSoja visa atender às necessidades específicas da cadeia produtiva da soja no Centro-Oeste brasileiro, contribuindo para a melhoria da qualidade e competitividade do setor.

## Funcionalidades

- **Registro de Análises Físico-Químicas:**
  - Teor de proteína em grãos e farelo
  - Umidade em diferentes tipos de amostras
  - Análises com correção de fatores

- **Gerenciamento de Amostras:**
  - Rastreabilidade por data e horário
  - Categorização por tipo de amostra
  - Histórico completo de análises

- **Relatórios e Visualizações:**
  - Relatórios em PDF e Excel
  - Visualizações gráficas interativas
  - Estatísticas detalhadas (média, mediana, desvio padrão)

- **Dashboard Analítico:**
  - Visualização de tendências temporais
  - Comparação por tipo de amostra
  - Exportação de dados e gráficos

## Tecnologias

- **Backend:**
  - Django (Python)
  - APIs REST
  - SQLite (desenvolvimento) / PostgreSQL (produção)

- **Frontend:**
  - HTML/CSS/JavaScript
  - Bootstrap
  - Chart.js para visualizações

- **DevOps:**
  - Git para controle de versão
  - GitHub Actions para CI/CD
  - Testes automatizados com Jest e Python unittest

## Estrutura do Projeto

```
QualiSoja/
├── analises/           # Módulo de análises (umidade e proteína)
├── relatorios/         # Módulo de relatórios e visualizações
├── users/              # Gerenciamento de usuários
├── templates/          # Templates globais
├── qualisoja/          # Configurações do projeto
└── docs/               # Documentação
```

## Instalação

Para instruções detalhadas de instalação e configuração, consulte o arquivo [SETUP.md](SETUP.md).

### Requisitos básicos

- Python 3.10+
- Node.js 16+ (para desenvolvimento JavaScript)
- Git

## Uso

Após a instalação, execute o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse o sistema em `http://127.0.0.1:8000/`.

### Usuário de teste

- Usuário: admin
- Senha: admin123

## Documentação Adicional

- [Configuração do Ambiente (SETUP.md)](SETUP.md)
- [Documentação de Arquitetura](docs/arquitetura.md)
- [Módulo de Análises](docs/modulo_analises.md)
- [Módulo de Relatórios](docs/modulo_relatorios.md)
- [Relatório de Melhorias JavaScript](docs/relatorio_melhorias_javascript.md)
- [Documentação do Módulo de Visualização](templates/static/geral/js/README.md)
- [Documentação da API (swagger)](api/docs)

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova funcionalidade'`)
4. Push para a Branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE.md para detalhes.

## Equipe

- Coordenação: Prof. Dr. João Paulo Delgado Preti
- Desenvolvimento: Equipe de Engenharia de Software IFMT
