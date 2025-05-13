import tkinter as tk
from UIController import UIController
from GraphManager import Graphmanager

class DeadlockSimulator:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Simulador de Deadlock")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.graphManager = Graphmanager(self.canvas)
        self.ui = UIController(root, self.canvas, self.graphManager)
