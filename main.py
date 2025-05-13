import tkinter as tk
from tkinter import  messagebox,simpledialog
from GraphManager import Graphmanager
from Node import Node

class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Deadlock")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.create_process = False
        self.create_resource = False

        self.graphManager = Graphmanager(self.canvas)

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
        self.graphManager.clear()

    def exit_create_mode(self):
        self.ativar_desativar_botao_resource(False)
        self.ativar_desativar_botao_processo(False)

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
        node = self.graphManager.add_process(x,y)

        self.canvas.tag_bind(node.id, "<Button-1>", lambda event, n=node: self.on_node_click(n))
        self.canvas.tag_bind(node.id, "<Button-3>", lambda event, n=node: self.graphManager.delete_node(n))

    def add_resource(self,x,y):
        max_alocations = self.ask_max_alocations()
        node = self.graphManager.add_resource(x,y,max_alocations)

        if node:
            self.canvas.tag_bind(node.id, "<Button-1>", lambda event, n=node: self.on_node_click(n))
            self.canvas.tag_bind(node.id, "<Button-3>", lambda event, n=node: self.graphManager.delete_node(n))
        

    def add_edge(self,node:Node):
        edge = self.graphManager.try_add_edge(node)

        if edge:
            edge.print_edge()
            self.canvas.tag_bind(edge.id, "<Button-3>", lambda event, e=edge: self.graphManager.delete_edge(e))

    def seleciona_node(self,node:Node):
        if(not node.can_add_edge()):
            messagebox.showwarning("Não foi possivel adicionar o processo", f"Numero máximo de alocações é {node.max_edges}")
            return
        
        self.graphManager.seleciona_node(node)
        self.exit_create_mode()

    def on_node_click(self, node:Node):
        if self.graphManager.selected_node:
            self.add_edge(node)
        else:
            self.seleciona_node(node)

    def on_canvas_click(self, event):
        if self.graphManager.has_node_at_position(event.x, event.y):
            return
        
        if self.create_process:
            self.add_process(event.x,event.y)
        
        if self.create_resource:
            self.add_resource(event.x,event.y)

    def detect_deadlock(self):
        return True
        
    def validate_input(self,P):
        if P == "" or P.isdigit(): 
            return True
        else:
            return False
    
    def ask_max_alocations(self) -> int:
        user_input = simpledialog.askstring("Recurso", "Digite o numero máximo de alocações:")
        
        if self.validate_input(user_input):
            return int(user_input)
        else:
            return None
        

# Inicializar
root = tk.Tk()
app = DeadlockSimulator(root)
root.mainloop()
