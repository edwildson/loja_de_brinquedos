from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.cliente import Cliente

class ClienteRepository(ABC):
    @abstractmethod
    def add(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def get(self, cliente_id: int) -> Optional[Cliente]:
        pass

    @abstractmethod
    def list(self, nome: Optional[str] = None, email: Optional[str] = None) -> List[Cliente]:
        pass

    @abstractmethod
    def update(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> None:
        pass
