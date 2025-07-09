from domain.repositories.venda_repository import VendaRepository
from application.dtos.venda_dto import VendaDTO
from typing import Optional


class ListarVendaUseCase:
    def __init__(self, venda_repository: VendaRepository):
        self.__venda_repository = venda_repository

    def execute(self, venda_id: int) -> Optional[VendaDTO]:
        venda = self.__venda_repository.get(venda_id)
        if not venda:
            return None
        return VendaDTO(
            id=venda.id,
            cliente_id=venda.cliente_id,
            data=venda.data,
            valor=venda.valor
        ) 