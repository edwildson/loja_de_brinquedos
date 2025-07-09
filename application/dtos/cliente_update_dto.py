from datetime import date
from typing import Optional


class ClienteUpdateDTO:
    def __init__(self, nome_completo: Optional[str] = None, email: Optional[str] = None, data_nascimento: Optional[date] = None):
        self.__nome_completo = nome_completo
        self.__email = email
        self.__data_nascimento = data_nascimento

    @property
    def nome_completo(self) -> Optional[str]:
        return self.__nome_completo

    @property
    def email(self) -> Optional[str]:
        return self.__email

    @property
    def data_nascimento(self) -> Optional[date]:
        return self.__data_nascimento 