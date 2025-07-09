import pytest
from unittest.mock import Mock, patch
from datetime import date, datetime, timedelta
from application.use_cases.cadastrar_cliente import CadastrarClienteUseCase
from application.use_cases.listar_clientes import ListarClientesUseCase
from application.use_cases.listar_cliente import ListarClienteUseCase
from application.use_cases.editar_cliente import EditarClienteUseCase
from application.use_cases.deletar_cliente import DeletarClienteUseCase
from application.use_cases.registrar_venda import RegistrarVendaUseCase
from application.use_cases.listar_venda import ListarVendaUseCase
from application.use_cases.editar_venda import EditarVendaUseCase
from application.use_cases.deletar_venda import DeletarVendaUseCase
from application.use_cases.estatisticas import EstatisticasUseCase
from application.dtos.cliente_dto import ClienteDTO
from application.dtos.venda_dto import VendaDTO
from application.dtos.estatisticas_dto import EstatisticasVendasPorDiaDTO, ClienteDestaqueDTO
from domain.entities.cliente import Cliente
from domain.entities.venda import Venda


class TestCadastrarClienteUseCase:
    """Testes para CadastrarClienteUseCase"""
    
    def test_executar_com_dados_validos(self, cliente_data):
        """Testa execução com dados válidos"""
        mock_repository = Mock()
        mock_cliente = Mock()
        mock_repository.add.return_value = mock_cliente
        
        use_case = CadastrarClienteUseCase(mock_repository)
        dto = ClienteDTO(id=None, **cliente_data)
        
        result = use_case.execute(dto)
        
        mock_repository.add.assert_called_once()
        assert result is not None
    
    def test_executar_com_email_duplicado(self, cliente_data):
        """Testa execução com email duplicado"""
        mock_repository = Mock()
        mock_repository.add.side_effect = Exception("Email já existe")
        
        use_case = CadastrarClienteUseCase(mock_repository)
        dto = ClienteDTO(id=None, **cliente_data)
        
        with pytest.raises(Exception):
            use_case.execute(dto)


class TestListarClientesUseCase:
    """Testes para ListarClientesUseCase"""
    
    def test_executar_sem_filtros(self):
        """Testa execução sem filtros"""
        mock_repository = Mock()
        mock_clientes = [Mock(), Mock()]
        mock_repository.list.return_value = mock_clientes
        
        use_case = ListarClientesUseCase(mock_repository)
        
        result = use_case.execute()
        
        mock_repository.list.assert_called_once_with(nome=None, email=None)
        assert len(result) == 2
    
    def test_executar_com_filtro_nome(self):
        """Testa execução com filtro por nome"""
        mock_repository = Mock()
        mock_clientes = [Mock()]
        mock_repository.list.return_value = mock_clientes
        
        use_case = ListarClientesUseCase(mock_repository)
        
        result = use_case.execute(nome="João")
        
        mock_repository.list.assert_called_once_with(nome="João", email=None)
        assert len(result) == 1
    
    def test_executar_com_filtro_email(self):
        """Testa execução com filtro por email"""
        mock_repository = Mock()
        mock_clientes = [Mock()]
        mock_repository.list.return_value = mock_clientes
        
        use_case = ListarClientesUseCase(mock_repository)
        
        result = use_case.execute(email="joao@example.com")
        
        mock_repository.list.assert_called_once_with(nome=None, email="joao@example.com")
        assert len(result) == 1


class TestListarClienteUseCase:
    """Testes para ListarClienteUseCase"""
    
    def test_executar_com_cliente_existente(self):
        """Testa execução com cliente existente"""
        mock_repository = Mock()
        mock_cliente = Mock()
        mock_repository.get.return_value = mock_cliente
        
        use_case = ListarClienteUseCase(mock_repository)
        
        result = use_case.execute(1)
        
        mock_repository.get.assert_called_once_with(1)
        assert result is not None
    
    def test_executar_com_cliente_inexistente(self):
        """Testa execução com cliente inexistente"""
        mock_repository = Mock()
        mock_repository.get.return_value = None
        
        use_case = ListarClienteUseCase(mock_repository)
        
        result = use_case.execute(999)
        
        mock_repository.get.assert_called_once_with(999)
        assert result is None


