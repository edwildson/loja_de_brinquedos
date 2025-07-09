from datetime import date
from typing import Optional, Union


class VendaDTO:
    def __init__(self, id: Optional[int], cliente_id: int, data: Union[date, str], valor: float):
        self.__id = id
        self.__cliente_id = cliente_id
        # Converte string para date se necessário
        if isinstance(data, str):
            self.__data = date.fromisoformat(data)
        else:
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
