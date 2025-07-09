from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.venda import Venda

class VendaRepository(ABC):
    @abstractmethod
    def add(self, venda: Venda) -> Venda:
        pass

    @abstractmethod
    def get(self, venda_id: int) -> Optional[Venda]:
        pass

    @abstractmethod
    def update(self, venda: Venda) -> Venda:
        pass

    @abstractmethod
    def delete(self, venda_id: int) -> None:
        pass

    @abstractmethod
    def list_by_cliente(self, cliente_id: int) -> List[Venda]:
        pass

    @abstractmethod
    def list_by_period(self, start_date, end_date) -> List[Venda]:
        pass
