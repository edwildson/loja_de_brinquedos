import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from domain.entities.cliente import Cliente
from domain.entities.venda import Venda
from datetime import date, datetime
from infra.models.cliente_model import ClienteModel
from infra.models.venda_model import VendaModel


@pytest.fixture
def api_client():
    """Fixture para cliente da API"""
    return APIClient()


@pytest.fixture
def user():
    """Fixture para usuário de teste"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture para cliente autenticado"""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def cliente_data():
    """Fixture com dados de cliente válidos"""
    return {
        'nome_completo': 'João Silva',
        'email': 'joao@example.com',
        'data_nascimento': '1990-01-15'
    }


@pytest.fixture
def cliente_entity(cliente_data):
    """Fixture para entidade Cliente"""
    return Cliente(
        id=None,
        nome_completo=cliente_data['nome_completo'],
        email=cliente_data['email'],
        data_nascimento=date.fromisoformat(cliente_data['data_nascimento'])
    )


@pytest.fixture
def venda_data():
    """Fixture com dados de venda válidos"""
    return {
        'cliente_id': 1,
        'data': '2024-01-15',
        'valor': 150.00
    }


@pytest.fixture
def venda_entity(venda_data):
    """Fixture para entidade Venda"""
    return Venda(
        id=None,
        cliente_id=venda_data['cliente_id'],
        data=date.fromisoformat(venda_data['data']),
        valor=venda_data['valor']
    )


@pytest.fixture
def cliente_model(db, cliente_data):
    """Fixture para modelo Cliente no banco"""
    return ClienteModel.objects.create(**cliente_data)


@pytest.fixture
def venda_model(db, cliente_model, venda_data):
    """Fixture para modelo Venda no banco"""
    return VendaModel.objects.create(
        cliente_id=cliente_model.id,
        data=venda_data['data'],
        valor=venda_data['valor']
    )


@pytest.fixture
def multiple_clientes(db):
    """Fixture com múltiplos clientes para testes"""
    clientes = []
    for i in range(5):
        cliente = ClienteModel.objects.create(
            nome_completo=f'Cliente {i+1}',
            email=f'cliente{i+1}@example.com',
            data_nascimento=date(1990, 1, 1)
        )
        clientes.append(cliente)
    
    return clientes


@pytest.fixture
def multiple_vendas(db, multiple_clientes):
    """Fixture com múltiplas vendas para testes"""
    vendas = []
    for i, cliente in enumerate(multiple_clientes):
        for j in range(3):  # 3 vendas por cliente
            venda = VendaModel.objects.create(
                cliente_id=cliente.id,
                data=date(2024, 1, 15 + j),
                valor=100.00 + (i * 10) + j
            )
            vendas.append(venda)
    
    return vendas


class BaseTestCase(TestCase):
    """Classe base para testes com configurações comuns"""
    
    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}'
        )
    
    def create_cliente(self, **kwargs):
        """Helper para criar cliente de teste"""
        data = {
            'nome_completo': 'Test Cliente',
            'email': 'test@example.com',
            'data_nascimento': '1990-01-01'
        }
        data.update(kwargs)
        return ClienteModel.objects.create(**data)
    
    def create_venda(self, cliente_id, **kwargs):
        """Helper para criar venda de teste"""
        data = {
            'cliente_id': cliente_id,
            'data': '2024-01-15',
            'valor': 100.00
        }
        data.update(kwargs)
        return VendaModel.objects.create(**data) 