class TestEditarClienteUseCase:
    """Testes para EditarClienteUseCase"""
    
    def test_executar_com_cliente_existente(self, cliente_data):
        """Testa execução com cliente existente"""
        mock_repository = Mock()
        mock_cliente = Mock()
        mock_cliente.id = 1
        mock_cliente.nome_completo = 'João Silva'
        mock_cliente.email = 'joao@example.com'
        mock_cliente.data_nascimento = date(1990, 1, 15)
        mock_repository.get.return_value = mock_cliente
        mock_repository.update.return_value = mock_cliente
        
        use_case = EditarClienteUseCase(mock_repository)
        dto = ClienteDTO(id=None, **cliente_data)
        
        result = use_case.execute(1, dto)
        
        mock_repository.get.assert_called_once_with(1)
        mock_repository.update.assert_called_once()
        assert result is not None
        assert result.nome_completo == cliente_data['nome_completo']
    
    def test_executar_com_cliente_inexistente(self, cliente_data):
        """Testa execução com cliente inexistente"""
        mock_repository = Mock()
        mock_repository.get.return_value = None
        
        use_case = EditarClienteUseCase(mock_repository)
        dto = ClienteDTO(id=None, **cliente_data)
        
        result = use_case.execute(999, dto)
        
        mock_repository.get.assert_called_once_with(999)
        mock_repository.update.assert_not_called()
        assert result is None


class TestDeletarClienteUseCase:
    """Testes para DeletarClienteUseCase"""
    
    def test_executar_com_cliente_existente(self):
        """Testa execução com cliente existente"""
        mock_repository = Mock()
        mock_repository.get.return_value = Mock()
        mock_repository.delete.return_value = True
        
        use_case = DeletarClienteUseCase(mock_repository)
        
        result = use_case.execute(1)
        
        mock_repository.get.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)
        assert result is True
    
    def test_executar_com_cliente_inexistente(self):
        """Testa execução com cliente inexistente"""
        mock_repository = Mock()
        mock_repository.get.return_value = None
        
        use_case = DeletarClienteUseCase(mock_repository)
        
        result = use_case.execute(999)
        
        mock_repository.get.assert_called_once_with(999)
        mock_repository.delete.assert_not_called()
        assert result is False


class TestRegistrarVendaUseCase:
    """Testes para RegistrarVendaUseCase"""
    
    def test_executar_com_dados_validos(self, venda_data):
        """Testa execução com dados válidos"""
        mock_repository = Mock()
        mock_venda = Mock()
        mock_repository.add.return_value = mock_venda
        
        use_case = RegistrarVendaUseCase(mock_repository)
        dto = VendaDTO(id=None, **venda_data)
        
        result = use_case.execute(dto)
        
        mock_repository.add.assert_called_once()
        assert result is not None
    
    def test_executar_com_cliente_inexistente(self, venda_data):
        """Testa execução com cliente inexistente"""
        mock_repository = Mock()
        mock_repository.add.side_effect = Exception("Cliente não encontrado")
        
        use_case = RegistrarVendaUseCase(mock_repository)
        dto = VendaDTO(id=None, **venda_data)
        
        with pytest.raises(Exception):
            use_case.execute(dto)


class TestListarVendaUseCase:
    """Testes para ListarVendaUseCase"""
    
    def test_executar_com_venda_existente(self):
        """Testa execução com venda existente"""
        mock_repository = Mock()
        mock_venda = Mock()
        mock_repository.get.return_value = mock_venda
        
        use_case = ListarVendaUseCase(mock_repository)
        
        result = use_case.execute(1)
        
        mock_repository.get.assert_called_once_with(1)
        assert result is not None
    
    def test_executar_com_venda_inexistente(self):
        """Testa execução com venda inexistente"""
        mock_repository = Mock()
        mock_repository.get.return_value = None
        
        use_case = ListarVendaUseCase(mock_repository)
        
        result = use_case.execute(999)
        
        mock_repository.get.assert_called_once_with(999)
        assert result is None


