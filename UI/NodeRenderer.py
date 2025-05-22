from components.Node import Node
import tkinter as tk


class NodeRenderer:
    def __init__(self, canvas: tk.Canvas):
            self.canvas = canvas

    def draw(self, node: Node):
        x, y = node.position
        node.NodeId = self.canvas.create_oval(
            x - node.radius,
            y - node.radius,
            x + node.radius,
            y + node.radius,
            fill=node.color,
            tags=(node.id),
        )
        node.TextId = self.canvas.create_text(
            x, y, text=node.text, fill="white", tags=(node.id)
        )

        if node.max_alocacoes:
            node.MaxAlocacoesId = self.canvas.create_text(
                x,
                y + node.radius / 2,
                text=str(node.max_alocacoes),
                fill="gray",
                tags=(node.id),
            )