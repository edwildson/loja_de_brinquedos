# Testes da Aplicação

Esta pasta contém todos os testes da aplicação **Loja de Brinquedos API**, organizados seguindo a Clean Architecture.

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py
├── conftest.py              # Configurações e fixtures comuns
├── domain/                  # Testes do domínio
│   ├── __init__.py
│   └── test_entities.py     # Testes das entidades
├── application/             # Testes da camada de aplicação
│   ├── __init__.py
│   └── test_use_cases.py   # Testes dos casos de uso
├── infra/                  # Testes da infraestrutura
│   ├── __init__.py
│   └── test_repositories.py # Testes dos repositórios
├── interface_adapters/      # Testes dos adaptadores de interface
│   ├── __init__.py
│   └── test_views.py       # Testes das views
└── integration/            # Testes de integração
    ├── __init__.py
    └── test_api_integration.py # Testes end-to-end
```

## 🧪 Tipos de Testes

### 1. Testes Unitários
- **Domínio**: Entidades e regras de negócio
- **Aplicação**: Casos de uso e DTOs
- **Infraestrutura**: Repositórios e modelos

### 2. Testes de Integração
- **API**: Endpoints e fluxos completos
- **Banco de Dados**: Operações CRUD reais
- **Autenticação**: JWT e autorização

### 3. Testes Funcionais
- **Fluxos de Negócio**: Cenários completos
- **Validações**: Dados inválidos e erros
- **Performance**: Testes básicos de performance

## 🚀 Como Executar os Testes

### Executar Todos os Testes
```bash
# Usando pytest
pytest

# Usando Django
python manage.py test

# Com cobertura
pytest --cov=. --cov-report=html
```

### Executar Testes Específicos
```bash
# Testes do domínio
pytest tests/domain/ -v

# Testes da aplicação
pytest tests/application/ -v

# Testes da infraestrutura
pytest tests/infra/ -v

# Testes das views
pytest tests/interface_adapters/ -v

# Testes de integração
pytest tests/integration/ -v
```

### Executar por Marcadores
```bash
# Testes unitários
pytest -m unit

# Testes de integração
pytest -m integration

# Testes da API
pytest -m api

# Testes lentos
pytest -m slow
```

### Executar com Docker
```bash
# Executar testes no container
docker-compose exec app pytest

# Executar com cobertura
docker-compose exec app pytest --cov=. --cov-report=html
```

## 📊 Cobertura de Testes

### Metas de Cobertura
- **Domínio**: 100% (entidades e regras de negócio)
- **Aplicação**: 90% (casos de uso)
- **Infraestrutura**: 85% (repositórios)
- **Interface**: 80% (views e serializers)
- **Geral**: 80% mínimo

### Gerar Relatório de Cobertura
```bash
# Gerar relatório HTML
pytest --cov=. --cov-report=html

# Abrir relatório
open htmlcov/index.html
```

## 🔧 Configuração

### Fixtures Disponíveis
- `api_client`: Cliente da API
- `user`: Usuário de teste
- `authenticated_client`: Cliente autenticado
- `cliente_data`: Dados de cliente válidos
- `venda_data`: Dados de venda válidos
- `cliente_entity`: Entidade Cliente
- `venda_entity`: Entidade Venda
- `cliente_model`: Modelo Cliente no banco
- `venda_model`: Modelo Venda no banco
- `multiple_clientes`: Múltiplos clientes
- `multiple_vendas`: Múltiplas vendas

### Classe Base
- `BaseTestCase`: Classe base com configurações comuns
- Métodos helper: `create_cliente()`, `create_venda()`

## 📝 Convenções

### Nomenclatura
- **Arquivos**: `test_*.py`
- **Classes**: `Test*`
- **Métodos**: `test_*`
- **Marcadores**: `@pytest.mark.*`

### Estrutura de Teste
```python
def test_nome_do_teste(self):
    """Descrição do teste"""
    # Arrange (preparar)
    # Act (executar)
    # Assert (verificar)
```

### Assertions
- Use `assert` para verificações simples
- Use `pytest.raises()` para exceções
- Use `unittest.mock` para mocks

## 🎯 Cenários de Teste

### Domínio
- ✅ Criação de entidades válidas
- ✅ Validação de dados inválidos
- ✅ Regras de negócio
- ✅ Igualdade e hash

### Aplicação
- ✅ Execução de casos de uso
- ✅ Tratamento de erros
- ✅ Conversão de DTOs
- ✅ Mocks de repositórios

### Infraestrutura
- ✅ Operações CRUD
- ✅ Filtros e consultas
- ✅ Tratamento de exceções
- ✅ Conversão entre entidades e modelos

### Interface
- ✅ Endpoints da API
- ✅ Autenticação
- ✅ Validação de dados
- ✅ Códigos de status HTTP

### Integração
- ✅ Fluxos completos
- ✅ Cenários reais
- ✅ Performance básica
- ✅ Tratamento de erros

## 🔍 Debugging

### Executar Teste Específico
```bash
# Executar um teste específico
pytest tests/domain/test_entities.py::TestCliente::test_criar_cliente_valido -v

# Executar com debug
pytest tests/domain/test_entities.py::TestCliente::test_criar_cliente_valido -v -s
```

### Verbose Output
```bash
# Output detalhado
pytest -v

# Output muito detalhado
pytest -vv

# Mostrar prints
pytest -s
```

### Relatórios
```bash
# Relatório de duração
pytest --durations=10

# Relatório de falhas
pytest --tb=long

# Relatório de cobertura
pytest --cov=. --cov-report=term-missing
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de importação**
   ```bash
   # Verificar se o PYTHONPATH está correto
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Erro de banco de dados**
   ```bash
   # Executar migrações
   python manage.py migrate
   
   # Criar banco de teste
   python manage.py test --keepdb
   ```

3. **Erro de autenticação**
   ```bash
   # Verificar configurações JWT
   python manage.py check
   ```

### Logs de Teste
```bash
# Executar com logs
pytest --log-cli-level=DEBUG

# Salvar logs em arquivo
pytest --log-file=test.log
```

## 📚 Recursos Adicionais

### Documentação
- [pytest Documentation](https://docs.pytest.org/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)

### Ferramentas
- [pytest-cov](https://pytest-cov.readthedocs.io/): Cobertura de código
- [pytest-django](https://pytest-django.readthedocs.io/): Integração Django
- [factory-boy](https://factoryboy.readthedocs.io/): Factories para testes

---

**Última atualização:** Julho 2025  
**Versão:** 1.0.0  
**Mantido por:** Equipe de Desenvolvimento 