import tkinter as tk
from Enums import ETipoNode

class Node:
    def __init__(self,x:int,y:int,id:str,text:str,canvas:tk.Canvas,color:str,tag:str,tipoNode:ETipoNode):
        self.position:tuple[int,int] = (x,y)
        self.id = id
        self.text = text
        self.canvas = canvas
        self.color = color
        self.tag = tag
        self.NodeId = None
        self.TextId = None
        self.radius = 30
        self.tipoNode = tipoNode

    def printNode(self):
        x,y = self.position

        self.NodeId = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=self.color, tags=(self.tag))
        self.TextId = self.canvas.create_text(x, y, text=self.text, fill="white", tags=(self.tag))

    def unhighlight_node(self):
        self.canvas.itemconfig(self.NodeId, outline="black", width=1)

    def highlight_node(self):
        self.canvas.itemconfig(self.NodeId, outline="red", width=2)

    def delete(self):
        self.canvas.delete(self.NodeId)
        self.canvas.delete(self.TextId)

    def isInPosition(self,x:int,y:int) -> bool:
        nx,ny = self.position
        return abs(x - nx) <= self.radius and abs(y - ny) <= self.radius
    
