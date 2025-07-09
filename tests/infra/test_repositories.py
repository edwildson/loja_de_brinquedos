import pytest
from datetime import date
from unittest.mock import patch
from infra.repositories.cliente_repository_impl import ClienteRepositoryImpl
from infra.repositories.venda_repository_impl import VendaRepositoryImpl
from domain.entities.cliente import Cliente
from domain.entities.venda import Venda
from infra.models.cliente_model import ClienteModel


class TestClienteRepositoryImpl:
    """Testes para ClienteRepositoryImpl"""
    
    def test_add_cliente_valido(self, db, cliente_entity):
        """Testa adicionar cliente válido"""
        repository = ClienteRepositoryImpl()
        
        result = repository.add(cliente_entity)
        
        assert result is not None
        assert result.nome_completo == cliente_entity.nome_completo
        assert result.email == cliente_entity.email
        # Converte string para date para comparação
        assert result.data_nascimento == date.fromisoformat(cliente_entity.data_nascimento.isoformat())
    
    def test_add_cliente_email_duplicado(self, db, cliente_entity):
        """Testa adicionar cliente com email duplicado"""
        repository = ClienteRepositoryImpl()
        
        # Adiciona primeiro cliente
        repository.add(cliente_entity)
        
        # Tenta adicionar cliente com mesmo email
        cliente_duplicado = Cliente(
            id=None,
            nome_completo='João Silva 2',
            email=cliente_entity.email,
            data_nascimento=date(1991, 1, 15)
        )
        
        with pytest.raises(Exception):
            repository.add(cliente_duplicado)
    
    def test_get_cliente_existente(self, db, cliente_model):
        """Testa buscar cliente existente"""
        repository = ClienteRepositoryImpl()
        
        result = repository.get(cliente_model.id)
        
        assert result is not None
        assert result.nome_completo == cliente_model.nome_completo
        assert result.email == cliente_model.email
        # Converter string para date antes de comparar
        expected_date = cliente_model.data_nascimento
        if isinstance(expected_date, str):
            expected_date = date.fromisoformat(expected_date)
        assert result.data_nascimento == expected_date
    
    def test_get_cliente_inexistente(self, db):
        """Testa buscar cliente inexistente"""
        repository = ClienteRepositoryImpl()
        
        result = repository.get(999)
        
        assert result is None
    
    def test_update_cliente_existente(self, db, cliente_model):
        """Testa atualizar cliente existente"""
        repository = ClienteRepositoryImpl()
        # Converter string para date
        data_nascimento = cliente_model.data_nascimento
        if isinstance(data_nascimento, str):
            data_nascimento = date.fromisoformat(data_nascimento)
        cliente_atualizado = Cliente(
            id=cliente_model.id,
            nome_completo='João Silva Atualizado',
            email=cliente_model.email,
            data_nascimento=data_nascimento
        )
        result = repository.update(cliente_atualizado)
        assert result is not None
        assert result.nome_completo == 'João Silva Atualizado'
        assert result.email == cliente_model.email
    
    def test_update_cliente_inexistente(self, db, cliente_entity):
        """Testa atualizar cliente inexistente"""
        repository = ClienteRepositoryImpl()
        
        with pytest.raises(Exception):
            repository.update(cliente_entity)
    
    def test_delete_cliente_existente(self, db, cliente_model):
        """Testa deletar cliente existente"""
        repository = ClienteRepositoryImpl()
        
        result = repository.delete(cliente_model.id)
        
        assert result is True
        
        # Verifica se foi realmente deletado
        cliente_deletado = repository.get(cliente_model.id)
        assert cliente_deletado is None
    
    def test_delete_cliente_inexistente(self, db):
        """Testa deletar cliente inexistente"""
        repository = ClienteRepositoryImpl()
        
        result = repository.delete(999)
        
        assert result is False
    
    def test_list_sem_filtros(self, db, multiple_clientes):
        """Testa listar clientes sem filtros"""
        repository = ClienteRepositoryImpl()
        
        result = repository.list()
        
        assert len(result) == 5
    
    def test_list_com_filtro_nome(self, db, multiple_clientes):
        """Testa listar clientes com filtro por nome"""
        repository = ClienteRepositoryImpl()
        
        result = repository.list(nome="Cliente 1")
        
        assert len(result) == 1
        assert result[0].nome_completo == "Cliente 1"
    
    def test_list_com_filtro_email(self, db, multiple_clientes):
        """Testa listar clientes com filtro por email"""
        repository = ClienteRepositoryImpl()
        
        result = repository.list(email="cliente1@example.com")
        
        assert len(result) == 1
        assert result[0].email == "cliente1@example.com"
    
    def test_list_com_filtros_combinations(self, db, multiple_clientes):
        """Testa listar clientes com combinações de filtros"""
        repository = ClienteRepositoryImpl()
        
        result = repository.list(nome="Cliente", email="cliente1@example.com")
        
        assert len(result) == 1
        assert result[0].nome_completo == "Cliente 1"
        assert result[0].email == "cliente1@example.com"


