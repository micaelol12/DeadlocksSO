import tkinter as tk
from Enums import ETipoNode
from Edge import Edge

class Node:
    def __init__(self,x:int,y:int,id:str,text:str,canvas:tk.Canvas,color:str,tipoNode:ETipoNode):
        self.position:tuple[int,int] = (x,y)
        self.id = id
        self.text = text
        self.canvas = canvas
        self.color = color
        self.NodeId = None
        self.TextId = None
        self.radius = 30
        self.tipoNode = tipoNode
        self.edges: list[Edge] = []

    def print_node(self):
        x,y = self.position

        self.NodeId = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=self.color, tags=(self.id))
        self.TextId = self.canvas.create_text(x, y, text=self.text, fill="white", tags=(self.id))

    def add_edge(self,edge:Edge):
        self.edges.append(edge)

    def unhighlight_node(self):
        self.canvas.itemconfig(self.NodeId, outline="black", width=1)

    def highlight_node(self):
        self.canvas.itemconfig(self.NodeId, outline="red", width=2)

    def delete(self):
        self.canvas.delete(self.NodeId)
        self.canvas.delete(self.TextId)
        self.delete_edges()
    
    def delete_edges(self):
        for edge in self.edges[:]:
            edge.delete()
            # Remove este edge das listas dos outros nós também
            if edge in edge.origem.edges:
                edge.origem.edges.remove(edge)
            if edge in edge.destino.edges:
                edge.destino.edges.remove(edge)

    def is_in_position(self,x:int,y:int) -> bool:
        nx,ny = self.position
        return abs(x - nx) <= self.radius and abs(y - ny) <= self.radius
    
