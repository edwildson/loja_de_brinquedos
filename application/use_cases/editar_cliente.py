from domain.repositories.cliente_repository import ClienteRepository
from application.dtos.cliente_update_dto import ClienteUpdateDTO
from application.dtos.cliente_dto import ClienteDTO
from domain.entities.cliente import Cliente
from typing import Optional


class EditarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.__cliente_repository = cliente_repository

    def execute(self, cliente_id: int, dto: ClienteUpdateDTO) -> Optional[ClienteDTO]:
        cliente = self.__cliente_repository.get(cliente_id)
        if not cliente:
            return None
        # Atualiza apenas os campos fornecidos
        nome = dto.nome_completo if dto.nome_completo is not None else cliente.nome_completo
        email = dto.email if dto.email is not None else cliente.email
        data_nascimento = dto.data_nascimento if dto.data_nascimento is not None else cliente.data_nascimento
        cliente_atualizado = Cliente(
            id=cliente.id,
            nome_completo=nome,
            email=email,
            data_nascimento=data_nascimento
        )
        cliente_salvo = self.__cliente_repository.update(cliente_atualizado)
        return ClienteDTO(
            id=cliente_salvo.id,
            nome_completo=cliente_salvo.nome_completo,
            email=cliente_salvo.email,
            data_nascimento=cliente_salvo.data_nascimento
        )
