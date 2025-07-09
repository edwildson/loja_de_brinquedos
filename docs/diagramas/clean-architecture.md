# Diagrama de Arquitetura Clean Architecture

## Visão Geral da Arquitetura

```mermaid
graph TB
    subgraph "Interface Adapters"
        Views[Views/ViewSets]
        Serializers[Serializers]
        Routers[Routers]
    end
    
    subgraph "Application"
        UseCases[Use Cases]
        DTOs[DTOs]
    end
    
    subgraph "Domain"
        Entities[Entities]
        Repositories[Repository Interfaces]
    end
    
    subgraph "Infrastructure"
        Models[Django Models]
        RepoImpl[Repository Implementations]
        DB[(PostgreSQL)]
    end
    
    Views --> Serializers
    Serializers --> UseCases
    UseCases --> DTOs
    UseCases --> Repositories
    Repositories --> Entities
    RepoImpl --> Models
    Models --> DB
    RepoImpl -.->|implements| Repositories
```

## Fluxo de Dados

```mermaid
sequenceDiagram
    participant Client
    participant ViewSet
    participant UseCase
    participant Repository
    participant Model
    participant Database
    
    Client->>ViewSet: HTTP Request
    ViewSet->>UseCase: execute()
    UseCase->>Repository: get/add/update/delete()
    Repository->>Model: Django ORM
    Model->>Database: SQL Query
    Database-->>Model: Result
    Model-->>Repository: Entity
    Repository-->>UseCase: Entity/DTO
    UseCase-->>ViewSet: Response DTO
    ViewSet-->>Client: HTTP Response
```

## Camadas da Arquitetura

### 1. Domain (Entidades e Contratos)
- **Entities**: Cliente, Venda (puro Python)
- **Repository Interfaces**: Contratos abstratos

### 2. Application (Casos de Uso)
- **Use Cases**: Lógica de negócio
- **DTOs**: Objetos de transferência de dados

### 3. Infrastructure (Implementações)
- **Models**: Django ORM
- **Repository Implementations**: Implementações concretas

### 4. Interface Adapters (Apresentação)
- **Views**: ViewSets do DRF
- **Serializers**: Serialização JSON
- **Routers**: Configuração de URLs

## Benefícios da Arquitetura

- ✅ **Independência de frameworks**
- ✅ **Testabilidade**
- ✅ **Manutenibilidade**
- ✅ **Escalabilidade**
- ✅ **Separação de responsabilidades** 