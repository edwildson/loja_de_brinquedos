from datetime import date
from typing import Optional, Union


class ClienteDTO:
    def __init__(self, id: Optional[int], nome_completo: str, email: str, data_nascimento: Union[date, str]):
        self.__id = id
        self.__nome_completo = nome_completo
        self.__email = email
        # Converte string para date se necessário
        if isinstance(data_nascimento, str):
            self.__data_nascimento = date.fromisoformat(data_nascimento)
        else:
            self.__data_nascimento = data_nascimento

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def nome_completo(self) -> str:
        return self.__nome_completo

    @property
    def email(self) -> str:
        return self.__email

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento
