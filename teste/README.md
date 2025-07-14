# Testes Automatizados - QualiSoja

Esta pasta contém scripts de teste automatizados para validar o funcionamento dos módulos do sistema QualiSoja.

## Estrutura dos Testes

```
teste/
├── README.md                 # Este arquivo
├── executar_testes.py       # Script principal que executa todos os testes
├── teste_analises.py        # Testes específicos do módulo de análises
└── teste_relatorios.py      # Testes específicos do módulo de relatórios
```

## Como Executar

### Executar Todos os Testes
```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar suíte completa de testes
python teste\executar_testes.py
```

### Executar Testes Específicos

#### Apenas Testes de Análises
```bash
python teste\teste_analises.py
```

#### Apenas Testes de Relatórios
```bash
python teste\teste_relatorios.py
```

## O Que os Testes Validam

### Teste de Análises (`teste_analises.py`)
- ✅ Criação de análises (CRUD completo)
- ✅ Validação de campos obrigatórios
- ✅ Validação de regras de negócio (datas futuras, valores negativos)
- ✅ Consultas complexas e filtros
- ✅ Funcionalidade de todos os tipos de análise:
  - AnaliseUmidade
  - AnaliseProteina
  - AnaliseOleoDegomado
  - AnaliseFibra
  - AnaliseCinza
  - AnaliseTeorOleo
  - AnaliseUrase
  - AnaliseSilica

### Teste de Relatórios (`teste_relatorios.py`)
- ✅ Criação de relatórios de expedição
- ✅ Relatórios com análises específicas selecionadas
- ✅ Consultas e filtros de relatórios
- ✅ Atualização de status (RASCUNHO → GERADO → ENVIADO)
- ✅ Manipulação de campos JSON
- ✅ Exclusão de relatórios
- ✅ Integração com análises existentes

### Teste de Integração (`executar_testes.py`)
- ✅ Conexão com banco de dados
- ✅ Funcionamento dos modelos Django
- ✅ Integração entre módulos (análises ↔ relatórios)
- ✅ Criação de dados relacionados
- ✅ Relatório completo de resultados

## Interpretando os Resultados

### Símbolos dos Resultados
- ✅ **Teste passou**: Funcionalidade está working corretamente
- ❌ **Teste falhou**: Problema encontrado que precisa correção
- ⚠️ **Aviso**: Teste passou mas com ressalvas

### Exemplo de Saída
```
=== INICIANDO TESTES DE ANÁLISES ===
--- Testando AnaliseUmidade ---
✅ Criado: AnaliseUmidade ID 123 - 12.35%
✅ Lido: FL - 12.35%
✅ Atualizado: Resultado alterado para 13.45%
✅ Deletado: AnaliseUmidade ID 123

=== RESUMO DOS TESTES ===
Total de testes: 6
Sucessos: 6
Falhas: 0
🎉 TODOS OS TESTES PASSARAM!
```

## Configuração dos Testes

### Pré-requisitos
1. Ambiente virtual ativado
2. Django configurado corretamente
3. Banco de dados acessível
4. Migrações aplicadas

### Dados de Teste
- Os testes criam dados temporários automaticamente
- Todos os dados são limpos após os testes
- Usuários de teste são criados conforme necessário:
  - `teste_usuario` (para análises)
  - `teste_relatorio` (para relatórios)
  - `integracao_teste` (para testes de integração)

## Resolução de Problemas

### Erro de Conexão com Banco
```
❌ Erro na conexão com banco: ...
```
**Solução**: Verificar se o banco de dados está acessível e as configurações em `settings.py` estão corretas.

### Erro de Migração
```
❌ Erro: no such column: ...
```
**Solução**: Executar migrações pendentes:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erro de Importação
```
❌ ModuleNotFoundError: No module named '...'
```
**Solução**: Verificar se o ambiente virtual está ativado e todas as dependências instaladas.

## Adicionando Novos Testes

### Para Análises
Edite `teste_analises.py` e adicione métodos seguindo o padrão:
```python
def testar_nova_funcionalidade(self):
    print("\n--- Testando Nova Funcionalidade ---")
    try:
        # Seu código de teste aqui
        print("✅ Teste passou")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
```

### Para Relatórios
Edite `teste_relatorios.py` seguindo a mesma estrutura.

### Para Integração
Edite o método `executar_testes_integracao()` em `executar_testes.py`.

## Integração Contínua

Os testes podem ser integrados em CI/CD:

```bash
# Script para CI
cd /caminho/para/projeto
source venv/bin/activate  # Linux/Mac
# ou .\venv\Scripts\Activate.ps1  # Windows
python teste/executar_testes.py
```

**Códigos de saída:**
- `0`: Todos os testes passaram
- `1`: Alguns testes falharam
- `2`: Testes interrompidos pelo usuário
- `3`: Erro crítico no sistema

## Observações Importantes

1. **Ambiente de Teste**: Execute sempre em ambiente de desenvolvimento/teste
2. **Backup**: Faça backup dos dados antes de executar em produção
3. **Performance**: Testes podem demorar alguns minutos dependendo do tamanho do banco
4. **Logs**: Logs detalhados são exibidos no console para debug

## Contato

Se encontrar problemas ou tiver sugestões para melhorar os testes, documente no sistema ou entre em contato com a equipe de desenvolvimento.
