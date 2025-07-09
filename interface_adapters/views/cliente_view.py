import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from interface_adapters.serializers.cliente_serializer import ClienteSerializer
from infra.repositories.cliente_repository_impl import ClienteRepositoryImpl
from application.use_cases.cadastrar_cliente import CadastrarClienteUseCase
from application.use_cases.listar_clientes import ListarClientesUseCase
from application.use_cases.editar_cliente import EditarClienteUseCase
from application.use_cases.deletar_cliente import DeletarClienteUseCase
from application.use_cases.listar_cliente import ListarClienteUseCase
from application.dtos.cliente_create_dto import ClienteCreateDTO
from application.dtos.cliente_update_dto import ClienteUpdateDTO
from rest_framework.permissions import IsAuthenticated
from infra.models.cliente_model import ClienteModel
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


logger = logging.getLogger(__name__)

@extend_schema(tags=['clientes'])
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = ClienteModel.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Listar clientes",
        description="Retorna uma lista de clientes com possibilidade de filtros",
        parameters=[
            OpenApiParameter(name='nome', description='Filtrar por nome', required=False, type=str),
            OpenApiParameter(name='email', description='Filtrar por email', required=False, type=str),
        ],
        responses={200: ClienteSerializer(many=True)}
    )
    def list(self, request):
        logger.info('Listando clientes', extra={'params': request.query_params.dict()})
        repo = ClienteRepositoryImpl()
        use_case = ListarClientesUseCase(repo)
        nome = request.query_params.get('nome')
        email = request.query_params.get('email')
        clientes = use_case.execute(nome=nome, email=email)
        serializer = ClienteSerializer([c for c in clientes], many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Criar cliente",
        description="Cria um novo cliente no sistema",
        request=ClienteSerializer,
        responses={201: ClienteSerializer}
    )
    def create(self, request):
        logger.info('Cadastrando novo cliente', extra={'data': request.data})
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = ClienteCreateDTO(
            nome_completo=serializer.validated_data['nome_completo'],
            email=serializer.validated_data['email'],
            data_nascimento=serializer.validated_data['data_nascimento']
        )
        repo = ClienteRepositoryImpl()
        use_case = CadastrarClienteUseCase(repo)
        cliente = use_case.execute(dto)
        response_serializer = ClienteSerializer({
            'id': cliente.id,
            'nome_completo': cliente.nome_completo,
            'email': cliente.email,
            'data_nascimento': cliente.data_nascimento
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Atualizar cliente",
        description="Atualiza os dados de um cliente existente",
        request=ClienteSerializer,
        responses={200: ClienteSerializer, 404: None}
    )
    def update(self, request, pk=None, partial=False):
        logger.info(f'Editando cliente id={pk}', extra={'data': request.data})
        try:
            instance = ClienteModel.objects.get(pk=pk)
        except ClienteModel.DoesNotExist:
            return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        dto = ClienteUpdateDTO(
            nome_completo=serializer.validated_data.get('nome_completo'),
            email=serializer.validated_data.get('email'),
            data_nascimento=serializer.validated_data.get('data_nascimento')
        )
        repo = ClienteRepositoryImpl()
        use_case = EditarClienteUseCase(repo)
        cliente = use_case.execute(int(pk), dto)
        if not cliente:
            return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        response_serializer = ClienteSerializer({
            'id': cliente.id,
            'nome_completo': cliente.nome_completo,
            'email': cliente.email,
            'data_nascimento': cliente.data_nascimento
        })
        return Response(response_serializer.data)

    @extend_schema(
        summary="Atualizar cliente (parcial)",
        description="Atualiza parcialmente os dados de um cliente existente",
        request=ClienteSerializer,
        responses={200: ClienteSerializer, 404: None}
    )
    def partial_update(self, request, pk=None):
        logger.info(f'Editando cliente id={pk} (parcial)', extra={'data': request.data})
        try:
            instance = ClienteModel.objects.get(pk=pk)
        except ClienteModel.DoesNotExist:
            return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        dto = ClienteUpdateDTO(
            nome_completo=serializer.validated_data.get('nome_completo'),
            email=serializer.validated_data.get('email'),
            data_nascimento=serializer.validated_data.get('data_nascimento')
        )
        repo = ClienteRepositoryImpl()
        use_case = EditarClienteUseCase(repo)
        cliente = use_case.execute(int(pk), dto)

        if not cliente:
            return Response(
                {'detail': 'Cliente não encontrado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )  # pragma: no cover
        response_serializer = ClienteSerializer({
            'id': cliente.id,
            'nome_completo': cliente.nome_completo,
            'email': cliente.email,
            'data_nascimento': cliente.data_nascimento
        })
        return Response(response_serializer.data)

    @extend_schema(
        summary="Deletar cliente",
        description="Remove um cliente do sistema",
        responses={204: None}
    )
    def destroy(self, request, pk=None):
        logger.info(f'Deletando cliente id={pk}')
        repo = ClienteRepositoryImpl()
        use_case = DeletarClienteUseCase(repo)
        deleted = use_case.execute(int(pk))
        if not deleted:
            return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Obter cliente específico",
        description="Retorna um cliente específico por ID",
        responses={200: ClienteSerializer, 404: None}
    )
    def retrieve(self, request, pk=None):
        logger.info(f'Listando cliente id={pk}')
        repo = ClienteRepositoryImpl()
        use_case = ListarClienteUseCase(repo)
        cliente = use_case.execute(int(pk))
        if not cliente:
            return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)