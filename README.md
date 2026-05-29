# Ticket Management API

API RESTful para gestão de chamados técnicos, desenvolvida com Django e Django Rest Framework. O sistema permite que clientes abram chamados e que atendentes acompanhem, classifiquem e atualizem o andamento das solicitações.

---

## Índice

- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Executando com Docker](#executando-com-docker)
- [Executando localmente](#executando-localmente)
- [Testes](#testes)
- [Frontend](#frontend)
- [Endpoints](#endpoints)
- [Autenticação](#autenticação)
- [Perfis de acesso](#perfis-de-acesso)
- [CI/CD](#cicd)

---

## Tecnologias

- Python 3.11
- Django 5 e Django Rest Framework
- PostgreSQL 15
- Docker e Docker Compose
- GitHub Actions
- SimpleJWT para autenticação
- drf-spectacular para documentação automática (Swagger)
- pytest e factory-boy para testes

---

## Requisitos

Para rodar com Docker:

- Docker 20+
- Docker Compose 2+

Para rodar localmente sem Docker:

- Python 3.11
- PostgreSQL 15

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/AlexRodrigues2004/ticket-management-api.git
cd ticket-management-api
```

Copie o arquivo de variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o `.env` com as configurações do seu ambiente antes de prosseguir.

---

## Variáveis de ambiente

O arquivo `.env.example` contém todas as variáveis necessárias:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

DB_ENGINE=django.db.backends.postgresql
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Em produção, defina `DEBUG=False` e configure `ALLOWED_HOSTS` com o domínio real da aplicação. A variável `DATABASE_URL` também é suportada e tem precedência sobre as variáveis individuais de banco, no formato:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

---

## Executando com Docker

Com o `.env` configurado, suba os containers:

```bash
docker compose up --build
```

O comando sobe o banco PostgreSQL e a aplicação Django. As migrations são executadas automaticamente na inicialização.

Para rodar em background:

```bash
docker compose up -d --build
```

Para criar o superusuário:

```bash
docker compose exec web python manage.py createsuperuser
```

Para parar os containers:

```bash
docker compose down
```

Para parar e remover os volumes (apaga os dados do banco):

```bash
docker compose down --volumes
```

A aplicação ficará disponível em:

- API: http://localhost:8000/api/
- Documentação Swagger: http://localhost:8000/api/docs/
- Painel administrativo: http://localhost:8000/admin/

---

## Executando localmente

Crie e ative o ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux e macOS
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o `.env` apontando para um PostgreSQL local ou altere `DB_ENGINE` para `django.db.backends.sqlite3` e `DB_NAME` para `db.sqlite3` para usar SQLite durante o desenvolvimento.

Execute as migrations:

```bash
python manage.py migrate
```

Crie o superusuário:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

---

## Testes

Os testes cobrem criação de registros, validações de serializers, regras de permissão e fluxos principais dos chamados. A cobertura atual é de 90%.

Para rodar os testes com Docker:

```bash
docker compose exec web pytest tests/ -v
```

Para rodar localmente:

```bash
pytest tests/ -v
```

O relatório de cobertura em HTML é gerado automaticamente na pasta `htmlcov/`. Para visualizar, abra `htmlcov/index.html` no navegador.

---

## Frontend

O frontend é uma interface HTML estática que consome todos os endpoints da API. Não requer instalação adicional.

Com o backend rodando, abra o arquivo `frontend/index.html` diretamente no navegador ou use a extensão Live Server do VS Code para evitar problemas de CORS.

Telas disponíveis:

- Login
- Dashboard com resumo dos chamados
- Listagem, criação e filtros de chamados
- Detalhe do chamado com histórico de interações
- Gestão de clientes
- Gestão de categorias
- Listagem de usuários (restrita ao perfil admin)

---

## Endpoints

### Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | /api/auth/register/ | Cadastro de usuário | Não |
| POST | /api/auth/login/ | Login, retorna token JWT | Não |
| POST | /api/auth/refresh/ | Renovação do token | Não |
| GET | /api/auth/me/ | Dados do usuário autenticado | Sim |
| POST | /api/auth/change-password/ | Alteração de senha | Sim |

### Clientes

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/customers/ | Listagem de clientes |
| POST | /api/customers/ | Criação de cliente |
| GET | /api/customers/{id}/ | Detalhes de um cliente |
| PUT/PATCH | /api/customers/{id}/ | Atualização de cliente |
| DELETE | /api/customers/{id}/ | Remoção de cliente |

### Categorias

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/categories/ | Listagem de categorias |
| POST | /api/categories/ | Criação de categoria |
| GET | /api/categories/{id}/ | Detalhes de uma categoria |
| PUT/PATCH | /api/categories/{id}/ | Atualização de categoria |
| DELETE | /api/categories/{id}/ | Remoção de categoria |

### Chamados

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/tickets/ | Listagem de chamados |
| POST | /api/tickets/ | Criação de chamado |
| GET | /api/tickets/{id}/ | Detalhes de um chamado |
| PUT/PATCH | /api/tickets/{id}/ | Atualização de chamado |
| DELETE | /api/tickets/{id}/ | Remoção de chamado |
| PATCH | /api/tickets/{id}/status/ | Atualização de status e prioridade |
| GET | /api/tickets/{id}/interactions/ | Listagem de interações |
| POST | /api/tickets/{id}/interactions/ | Criação de interação |

### Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/users/ | Listagem de usuários |
| GET | /api/users/{id}/ | Detalhes de um usuário |

### Filtros disponíveis em /api/tickets/

A listagem de chamados aceita os seguintes parâmetros de query:

| Parâmetro | Exemplo | Descrição |
|-----------|---------|-----------|
| status | ?status=aberto | Filtra por status |
| priority | ?priority=alta | Filtra por prioridade |
| category | ?category=1 | Filtra por categoria |
| customer | ?customer=1 | Filtra por cliente |
| search | ?search=erro | Busca em título e descrição |
| ordering | ?ordering=-opened_at | Ordenação por campo |

---

## Autenticação

A API utiliza JWT. Para autenticar as requisições, inclua o header:

```
Authorization: Bearer <access_token>
```

O token de acesso é obtido no endpoint `/api/auth/login/` e tem validade de 5 minutos por padrão. Use o endpoint `/api/auth/refresh/` com o `refresh_token` para renovar o acesso sem precisar fazer login novamente.

Exemplo de login:

```json
POST /api/auth/login/
{
    "username": "usuario",
    "password": "senha"
}
```

Resposta:

```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

---

## Perfis de acesso

O sistema possui três perfis de usuário, definidos no campo `role` do cadastro.

O perfil `cliente` pode abrir chamados e visualizar apenas os próprios chamados e suas interações.

O perfil `atendente` pode visualizar todos os chamados, alterar status, prioridade e responsável, além de registrar interações.

O perfil `admin` tem acesso total, incluindo remoção de registros, acesso ao painel administrativo e listagem de usuários.

---

## CI/CD

### Integração contínua

O arquivo `.github/workflows/ci.yml` configura a pipeline de CI, que executa automaticamente a cada push nas branches `main` e `feature/**` e em pull requests para a `main`.

A pipeline executa as seguintes etapas:

1. Checkout do código
2. Configuração do Python 3.11
3. Instalação das dependências
4. Verificação do projeto com `manage.py check`
5. Execução das migrations
6. Execução dos testes com relatório de cobertura
7. Verificação de qualidade de código com flake8

### Entrega contínua

O arquivo `.github/workflows/cd.yml` configura a pipeline de CD, que executa automaticamente a cada push na branch `main`.

A estratégia adotada é o build e publicação da imagem Docker no GitHub Container Registry. A cada execução, a imagem é publicada com as tags `latest` e `sha-<commit>`.

A imagem está disponível em:

```
ghcr.io/alexrodrigues2004/ticket-management-api:latest
```

Para usar a imagem publicada:

```bash
docker pull ghcr.io/alexrodrigues2004/ticket-management-api:latest
```

---

## Estrutura do projeto

```
ticket-management-api/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── permissions.py
├── users/
├── customers/
├── categories/
├── tickets/
├── interactions/
├── tests/
│   ├── factories.py
│   ├── test_customers.py
│   ├── test_categories.py
│   ├── test_tickets.py
│   └── test_interactions.py
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── tickets.html
│   ├── ticket-detail.html
│   ├── customers.html
│   ├── categories.html
│   ├── users.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       ├── auth.js
│       ├── dashboard.js
│       ├── tickets.js
│       ├── customers.js
│       └── categories.js
├── .env.example
├── .coveragerc
├── .flake8
├── build.sh
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pytest.ini
└── requirements.txt
```
