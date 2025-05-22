from UI.Enums import ETipoNode, ETipoEdge
from components.Edge import Edge


class Node:
    def __init__(
        self,
        x: int,
        y: int,
        id: str,
        text: str,
        color: str,
        tipoNode: ETipoNode,
        max_alocacoes: int = None,
    ):
        self.position: tuple[int, int] = (x, y)
        self.id = id
        self.text = text
        self.color = color
        self.NodeId = None
        self.TextId = None
        self.MaxAlocacoesId = None
        self.radius = 30
        self.tipoNode = tipoNode
        self.edges: list[Edge] = []
        self.max_alocacoes = max_alocacoes

    def can_add_edge(self, edge: Edge = None) -> bool:
        if edge and edge.tipo == ETipoEdge.REQUISACAO:
            return True

        return self.tipoNode == ETipoNode.PROCESSO or  self.get_alocados_size() < self.max_alocacoes
    
    def get_alocados_size(self) -> int:
       alocados = [e for e in self.edges if e.tipo == ETipoEdge.ALOCACAO]
       return len(alocados)

    def add_edge(self, edge: Edge) -> bool:
        if self.can_add_edge(edge):
            self.edges.append(edge)
            return True

        return False

    def delete_all_edges(self):
        for edge in self.edges.copy():
           self.edges.remove(edge)

    def delete_edge(self, edge: Edge):
        self.edges.remove(edge)

    def is_in_position(self, x: int, y: int) -> bool:
        nx, ny = self.position
        return abs(x - nx) <= self.radius and abs(y - ny) <= self.radius