class TestEditarVendaUseCase:
    """Testes para EditarVendaUseCase"""
    
    def test_executar_com_venda_existente(self, venda_data):
        """Testa execução com venda existente"""
        mock_repository = Mock()
        mock_venda = Mock()
        mock_venda.id = 1
        mock_venda.cliente_id = 1
        mock_venda.data = date(2024, 1, 15)
        mock_venda.valor = 150.0
        mock_repository.get.return_value = mock_venda
        mock_repository.update.return_value = mock_venda
        
        use_case = EditarVendaUseCase(mock_repository)
        dto = VendaDTO(id=None, **venda_data)
        
        result = use_case.execute(1, dto)
        
        mock_repository.get.assert_called_once_with(1)
        mock_repository.update.assert_called_once()
        assert result is not None
        assert result.cliente_id == venda_data['cliente_id']
    
    def test_executar_com_venda_inexistente(self, venda_data):
        """Testa execução com venda inexistente"""
        mock_repository = Mock()
        mock_repository.get.return_value = None
        
        use_case = EditarVendaUseCase(mock_repository)
        dto = VendaDTO(id=None, **venda_data)
        
        result = use_case.execute(999, dto)
        
        mock_repository.get.assert_called_once_with(999)
        mock_repository.update.assert_not_called()
        assert result is None


class TestDeletarVendaUseCase:
    """Testes para DeletarVendaUseCase"""
    
    def test_executar_com_venda_existente(self):
        """Testa execução com venda existente"""
        mock_repository = Mock()
        mock_repository.get.return_value = Mock()
        mock_repository.delete.return_value = True
        
        use_case = DeletarVendaUseCase(mock_repository)
        
        result = use_case.execute(1)
        
        mock_repository.get.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)
        assert result is True
    
    def test_executar_com_venda_inexistente(self):
        """Testa execução com venda inexistente"""
        mock_repository = Mock()
        mock_repository.get.return_value = None
        
        use_case = DeletarVendaUseCase(mock_repository)
        
        result = use_case.execute(999)
        
        mock_repository.get.assert_called_once_with(999)
        mock_repository.delete.assert_not_called()
        assert result is False


