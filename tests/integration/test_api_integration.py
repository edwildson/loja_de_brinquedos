import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.conftest import BaseTestCase


class TestAPIEndToEnd(BaseTestCase):
    """Testes de integração end-to-end da API"""
    
    def test_fluxo_completo_cliente(self):
        """Testa fluxo completo de CRUD de cliente"""
        # 1. Criar cliente
        data = {
            'nome_completo': 'João Silva',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-list')
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        cliente_id = response.data['id']
        
        # 2. Listar clientes
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
        # 3. Obter cliente específico
        url_detail = reverse('cliente-detail', args=[cliente_id])
        response = self.client.get(url_detail)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == 'João Silva'
        
        # 4. Atualizar cliente
        update_data = {
            'nome_completo': 'João Silva Atualizado',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        response = self.client.patch(url_detail, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == 'João Silva Atualizado'
        
        # 5. Deletar cliente
        response = self.client.delete(url_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # 6. Verificar se foi deletado
        response = self.client.get(url_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_fluxo_completo_venda(self):
        """Testa fluxo completo de CRUD de venda"""
        # 1. Criar cliente primeiro
        cliente_data = {
            'nome_completo': 'Maria Silva',
            'email': 'maria@example.com',
            'data_nascimento': '1985-05-20'
        }
        
        url_cliente = reverse('cliente-list')
        response = self.client.post(url_cliente, cliente_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        cliente_id = response.data['id']
        
        # 2. Criar venda
        venda_data = {
            'cliente_id': cliente_id,
            'data': '2024-01-15',
            'valor': 150.00
        }
        
        url_venda = reverse('venda-list')
        response = self.client.post(url_venda, venda_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        venda_id = response.data['id']
        
        # 3. Listar vendas
        response = self.client.get(url_venda)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
        # 4. Obter venda específica
        url_venda_detail = reverse('venda-detail', args=[venda_id])
        response = self.client.get(url_venda_detail)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valor'] == '150.00'
        
        # 5. Atualizar venda
        update_data = {
            'cliente_id': cliente_id,
            'data': '2024-02-15',
            'valor': 200.00
        }
        response = self.client.patch(url_venda_detail, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valor'] == '200.00'
        
        # 6. Deletar venda
        response = self.client.delete(url_venda_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # 7. Verificar se foi deletada
        response = self.client.get(url_venda_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_estatisticas_com_dados_reais(self):
        """Testa estatísticas com dados reais"""
        # 1. Criar clientes
        cliente1 = self.create_cliente(nome_completo='Cliente 1', email='cliente1@example.com')
        cliente2 = self.create_cliente(nome_completo='Cliente 2', email='cliente2@example.com')
        
        # 2. Criar vendas
        self.create_venda(cliente1.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente1.id, data='2024-01-15', valor=200.00)  # Mesmo dia
        self.create_venda(cliente1.id, data='2024-01-16', valor=150.00)
        self.create_venda(cliente2.id, data='2024-01-15', valor=300.00)
        self.create_venda(cliente2.id, data='2024-01-17', valor=250.00)
        
        # 3. Testar estatísticas de vendas por dia
        url_vendas_por_dia = reverse('estatisticas-vendas-por-dia')
        response = self.client.get(url_vendas_por_dia)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        
        # Verificar se há dados para 2024-01-15 (deve ter 3 vendas)
        vendas_15 = [v for v in response.data if v['data'] == '2024-01-15' or v['data'] == '2024-01-15T00:00:00Z' or str(v['data']) == '2024-01-15']
        assert len(vendas_15) == 1
        assert vendas_15[0]['total_vendas'] == 600.00  # 100 + 200 + 300
        
        # 4. Testar estatísticas de clientes destaque
        url_clientes_destaque = reverse('estatisticas-clientes-destaque')
        response = self.client.get(url_clientes_destaque)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'maior_volume' in response.data
        assert 'maior_media' in response.data
        assert 'maior_frequencia' in response.data
    
    def test_filtros_e_paginacao(self):
        """Testa filtros e paginação"""
        # 1. Criar múltiplos clientes
        for i in range(10):
            self.create_cliente(
                nome_completo=f'Cliente {i+1}',
                email=f'cliente{i+1}@example.com'
            )
        
        # 2. Testar filtro por nome (busca exata)
        url = reverse('cliente-list')
        response = self.client.get(url, {'nome': 'Cliente 1'})
        assert response.status_code == status.HTTP_200_OK
        # Como icontains retorna "Cliente 1" e "Cliente 10", esperamos 2 resultados
        assert len(response.data) == 2
        
        # 3. Testar filtro por email
        response = self.client.get(url, {'email': 'cliente5@example.com'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
        # 4. Testar listagem sem filtros
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10
    
    def test_validacoes_e_erros(self):
        """Testa validações e tratamento de erros"""
        # 1. Testar criação de cliente com email duplicado
        cliente_data = {
            'nome_completo': 'João Silva',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-list')
        response = self.client.post(url, cliente_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Tentar criar outro com mesmo email
        response = self.client.post(url, cliente_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # 2. Testar criação de venda com cliente inexistente
        venda_data = {
            'cliente_id': 999,
            'data': '2024-01-15',
            'valor': 150.00
        }
        
        url_venda = reverse('venda-list')
        response = self.client.post(url_venda, venda_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # 3. Testar acesso a recursos inexistentes
        url_detail = reverse('cliente-detail', args=[999])
        response = self.client.get(url_detail)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # 4. Testar dados inválidos
        invalid_data = {
            'nome_completo': '',  # Nome vazio
            'email': 'email-invalido',
            'data_nascimento': '1990-01-15'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_autenticacao_e_autorizacao(self):
        """Testa autenticação e autorização"""
        # 1. Testar acesso sem autenticação
        client = APIClient()  # Cliente sem autenticação
        
        url = reverse('cliente-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # 2. Testar criação sem autenticação
        data = {
            'nome_completo': 'João Silva',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # 3. Testar estatísticas sem autenticação
        url_estatisticas = reverse('estatisticas-vendas-por-dia')
        response = client.get(url_estatisticas)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_performance_basica(self):
        """Testa performance básica com múltiplos registros"""
        import time
        
        # 1. Criar múltiplos clientes
        start_time = time.time()
        
        for i in range(50):
            self.create_cliente(
                nome_completo=f'Cliente Performance {i+1}',
                email=f'cliente{i+1}@performance.com'
            )
        
        creation_time = time.time() - start_time
        assert creation_time < 5.0  # Deve ser rápido
        
        # 2. Testar listagem
        start_time = time.time()
        url = reverse('cliente-list')
        response = self.client.get(url)
        list_time = time.time() - start_time
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 50
        assert list_time < 2.0  # Deve ser rápido
        
        # 3. Testar filtro
        start_time = time.time()
        response = self.client.get(url, {'nome': 'Performance'})
        filter_time = time.time() - start_time
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 50
        assert filter_time < 1.0  # Deve ser rápido 


class TestASGIWSGI:
    """Testes para ASGI e WSGI"""
    
    def test_asgi_application(self):
        """Testa se a aplicação ASGI pode ser importada"""
        from loja_brinquedos.asgi import application
        
        assert application is not None
    
    def test_wsgi_application(self):
        """Testa se a aplicação WSGI pode ser importada"""
        from loja_brinquedos.wsgi import application
        
        assert application is not None
    
    def test_asgi_os_environ(self):
        """Testa configuração do ASGI com os.environ"""
        import os
        from unittest.mock import patch
        
        with patch.dict(os.environ, {'DJANGO_SETTINGS_MODULE': 'loja_brinquedos.settings'}):
            from loja_brinquedos.asgi import application
            assert application is not None
    
    def test_wsgi_os_environ(self):
        """Testa configuração do WSGI com os.environ"""
        import os
        from unittest.mock import patch
        
        with patch.dict(os.environ, {'DJANGO_SETTINGS_MODULE': 'loja_brinquedos.settings'}):
            from loja_brinquedos.wsgi import application
            assert application is not None 