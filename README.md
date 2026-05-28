# Ticket Management API

API RESTful de Gestão de Chamados Técnicos desenvolvida com Django, DRF, PostgreSQL, Docker e CI/CD.

## Tecnologias
- Python 3.11 + Django 5 + Django Rest Framework
- PostgreSQL 15
- Docker + Docker Compose
- GitHub Actions (CI)
- JWT Authentication (SimpleJWT)
- Swagger/Redoc (drf-spectacular)
- pytest + factory-boy

## Status das Etapas

| Etapa | Branch | Status |
|-------|--------|--------|
| Parte 1 – Estrutura inicial | feature/parte-1-estrutura-inicial | ✅ Concluída |
| Parte 2 – Models | feature/parte-2-models | ✅ Concluída |
| Parte 3 – Serializers | feature/parte-3-serializers | ✅ Concluída |
| Parte 4 – ViewSets e Rotas | feature/parte-4-viewsets | ✅ Concluída |
| Parte 5 – Testes | feature/parte-5-testes | ✅ Concluída |
| Parte 6 – Docker | feature/parte-6-docker | ✅ Concluída |
| Parte 7 – CI GitHub Actions | feature/parte-7-ci | ⏳ Pendente |
| Parte 8 – CD | feature/parte-8-cd | ⏳ Pendente |
| Parte 9 – Documentação final | feature/parte-9-docs | ⏳ Pendente |

## Como rodar com Docker Compose

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/ticket-management-api.git
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

## Como rodar os testes

```bash
docker compose exec web pytest tests/ -v
```

## Endpoints principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/auth/register/ | Cadastro de usuário |
| POST | /api/auth/login/ | Login (retorna JWT) |
| POST | /api/auth/refresh/ | Refresh do token |
| GET | /api/auth/me/ | Dados do usuário logado |
| GET/POST | /api/customers/ | Listar/criar clientes |
| GET/PUT/DELETE | /api/customers/{id}/ | Detalhe do cliente |
| GET/POST | /api/categories/ | Listar/criar categorias |
| GET/PUT/DELETE | /api/categories/{id}/ | Detalhe da categoria |
| GET/POST | /api/tickets/ | Listar/criar chamados |
| GET/PUT/DELETE | /api/tickets/{id}/ | Detalhe do chamado |
| PATCH | /api/tickets/{id}/status/ | Alterar status/prioridade |
| GET/POST | /api/tickets/{id}/interactions/ | Interações do chamado |

## Observação sobre Docker no Windows

Este projeto usa `python:3.11-bullseye` e `postgres:15-bullseye` por compatibilidade
com processadores mais antigos (ex: Xeon E5 v3) que não suportam certas instruções
das imagens `-slim`.

## Contexto para retomada em novo chat

Projeto: API de gestão de chamados técnicos (Django + DRF + PostgreSQL + Docker).
Repositório: https://github.com/SEU_USUARIO/ticket-management-api
Situação atual: Partes 1-6 concluídas e mergeadas na main.
Próximo passo: Parte 7 — CI com GitHub Actions (.github/workflows/ci.yml).
O projeto roda com `docker compose up --build`. Testes: `docker compose exec web pytest tests/ -v`.
22 testes passando. Imagem base: python:3.11-bullseye (compatibilidade Xeon E5 v3).