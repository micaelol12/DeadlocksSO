import tkinter as tk
from tkinter import messagebox
from GraphManager import Graphmanager as GM
from Node import Node
from dialog import ask_max_allocations

class UIController:
    def __init__(self, root, canvas:tk.Canvas, graphManager:GM):
        self.canvas = canvas
        self.graphManager = graphManager
        self.create_process = False
        self.create_resource = False

        self.setup_buttons(root)
        self.canvas.bind("<Button-1>", self.handle_canvas_click)


    def setup_buttons(self, root):
        frame = tk.LabelFrame(root, text="Controles", padx=5, pady=5)
        frame.pack()

        self.btn_process = tk.Button(frame, text="Novo Processo", command=self.toggle_process_mode)
        self.btn_resource = tk.Button(frame, text="Novo Recurso", command=self.toggle_resource_mode)

        self.btn_process.pack(side=tk.LEFT, padx=5)
        self.btn_resource.pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Detectar Deadlock", command=self.detect_deadlock).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Limpar", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
    
    def toggle_process_mode(self):
        self.create_process = not self.create_process
        self.create_resource = False
        self.update_button_states()

    def toggle_resource_mode(self):
        self.create_resource = not self.create_resource
        self.create_process = False
        self.update_button_states()

    def update_button_states(self):
        self.btn_process.config(bg='red' if self.create_process else 'SystemButtonFace')
        self.btn_resource.config(bg='red' if self.create_resource else 'SystemButtonFace')

    def handle_canvas_click(self, event):
        if self.graphManager.has_node_at_position(event.x, event.y):
            return

        if self.create_process:
            node = self.graphManager.add_process(event.x, event.y)
            node.print_node()
            self.bind_node_events(node)

        elif self.create_resource:
            max_allocs = ask_max_allocations()
            if max_allocs is not None:
                node = self.graphManager.add_resource(event.x, event.y, max_allocs)
                node.print_node()
                self.bind_node_events(node)
    
    def bind_node_events(self, node: Node):
        self.canvas.tag_bind(node.id, "<Button-1>", lambda e, n=node: self.on_node_click(n))
        self.canvas.tag_bind(node.id, "<Button-3>", lambda e, n=node: self.graphManager.delete_node(n))
    
    def on_node_click(self, node: Node):
        if self.graphManager.selected_node:
            if self.graphManager.can_add_edge(node):
                edge = self.graphManager.add_edge(node)
                edge.print_edge()
                self.canvas.tag_bind(edge.id, "<Button-3>", lambda e, edge=edge: self.graphManager.delete_edge(edge))
        else:
            if not node.can_add_edge():
                messagebox.showwarning("Limite atingido", f"Máximo de alocações: {node.max_edges}")
                return
            self.graphManager.seleciona_node(node)
            self.create_process = self.create_resource = False
            self.update_button_states()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.graphManager.clear()

    def detect_deadlock(self):
        # Aqui você poderá chamar um detector real futuramente
        messagebox.showinfo("Deadlock", "Função ainda não implementada.")