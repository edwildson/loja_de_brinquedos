from rest_framework import viewsets, status
from rest_framework.response import Response
from interface_adapters.serializers.venda_serializer import VendaSerializer
from infra.repositories.venda_repository_impl import VendaRepositoryImpl
from application.use_cases.registrar_venda import RegistrarVendaUseCase
from application.use_cases.listar_venda import ListarVendaUseCase
from application.use_cases.editar_venda import EditarVendaUseCase
from application.use_cases.deletar_venda import DeletarVendaUseCase
from application.dtos.venda_create_dto import VendaCreateDTO
from application.dtos.venda_update_dto import VendaUpdateDTO
from domain.repositories.venda_repository import VendaRepository
from application.use_cases.estatisticas import EstatisticasUseCase
from datetime import datetime
import logging
from infra.models.cliente_model import ClienteModel
from infra.models.venda_model import VendaModel
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

logger = logging.getLogger(__name__)


@extend_schema(tags=['vendas'])
class VendaViewSet(viewsets.ModelViewSet):
    queryset = VendaModel.objects.all()
    serializer_class = VendaSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Listar vendas",
        description="Retorna uma lista de vendas com possibilidade de filtros",
        parameters=[
            OpenApiParameter(name='cliente_id', description='Filtrar por cliente', required=False, type=int),
            OpenApiParameter(name='start_date', description='Data inicial (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='end_date', description='Data final (YYYY-MM-DD)', required=False, type=str),
        ],
        responses={200: VendaSerializer(many=True)}
    )
    def list(self, request):
        logger.info('Listando vendas', extra={'params': request.query_params.dict()})
        cliente_id = request.query_params.get('cliente_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if cliente_id:
            vendas = VendaModel.objects.filter(cliente_id=int(cliente_id))
        else:
            vendas = VendaModel.objects.all()
            if start_date:
                vendas = vendas.filter(data__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
            if end_date:
                vendas = vendas.filter(data__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Criar venda",
        description="Registra uma nova venda no sistema",
        request=VendaSerializer,
        responses={201: VendaSerializer}
    )
    def create(self, request):
        logger.info('Registrando nova venda', extra={'data': request.data})
        serializer = VendaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = VendaCreateDTO(
            cliente_id=serializer.validated_data['cliente_id'],
            data=serializer.validated_data['data'],
            valor=serializer.validated_data['valor']
        )
        repo = VendaRepositoryImpl()
        use_case = RegistrarVendaUseCase(repo)
        venda = use_case.execute(dto)
        cliente_obj = ClienteModel.objects.get(id=venda.cliente_id)
        response_serializer = VendaSerializer({
            'id': venda.id,
            'cliente': cliente_obj,
            'data': venda.data,
            'valor': venda.valor
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Obter venda específica",
        description="Retorna uma venda específica por ID",
        responses={200: VendaSerializer, 404: None}
    )
    def retrieve(self, request, pk=None):
        logger.info(f'Listando venda id={pk}')
        repo = VendaRepositoryImpl()
        use_case = ListarVendaUseCase(repo)
        venda = use_case.execute(int(pk))
        if not venda:
            return Response({'detail': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        cliente_obj = ClienteModel.objects.get(id=venda.cliente_id)
        serializer = VendaSerializer({
            'id': venda.id,
            'cliente': cliente_obj,
            'data': venda.data,
            'valor': venda.valor
        })
        return Response(serializer.data)

    @extend_schema(
        summary="Atualizar venda",
        description="Atualiza os dados de uma venda existente",
        request=VendaSerializer,
        responses={200: VendaSerializer, 404: None}
    )
    def update(self, request, pk=None, partial=False):
        logger.info(f'Editando venda id={pk}', extra={'data': request.data})
        try:
            instance = VendaModel.objects.get(pk=pk)
        except VendaModel.DoesNotExist:
            return Response({'detail': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendaSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        dto = VendaUpdateDTO(
            cliente_id=serializer.validated_data.get('cliente_id'),
            data=serializer.validated_data.get('data'),
            valor=serializer.validated_data.get('valor')
        )
        repo = VendaRepositoryImpl()
        use_case = EditarVendaUseCase(repo)
        venda = use_case.execute(int(pk), dto)
        if not venda:
            return Response({'detail': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        cliente_obj = ClienteModel.objects.get(id=venda.cliente_id)
        response_serializer = VendaSerializer({
            'id': venda.id,
            'cliente': cliente_obj,
            'data': venda.data,
            'valor': venda.valor
        })
        return Response(response_serializer.data)

    @extend_schema(
        summary="Atualizar venda (parcial)",
        description="Atualiza parcialmente os dados de uma venda existente",
        request=VendaSerializer,
        responses={200: VendaSerializer, 404: None}
    )
    def partial_update(self, request, pk=None):
        logger.info(f'Editando venda id={pk} (parcial)', extra={'data': request.data})
        try:
            instance = VendaModel.objects.get(pk=pk)
        except VendaModel.DoesNotExist:
            return Response({'detail': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendaSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        dto = VendaUpdateDTO(
            cliente_id=serializer.validated_data.get('cliente_id'),
            data=serializer.validated_data.get('data'),
            valor=serializer.validated_data.get('valor')
        )
        repo = VendaRepositoryImpl()
        use_case = EditarVendaUseCase(repo)
        venda = use_case.execute(int(pk), dto)
        if not venda:
            return Response(
                {'detail': 'Venda não encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )  # pragma: no cover
        cliente_obj = ClienteModel.objects.get(id=venda.cliente_id)
        response_serializer = VendaSerializer({
            'id': venda.id,
            'cliente': cliente_obj,
            'data': venda.data,
            'valor': venda.valor
        })
        return Response(response_serializer.data)

    @extend_schema(
        summary="Deletar venda",
        description="Remove uma venda do sistema",
        responses={204: None}
    )
    def destroy(self, request, pk=None):
        logger.info(f'Deletando venda id={pk}')
        repo = VendaRepositoryImpl()
        use_case = DeletarVendaUseCase(repo)
        deleted = use_case.execute(int(pk))
        if not deleted:
            return Response({'detail': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Estatísticas de vendas por dia",
        description="Retorna o total de vendas agrupadas por dia",
        tags=['estatísticas'],
        parameters=[
            OpenApiParameter(name='data_inicio', description='Data inicial (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='data_fim', description='Data final (YYYY-MM-DD)', required=False, type=str),
        ],
        responses={200: None}
    )
    @action(detail=False, methods=['get'], url_path='estatisticas/vendas-por-dia', name='estatisticas-vendas-por-dia')
    def vendas_por_dia(self, request):
        logger.info('Obtendo estatísticas de vendas por dia', extra={'params': request.query_params.dict()})
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        use_case = EstatisticasUseCase(VendaRepositoryImpl())
        resultado = use_case.vendas_por_dia(data_inicio=data_inicio, data_fim=data_fim)
        return Response(resultado.vendas_por_dia)

    @extend_schema(
        summary="Estatísticas de clientes destaque",
        description="Retorna estatísticas dos clientes com maior volume, média e frequência de compras",
        tags=['estatísticas'],
        responses={200: None}
    )
    @action(detail=False, methods=['get'], url_path='estatisticas/clientes-destaque', name='estatisticas-clientes-destaque')
    def clientes_destaque(self, request):
        logger.info('Obtendo estatísticas de clientes destaque')
        use_case = EstatisticasUseCase(VendaRepositoryImpl())
        destaques = use_case.clientes_destaque()
        return Response(destaques)
