from enum import Enum

class ETipoNode(Enum):
    PROCESSO = 1
    RECURSO = 2

class ETipoEdge(Enum):
    PEDIDO = 1
    ALOCADO = 2