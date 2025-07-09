from datetime import date
from typing import Optional


class Venda:
    def __init__(self, id: Optional[int], cliente_id: int, data: date, valor: float):
        if cliente_id is None or cliente_id <= 0:
            raise ValueError("Cliente ID deve ser um número positivo")
        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        if data > date.today():
            raise ValueError("Data da venda não pode ser futura")
        self.__id = id
        self.__cliente_id = cliente_id
        self.__data = data
        self.__valor = valor

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def cliente_id(self) -> int:
        return self.__cliente_id

    @property
    def data(self) -> date:
        return self.__data

    @property
    def valor(self) -> float:
        return self.__valor

    def __eq__(self, other):
        if not isinstance(other, Venda):
            return False
        return (
            self.id == other.id and
            self.cliente_id == other.cliente_id and
            self.data == other.data and
            self.valor == other.valor
        )

    def __repr__(self):
        return f"Venda(id={self.id}, cliente_id={self.cliente_id}, data={self.data}, valor={self.valor})"
