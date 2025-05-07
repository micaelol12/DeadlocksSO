import tkinter as tk
from Node import Node 
class Edge:
    def __init__(self,id:str,origem:Node,destino:Node,canvas:tk.Canvas):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.canvas = canvas

    def printEdge(self):
        x1, y1 = self.origem.position
        x2, y2 = self.destino.position
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)