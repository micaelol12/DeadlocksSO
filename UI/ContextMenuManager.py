from UI.Enums import ETipoNode
from components.Node import Node
import tkinter as tk


class ContextMenuManager:
    def __init__(self, root, canvas, graphManager, edit_callback, delete_callback):
        self.root = root
        self.canvas = canvas
        self.graphManager = graphManager
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback

    def show(self, node: Node, event):
        menu = tk.Menu(self.root, tearoff=0)
        
        if node.tipoNode == ETipoNode.RECURSO:
            menu.add_command(label="Remover", command=lambda: self.delete_callback(node))
            menu.add_command(label="Editar Recurso", command=lambda: self.edit_callback(node))
        else:
            menu.add_command(label="Remover", command=lambda: self.delete_callback(node))

        menu.post(event.x_root, event.y_root)
