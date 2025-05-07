import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx

class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Deadlock")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.graph = nx.DiGraph()
        self.nodes = {}
        self.node_positions = {}
        self.node_count = {'P': 0, 'R': 0}
        self.selected_node = None
        self.create_process = False
        self.create_resource = False

        # Botões
        button_frame = tk.Frame(root)
        button_frame.pack()
        self.add_process_button = tk.Button(button_frame, text="Novo Processo", command=self.enter_create_process_mode)
        self.add_resource_button = tk.Button(button_frame, text="Novo Recurso", command=self.enter_create_resource_mode)

        self.add_resource_button.pack(side=tk.LEFT)
        self.add_process_button.pack(side=tk.LEFT)
        tk.Button(button_frame, text="Detectar Deadlock", command=self.detect_deadlock).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Limpar", command=self.limpar_quadro).pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
    
    def limpar_quadro(self):
        self.canvas.delete("all")
        self.graph.clear()
        self.nodes.clear()
        self.node_positions.clear()
        self.node_count = {'P': 0, 'R': 0}
        self.selected_node = None

    def enter_create_process_mode(self):
        self.ativar_desativar_botao_processo(not self.create_process)
        self.ativar_desativar_botao_resource(False)

    def enter_create_resource_mode(self):
        self.ativar_desativar_botao_resource(not self.create_resource)
        self.ativar_desativar_botao_processo(False)

    def ativar_desativar_botao_processo(self,active):
        self.create_process = active
        self.add_process_button.config(bg='red' if active else 'SystemButtonFace')
    
    def ativar_desativar_botao_resource(self,active):
        self.create_resource = active
        self.add_resource_button.config(bg='red' if active else 'SystemButtonFace')

    def add_process(self,x,y):
        self.node_count['P'] += 1
        name = f"P{self.node_count['P']}"
        self.create_node(name, "blue",x,y)

    def add_resource(self,x,y):
        self.node_count['R'] += 1
        name = f"R{self.node_count['R']}"
        self.create_node(name, "orange",x,y)

    def create_node(self, name, color,x,y):
        r = 20
        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)
        text = self.canvas.create_text(x, y, text=name, fill="white")
        self.nodes[name] = (oval, text)
        self.node_positions[name] = (x, y)
        self.graph.add_node(name)

    def on_canvas_click(self, event):
        clicked = self.get_node_at_position(event.x, event.y)

        if clicked:
            if self.selected_node:
                if self.selected_node != clicked:
                    self.graph.add_edge(self.selected_node, clicked)
                    x1, y1 = self.node_positions[self.selected_node]
                    x2, y2 = self.node_positions[clicked]
                    self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
                    self.selected_node = None
            else:
                self.selected_node = clicked
                self.highlight_node(clicked)
        else:
            if self.create_process:
                self.add_process(event.x,event.y)
            if self.create_resource:
                self.add_resource(event.x,event.y)

    def get_node_at_position(self, x, y):
        for name, (nx, ny) in self.node_positions.items():
            if abs(x - nx) <= 20 and abs(y - ny) <= 20:
                return name
        return None

    def highlight_node(self, name):
        for n, (oval, _) in self.nodes.items():
            color = "blue" if n.startswith("P") else "orange"
            self.canvas.itemconfig(oval, outline="black", width=1)
            if n == name:
                self.canvas.itemconfig(oval, outline="red", width=2)

    def detect_deadlock(self):
        cycles = list(nx.simple_cycles(self.graph))
        if cycles:
            messagebox.showerror("Deadlock Detectado", f"Deadlock entre: {', '.join(cycles[0])}")
        else:
            messagebox.showinfo("Sem Deadlock", "Nenhum deadlock detectado.")

# Inicializar
root = tk.Tk()
app = DeadlockSimulator(root)
root.mainloop()
