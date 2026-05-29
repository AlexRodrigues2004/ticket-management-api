# Ticket Management API

API RESTful para gestão de chamados técnicos de suporte.

## Stack

- Python 3.11, Django 5, Django Rest Framework
- PostgreSQL 15
- Docker, Docker Compose
- GitHub Actions (CI/CD)
- JWT (SimpleJWT)
- Swagger (drf-spectacular)
- pytest, factory-boy

## Estrutura
ticket-management-api/
├── core/           # Configuracoes principais
├── users/          # Usuarios e autenticacao
├── customers/      # Clientes
├── categories/     # Categorias
├── tickets/        # Chamados
├── interactions/   # Interacoes nos chamados
├── tests/          # Testes automatizados
├── frontend/       # Interface HTML
└── .github/        # Pipelines CI/CD

## Perfis de acesso

| Perfil | Permissoes |
|--------|-----------|
| cliente | Abre e visualiza os proprios chamados |
| atendente | Visualiza todos os chamados, altera status e prioridade |
| admin | Acesso total |

## Como rodar

```bash
cp .env.example .env
docker compose up --build
```

Criar superusuario:
```bash
docker compose exec web python manage.py createsuperuser
```

Acessos:
- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/
- Frontend: abrir frontend/index.html no navegador

## Testes

```bash
docker compose exec web pytest tests/ -v
```

## Endpoints

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| POST | /api/auth/register/ | Cadastro |
| POST | /api/auth/login/ | Login |
| GET | /api/auth/me/ | Usuario logado |
| GET/POST | /api/customers/ | Clientes |
| GET/POST | /api/categories/ | Categorias |
| GET/POST | /api/tickets/ | Chamados |
| PATCH | /api/tickets/{id}/status/ | Atualizar status |
| GET/POST | /api/tickets/{id}/interactions/ | Interacoes |

## CI/CD

- CI: testes e linting a cada push via GitHub Actions
- CD: build e push da imagem Docker no ghcr.io a cada push na main

Imagem:
ghcr.io/alexrodrigues2004/ticket-management-api:latest

