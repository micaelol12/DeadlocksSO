import tkinter as tk
from UI.UIController import UIController
from services import GraphManager

class DeadlockSimulator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulador de Deadlock")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.graphManager = GraphManager()
        self.ui = UIController(root, self.canvas, self.graphManager)
