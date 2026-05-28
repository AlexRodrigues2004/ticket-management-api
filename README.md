# Ticket Management API

API RESTful de Gestão de Chamados Técnicos desenvolvida com Django, DRF, PostgreSQL, Docker e CI/CD.

---

## Tecnologias

- Python 3.11
- Django 5 + Django Rest Framework
- PostgreSQL 15
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- JWT Authentication (SimpleJWT)
- Swagger (drf-spectacular)
- pytest + factory-boy + faker

---

## Status das Etapas

| Etapa | Branch | Status |
|-------|--------|--------|
| Parte 1 – Estrutura inicial | feature/parte-1-estrutura-inicial | ✅ Concluída |
| Parte 2 – Models | feature/parte-2-models | ✅ Concluída |
| Parte 3 – Serializers | feature/parte-3-serializers | ✅ Concluída |
| Parte 4 – ViewSets e Rotas | feature/parte-4-viewsets | ✅ Concluída |
| Parte 5 – Testes | feature/parte-5-testes | ✅ Concluída |
| Parte 6 – Docker | feature/parte-6-docker | ✅ Concluída |
| Parte 7 – CI GitHub Actions | feature/parte-7-ci | ✅ Concluída |
| Parte 8 – CD | feature/parte-8-cd | ✅ Concluída |
| Parte 9 – Documentação final | feature/parte-9-docs | ✅ Concluída |

---

## Estrutura do Projeto
ticket-management-api/
├── core/                  # Configurações principais (settings, urls, permissions)
├── users/                 # App de usuários e autenticação
├── customers/             # App de clientes
├── categories/            # App de categorias
├── tickets/               # App de chamados
├── interactions/          # App de interações nos chamados
├── tests/                 # Testes automatizados
├── .github/workflows/     # Pipelines CI/CD
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## Perfis de Usuário

| Perfil | Permissões |
|--------|-----------|
| `cliente` | Abre chamados, visualiza apenas os próprios chamados |
| `atendente` | Visualiza todos os chamados, altera status e prioridade |
| `admin` | Acesso total, pode deletar registros |

---

## Como rodar localmente (sem Docker)

### Pré-requisitos
- Python 3.11
- PostgreSQL instalado e rodando

```bash
# 1. Clone o repositório
git clone https://github.com/AlexRodrigues2004/ticket-management-api.git
cd ticket-management-api

# 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite o .env com suas configurações de banco

# 5. Rode as migrations
python manage.py migrate

# 6. Crie o superusuário
python manage.py createsuperuser

# 7. Inicie o servidor
python manage.py runserver
```

---

## Como rodar com Docker Compose

```bash
# 1. Clone o repositório
git clone https://github.com/AlexRodrigues2004/ticket-management-api.git
cd ticket-management-api

# 2. Copie o .env
cp .env.example .env

# 3. Suba os containers
docker compose up --build

# 4. Crie o superusuário (outro terminal)
docker compose exec web python manage.py createsuperuser

# 5. Acesse
# Swagger: http://localhost:8000/api/docs/
# Admin:   http://localhost:8000/admin/
```

---

## Como executar as migrations

```bash
# Com Docker
docker compose exec web python manage.py migrate

# Sem Docker
python manage.py migrate
```

---

## Como rodar os testes

```bash
# Com Docker
docker compose exec web pytest tests/ -v

# Sem Docker
pytest tests/ -v
```

> 22 testes cobrindo: customers, categories, tickets, interactions, permissões e filtros.

---

## Endpoints principais

### Autenticação
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | /api/auth/register/ | Cadastro de usuário | ❌ |
| POST | /api/auth/login/ | Login (retorna JWT) | ❌ |
| POST | /api/auth/refresh/ | Refresh do token | ❌ |
| GET | /api/auth/me/ | Dados do usuário logado | ✅ |
| POST | /api/auth/change-password/ | Alterar senha | ✅ |

### Clientes
| Método | Endpoint | Descrição | Perfil |
|--------|----------|-----------|--------|
| GET | /api/customers/ | Listar clientes | Todos |
| POST | /api/customers/ | Criar cliente | Atendente/Admin |
| GET | /api/customers/{id}/ | Detalhe do cliente | Todos |
| PUT/PATCH | /api/customers/{id}/ | Atualizar cliente | Atendente/Admin |
| DELETE | /api/customers/{id}/ | Remover cliente | Admin |

