from UI.Enums import ETipoEdge
from components.Edge import Edge
from components.Node import Node
import tkinter as tk


class EdgeRenderer:
    def __init__(self, canvas: tk.Canvas):
            self.canvas = canvas

    def draw(self, edge: Edge):
        color = "red" if edge.tipo == ETipoEdge.ALOCACAO else "green"
        ctrl_x, ctrl_y, x1, y1, x2, y2 = edge.get_bezier_arrow()

        element = self.canvas.create_line(
            x1,
            y1,
            ctrl_x,
            ctrl_y,
            x2,
            y2,
            smooth=True,
            arrow=tk.LAST,
            fill=color,
            width=2,
            tags=(edge.id),
        )

        edge.edgeElementId = element