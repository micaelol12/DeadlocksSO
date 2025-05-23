from components.Edge import Edge
import tkinter as tk


class EdgeEventBinder:
    def __init__(self, canvas: tk.Canvas,on_delete_edge_callback):
            self.canvas = canvas
            self.on_delete_edge_callback = on_delete_edge_callback


    def bind(self, edge: Edge):
         self.canvas.tag_bind(
            edge.id, "<Button-3>", lambda e, edge=edge: self.on_delete_edge_callback(edge)
        )