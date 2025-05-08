import tkinter as tk
from tkinter import  messagebox
import networkx as nx
from Node import Node
from Edge import Edge
from Enums import ETipoNode


class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Deadlock")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.graph = nx.DiGraph()
        self.nodes: dict[str,Node] = {}
        self.edges: dict[str,Edge] = {}
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node:Node = None
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
        self.edges.clear()
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node = None

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
        self.node_count['P'] += 1
        name = f"Processo {self.node_count['P']}"
        id = f"P{self.node_count['P']}"
        self.create_node(name,id, "blue",x,y,ETipoNode.PROCESSO)

    def add_resource(self,x,y):
        self.node_count['R'] += 1
        name = f"Recurso {self.node_count['R']}"
        id = f"R{self.node_count['R']}"
        self.create_node(name,id,"orange",x,y,ETipoNode.RECURSO)

    def add_edge(self,origem:Node,destino:Node):
        self.node_count['E'] += 1
        id = f"E{self.node_count['E']}"
        self.graph.add_edge(origem.id, destino.id)

        edge = Edge(id,origem,destino,self.canvas)

        origem.add_edge(edge)
        destino.add_edge(edge)

        self.edges[id] = edge
        edge.print_edge()

    def create_node(self, name, id , color, x, y,tipo: ETipoNode):
        tag = f"node_{id}"

        node = Node(x,y,id,name,self.canvas,color,tag,tipo)

        node.print_node()
        self.nodes[id] = node
        self.graph.add_node(id)

        self.canvas.tag_bind(tag, "<Button-1>", lambda event, n=node: self.on_node_click(n))
        self.canvas.tag_bind(tag, "<Button-3>", lambda event, n=node: self.delete_node(n))

    def delete_node(self, node:Node):
        if node.id in self.nodes:
            node.delete()
            self.graph.remove_node(node.id)

            del self.nodes[node.id]

            if self.selected_node == node:
                self.selected_node = None

    def on_node_click(self, node:Node):
        if self.selected_node:
            isDiferenteNode =  self.selected_node != node
            iDiferenteNodeType = self.selected_node.tipoNode != node.tipoNode

            if isDiferenteNode and iDiferenteNodeType:
                  self.add_edge(self.selected_node,node)

            self.selected_node.unhighlight_node()
            self.selected_node = None
        else:
            node.highlight_node()
            self.selected_node = node
            self.exit_create_mode()

    def on_canvas_click(self, event):
        if self.has_node_at_position(event.x, event.y):
            return
        
        if self.create_process:
            self.add_process(event.x,event.y)
        
        if self.create_resource:
            self.add_resource(event.x,event.y)

    def has_node_at_position(self, x, y) -> bool:
        return any(node.is_in_position(x, y) for node in self.nodes.values())

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
