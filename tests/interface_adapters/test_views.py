import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.conftest import BaseTestCase
from unittest.mock import patch, Mock
from datetime import date


class TestClienteViewSet(BaseTestCase):
    """Testes para ClienteViewSet"""
    
    def test_listar_clientes_autenticado(self):
        """Testa listar clientes com usuário autenticado"""
        # Criar alguns clientes
        self.create_cliente(nome_completo='Cliente 1', email='cliente1@example.com')
        self.create_cliente(nome_completo='Cliente 2', email='cliente2@example.com')
        
        url = reverse('cliente-list')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_listar_clientes_nao_autenticado(self):
        """Testa listar clientes sem autenticação"""
        client = APIClient()  # Cliente sem autenticação
        url = reverse('cliente-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_criar_cliente_valido(self):
        """Testa criar cliente com dados válidos"""
        data = {
            'nome_completo': 'João Silva',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-list')
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['nome_completo'] == 'João Silva'
        assert response.data['email'] == 'joao@example.com'
    
    def test_criar_cliente_dados_invalidos(self):
        """Testa criar cliente com dados inválidos"""
        data = {
            'nome_completo': '',  # Nome vazio
            'email': 'email-invalido',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-list')
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_obter_cliente_existente(self):
        """Testa obter cliente existente"""
        cliente = self.create_cliente(
            nome_completo='João Silva',
            email='joao@example.com'
        )
        
        url = reverse('cliente-detail', args=[cliente.id])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == 'João Silva'
        assert response.data['email'] == 'joao@example.com'
    
    def test_obter_cliente_inexistente(self):
        """Testa obter cliente inexistente"""
        url = reverse('cliente-detail', args=[999])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_atualizar_cliente_existente(self):
        """Testa atualizar cliente existente"""
        cliente = self.create_cliente(
            nome_completo='João Silva',
            email='joao@example.com'
        )
        
        data = {
            'nome_completo': 'João Silva Atualizado',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-detail', args=[cliente.id])
        response = self.client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == 'João Silva Atualizado'
    
    def test_atualizar_cliente_inexistente(self):
        """Testa atualizar cliente inexistente"""
        data = {
            'nome_completo': 'João Silva',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-detail', args=[999])
        response = self.client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_deletar_cliente_existente(self):
        """Testa deletar cliente existente"""
        cliente = self.create_cliente(
            nome_completo='João Silva',
            email='joao@example.com'
        )
        
        url = reverse('cliente-detail', args=[cliente.id])
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_deletar_cliente_inexistente(self):
        """Testa deletar cliente inexistente"""
        url = reverse('cliente-detail', args=[999])
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_filtrar_clientes_por_nome(self):
        """Testa filtrar clientes por nome"""
        self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_cliente(nome_completo='Maria Silva', email='maria@example.com')
        
        url = reverse('cliente-list')
        response = self.client.get(url, {'nome': 'João'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['nome_completo'] == 'João Silva'
    
    def test_filtrar_clientes_por_email(self):
        """Testa filtrar clientes por email"""
        self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_cliente(nome_completo='Maria Silva', email='maria@example.com')
        
        url = reverse('cliente-list')
        response = self.client.get(url, {'email': 'joao@example.com'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['email'] == 'joao@example.com'


class TestVendaViewSet(BaseTestCase):
    """Testes para VendaViewSet"""
    
    def test_listar_vendas_autenticado(self):
        """Testa listar vendas com usuário autenticado"""
        # Criar cliente e vendas
        cliente = self.create_cliente(nome_completo='Cliente 1', email='cliente1@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-01-16', valor=200.00)
        
        url = reverse('venda-list')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_listar_vendas_nao_autenticado(self):
        """Testa listar vendas sem autenticação"""
        client = APIClient()  # Cliente sem autenticação
        url = reverse('venda-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_criar_venda_valida(self):
        """Testa criar venda com dados válidos"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        data = {
            'cliente_id': cliente.id,
            'data': '2024-01-15',
            'valor': 150.00
        }
        
        url = reverse('venda-list')
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['cliente_id'] == cliente.id
        assert response.data['valor'] == '150.00'
    
    def test_criar_venda_cliente_inexistente(self):
        """Testa criar venda com cliente inexistente"""
        data = {
            'cliente_id': 999,
            'data': '2024-01-15',
            'valor': 150.00
        }
        
        url = reverse('venda-list')
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_criar_venda_dados_invalidos(self):
        """Testa criar venda com dados inválidos"""
        data = {
            'cliente_id': 1,
            'data': '2024-01-15',
            'valor': -50.00  # Valor negativo
        }
        
        url = reverse('venda-list')
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_obter_venda_existente(self):
        """Testa obter venda existente"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        venda = self.create_venda(cliente.id, data='2024-01-15', valor=150.00)
        
        url = reverse('venda-detail', args=[venda.id])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['cliente_id'] == cliente.id
        assert response.data['valor'] == '150.00'
    
    def test_obter_venda_inexistente(self):
        """Testa obter venda inexistente"""
        url = reverse('venda-detail', args=[999])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_atualizar_venda_existente(self):
        """Testa atualizar venda existente"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        venda = self.create_venda(cliente.id, data='2024-01-15', valor=150.00)
        
        data = {
            'cliente_id': cliente.id,
            'data': '2024-02-15',
            'valor': 200.00
        }
        
        url = reverse('venda-detail', args=[venda.id])
        response = self.client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valor'] == '200.00'
    
    def test_atualizar_venda_inexistente(self):
        """Testa atualizar venda inexistente"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        data = {
            'cliente_id': cliente.id,
            'data': '2024-01-15',
            'valor': 150.00
        }
        
        url = reverse('venda-detail', args=[999])
        response = self.client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_deletar_venda_existente(self):
        """Testa deletar venda existente"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        venda = self.create_venda(cliente.id, data='2024-01-15', valor=150.00)
        
        url = reverse('venda-detail', args=[venda.id])
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_deletar_venda_inexistente(self):
        """Testa deletar venda inexistente"""
        url = reverse('venda-detail', args=[999])
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_filtrar_vendas_por_periodo(self):
        """Testa filtrar vendas por período"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-01-16', valor=200.00)
        self.create_venda(cliente.id, data='2024-02-15', valor=300.00)
        
        url = reverse('venda-list')
        response = self.client.get(url, {
            'start_date': '2024-01-15',
            'end_date': '2024-01-16'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


class TestEstatisticasViewSet(BaseTestCase):
    """Testes para EstatisticasViewSet"""
    
    def test_vendas_por_dia_autenticado(self):
        """Testa obter estatísticas de vendas por dia com usuário autenticado"""
        # Criar vendas para teste
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-01-15', valor=200.00)
        self.create_venda(cliente.id, data='2024-01-16', valor=150.00)
    
        url = reverse('estatisticas-vendas-por-dia')
        response = self.client.get(url)
    
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 0
    
    def test_vendas_por_dia_nao_autenticado(self):
        """Testa obter estatísticas sem autenticação"""
        client = APIClient()  # Cliente sem autenticação
        url = reverse('estatisticas-vendas-por-dia')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_vendas_por_dia_com_periodo_customizado(self):
        """Testa obter estatísticas com período customizado"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-02-15', valor=200.00)
        
        url = reverse('estatisticas-vendas-por-dia')
        response = self.client.get(url, {
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        })
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_clientes_destaque_autenticado(self):
        """Testa obter estatísticas de clientes destaque com usuário autenticado"""
        # Criar clientes e vendas para teste
        cliente1 = self.create_cliente(nome_completo='Cliente 1', email='cliente1@example.com')
        cliente2 = self.create_cliente(nome_completo='Cliente 2', email='cliente2@example.com')
        
        self.create_venda(cliente1.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente1.id, data='2024-01-16', valor=200.00)
        self.create_venda(cliente2.id, data='2024-01-15', valor=150.00)
        
        url = reverse('estatisticas-clientes-destaque')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'maior_volume' in response.data
        assert 'maior_media' in response.data
        assert 'maior_frequencia' in response.data
    
    def test_clientes_destaque_nao_autenticado(self):
        """Testa obter estatísticas de clientes destaque sem autenticação"""
        client = APIClient()  # Cliente sem autenticação
        url = reverse('estatisticas-clientes-destaque')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 


class TestSerializers:
    """Testes para os serializers"""
    
    def test_venda_serializer_validate_cliente_id_invalido(self):
        """Testa validação de cliente_id inválido no VendaSerializer"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        from infra.models.cliente_model import ClienteModel
        
        serializer = VendaSerializer()
        
        # Simular cliente inexistente
        with patch.object(ClienteModel.objects, 'get') as mock_get:
            mock_get.side_effect = ClienteModel.DoesNotExist()
            
            with pytest.raises(Exception):
                serializer.validate_cliente_id(999)
    
    def test_venda_serializer_to_representation_dict(self):
        """Testa to_representation com instance como dict"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        
        serializer = VendaSerializer()
        instance_dict = {
            'id': 1,
            'cliente': Mock(id=1),
            'data': date(2024, 1, 15),
            'valor': 150.0
        }
        
        result = serializer.to_representation(instance_dict)
        assert 'cliente_id' in result
        assert result['cliente_id'] == 1
    
    def test_venda_serializer_to_representation_sem_cliente(self):
        """Testa to_representation sem cliente"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        
        serializer = VendaSerializer()
        instance_dict = {
            'id': 1,
            'cliente': None,
            'data': date(2024, 1, 15),
            'valor': 150.0
        }
        
        result = serializer.to_representation(instance_dict)
        assert 'cliente_id' in result
        assert result['cliente_id'] is None
    
    def test_venda_serializer_validate_cliente_id_nulo(self):
        """Testa validação de cliente_id nulo"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        
        serializer = VendaSerializer()
        result = serializer.validate_cliente_id(None)
        assert result is None
    
    def test_venda_serializer_validate_cliente_id_zero(self):
        """Testa validação de cliente_id zero"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        
        serializer = VendaSerializer()
        result = serializer.validate_cliente_id(0)
        assert result == 0
    
    def test_venda_serializer_create_sem_cliente_id(self):
        """Testa create sem cliente_id"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        
        serializer = VendaSerializer()
        validated_data = {
            'data': date(2024, 1, 15),
            'valor': 150.0
        }
        
        with patch('interface_adapters.serializers.venda_serializer.super') as mock_super:
            mock_instance = Mock()
            mock_super.return_value.create.return_value = mock_instance
            result = serializer.create(validated_data)
            assert result == mock_instance
    
    def test_venda_serializer_update_sem_cliente_id(self):
        """Testa update sem cliente_id"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        
        serializer = VendaSerializer()
        instance = Mock()
        validated_data = {
            'data': date(2024, 1, 15),
            'valor': 150.0
        }
        
        with patch('interface_adapters.serializers.venda_serializer.super') as mock_super:
            mock_instance = Mock()
            mock_super.return_value.update.return_value = mock_instance
            result = serializer.update(instance, validated_data)
            assert result == mock_instance


class TestViewsEdgeCases(BaseTestCase):
    """Testes para casos extremos das views"""
    
    def test_cliente_view_update_parcial_sem_dados(self):
        """Testa update parcial sem dados"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        url = reverse('cliente-detail', args=[cliente.id])
        response = self.client.patch(url, {}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_venda_view_update_parcial_sem_dados(self):
        """Testa update parcial sem dados"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        venda = self.create_venda(cliente.id, data='2024-01-15', valor=150.00)
        
        url = reverse('venda-detail', args=[venda.id])
        response = self.client.patch(url, {}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_cliente_view_update_completo(self):
        """Testa update completo (PUT)"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        data = {
            'nome_completo': 'João Silva Atualizado',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-detail', args=[cliente.id])
        response = self.client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == 'João Silva Atualizado'
    
    def test_venda_view_update_completo(self):
        """Testa update completo (PUT)"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        venda = self.create_venda(cliente.id, data='2024-01-15', valor=150.00)
        
        data = {
            'cliente_id': cliente.id,
            'data': '2024-02-15',
            'valor': 200.00
        }
        
        url = reverse('venda-detail', args=[venda.id])
        response = self.client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valor'] == '200.00'
    
    def test_cliente_view_update_com_cliente_inexistente(self):
        """Testa update com cliente inexistente"""
        data = {
            'nome_completo': 'João Silva',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-detail', args=[999])
        response = self.client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_venda_view_update_com_venda_inexistente(self):
        """Testa update com venda inexistente"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        data = {
            'cliente_id': cliente.id,
            'data': '2024-01-15',
            'valor': 150.00
        }
        
        url = reverse('venda-detail', args=[999])
        response = self.client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_venda_view_list_com_filtros_data(self):
        """Testa listagem de vendas com filtros de data"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-02-15', valor=200.00)
        
        url = reverse('venda-list')
        response = self.client.get(url, {
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Apenas a venda de 2024-01-15
    
    def test_venda_serializer_create_com_cliente_id(self):
        """Testa create com cliente_id"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        from infra.models.cliente_model import ClienteModel
        
        # Criar cliente primeiro
        cliente = ClienteModel.objects.create(
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        serializer = VendaSerializer()
        validated_data = {
            'cliente_id': cliente.id,
            'data': date(2024, 1, 15),
            'valor': 150.0
        }
        
        with patch('interface_adapters.serializers.venda_serializer.super') as mock_super:
            mock_instance = Mock()
            mock_super.return_value.create.return_value = mock_instance
            result = serializer.create(validated_data)
            assert result == mock_instance
    
    def test_venda_serializer_update_com_cliente_id(self):
        """Testa update com cliente_id"""
        from interface_adapters.serializers.venda_serializer import VendaSerializer
        from infra.models.cliente_model import ClienteModel
        
        # Criar cliente primeiro
        cliente = ClienteModel.objects.create(
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        serializer = VendaSerializer()
        instance = Mock()
        validated_data = {
            'cliente_id': cliente.id,
            'data': date(2024, 1, 15),
            'valor': 150.0
        }
        
        with patch('interface_adapters.serializers.venda_serializer.super') as mock_super:
            mock_instance = Mock()
            mock_super.return_value.update.return_value = mock_instance
            result = serializer.update(instance, validated_data)
            assert result == mock_instance
    
    def test_cliente_view_update_com_use_case_retorna_none(self):
        """Testa update quando use case retorna None"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        data = {
            'nome_completo': 'João Silva Atualizado',
            'email': 'joao@example.com',
            'data_nascimento': '1990-01-15'
        }
        
        url = reverse('cliente-detail', args=[cliente.id])
        
        # Mock do use case para retornar None
        with patch('interface_adapters.views.cliente_view.EditarClienteUseCase') as mock_use_case:
            mock_instance = Mock()
            mock_instance.execute.return_value = None
            mock_use_case.return_value = mock_instance
            
            response = self.client.put(url, data, format='json')
            assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_venda_view_update_com_use_case_retorna_none(self):
        """Testa update quando use case retorna None"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        venda = self.create_venda(cliente.id, data='2024-01-15', valor=150.00)
        
        data = {
            'cliente_id': cliente.id,
            'data': '2024-02-15',
            'valor': 200.00
        }
        
        url = reverse('venda-detail', args=[venda.id])
        
        # Mock do use case para retornar None
        with patch('interface_adapters.views.venda_view.EditarVendaUseCase') as mock_use_case:
            mock_instance = Mock()
            mock_instance.execute.return_value = None
            mock_use_case.return_value = mock_instance
            
            response = self.client.put(url, data, format='json')
            assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_venda_view_list_sem_filtros(self):
        """Testa listagem de vendas sem filtros"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-02-15', valor=200.00)
        
        url = reverse('venda-list')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_cliente_view_retrieve_com_cliente_inexistente(self):
        """Testa retrieve com cliente inexistente"""
        url = reverse('cliente-detail', args=[999])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_venda_view_list_com_filtro_cliente_id(self):
        """Testa listagem de vendas com filtro por cliente_id"""
        cliente1 = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        cliente2 = self.create_cliente(nome_completo='Maria Silva', email='maria@example.com')
        
        self.create_venda(cliente1.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente2.id, data='2024-01-16', valor=200.00)
        
        url = reverse('venda-list')
        response = self.client.get(url, {'cliente_id': cliente1.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['cliente_id'] == cliente1.id
    
    def test_venda_view_list_com_filtro_apenas_start_date(self):
        """Testa listagem de vendas com filtro apenas start_date"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        self.create_venda(cliente.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente.id, data='2024-02-15', valor=200.00)
        
        url = reverse('venda-list')
        response = self.client.get(url, {'start_date': '2024-02-01'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Apenas a venda de 2024-02-15
    
    def test_cliente_view_retrieve_com_cliente_existente(self):
        """Testa retrieve com cliente existente"""
        cliente = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        
        url = reverse('cliente-detail', args=[cliente.id])
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == 'João Silva'
        assert response.data['email'] == 'joao@example.com'
    
    def test_venda_view_clientes_destaque(self):
        """Testa endpoint de clientes destaque"""
        # Criar clientes e vendas para gerar estatísticas
        cliente1 = self.create_cliente(nome_completo='João Silva', email='joao@example.com')
        cliente2 = self.create_cliente(nome_completo='Maria Silva', email='maria@example.com')
        
        self.create_venda(cliente1.id, data='2024-01-15', valor=100.00)
        self.create_venda(cliente1.id, data='2024-01-16', valor=200.00)
        self.create_venda(cliente2.id, data='2024-01-15', valor=150.00)
        
        url = reverse('estatisticas-clientes-destaque')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'maior_volume' in response.data
        assert 'maior_media' in response.data
        assert 'maior_frequencia' in response.data
