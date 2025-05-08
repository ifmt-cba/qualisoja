<p aling="center">
<b>QualiSoja</b><br>
</p>
<p align="center">
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
  - Teor de proteína em grãos
  - Umidade e impurezas
  - Análises de óleo degomado
  - Análises específicas (OGM, micotoxinas, etc.)

- **Gerenciamento de Amostras:**
  - Rastreabilidade completa
  - Controle de lotes
  - Histórico de análises

- **Relatórios e Certificações:**
  - Relatórios de expedição para vendas
  - Certificados de qualidade
  - Relatórios comparativos e estatísticos

- **Gestão de Laboratório:**
  - Controle de equipamentos e calibrações
  - Gerenciamento de métodos analíticos
  - Fluxo de trabalho laboratorial

## Tecnologias

- **Backend:**
  - Java/Spring Boot
  - API REST
  - PostgreSQL

- **Frontend:**
  - React.js
  - Material-UI
  - Chart.js para visualizações

- **DevOps:**
  - Docker
  - GitHub Actions para CI/CD
  - Monitoramento com Prometheus/Grafana

## Instalação

### Pré-requisitos

- Java JDK 17+
- Node.js 16+
- PostgreSQL 13+ ou Docker
- Maven 3.8+

### Configurando o ambiente de desenvolvimento

1. Clone o repositório:
   ```bash
   git clone https://github.com/ifmt-cba/qualisoja.git
   cd qualisoja
