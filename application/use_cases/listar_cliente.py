from domain.repositories.cliente_repository import ClienteRepository
from application.dtos.cliente_dto import ClienteDTO
from typing import Optional


class ListarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.__cliente_repository = cliente_repository

    def execute(self, cliente_id: int) -> Optional[ClienteDTO]:
        cliente = self.__cliente_repository.get(cliente_id)
        if not cliente:
            return None
        return ClienteDTO(
            id=cliente.id,
            nome_completo=cliente.nome_completo,
            email=cliente.email,
            data_nascimento=cliente.data_nascimento
        ) 