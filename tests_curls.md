# Testes de API - Sequência de comandos curl

## 0. Obter token JWT (login)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SENHA_DO_ADMIN"
  }'
```

## 0.1. Renovar token JWT
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<REFRESH_TOKEN_AQUI>"
  }'
```

> **Atenção:** Para todos os comandos abaixo, adicione o header:
> 
>     -H "Authorization: Bearer <access_token>"
>
> Substitua `<access_token>` pelo token obtido no login.

## 1. Listar clientes (deve retornar vazio inicialmente)
```bash
curl -X GET http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <access_token>"
```

## 2. Cadastrar cliente 1
```bash
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nome_completo": "Maria Teste",
    "email": "maria@example.com",
    "data_nascimento": "1995-05-10"
  }'
```

## 3. Cadastrar cliente 2
```bash
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nome_completo": "João Silva",
    "email": "joao@example.com",
    "data_nascimento": "1990-01-01"
  }'
```

## 4. Listar clientes (deve retornar os dois cadastrados)
```bash
curl -X GET http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <access_token>"
```

## 5. Editar cliente 1 (completo)
```bash
curl -X PUT http://localhost:8000/api/clientes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nome_completo": "Maria Teste Editada",
    "email": "maria.editada@example.com",
    "data_nascimento": "1995-05-10"
  }'
```

## 5.1. Editar cliente 1 (parcial - apenas nome)
```bash
curl -X PATCH http://localhost:8000/api/clientes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nome_completo": "Maria Teste Atualizada"
  }'
```

## 5.2. Editar cliente 1 (parcial - apenas email)
```bash
curl -X PATCH http://localhost:8000/api/clientes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "email": "maria.nova@example.com"
  }'
```

## 6. Listar clientes filtrando por nome
```bash
curl -X GET "http://localhost:8000/api/clientes/?nome=Maria" \
  -H "Authorization: Bearer <access_token>"
```

## 7. Registrar venda para cliente 1
```bash
curl -X POST http://localhost:8000/api/vendas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "cliente": 1,
    "data": "2024-06-01",
    "valor": 200.00
  }'
```

## 8. Registrar venda para cliente 2
```bash
curl -X POST http://localhost:8000/api/vendas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "cliente": 2,
    "data": "2024-06-02",
    "valor": 150.00
  }'
```

## 9. Listar vendas (todas)
```bash
curl -X GET http://localhost:8000/api/vendas/ \
  -H "Authorization: Bearer <access_token>"
```

## 9.1. Obter venda específica
```bash
curl -X GET http://localhost:8000/api/vendas/1/ \
  -H "Authorization: Bearer <access_token>"
```

## 9.2. Atualizar venda (completo)
```bash
curl -X PUT http://localhost:8000/api/vendas/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "cliente": 1,
    "data": "2024-06-15",
    "valor": 250.00
  }'
```

## 9.3. Atualizar venda (parcial - apenas valor)
```bash
curl -X PATCH http://localhost:8000/api/vendas/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "valor": 300.00
  }'
```

## 9.4. Atualizar venda (parcial - apenas data)
```bash
curl -X PATCH http://localhost:8000/api/vendas/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "data": "2024-06-20"
  }'
```

## 9.5. Deletar venda
```bash
curl -X DELETE http://localhost:8000/api/vendas/1/ \
  -H "Authorization: Bearer <access_token>"
```

## 10. Listar vendas do cliente 1
```bash
curl -X GET "http://localhost:8000/api/vendas/?cliente_id=1" \
  -H "Authorization: Bearer <access_token>"
```

## 11. Listar vendas por período
```bash
curl -X GET "http://localhost:8000/api/vendas/?start_date=2024-06-01&end_date=2024-06-30" \
  -H "Authorization: Bearer <access_token>"
```

## 12. Deletar cliente 2
```bash
curl -X DELETE http://localhost:8000/api/clientes/2/ \
  -H "Authorization: Bearer <access_token>"
```

## 13. Listar clientes (deve restar apenas cliente 1)
```bash
curl -X GET http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <access_token>"
```

## 14. Estatística: total de vendas por dia (últimos 30 dias por padrão)
```bash
curl -X GET http://localhost:8000/api/vendas/estatisticas/vendas-por-dia/ \
  -H "Authorization: Bearer <access_token>"
```

## 14.1. Estatística: vendas por dia com filtro de período
```bash
curl -X GET "http://localhost:8000/api/vendas/estatisticas/vendas-por-dia/?data_inicio=2024-06-01&data_fim=2024-06-30" \
  -H "Authorization: Bearer <access_token>"
```

## 14.2. Estatística: vendas por dia com apenas data inicial (30 dias a partir da data)
```bash
curl -X GET "http://localhost:8000/api/vendas/estatisticas/vendas-por-dia/?data_inicio=2024-06-01" \
  -H "Authorization: Bearer <access_token>"
```

## 14.3. Estatística: vendas por dia com apenas data final (30 dias antes da data)
```bash
curl -X GET "http://localhost:8000/api/vendas/estatisticas/vendas-por-dia/?data_fim=2024-06-30" \
  -H "Authorization: Bearer <access_token>"
```

## 15. Estatística: clientes destaque
```bash
curl -X GET http://localhost:8000/api/vendas/estatisticas/clientes-destaque/ \
  -H "Authorization: Bearer <access_token>"
``` 