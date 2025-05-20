# Configuração do Ambiente QualiSoja

Este documento fornece instruções para configurar um ambiente de desenvolvimento para o projeto QualiSoja.

## Requisitos

- Python 3.10 ou superior
- Node.js 16.x ou superior (para testes JavaScript)
- SQLite (já incluído com Python)

## Configuração Python

1. Clone o repositório:
   ```bash
   git clone https://github.com/Mafe519/QualiSoja.git
   cd QualiSoja
   ```

2. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```

5. Aplique as migrações ao banco de dados:
   ```bash
   python manage.py migrate
   ```

6. Correção para os campos temporais:
   Execute no SQLite:
   ```bash
   python manage.py dbshell
   ```
   
   Dentro do shell SQLite, execute:
   ```sql
   UPDATE analises_analiseproteina SET criado_em = datetime('now'), atualizado_em = datetime('now');
   UPDATE analises_analiseumidade SET criado_em = datetime('now'), atualizado_em = datetime('now');
   .quit
   ```

## Configuração JavaScript (para testes)

1. Instale as dependências Node.js:
   ```bash
   npm install
   ```

2. Execute os testes JavaScript:
   ```bash
   npm test
   ```

## Executando o servidor de desenvolvimento

```bash
python manage.py runserver
```

O site estará disponível em `http://127.0.0.1:8000/`.

## Estrutura do Projeto

- `analises/` - Aplicação principal para análises de soja
- `templates/static/geral/js/` - Código JavaScript para visualizações
- `tests/js/` - Testes JavaScript
- `docs/` - Documentação adicional

## Documentação Adicional

- [Relatório de Melhorias JavaScript](docs/relatorio_melhorias_javascript.md)
- [Documentação JavaScript](templates/static/geral/js/README.md)
