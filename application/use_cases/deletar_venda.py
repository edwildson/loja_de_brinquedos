from domain.repositories.venda_repository import VendaRepository


class DeletarVendaUseCase:
    def __init__(self, venda_repository: VendaRepository):
        self.__venda_repository = venda_repository

    def execute(self, venda_id: int) -> bool:
        venda = self.__venda_repository.get(venda_id)
        if not venda:
            return False
        return self.__venda_repository.delete(venda_id) 