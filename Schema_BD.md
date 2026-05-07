# Centrix — Schema do Banco de Dados (PostgreSQL)

## Visão geral

O banco de dados do Centrix modela a gestão de condomínios, incluindo contratos de serviços, usuários internos, síndicos e gerentes. O banco é PostgreSQL e é consultado via SQL gerado por uma LLM a partir de perguntas em linguagem natural.

## Tabelas

### condominios
Tabela central do sistema. Armazena os condomínios gerenciados.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_cond | SERIAL | PRIMARY KEY |
| nome_cond | VARCHAR(100) | NOT NULL |
| cnpj | CHAR(14) | NOT NULL, UNIQUE, CHECK(length = 14) |
| cep | CHAR(8) | NOT NULL, CHECK(length = 8) |
| endereco | VARCHAR(100) | NOT NULL |
| capacidade_habitacional | INT | — |
| id_sindico | INT | FK -> sindico(id_sindico) |
| id_gerente | INT | FK -> gerente(id_gerente) | 

### gerente
Gerentes responsáveis por condomínios.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_gerente | SERIAL | PRIMARY KEY |
| nome_gerente | VARCHAR(100) | NOT NULL |
| email_gerente | VARCHAR(100) | NOT NULL |
| telefone_gerente | CHAR(11) | NOT NULL, CHECK(length = 11) |

### sindico
Síndicos dos condomínios.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_sindico | SERIAL | PRIMARY KEY |
| nome_sindico | VARCHAR(100) | NOT NULL |
| email_sindico | VARCHAR(100) | NOT NULL |
| telefone_sindico | CHAR(11) | NOT NULL, CHECK(length = 11) |

### servico
Tipos de serviço que podem ser contratados por condomínios.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_servico | SERIAL | PRIMARY KEY |
| nome_servico | VARCHAR(100) | NOT NULL |

### status_contrato
Tabela de lookup para status possíveis de um contrato (ex: ativo, cancelado, vencido).

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_status | SERIAL | PRIMARY KEY |
| nome_status | VARCHAR(100) | NOT NULL |

### contrato
Contratos de serviço vinculados a condomínios. Cada contrato tem um serviço, um status, período de vigência e pode ter uma cortesia.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_contrato | SERIAL | PRIMARY KEY |
| id_status | INT | FK → status_contrato(id_status) |
| data_inicio | DATE | — |
| data_fim | DATE | — |
| servico_id | INT | FK → servico(id_servico) |
| cortesia | VARCHAR(100) | — |
| id_cond | INT | FK → condominios(id_cond) |

### usuario
Usuários internos do sistema (funcionários da empresa).

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_user | SERIAL | PRIMARY KEY |
| nome_user | VARCHAR(100) | NOT NULL |
| id_departamento | INT | NOT NULL, FK → departamento(id_departamento) |

### departamento
Departamentos da empresa.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_departamento | SERIAL | PRIMARY KEY |
| nome_departamento | VARCHAR(100) | NOT NULL |

### cargo
Cargos que podem ser atribuídos a usuários.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_cargo | SERIAL | PRIMARY KEY |
| nome_cargo | VARCHAR(100) | NOT NULL |

### usuario_cargo (tabela associativa)
Relacionamento N:N entre usuários e cargos. Um usuário pode ter múltiplos cargos.

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id_cargo | INT | NOT NULL, FK → cargo(id_cargo) |
| id_user | INT | NOT NULL, FK → usuario(id_user) |

## Relacionamentos

- **condominios → contrato**: um condomínio pode ter vários contratos (1:N via id_cond)
- **condominios ↔ gerente**: relação N:1. Um gerente pode ser gerente de varios cond 
- **condominios ↔ sindico**: relação N:1 Um sindico pode ser sindico de varios cond 
- **contrato → servico**: cada contrato tem um serviço (N:1 via servico_id)
- **contrato → status_contrato**: cada contrato tem um status (N:1 via id_status)
- **usuario → departamento**: cada usuário pertence a um departamento (N:1 via id_departamento)
- **usuario ↔ cargo**: relação N:N via tabela usuario_cargo

## Exemplos de perguntas que o Centrix deve responder

Baseado neste schema, a LLM deve ser capaz de gerar SQL para perguntas como:

- "Quantos condomínios temos cadastrados?"
- "Quais contratos estão ativos?"
- "Quem é o gerente do condomínio X?"
- "Quais serviços o condomínio Y contratou?"
- "Quantos contratos vencem neste mês?"
- "Quais usuários são do departamento financeiro?"
- "Qual condomínio tem a maior capacidade habitacional?"
- "Liste os condomínios que não têm síndico atribuído."
- "Quais contratos incluem cortesia?"
- "Quais gerentes cuidam de mais de um condomínio?"

## Observações técnicas

- O banco é PostgreSQL. Funções como CURRENT_DATE, EXTRACT(), TO_CHAR() são válidas.
- CNPJ é armazenado sem pontuação (14 dígitos puros). CEP também sem pontuação (8 dígitos).
- Telefones são armazenados com 11 dígitos (DDD + número), sem formatação.
- As tabelas associativas (usuario_cargo, condominio_gerente, condominio_sindico) não possuem PRIMARY KEY composta definida explicitamente — considerar adicionar no futuro.
- A coluna "email" na tabela gerente está nomeada como "email_gerente" no ALTER TABLE (possível divergência com o CREATE TABLE que usa "eamil" — provável typo no CREATE original).