class TestEstatisticasUseCase:
    """Testes para EstatisticasUseCase"""
    
    @pytest.mark.django_db
    def test_vendas_por_dia_ultimos_30_dias(self):
        """Testa geração de estatísticas dos últimos 30 dias"""
        from infra.models.venda_model import VendaModel
        
        # Mock do ORM - quando não há filtros, usa values() diretamente
        with patch.object(VendaModel.objects, 'values') as mock_values:
            mock_annotate = Mock()
            mock_order_by = Mock()
            mock_order_by.order_by.return_value = [
                {'data': date(2024, 1, 15), 'total_vendas': 300.0},
                {'data': date(2024, 1, 16), 'total_vendas': 150.0},
            ]
            mock_annotate.annotate.return_value = mock_order_by
            mock_values.return_value = mock_annotate
            
            use_case = EstatisticasUseCase(Mock())
            result = use_case.vendas_por_dia()
            
            # Verifica se retorna um DTO com a propriedade vendas_por_dia
            assert hasattr(result, 'vendas_por_dia')
            assert len(result.vendas_por_dia) == 2  # 2 dias diferentes
    
    @pytest.mark.django_db
    def test_vendas_por_dia_periodo_customizado(self):
        """Testa geração de estatísticas com período customizado"""
        from infra.models.venda_model import VendaModel
        
        # Mock do ORM
        with patch.object(VendaModel.objects, 'filter') as mock_filter:
            mock_values = Mock()
            mock_values.values.return_value = mock_values
            mock_values.annotate.return_value = mock_values
            mock_values.order_by.return_value = [
                {'data': date(2024, 1, 15), 'total_vendas': 100.0},
            ]
            mock_filter.return_value = mock_values
            
            use_case = EstatisticasUseCase(Mock())
            start_date = "2024-01-01"
            end_date = "2024-01-31"
            result = use_case.vendas_por_dia(data_inicio=start_date, data_fim=end_date)
            
            assert hasattr(result, 'vendas_por_dia')
            assert len(result.vendas_por_dia) == 1
    
    @pytest.mark.django_db
    def test_clientes_destaque(self):
        """Testa geração de estatísticas de clientes destaque"""
        mock_repository = Mock()
        
        use_case = EstatisticasUseCase(mock_repository)
        
        result = use_case.clientes_destaque()
        
        assert 'maior_volume' in result
        assert 'maior_media' in result
        assert 'maior_frequencia' in result
        
        # Verifica se os dados estão corretos
        assert result['maior_volume'] is not None
        assert result['maior_media'] is not None
        assert result['maior_frequencia'] is not None
    
    @pytest.mark.django_db
    def test_vendas_por_dia_apenas_data_inicio(self):
        """Testa vendas por dia com apenas data_inicio"""
        from infra.models.venda_model import VendaModel
        
        with patch.object(VendaModel.objects, 'filter') as mock_filter:
            mock_values = Mock()
            mock_values.values.return_value = mock_values
            mock_values.annotate.return_value = mock_values
            mock_values.order_by.return_value = [
                {'data': date(2024, 1, 15), 'total_vendas': 100.0},
            ]
            mock_filter.return_value = mock_values
            
            use_case = EstatisticasUseCase(Mock())
            result = use_case.vendas_por_dia(data_inicio="2024-01-01")
            
            assert hasattr(result, 'vendas_por_dia')
            assert len(result.vendas_por_dia) == 1
    
    @pytest.mark.django_db
    def test_vendas_por_dia_apenas_data_fim(self):
        """Testa vendas por dia com apenas data_fim"""
        from infra.models.venda_model import VendaModel
        
        with patch.object(VendaModel.objects, 'filter') as mock_filter:
            mock_values = Mock()
            mock_values.values.return_value = mock_values
            mock_values.annotate.return_value = mock_values
            mock_values.order_by.return_value = [
                {'data': date(2024, 1, 15), 'total_vendas': 100.0},
            ]
            mock_filter.return_value = mock_values
            
            use_case = EstatisticasUseCase(Mock())
            result = use_case.vendas_por_dia(data_fim="2024-01-31")
            
            assert hasattr(result, 'vendas_por_dia')
            assert len(result.vendas_por_dia) == 1


class TestEstatisticasDTOs:
    """Testes para os DTOs de estatísticas"""
    
    def test_estatisticas_vendas_por_dia_dto(self):
        """Testa EstatisticasVendasPorDiaDTO"""
        vendas_data = [
            {'data': date(2024, 1, 15), 'total_vendas': 300.0},
            {'data': date(2024, 1, 16), 'total_vendas': 150.0}
        ]
        
        dto = EstatisticasVendasPorDiaDTO(vendas_por_dia=vendas_data)
        
        assert dto.vendas_por_dia == vendas_data
        assert len(dto.vendas_por_dia) == 2
        assert dto.vendas_por_dia[0]['data'] == date(2024, 1, 15)
        assert dto.vendas_por_dia[0]['total_vendas'] == 300.0
    
    def test_cliente_destaque_dto(self):
        """Testa ClienteDestaqueDTO"""
        dto = ClienteDestaqueDTO(
            cliente_id=1,
            nome_completo='João Silva',
            valor=500.0
        )
        
        assert dto.cliente_id == 1
        assert dto.nome_completo == 'João Silva'
        assert dto.valor == 500.0
    
    def test_cliente_destaque_dto_com_valores_zero(self):
        """Testa ClienteDestaqueDTO com valores zero"""
        dto = ClienteDestaqueDTO(
            cliente_id=0,
            nome_completo='',
            valor=0.0
        )
        
        assert dto.cliente_id == 0
        assert dto.nome_completo == ''
        assert dto.valor == 0.0
    
    def test_cliente_destaque_dto_com_valores_negativos(self):
        """Testa ClienteDestaqueDTO com valores negativos"""
        dto = ClienteDestaqueDTO(
            cliente_id=-1,
            nome_completo='Teste',
            valor=-100.0
        )
        
        assert dto.cliente_id == -1
        assert dto.nome_completo == 'Teste'
        assert dto.valor == -100.0 