from datetime import date


class ClienteCreateDTO:
    def __init__(self, nome_completo: str, email: str, data_nascimento: date):
        self.__nome_completo = nome_completo
        self.__email = email
        self.__data_nascimento = data_nascimento

    @property
    def nome_completo(self) -> str:
        return self.__nome_completo

    @property
    def email(self) -> str:
        return self.__email

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento 