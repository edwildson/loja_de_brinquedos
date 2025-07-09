from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class VendaUpdateDTO:
    cliente_id: Optional[int] = None
    data: Optional[date] = None
    valor: Optional[float] = None 