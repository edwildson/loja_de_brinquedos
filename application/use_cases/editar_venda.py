from domain.repositories.venda_repository import VendaRepository
from application.dtos.venda_update_dto import VendaUpdateDTO
from application.dtos.venda_dto import VendaDTO
from domain.entities.venda import Venda
from typing import Optional


class EditarVendaUseCase:
    def __init__(self, venda_repository: VendaRepository):
        self.__venda_repository = venda_repository

    def execute(self, venda_id: int, dto: VendaUpdateDTO) -> Optional[VendaDTO]:
        venda = self.__venda_repository.get(venda_id)
        if not venda:
            return None
        
        # Atualiza apenas os campos fornecidos
        cliente_id = dto.cliente_id if dto.cliente_id is not None else venda.cliente_id
        data = dto.data if dto.data is not None else venda.data
        valor = dto.valor if dto.valor is not None else venda.valor
        
        venda_atualizada = Venda(
            id=venda.id,
            cliente_id=cliente_id,
            data=data,
            valor=valor
        )
        venda_salva = self.__venda_repository.update(venda_atualizada)
        return VendaDTO(
            id=venda_salva.id,
            cliente_id=venda_salva.cliente_id,
            data=venda_salva.data,
            valor=venda_salva.valor
        ) 