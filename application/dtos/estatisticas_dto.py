from typing import List, Dict, Any


class EstatisticasVendasPorDiaDTO:
    def __init__(self, vendas_por_dia: List[Dict[str, Any]]):
        self.__vendas_por_dia = vendas_por_dia

    @property
    def vendas_por_dia(self) -> List[Dict[str, Any]]:
        return self.__vendas_por_dia


class ClienteDestaqueDTO:
    def __init__(self, cliente_id: int, nome_completo: str, valor: float):
        self.__cliente_id = cliente_id
        self.__nome_completo = nome_completo
        self.__valor = valor

    @property
    def cliente_id(self) -> int:
        return self.__cliente_id

    @property
    def nome_completo(self) -> str:
        return self.__nome_completo

    @property
    def valor(self) -> float:
        return self.__valor 