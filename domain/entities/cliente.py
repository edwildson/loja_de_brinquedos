from datetime import date
from typing import Optional
import re


class Cliente:
    def __init__(self, id: Optional[int], nome_completo: str, email: str, data_nascimento: date):
        if not nome_completo or not nome_completo.strip():
            raise ValueError("Nome completo é obrigatório")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email deve ser válido")
        if data_nascimento > date.today():
            raise ValueError("Data de nascimento não pode ser futura")
        self.__id = id
        self.__nome_completo = nome_completo
        self.__email = email
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

    def __eq__(self, other):
        if not isinstance(other, Cliente):
            return False
        return (
            self.id == other.id and
            self.nome_completo == other.nome_completo and
            self.email == other.email and
            self.data_nascimento == other.data_nascimento
        )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome_completo='{self.nome_completo}', email='{self.email}')"
