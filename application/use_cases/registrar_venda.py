from domain.repositories.venda_repository import VendaRepository
from application.dtos.venda_create_dto import VendaCreateDTO
from application.dtos.venda_dto import VendaDTO
from domain.entities.venda import Venda


class RegistrarVendaUseCase:
    def __init__(self, venda_repository: VendaRepository):
        self.__venda_repository = venda_repository

    def execute(self, dto: VendaCreateDTO) -> VendaDTO:
        nova_venda = Venda(
            id=None,
            cliente_id=dto.cliente_id,
            data=dto.data,
            valor=dto.valor
        )
        venda_salva = self.__venda_repository.add(nova_venda)
        return VendaDTO(
            id=venda_salva.id,
            cliente_id=venda_salva.cliente_id,
            data=venda_salva.data,
            valor=venda_salva.valor
        )
