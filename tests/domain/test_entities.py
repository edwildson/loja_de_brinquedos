import pytest
from datetime import date
from domain.entities.cliente import Cliente
from domain.entities.venda import Venda


class TestCliente:
    """Testes para a entidade Cliente"""
    
    def test_criar_cliente_valido(self):
        """Testa criação de cliente com dados válidos"""
        cliente = Cliente(
            id=None,
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        assert cliente.nome_completo == 'João Silva'
        assert cliente.email == 'joao@example.com'
        assert cliente.data_nascimento == date(1990, 1, 15)
        assert cliente.id is None
    
    def test_criar_cliente_com_nome_vazio(self):
        """Testa criação de cliente com nome vazio"""
        with pytest.raises(ValueError, match="Nome completo é obrigatório"):
            Cliente(
                id=None,
                nome_completo='',
                email='joao@example.com',
                data_nascimento=date(1990, 1, 15)
            )
    
    def test_criar_cliente_com_email_invalido(self):
        """Testa criação de cliente com email inválido"""
        with pytest.raises(ValueError, match="Email deve ser válido"):
            Cliente(
                id=None,
                nome_completo='João Silva',
                email='email-invalido',
                data_nascimento=date(1990, 1, 15)
            )
    
    def test_criar_cliente_com_data_futura(self):
        """Testa criação de cliente com data de nascimento futura"""
        data_futura = date.today().replace(year=date.today().year + 1)
        with pytest.raises(ValueError, match="Data de nascimento não pode ser futura"):
            Cliente(
                id=None,
                nome_completo='João Silva',
                email='joao@example.com',
                data_nascimento=data_futura
            )
    
    def test_igualdade_entre_clientes(self):
        """Testa igualdade entre clientes com mesmo email"""
        cliente1 = Cliente(
            id=1,
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        cliente2 = Cliente(
            id=1,
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        assert cliente1 == cliente2
    
    def test_diferenca_entre_clientes(self):
        """Testa diferença entre clientes com emails diferentes"""
        cliente1 = Cliente(
            id=1,
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        cliente2 = Cliente(
            id=2,
            nome_completo='Maria Santos',
            email='maria@example.com',
            data_nascimento=date(1985, 5, 20)
        )
        
        assert cliente1 != cliente2


class TestVenda:
    """Testes para a entidade Venda"""
    
    def test_criar_venda_valida(self):
        """Testa criação de venda com dados válidos"""
        venda = Venda(
            id=None,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.00
        )
        
        assert venda.cliente_id == 1
        assert venda.data == date(2024, 1, 15)
        assert venda.valor == 150.00
        assert venda.id is None
    
    def test_criar_venda_com_valor_zero(self):
        """Testa criação de venda com valor zero"""
        with pytest.raises(ValueError, match="Valor deve ser maior que zero"):
            Venda(
                id=None,
                cliente_id=1,
                data=date(2024, 1, 15),
                valor=0.00
            )
    
    def test_criar_venda_com_valor_negativo(self):
        """Testa criação de venda com valor negativo"""
        with pytest.raises(ValueError, match="Valor deve ser maior que zero"):
            Venda(
                id=None,
                cliente_id=1,
                data=date(2024, 1, 15),
                valor=-50.00
            )
    
    def test_criar_venda_com_data_futura(self):
        """Testa criação de venda com data futura"""
        data_futura = date.today().replace(year=date.today().year + 1)
        with pytest.raises(ValueError, match="Data da venda não pode ser futura"):
            Venda(
                id=None,
                cliente_id=1,
                data=data_futura,
                valor=150.00
            )
    
    def test_criar_venda_com_cliente_id_invalido(self):
        """Testa criação de venda com cliente_id inválido"""
        with pytest.raises(ValueError, match="Cliente ID deve ser um número positivo"):
            Venda(
                id=None,
                cliente_id=0,
                data=date(2024, 1, 15),
                valor=150.00
            )
    
    def test_igualdade_entre_vendas(self):
        """Testa igualdade entre vendas com mesmos dados"""
        venda1 = Venda(
            id=1,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.00
        )
        venda2 = Venda(
            id=1,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.00
        )
        
        assert venda1 == venda2
    
    def test_diferenca_entre_vendas(self):
        """Testa diferença entre vendas com dados diferentes"""
        venda1 = Venda(
            id=1,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.00
        )
        venda2 = Venda(
            id=2,
            cliente_id=2,
            data=date(2024, 1, 16),
            valor=200.00
        )
        
        assert venda1 != venda2
    
    def test_venda_com_valor_decimal(self):
        """Testa criar venda com valor decimal"""
        venda = Venda(
            id=1,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.50
        )
        
        assert venda.id == 1
        assert venda.cliente_id == 1
        assert venda.data == date(2024, 1, 15)
        assert venda.valor == 150.50
    
    def test_venda_repr(self):
        """Testa o método __repr__ da venda"""
        venda = Venda(
            id=1,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.0
        )
        
        repr_str = repr(venda)
        assert "Venda" in repr_str
        assert "1" in repr_str
        assert "150.0" in repr_str
    
    def test_cliente_repr(self):
        """Testa o método __repr__ do cliente"""
        cliente = Cliente(
            id=1,
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        repr_str = repr(cliente)
        assert "Cliente" in repr_str
        assert "João Silva" in repr_str
        assert "joao@example.com" in repr_str
    
    def test_cliente_igualdade_com_tipo_diferente(self):
        """Testa igualdade com tipo diferente"""
        cliente = Cliente(
            id=1,
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        # Comparar com string (tipo diferente)
        assert cliente != "João Silva"
        
        # Comparar com None
        assert cliente != None
    
    def test_venda_igualdade_com_tipo_diferente(self):
        """Testa igualdade com tipo diferente"""
        venda = Venda(
            id=1,
            cliente_id=1,
            data=date(2024, 1, 15),
            valor=150.0
        )
        
        # Comparar com string (tipo diferente)
        assert venda != "Venda"
        
        # Comparar com None
        assert venda != None 