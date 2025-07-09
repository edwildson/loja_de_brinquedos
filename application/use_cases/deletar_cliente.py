from domain.repositories.cliente_repository import ClienteRepository


class DeletarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.__cliente_repository = cliente_repository

    def execute(self, cliente_id: int) -> bool:
        cliente = self.__cliente_repository.get(cliente_id)
        if not cliente:
            return False
        return self.__cliente_repository.delete(cliente_id)