### Categorias
| Método | Endpoint | Descrição | Perfil |
|--------|----------|-----------|--------|
| GET | /api/categories/ | Listar categorias | Todos |
| POST | /api/categories/ | Criar categoria | Atendente/Admin |
| GET | /api/categories/{id}/ | Detalhe da categoria | Todos |
| PUT/PATCH | /api/categories/{id}/ | Atualizar categoria | Atendente/Admin |
| DELETE | /api/categories/{id}/ | Remover categoria | Admin |

### Chamados
| Método | Endpoint | Descrição | Perfil |
|--------|----------|-----------|--------|
| GET | /api/tickets/ | Listar chamados | Todos* |
| POST | /api/tickets/ | Criar chamado | Todos |
| GET | /api/tickets/{id}/ | Detalhe do chamado | Todos* |
| PUT/PATCH | /api/tickets/{id}/ | Atualizar chamado | Todos* |
| DELETE | /api/tickets/{id}/ | Remover chamado | Admin |
| PATCH | /api/tickets/{id}/status/ | Alterar status/prioridade | Atendente/Admin |
| GET | /api/tickets/{id}/interactions/ | Listar interações | Todos* |
| POST | /api/tickets/{id}/interactions/ | Criar interação | Todos |

> *Clientes veem apenas os próprios chamados.

### Filtros disponíveis em /api/tickets/
| Parâmetro | Exemplo |
|-----------|---------|
| status | ?status=aberto |
| priority | ?priority=alta |
| category | ?category=1 |
| customer | ?customer=1 |
| search | ?search=erro |
| ordering | ?ordering=-opened_at |

---

## Exemplos de requisições

### Login
```json
POST /api/auth/login/
{
  "username": "jones",
  "password": "sua_senha"
}
```

### Criar chamado
```json
POST /api/tickets/
Authorization: Bearer <token>
{
  "title": "Erro no sistema de pagamento",
  "description": "O sistema não processa pagamentos via PIX",
  "customer": 1,
  "category": 2,
  "priority": "alta"
}
```

### Alterar status
```json
PATCH /api/tickets/1/status/
Authorization: Bearer <token>
{
  "status": "em_atendimento",
  "assigned_to": 3
}
```

### Adicionar interação
```json
POST /api/tickets/1/interactions/
Authorization: Bearer <token>
{
  "message": "Estamos investigando o problema."
}
```

---

## Como funciona o CI

Pipeline configurada em `.github/workflows/ci.yml`.
Executa automaticamente a cada push nas branches `main` e `feature/**`.

Etapas:
1. Checkout do código
2. Configuração do Python 3.11
3. Instalação das dependências
4. Verificação do projeto Django
5. Execução das migrations
6. Execução dos testes (pytest)
7. Verificação de qualidade (flake8)

---

## Como funciona o CD

Pipeline configurada em `.github/workflows/cd.yml`.
Executa automaticamente a cada push na branch `main`.

Estratégia: **Build e publicação de imagem Docker no GitHub Container Registry (ghcr.io)**.

Etapas:
1. Login no GitHub Container Registry
2. Build da imagem Docker
3. Push com tags `latest` e `sha-<commit>`

Imagem disponível em:
ghcr.io/alexrodrigues2004/ticket-management-api:latest

Para usar:
```bash
docker pull ghcr.io/alexrodrigues2004/ticket-management-api:latest
```

---

## Observação sobre Docker no Windows

Este projeto usa `python:3.11-bullseye` e `postgres:15-bullseye` por compatibilidade
com processadores mais antigos (ex: Xeon E5 v3) que não suportam instruções AVX
presentes nas imagens `-slim`.

---

## Contexto para retomada em novo chat

Projeto: API de gestão de chamados técnicos (Django + DRF + PostgreSQL + Docker).
Repositório: https://github.com/AlexRodrigues2004/ticket-management-api
Situação: PROJETO CONCLUÍDO — todas as 9 partes implementadas e mergeadas na main.
Stack: Python 3.11, Django 5, DRF, PostgreSQL 15, Docker, GitHub Actions CI/CD, JWT, Swagger.
Testes: 22 testes passando com pytest.
CI: GitHub Actions rodando testes + flake8 a cada push.
CD: Build e push automático de imagem Docker no ghcr.io a cada push na main.
Imagem base Docker: python:3.11-bullseye (compatibilidade Xeon E5 v3).
Para rodar: docker compose up --build
Para testar: docker compose exec web pytest tests/ -v
Swagger: http://localhost:8000/api/docs/