class TestVendaRepositoryImpl:
    """Testes para VendaRepositoryImpl"""
    
    def test_add_venda_valida(self, db, cliente_model, venda_entity):
        """Testa adicionar venda válida"""
        repository = VendaRepositoryImpl()
        
        # Atualiza cliente_id da entidade
        venda_entity = Venda(
            id=None,
            cliente_id=cliente_model.id,
            data=venda_entity.data,
            valor=venda_entity.valor
        )
        
        result = repository.add(venda_entity)
        
        assert result is not None
        assert result.cliente_id == cliente_model.id
        # Converte string para date para comparação
        assert result.data == date.fromisoformat(venda_entity.data.isoformat())
        assert result.valor == venda_entity.valor
    
    def test_add_venda_cliente_inexistente(self, db, venda_entity):
        """Testa adicionar venda com cliente inexistente"""
        repository = VendaRepositoryImpl()
        
        # Cria uma venda com cliente_id inexistente
        venda_inexistente = Venda(
            id=None,
            cliente_id=999,
            data=venda_entity.data,
            valor=venda_entity.valor
        )
        
        with pytest.raises(Exception):
            repository.add(venda_inexistente)
    
    def test_get_venda_existente(self, db, venda_model):
        """Testa buscar venda existente"""
        repository = VendaRepositoryImpl()
        result = repository.get(venda_model.id)
        assert result is not None
        assert result.cliente_id == venda_model.cliente_id
        # Converter string para date antes de comparar
        expected_date = venda_model.data
        if isinstance(expected_date, str):
            expected_date = date.fromisoformat(expected_date)
        assert result.data == expected_date
        assert result.valor == venda_model.valor
    
    def test_get_venda_inexistente(self, db):
        """Testa buscar venda inexistente"""
        repository = VendaRepositoryImpl()
        
        result = repository.get(999)
        
        assert result is None
    
    def test_update_venda_existente(self, db, venda_model):
        """Testa atualizar venda existente"""
        repository = VendaRepositoryImpl()
        
        venda_atualizada = Venda(
            id=venda_model.id,
            cliente_id=venda_model.cliente_id,
            data=date(2024, 2, 15),
            valor=200.00
        )
        
        result = repository.update(venda_atualizada)
        
        assert result is not None
        assert result.data == date(2024, 2, 15)
        assert result.valor == 200.00
    
    def test_update_venda_inexistente(self, db, venda_entity):
        """Testa atualizar venda inexistente"""
        repository = VendaRepositoryImpl()
        
        with pytest.raises(Exception):
            repository.update(venda_entity)
    
    def test_delete_venda_existente(self, db, venda_model):
        """Testa deletar venda existente"""
        repository = VendaRepositoryImpl()
        
        result = repository.delete(venda_model.id)
        
        assert result is True
        
        # Verifica se foi realmente deletada
        venda_deletada = repository.get(venda_model.id)
        assert venda_deletada is None
    
    def test_delete_venda_inexistente(self, db):
        """Testa deletar venda inexistente"""
        repository = VendaRepositoryImpl()
        
        result = repository.delete(999)
        
        assert result is False
    
    def test_list_by_cliente(self, db, multiple_vendas):
        """Testa listar vendas por cliente"""
        repository = VendaRepositoryImpl()
        
        # Pega o primeiro cliente
        cliente = ClienteModel.objects.first()
        
        result = repository.list_by_cliente(cliente.id)
        
        assert len(result) == 3  # 3 vendas por cliente
    
    def test_list_by_period_sem_filtros(self, db, multiple_vendas):
        """Testa listar vendas por período sem filtros"""
        repository = VendaRepositoryImpl()
        
        # Usa datas padrão para o período
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)
        
        result = repository.list_by_period(start_date, end_date)
        
        assert len(result) == 15  # 5 clientes * 3 vendas
    
    def test_list_by_period_com_filtros(self, db, multiple_vendas):
        """Testa listar vendas por período com filtros"""
        repository = VendaRepositoryImpl()
        
        start_date = date(2024, 1, 15)
        end_date = date(2024, 1, 17)
        
        result = repository.list_by_period(start_date, end_date)
        
        assert len(result) > 0
        for venda in result:
            assert start_date <= venda.data <= end_date
    
    def test_get_clientes_destaque(self, db, multiple_vendas):
        """Testa buscar clientes destaque"""
        repository = VendaRepositoryImpl()
        
        result = repository.get_clientes_destaque()
        
        assert 'maior_volume' in result
        assert 'maior_media' in result
        assert 'maior_frequencia' in result
        
        # Verifica se os dados estão corretos
        assert result['maior_volume'] is not None
        assert result['maior_media'] is not None
        assert result['maior_frequencia'] is not None


class TestModels:
    """Testes para os models Django"""
    
    @pytest.mark.django_db
    def test_cliente_model_str(self):
        """Testa o método __str__ do ClienteModel"""
        from infra.models.cliente_model import ClienteModel
        
        cliente = ClienteModel.objects.create(
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        str_repr = str(cliente)
        assert 'João Silva' in str_repr
        # O __str__ retorna apenas o nome_completo, não o email
        assert str_repr == 'João Silva'
    
    @pytest.mark.django_db
    def test_venda_model_str(self):
        """Testa o método __str__ do VendaModel"""
        from infra.models.cliente_model import ClienteModel
        from infra.models.venda_model import VendaModel
        
        cliente = ClienteModel.objects.create(
            nome_completo='João Silva',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 15)
        )
        
        venda = VendaModel.objects.create(
            cliente=cliente,
            data=date(2024, 1, 15),
            valor=150.0
        )
        
        str_repr = str(venda)
        assert 'Venda' in str_repr
        assert 'João Silva' in str_repr
        assert str(venda.id) in str_repr 