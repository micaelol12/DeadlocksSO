import tkinter as tk
from Node import Node 
from Enums import ETipoEdge,ETipoNode
class Edge:
    def __init__(self,id:str,origem:Node,destino:Node,canvas:tk.Canvas):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.canvas = canvas
        self.tipo = self.getTipo()
        self.edgeElementId = None

    def getTipo(self):
        if self.origem.tipoNode == ETipoNode.PROCESSO and self.destino.tipoNode == ETipoNode.RECURSO:
            return ETipoEdge.PEDIDO
        
        return ETipoEdge.ALOCADO
        
    def delete(self):
        self.canvas.delete(self.edgeElementId)
        
    def printEdge(self):
        x1, y1 = self.origem.position
        x2, y2 = self.destino.position

        color = 'red' if self.tipo == ETipoEdge.ALOCADO else 'blue'

        self.edgeElementId = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST,width=2,fill=color)