# Diagrama de Sequência

## Fluxo: Cadastrar Cliente e Registrar Venda

### 1. Cadastro de Cliente

```mermaid
sequenceDiagram
    participant Client
    participant ViewSet
    participant UseCase
    participant Repository
    participant Model
    participant Database
    
    Client->>ViewSet: POST /api/clientes/
    Note over Client,ViewSet: {nome_completo, email, data_nascimento}
    
    ViewSet->>ViewSet: Validar dados
    ViewSet->>UseCase: CadastrarClienteUseCase.execute(dto)
    
    UseCase->>Repository: add(cliente)
    Repository->>Model: ClienteModel.objects.create()
    Model->>Database: INSERT INTO clientes
    Database-->>Model: Cliente criado
    Model-->>Repository: ClienteModel object
    Repository-->>UseCase: Cliente entity
    UseCase-->>ViewSet: ClienteDTO
    ViewSet-->>Client: 201 Created + Cliente data
```

### 2. Registro de Venda

```mermaid
sequenceDiagram
    participant Client
    participant ViewSet
    participant UseCase
    participant Repository
    participant Model
    participant Database
    
    Client->>ViewSet: POST /api/vendas/
    Note over Client,ViewSet: {cliente_id, data, valor}
    
    ViewSet->>ViewSet: Validar dados
    ViewSet->>UseCase: RegistrarVendaUseCase.execute(dto)
    
    UseCase->>Repository: add(venda)
    Repository->>Model: VendaModel.objects.create()
    Model->>Database: INSERT INTO sales
    Database-->>Model: Venda criada
    Model-->>Repository: VendaModel object
    Repository-->>UseCase: Venda entity
    UseCase-->>ViewSet: VendaDTO
    ViewSet-->>Client: 201 Created + Venda data
```

### 3. Consulta de Estatísticas

```mermaid
sequenceDiagram
    participant Client
    participant ViewSet
    participant UseCase
    participant Repository
    participant Model
    participant Database
    
    Client->>ViewSet: GET /api/vendas/estatisticas/clientes-destaque/
    
    ViewSet->>UseCase: EstatisticasUseCase.clientes_destaque()
    
    UseCase->>Model: ClienteModel.objects.annotate()
    Model->>Database: SELECT com agregações
    Database-->>Model: Dados agregados
    Model-->>UseCase: QuerySet com estatísticas
    
    UseCase->>UseCase: Processar dados
    UseCase-->>ViewSet: Dict com estatísticas
    ViewSet-->>Client: 200 OK + Estatísticas
```

## Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant Client
    participant AuthView
    participant Django
    participant Database
    
    Client->>AuthView: POST /api/token/
    Note over Client,AuthView: {username, password}
    
    AuthView->>Django: authenticate()
    Django->>Database: SELECT user
    Database-->>Django: User object
    Django-->>AuthView: User validado
    
    AuthView->>AuthView: generate_tokens()
    AuthView-->>Client: 200 OK + {access, refresh}
    
    Note over Client: Usar access token em requests subsequentes
    Client->>AuthView: GET /api/clientes/ (com Authorization header)
    AuthView->>AuthView: validate_token()
    AuthView-->>Client: 200 OK + Dados
```

## Fluxo de Erro

```mermaid
sequenceDiagram
    participant Client
    participant ViewSet
    participant UseCase
    participant Repository
    participant Model
    participant Database
    
    Client->>ViewSet: PUT /api/clientes/999/
    Note over Client,ViewSet: Cliente inexistente
    
    ViewSet->>UseCase: EditarClienteUseCase.execute(999, dto)
    UseCase->>Repository: get(999)
    Repository->>Model: ClienteModel.objects.get(999)
    Model->>Database: SELECT WHERE id=999
    Database-->>Model: No results
    Model-->>Repository: None
    Repository-->>UseCase: None
    UseCase-->>ViewSet: None
    ViewSet-->>Client: 404 Not Found + {"detail": "Cliente não encontrado"}
```

## Componentes da Sequência

### ViewSet
- Recebe requisições HTTP
- Valida dados de entrada
- Chama use cases
- Retorna respostas HTTP

### Use Case
- Contém lógica de negócio
- Orquestra operações
- Valida regras de domínio
- Retorna DTOs

### Repository
- Abstrai acesso a dados
- Implementa contratos
- Converte entre entidades e models

### Model
- Representa tabela no banco
- Usa Django ORM
- Executa queries SQL

### Database
- PostgreSQL
- Armazena dados persistentes
- Executa queries SQL 