from datetime import date


class VendaCreateDTO:
    def __init__(self, cliente_id: int, data: date, valor: float):
        self.__cliente_id = cliente_id
        self.__data = data
        self.__valor = valor

    @property
    def cliente_id(self) -> int:
        return self.__cliente_id

    @property
    def data(self) -> date:
        return self.__data

    @property
    def valor(self) -> float:
        return self.__valor 