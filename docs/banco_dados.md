# Documentação do Banco de Dados - QualiSoja

## Visão Geral

O sistema QualiSoja utiliza um banco de dados relacional para armazenar informações sobre análises de proteína, umidade e outros parâmetros de qualidade da soja. Esta documentação descreve a estrutura do banco de dados, relacionamentos entre tabelas e informações importantes para desenvolvedores.

## Tecnologia

- **Desenvolvimento:** SQLite
- **Produção:** PostgreSQL (recomendado)

## Esquema do Banco de Dados

### Tabela: analises_analiseumidade

Armazena as análises de umidade realizadas em diferentes tipos de amostras.

| Coluna           | Tipo           | Restrições        | Descrição                                  |
|------------------|----------------|-------------------|-------------------------------------------|
| id               | INTEGER        | PK, AUTOINCREMENT | Identificador único                        |
| criado_em        | DATETIME       | NOT NULL          | Data e hora de criação do registro        |
| atualizado_em    | DATETIME       | NOT NULL          | Data e hora da última atualização         |
| data             | DATE           | NOT NULL          | Data da análise                           |
| horario          | TIME           | NOT NULL          | Horário da análise                        |
| tipo_amostra     | VARCHAR(2)     | NOT NULL          | Tipo de amostra (FG, FF, SI, PE)          |
| tara             | DECIMAL(10,2)  | NULL              | Tara do recipiente                        |
| liquido          | DECIMAL(10,2)  | NULL              | Peso líquido                              |
| peso_amostra     | DECIMAL(10,2)  | NOT NULL          | Peso da amostra                           |
| resultado        | DECIMAL(10,2)  | NULL              | Resultado da análise (%)                  |
| fator_correcao   | DECIMAL(10,2)  | NULL              | Fator de correção aplicado                |

**Tipos de amostra:**
- FG: Farelo Grosso
- FF: Farelo Fino
- SI: Soja Industrializada
- PE: Peletizado

### Tabela: analises_analiseproteina

Armazena as análises de proteína realizadas em diferentes tipos de amostras.

| Coluna            | Tipo           | Restrições        | Descrição                                  |
|-------------------|----------------|-------------------|-------------------------------------------|
| id                | INTEGER        | PK, AUTOINCREMENT | Identificador único                        |
| criado_em         | DATETIME       | NOT NULL          | Data e hora de criação do registro        |
| atualizado_em     | DATETIME       | NOT NULL          | Data e hora da última atualização         |
| data              | DATE           | NOT NULL          | Data da análise                           |
| horario           | TIME           | NOT NULL          | Horário da análise                        |
| tipo_amostra      | VARCHAR(2)     | NOT NULL          | Tipo de amostra (FL, SI)                  |
| peso_amostra      | DECIMAL(4,2)   | NOT NULL          | Peso da amostra em gramas                 |
| ml_gasto          | DECIMAL(6,2)   | NULL              | Mililitros gastos na titulação            |
| resultado         | DECIMAL(5,2)   | NULL              | Resultado da análise (%)                  |
| resultado_corrigido | DECIMAL(5,2) | NULL              | Resultado corrigido (%)                    |
| eh_media_24h      | BOOLEAN        | NOT NULL          | Indica se é média de 24h                  |

**Tipos de amostra:**
- FL: Farelo
- SI: Soja Industrializada

### Tabela: analises_configuracaorelatorio

Armazena configurações para geração de relatórios.

| Coluna           | Tipo           | Restrições        | Descrição                                  |
|------------------|----------------|-------------------|-------------------------------------------|
| id               | INTEGER        | PK, AUTOINCREMENT | Identificador único                        |
| criado_em        | DATETIME       | NOT NULL          | Data e hora de criação do registro        |
| atualizado_em    | DATETIME       | NOT NULL          | Data e hora da última atualização         |
| nome             | VARCHAR(100)   | NOT NULL          | Nome do relatório                         |
| tipo_relatorio   | VARCHAR(15)    | NOT NULL          | Tipo de relatório                         |
| periodo_padrao   | INTEGER        | NOT NULL          | Período padrão em dias                    |
| ativo            | BOOLEAN        | NOT NULL          | Indica se a configuração está ativa       |

**Tipos de relatório:**
- UMIDADE: Relatório de Umidade
- PROTEINA: Relatório de Proteína
- COMBINADO: Relatório Combinado

### Tabela: auth_user

Tabela padrão do Django para armazenamento de usuários.

| Coluna           | Tipo           | Restrições        | Descrição                                  |
|------------------|----------------|-------------------|-------------------------------------------|
| id               | INTEGER        | PK, AUTOINCREMENT | Identificador único                        |
| username         | VARCHAR(150)   | UNIQUE, NOT NULL  | Nome de usuário                           |
| email            | VARCHAR(254)   | NOT NULL          | Email do usuário                          |
| password         | VARCHAR(128)   | NOT NULL          | Senha (hash)                              |
| ... (outros campos padrão do Django) ... |

### Tabela: users_profile

Estende o modelo de usuário com campos adicionais.

| Coluna           | Tipo           | Restrições        | Descrição                                  |
|------------------|----------------|-------------------|-------------------------------------------|
| id               | INTEGER        | PK, AUTOINCREMENT | Identificador único                        |
| user_id          | INTEGER        | FK, UNIQUE        | Referência ao usuário (auth_user)         |
| cargo            | VARCHAR(100)   | NULL              | Cargo do usuário                          |
| departamento     | VARCHAR(100)   | NULL              | Departamento do usuário                   |

## Migrações

O sistema utiliza o sistema de migrações do Django para controle de versão do banco de dados.

### Migrações principais

1. `0001_initial.py`: Criação inicial das tabelas
2. `0002_alter_analiseproteina_horario_and_more.py`: Alterações nos campos de horário
3. `0003_alter_analiseproteina_horario_and_more.py`: Ajustes adicionais nos campos de horário

## Índices e Performance

- Índices nas colunas `data` e `tipo_amostra` para otimizar consultas de relatórios
- A coluna `id` em todas as tabelas é indexada por padrão como chave primária

## Integridade Referencial

- A tabela `users_profile` tem uma relação de um-para-um com a tabela `auth_user`
- Restrições de integridade são gerenciadas pelo ORM do Django

## Backup e Restauração

### Backup do SQLite
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Backup via Django (dados em formato JSON)
```bash
python manage.py dumpdata > backup.json
```

### Restauração via Django
```bash
python manage.py loaddata backup.json
```

## Troubleshooting

### Problema: Erro "no such column: analises_analiseproteina.criado_em"

**Solução:**
1. Verificar se as migrações foram aplicadas:
   ```bash
   python manage.py showmigrations analises
   ```

2. Se necessário, corrigir os valores nos campos temporais:
   ```sql
   UPDATE analises_analiseproteina SET criado_em = datetime('now'), atualizado_em = datetime('now');
   UPDATE analises_analiseumidade SET criado_em = datetime('now'), atualizado_em = datetime('now');
   ```

### Problema: Migrações não aplicadas corretamente

**Solução:**
1. Fazer fake das migrações iniciais:
   ```bash
   python manage.py migrate analises --fake
   ```

2. Aplicar as migrações faltantes:
   ```bash
   python manage.py migrate analises
   ```

## Evolução do Banco

Para adicionar novos tipos de análises ao sistema:

1. Criar um novo modelo em `models.py` herdando de `BaseModel`
2. Executar `python manage.py makemigrations`
3. Aplicar as migrações com `python manage.py migrate`
4. Atualizar as views e templates para incluir o novo tipo de análise
