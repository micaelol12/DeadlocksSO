import tkinter as tk
from tkinter import messagebox
from Edge import Edge
from Enums import ETipoEdge
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
            self.print_node(node)
            self.bind_node_events(node)

        elif self.create_resource:
            max_allocs = ask_max_allocations()
            if max_allocs is not None:
                node = self.graphManager.add_resource(event.x, event.y, max_allocs)
                self.print_node(node)
                self.bind_node_events(node)

    def print_node(self,node:Node):
        x,y = node.position
        node.NodeId = self.canvas.create_oval(x - node.radius, y - node.radius, x + node.radius, y + node.radius, fill=node.color, tags=(node.id))
        node.TextId = self.canvas.create_text(x, y, text=node.text, fill="white", tags=(node.id))

        if(node.max_alocacoes):
            node.MaxAlocacoesId = self.canvas.create_text(x, y + node.radius/2, text=str(node.max_alocacoes), fill="gray", tags=(node.id))
    
    def bind_node_events(self, node: Node):
        self.canvas.tag_bind(node.id, "<Button-1>", lambda e, n=node: self.on_node_click(n))
        self.canvas.tag_bind(node.id, "<Button-3>", lambda e, n=node: self.delete_node(n))

    def print_edge(self,edge:Edge):
        color = 'red' if edge.tipo == ETipoEdge.ALOCACAO else 'green'
        ctrl_x,ctrl_y,x1,y1,x2,y2 = edge.get_bezier_arrow()

        element =  self.canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2,
                                       smooth=True,
                                       arrow=tk.LAST,
                                       fill= color,
                                       width=2,
                                       tags=(edge.id))
        edge.edgeElementId = element

    def on_node_click(self, node: Node):
        if self.graphManager.selected_node:
            if self.graphManager.can_add_edge(node):
                edge = self.graphManager.add_edge(node)
                self.print_edge(edge)
                self.canvas.tag_bind(edge.id, "<Button-3>", lambda e, edge=edge: self.delete_edge(edge))
            
            self.unhighlight_node()
        else:
            if not node.can_add_edge():
                messagebox.showwarning("Limite atingido", f"Máximo de alocações: {node.max_alocacoes}")
                return
            
            self.highlight_node(node)

            self.create_process = self.create_resource = False
            self.update_button_states()

    def delete_node(self,node:Node):
        for edge in node.edges.copy():
            self.delete_edge(edge)

        self.canvas.delete(node.NodeId)
        self.canvas.delete(node.TextId)
        
        if(node.MaxAlocacoesId):
            self.canvas.delete(node.MaxAlocacoesId)

        self.graphManager.delete_node(node)

    def delete_edge(self,edge:Edge):
        self.canvas.delete(edge.edgeElementId)
        self.graphManager.delete_edge(edge)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.graphManager.clear()

    def unhighlight_node(self):
        self.canvas.itemconfig(self.graphManager.selected_node.NodeId,outline="black", width=1)
        self.graphManager.selected_node = None

    def highlight_node(self,node:Node):
        self.canvas.itemconfig(node.NodeId, outline="red", width=2)
        self.graphManager.select_node(node)

    def detect_deadlock(self):
        deadlocked, liberaveis = self.graphManager.detect_deadlock_with_terminable_edges()
        self.remove_edges_step_by_step(liberaveis, deadlocked)
    
    def remove_edges_step_by_step(self, liberaveis, deadlocked, index=0):
        if index < len(liberaveis):
            edge_id = liberaveis[index]
            edge = self.graphManager.edges.get(edge_id)
            if edge:
                self.delete_edge(edge)
            # Chama recursivamente o próximo passo após 500ms
            self.canvas.after(500, lambda: self.remove_edges_step_by_step(liberaveis, deadlocked, index + 1))
        else:
            # Após terminar a remoção, mostra a mensagem
            if deadlocked:
                messagebox.showwarning("Deadlock detectado", f"Processos em deadlock: {', '.join(deadlocked)}")
                self.highlight_deadlocked_processes(deadlocked)
            else:
                messagebox.showinfo("Sem Deadlock", "Nenhum deadlock foi detectado.")

    def highlight_deadlocked_processes(self, deadlocked_ids: list[str]):
        for pid in deadlocked_ids:
            processo = self.graphManager.processos.get(pid)
            if processo:
                self.canvas.itemconfig(processo.NodeId, fill="red")
