import tkinter as tk
from Enums import ETipoNode,ETipoEdge
from Edge import Edge

class Node:
    def __init__(self,x:int,y:int,id:str,text:str,canvas:tk.Canvas,color:str,tipoNode:ETipoNode,max_edges:int = None):
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
        self.max_edges = max_edges

    def print_node(self):
        x,y = self.position

        self.NodeId = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=self.color, tags=(self.id))
        self.TextId = self.canvas.create_text(x, y, text=self.text, fill="white", tags=(self.id))

    def can_add_edge(self) -> bool:
        alocados = [e for e in self.edges if e.tipo == ETipoEdge.ALOCADO]
        return self.tipoNode == ETipoNode.PROCESSO or len(alocados) < self.max_edges

    def add_edge(self,edge:Edge) -> bool:
        if self.can_add_edge():
            self.edges.append(edge)
            return True
        
        return False

    def unhighlight_node(self):
        self.canvas.itemconfig(self.NodeId, outline="black", width=1)

    def highlight_node(self):
        self.canvas.itemconfig(self.NodeId, outline="red", width=2)

    def delete(self):
        self.canvas.delete(self.NodeId)
        self.canvas.delete(self.TextId)
        self.delete_all_edges()
    
    def delete_all_edges(self):
        for edge in self.edges[:]:
            edge.delete()
            edge.origem.delete_edge(edge)
            edge.destino.delete_edge(edge)
    
    def delete_edge(self,edge:Edge):
        self.edges.remove(edge)

    def is_in_position(self,x:int,y:int) -> bool:
        nx,ny = self.position
        return abs(x - nx) <= self.radius and abs(y - ny) <= self.radius
    
