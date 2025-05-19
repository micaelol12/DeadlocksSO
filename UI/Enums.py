from enum import Enum

class ETipoNode(Enum):
    PROCESSO = 1
    RECURSO = 2

class ETipoEdge(Enum):
    REQUISACAO = 1
    ALOCACAO = 2