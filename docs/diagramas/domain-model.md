# Diagrama do Modelo de Domínio

## Entidades do Domínio

```mermaid
classDiagram
    class Cliente {
        -id: int
        -nome_completo: str
        -email: str
        -data_nascimento: date
        +__init__(nome_completo, email, data_nascimento)
        +get_nome_completo() str
        +get_email() str
        +get_data_nascimento() date
    }
    
    class Venda {
        -id: int
        -cliente_id: int
        -data: date
        -valor: float
        +__init__(cliente_id, data, valor)
        +get_cliente_id() int
        +get_data() date
        +get_valor() float
    }
    
    Cliente ||--o{ Venda : "faz"
```

## Contratos de Repositório

```mermaid
classDiagram
    class ClienteRepository {
        <<interface>>
        +add(cliente: Cliente) Cliente
        +get(cliente_id: int) Cliente?
        +update(cliente: Cliente) Cliente
        +delete(cliente_id: int) void
        +list(nome?: str, email?: str) Cliente[]
    }
    
    class VendaRepository {
        <<interface>>
        +add(venda: Venda) Venda
        +get(venda_id: int) Venda?
        +update(venda: Venda) Venda
        +delete(venda_id: int) void
        +list_by_cliente(cliente_id: int) Venda[]
        +list_by_period(start_date?, end_date?) Venda[]
    }
    
    class ClienteRepositoryImpl {
        +add(cliente: Cliente) Cliente
        +get(cliente_id: int) Cliente?
        +update(cliente: Cliente) Cliente
        +delete(cliente_id: int) void
        +list(nome?: str, email?: str) Cliente[]
    }
    
    class VendaRepositoryImpl {
        +add(venda: Venda) Venda
        +get(venda_id: int) Venda?
        +update(venda: Venda) Venda
        +delete(venda_id: int) void
        +list_by_cliente(cliente_id: int) Venda[]
        +list_by_period(start_date?, end_date?) Venda[]
    }
    
    ClienteRepositoryImpl ..|> ClienteRepository
    VendaRepositoryImpl ..|> VendaRepository
```

## Regras de Negócio

### Cliente
- ✅ **Email único**: Não pode haver dois clientes com o mesmo email
- ✅ **Nome obrigatório**: Nome completo é obrigatório
- ✅ **Data de nascimento**: Deve ser uma data válida

### Venda
- ✅ **Cliente obrigatório**: Toda venda deve ter um cliente
- ✅ **Valor positivo**: Valor da venda deve ser maior que zero
- ✅ **Data válida**: Data da venda deve ser uma data válida

## Relacionamentos

```mermaid
erDiagram
    CLIENTE {
        int id PK
        string nome_completo
        string email UK
        date data_nascimento
        datetime created_at
        datetime updated_at
    }
    
    VENDA {
        int id PK
        int cliente_id FK
        date data
        decimal valor
        datetime created_at
        datetime updated_at
    }
    
    CLIENTE ||--o{ VENDA : "faz"
```

## Validações de Domínio

### Cliente
- Email deve ser único no sistema
- Nome completo não pode ser vazio
- Data de nascimento deve ser uma data válida

### Venda
- Cliente deve existir no sistema
- Valor deve ser maior que zero
- Data deve ser uma data válida 