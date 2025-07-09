from domain.repositories.cliente_repository import ClienteRepository
from application.dtos.cliente_create_dto import ClienteCreateDTO
from application.dtos.cliente_dto import ClienteDTO
from domain.entities.cliente import Cliente


class CadastrarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.__cliente_repository = cliente_repository

    def execute(self, dto: ClienteCreateDTO) -> ClienteDTO:
        novo_cliente = Cliente(
            id=None,
            nome_completo=dto.nome_completo,
            email=dto.email,
            data_nascimento=dto.data_nascimento
        )
        cliente_salvo = self.__cliente_repository.add(novo_cliente)
        return ClienteDTO(
            id=cliente_salvo.id,
            nome_completo=cliente_salvo.nome_completo,
            email=cliente_salvo.email,
            data_nascimento=cliente_salvo.data_nascimento
        )
