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
        x1, y1 = self.origem.position
        x2, y2 = self.destino.position
        color = 'red' if self.tipo == ETipoEdge.ALOCADO else 'green'
        self.edgeElementId = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill=color)
