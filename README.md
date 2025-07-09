# Loja de Brinquedos API

Backend Django para gestão de clientes e vendas de uma loja de brinquedos, implementado com Clean Architecture, autenticação JWT e documentação automática.

## 🚀 Sumário
- [Visão geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Diagramas da Aplicação](#diagramas-da-aplicação)
- [Tecnologias](#tecnologias)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Documentação da API](#documentação-da-api)
- [Autenticação JWT](#autenticação-jwt)
- [Testes](#testes)
- [Principais endpoints](#principais-endpoints)
- [Desenvolvimento](#desenvolvimento)

---

## 📋 Visão geral

API RESTful completa para cadastro, edição, listagem e deleção de clientes e vendas, com autenticação JWT, estatísticas avançadas e arquitetura baseada em Clean Architecture.

### ✨ Funcionalidades
- ✅ CRUD completo de clientes
- ✅ Registro e consulta de vendas
- ✅ Estatísticas de vendas por dia
- ✅ Clientes destaque (maior volume, média e frequência)
- ✅ Autenticação JWT segura
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Interface Browsable API do DRF
- ✅ Logs detalhados
- ✅ Clean Architecture

---

## 🏗️ Arquitetura

### Clean Architecture
- **Domain:** Entidades e contratos de repositório (puro Python)
- **Application:** Casos de uso e DTOs
- **Infra:** Models Django, repositórios concretos
- **Interface Adapters:** Serializers, views, rotas

### Estrutura de pastas
```
├── domain/                 # Entidades e contratos
├── application/            # Casos de uso e DTOs
├── infra/                 # Models Django e repositórios
├── interface_adapters/    # Serializers, views, rotas
├── loja_brinquedos/      # Settings, URLs, WSGI
├── tests_curls.md        # Roteiro de testes
└── README.md             # Este arquivo
```

---

## 📊 Diagramas da Aplicação

A aplicação possui uma documentação visual completa através de diagramas que facilitam o entendimento da arquitetura e fluxos do sistema.

### 🎯 Diagramas Disponíveis

#### **1. Clean Architecture** ([Ver diagrama](./docs/diagramas/clean-architecture.md))
- **Arquitetura geral** da aplicação
- **Fluxo de dados** entre camadas
- **Benefícios** da Clean Architecture
- **Separação de responsabilidades**

#### **2. Domain Model** ([Ver diagrama](./docs/diagramas/domain-model.md))
- **Entidades** do domínio (Cliente, Venda)
- **Contratos** de repositório
- **Regras de negócio**
- **Relacionamentos** entre entidades

#### **3. Use Cases** ([Ver diagrama](./docs/diagramas/use-cases.md))
- **Casos de uso** principais
- **Atores** do sistema
- **Fluxos** detalhados
- **Regras de validação**

#### **4. Sequence Diagram** ([Ver diagrama](./docs/diagramas/sequence-diagram.md))
- **Fluxos de sequência** típicos
- **Interação** entre componentes
- **Fluxos de erro**
- **Autenticação JWT**

#### **5. Deployment** ([Ver diagrama](./docs/diagramas/deployment.md))
- **Infraestrutura Docker**
- **Configuração de rede**
- **Volumes e persistência**
- **Segurança e escalabilidade**

### 🔧 Como Usar os Diagramas

#### **Para Desenvolvedores**
- Entender a **arquitetura** do sistema
- Compreender **fluxos** de dados
- Identificar **pontos de extensão**
- Planejar **novas funcionalidades**

#### **Para Arquitetos**
- Avaliar **qualidade** da arquitetura
- Identificar **acoplamentos**
- Sugerir **melhorias**
- Documentar **decisões**

#### **Para Stakeholders**
- Visualizar **funcionalidades**
- Entender **complexidade**
- Planejar **recursos**
- Comunicar **requisitos**

### 📝 Tecnologias dos Diagramas

- **Mermaid**: Linguagem de diagramação
- **Markdown**: Formato de documentação
- **GitHub**: Renderização automática
- **VS Code**: Extensão Mermaid

### 🎨 Convenções Visuais

#### **Cores**
- 🟢 **Verde**: Sucesso, validação
- 🔴 **Vermelho**: Erro, rejeição
- 🔵 **Azul**: Processamento, fluxo
- 🟡 **Amarelo**: Aviso, atenção

#### **Símbolos**
- ✅ **Check**: Implementado
- 🔄 **Loop**: Processo repetitivo
- ⚡ **Lightning**: Operação rápida
- 🔒 **Lock**: Segurança, autenticação

### 📚 Recursos Adicionais

- **Documentação completa**: [docs/diagramas/README.md](./docs/diagramas/README.md)
- **Mermaid Live Editor**: [mermaid.live](https://mermaid.live/)
- **Extensão VS Code**: Mermaid Preview

---

## 🛠️ Tecnologias

- **Backend:** Django 5.2 + Django REST Framework
- **Autenticação:** JWT (djangorestframework-simplejwt)
- **Banco de dados:** PostgreSQL
- **Documentação:** drf-spectacular (Swagger/OpenAPI)
- **Containerização:** Docker + Docker Compose
- **Gerenciamento de dependências:** Poetry
- **Logs:** Logging nativo Python
- **Arquitetura:** Clean Architecture

---

## 🚀 Como rodar o projeto

### Pré-requisitos

#### **Sistema Operacional**
- **Linux:** Ubuntu 20.04+, CentOS 8+, ou similar
- **macOS:** 10.15+ (Catalina) ou superior
- **Windows:** Windows 10/11 com WSL2 ou Docker Desktop

#### **Software Necessário**
- **Docker:** Versão 20.10+ ([Instalar Docker](https://docs.docker.com/get-docker/))
- **Docker Compose:** Versão 2.0+ (incluído no Docker Desktop)
- **Git:** Versão 2.30+ ([Instalar Git](https://git-scm.com/downloads))

#### **Recursos do Sistema**
- **RAM:** Mínimo 4GB, recomendado 8GB+
- **Espaço em disco:** Mínimo 2GB livres
- **CPU:** 2 cores mínimo, 4 cores recomendado

#### **Portas Necessárias**
- **8000:** API Django (HTTP)
- **5432:** PostgreSQL (interno do Docker)

#### **Verificação dos Pré-requisitos**
```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Git
git --version

# Verificar se as portas estão livres
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432
```

#### **Configuração Opcional (Recomendada)**
- **Poetry:** Para desenvolvimento local ([Instalar Poetry](https://python-poetry.org/docs/#installation))
- **VS Code:** Editor recomendado com extensões Python/Django
- **Postman/Insomnia:** Para testar APIs
- **pgAdmin:** Para gerenciar banco PostgreSQL (opcional)

### Passos

1. **Clone o repositório:**
   ```bash
   git clone git@github.com:edwildson/loja_de_brinquedos.git
   cd loja_de_brinquedos
   ```

2. **Crie o arquivo `.env` na raiz:**
   ```env
   DEBUG=1
   SECRET_KEY=changeme
   DJANGO_ALLOWED_HOSTS=*
   DB_NAME=loja_brinquedos
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   ```

3. **Suba os containers:**
   ```bash
   docker-compose build app
   docker-compose up -d
   ```

4. **Colete os arquivos estáticos:**
   ```bash
   docker compose exec app poetry run python manage.py collectstatic
   ```

5. **Aplique as migrations:**
   ```bash
   docker-compose exec app poetry run python manage.py migrate
   ```

6. **Crie um superusuário:**
   ```bash
   docker-compose exec app poetry run python manage.py createsuperuser
   ```

7. **Acesse a API:**
   - **Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - **Documentação:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 📚 Documentação da API

A API possui documentação automática gerada pelo **drf-spectacular**:

### **Swagger UI (Interface Interativa)**
- **URL:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **Recursos:** Interface interativa para testar endpoints, autenticação JWT, exemplos de requisição/resposta

### **ReDoc (Documentação Alternativa)**
- **URL:** [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- **Recursos:** Documentação mais limpa e organizada

### **Schema OpenAPI (JSON)**
- **URL:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
- **Recursos:** Schema completo em formato JSON para integração com ferramentas externas

### **Como usar a documentação:**
1. Acesse [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
2. Clique em **"Authorize"** no topo da página
3. Insira seu JWT token no formato: `Bearer <seu_token>`
4. Explore os endpoints organizados por tags:
   - **clientes:** CRUD de clientes
   - **vendas:** CRUD de vendas
   - **estatísticas:** Endpoints de estatísticas

---

## 🔐 Autenticação JWT

### Obter token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SENHA_DO_ADMIN"}'
```

### Usar token
```bash
curl -X GET http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <access_token>"
```

### Renovar token
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

## �� Testes

### Testes Automatizados

O projeto possui uma suíte completa de testes automatizados organizados por camadas da Clean Architecture:

#### **Executar todos os testes:**
```bash
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings -v
```

#### **Executar testes por camada:**
```bash
# Testes de Domain (Entidades)
docker-compose exec app poetry run pytest tests/domain/ --ds=loja_brinquedos.test_settings -v

# Testes de Application (Use Cases)
docker-compose exec app poetry run pytest tests/application/ --ds=loja_brinquedos.test_settings -v

# Testes de Infrastructure (Repositories)
docker-compose exec app poetry run pytest tests/infra/ --ds=loja_brinquedos.test_settings -v

# Testes de Interface Adapters (Views)
docker-compose exec app poetry run pytest tests/interface_adapters/ --ds=loja_brinquedos.test_settings -v

# Testes de Integração
docker-compose exec app poetry run pytest tests/integration/ --ds=loja_brinquedos.test_settings -v
```

#### **Executar testes específicos:**
```bash
# Teste específico
docker-compose exec app poetry run pytest tests/domain/test_entities.py::TestCliente::test_criar_cliente_valido -v

# Teste com debug
docker-compose exec app poetry run pytest tests/interface_adapters/test_views.py::TestVendaViewSet::test_criar_venda_valida -v -s
```

### Coverage (Cobertura de Código)

#### **Instalar dependência de coverage:**
```bash
docker-compose exec app poetry add pytest-cov --group dev
```

#### **Executar coverage:**
```bash
# Coverage completo
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings --cov=. --cov-report=term-missing

# Coverage por camada
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings --cov=application --cov=domain --cov=infra --cov=interface_adapters --cov-report=term-missing

# Coverage com relatório HTML
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings --cov=. --cov-report=html --cov-report=term-missing
```

#### **Usando coverage diretamente:**
```bash
# Executar testes com coverage
docker-compose exec app python -m coverage run --source=application,domain,infra,interface_adapters -m pytest --ds=loja_brinquedos.test_settings

# Gerar relatório
docker-compose exec app python -m coverage report --show-missing

# Gerar relatório HTML
docker-compose exec app python -m coverage html
```

#### **Configuração do Coverage (.coveragerc):**
```ini
[run]
source = application,domain,infra,interface_adapters
omit = 
    */tests/*
    */migrations/*
    */settings/*
    manage.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### Estrutura dos Testes

```
tests/
├── domain/                    # Testes das entidades
│   └── test_entities.py      # Testes de Cliente e Venda
├── application/               # Testes dos use cases
│   └── test_use_cases.py     # Testes de todos os use cases
├── infra/                    # Testes dos repositories
│   └── test_repositories.py  # Testes dos repositories
├── interface_adapters/        # Testes das views
│   └── test_views.py         # Testes das ViewSets
├── integration/              # Testes de integração
│   └── test_api_integration.py # Testes end-to-end
└── conftest.py              # Configurações e fixtures
```

### Tipos de Testes

#### **Testes Unitários:**
- **Domain:** Validação de entidades, regras de negócio
- **Application:** Use cases, DTOs
- **Infrastructure:** Repositories, models
- **Interface Adapters:** Serializers, views

#### **Testes de Integração:**
- Fluxos completos da API
- Autenticação e autorização
- Endpoints de estatísticas
- Validações e tratamento de erros

#### **Testes de Performance:**
- Criação de múltiplos registros
- Filtros e listagens
- Tempo de resposta

### Comandos Úteis para Testes

```bash
# Executar testes com verbose
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings -v

# Executar testes com stop on first failure
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings -x

# Executar testes com maxfail
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings --maxfail=3

# Executar testes com coverage e mostrar linhas faltantes
docker-compose exec app poetry run pytest --ds=loja_brinquedos.test_settings --cov=. --cov-report=term-missing

# Executar testes específicos com coverage
docker-compose exec app poetry run pytest tests/application/ --ds=loja_brinquedos.test_settings --cov=application --cov-report=term-missing
```

### Testes Manuais

#### **Testes manuais via curl:**
Veja o roteiro completo em [tests_curls.md](./tests_curls.md) para testar todos os fluxos da API passo a passo.

#### **Interface Browsable API:**
- Acesse qualquer endpoint no navegador (ex: `/api/clientes/`)
- Insira o token JWT no campo de autenticação
- Use os botões de método (GET, POST, PUT, DELETE)

---

## 📡 Principais endpoints

### Autenticação
- `POST /api/token/` — Obter token JWT
- `POST /api/token/refresh/` — Renovar token JWT

### Clientes
- `GET /api/clientes/` — Listar clientes
- `POST /api/clientes/` — Criar cliente
- `GET /api/clientes/{id}/` — Obter cliente
- `PUT /api/clientes/{id}/` — Atualizar cliente (completo)
- `PATCH /api/clientes/{id}/` — Atualizar cliente (parcial)
- `DELETE /api/clientes/{id}/` — Deletar cliente

### Vendas
- `GET /api/vendas/` — Listar vendas
- `POST /api/vendas/` — Registrar venda
- `GET /api/vendas/{id}/` — Obter venda
- `PUT /api/vendas/{id}/` — Atualizar venda (completo)
- `PATCH /api/vendas/{id}/` — Atualizar venda (parcial)
- `DELETE /api/vendas/{id}/` — Deletar venda

### Estatísticas
- `GET /api/vendas/estatisticas/vendas-por-dia/` — Total de vendas por dia (últimos 30 dias por padrão)
  - Parâmetros opcionais: `data_inicio` e `data_fim` (formato: YYYY-MM-DD)
- `GET /api/vendas/estatisticas/clientes-destaque/` — Clientes destaque

---

## 💻 Desenvolvimento

### Comandos úteis

**Rebuild após adicionar dependências:**
```bash
docker-compose build app
```

**Ver logs:**
```bash
docker-compose logs -f app
```

**Acessar shell do container:**
```bash
docker-compose exec app bash
```

**Criar nova migration:**
```bash
docker-compose exec app poetry run python manage.py makemigrations
```

**Aplicar migrations:**
```bash
docker-compose exec app poetry run python manage.py migrate
```

### Estrutura do banco
- **Tabela clientes:** Armazena dados dos clientes
- **Tabela sales:** Armazena dados das vendas (renomeada de 'vendas')

---

## 📝 Observações

- ✅ **Gitignore:** Configurado para ignorar arquivos desnecessários
- ✅ **Documentação:** Gerada automaticamente com drf-spectacular
- ✅ **Logs:** Sistema robusto de logging
- ✅ **Clean Architecture:** Separação clara de responsabilidades
- ✅ **Docker:** Containerização completa
- ✅ **JWT:** Autenticação segura
- ✅ **PostgreSQL:** Banco de dados robusto

### Dicas
- Sempre que adicionar dependências, rode `docker-compose build app`
- Use a documentação Swagger para testar endpoints
- O arquivo `.env` não é versionado (segurança)

---

**Desenvolvido com ❤️ usando Django, Clean Architecture e Docker** 