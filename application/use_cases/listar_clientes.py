from domain.repositories.cliente_repository import ClienteRepository
from application.dtos.cliente_dto import ClienteDTO
from typing import List, Optional


class ListarClientesUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.__cliente_repository = cliente_repository

    def execute(self, nome: Optional[str] = None, email: Optional[str] = None) -> List[ClienteDTO]:
        clientes = self.__cliente_repository.list(nome=nome, email=email)
        return [
            ClienteDTO(
                id=c.id,
                nome_completo=c.nome_completo,
                email=c.email,
                data_nascimento=c.data_nascimento
            ) for c in clientes
        ]
