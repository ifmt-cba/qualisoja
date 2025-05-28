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

## Configuração após atualização do repositório

Se você está atualizando um repositório existente e ocorreram mudanças significativas na estrutura (como a migração do módulo de relatórios), siga estas etapas adicionais:

1. Atualize seu repositório:
   ```bash
   git pull
   ```

2. Instale quaisquer novas dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Aplique as migrações para garantir que seu banco de dados esteja sincronizado:
   ```bash
   python manage.py migrate
   ```

4. Se encontrar erros durante a migração relacionados a modelos que foram movidos (como ConfiguracaoRelatorio), pode ser necessário usar a opção de migração fake:
   ```bash
   python manage.py migrate analises --fake
   python manage.py migrate relatorios
   ```

5. Limpe os arquivos de cache Python:
   ```bash
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -delete
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
- `relatorios/` - Aplicação para geração e visualização de relatórios
- `templates/static/geral/js/` - Código JavaScript global
- `relatorios/static/relatorios/js/` - Código JavaScript específico para relatórios
- `tests/js/` - Testes JavaScript
- `docs/` - Documentação adicional

## Documentação Adicional

- [Relatório de Melhorias JavaScript](docs/relatorio_melhorias_javascript.md)
- [Documentação JavaScript](templates/static/geral/js/README.md)
- [Módulo de Relatórios](docs/modulo_relatorios.md)
- [Changelog](CHANGELOG.md)
