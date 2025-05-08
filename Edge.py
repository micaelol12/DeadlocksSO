import tkinter as tk
from Enums import ETipoEdge, ETipoNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Node import Node

class Edge:
    def __init__(self, id: str, origem: 'Node', destino: 'Node', canvas: tk.Canvas):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.canvas = canvas
        self.tipo = self.get_tipo()
        self.edgeElementId = None

    def get_tipo(self):
        if self.origem.tipoNode == ETipoNode.PROCESSO and self.destino.tipoNode == ETipoNode.RECURSO:
            return ETipoEdge.PEDIDO
        return ETipoEdge.ALOCADO

    def delete(self):
        self.canvas.delete(self.edgeElementId)

    def print_edge(self):
        color = 'red' if self.tipo == ETipoEdge.ALOCADO else 'green'
        self.edgeElementId = self.draw_bezier_arrow(color)

    def draw_bezier_arrow(self,color):
        x1, y1 = self.origem.position
        x2, y2 = self.destino.position

        offset_escalor = 20
        comum_edges = list(set(self.origem.edges) & set(self.destino.edges))
        curve_offset= len(comum_edges) * offset_escalor

        ctrl_x = (x1 + x2) / 2 + curve_offset * ((y2 - y1) / max(abs(y2 - y1) + abs(x2 - x1), 1))
        ctrl_y = (y1 + y2) / 2 - curve_offset * ((x2 - x1) / max(abs(y2 - y1) + abs(x2 - x1), 1))

        return self.canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2,
                                       smooth=True,
                                       arrow=tk.LAST,
                                       fill= color,
                                       width=2)
