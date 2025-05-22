import tkinter as tk
from tkinter import messagebox
from UI.EdgeEventBinder import EdgeEventBinder
from UI.ContextMenuManager import ContextMenuManager
from UI.DragManager import DragManager
from UI.EdgeRenderer import EdgeRenderer
from UI.NodeEventBinder import NodeEventBinder
from UI.NodeRenderer import NodeRenderer
from components.Edge import Edge
from UI.Enums import  ETipoNode
from services.File import loadData, storeData
from services.GraphManager import Graphmanager as GM
from components.Node import Node
from utils.dialog import ask_max_allocations


class UIController:
    def __init__(self, root, canvas: tk.Canvas, graphManager: GM):
        self.root = root
        self.canvas = canvas
        self.graphManager = graphManager
        self.mode: ETipoNode = False
        self.node_renderer = NodeRenderer(canvas)
        self.edge_renderer = EdgeRenderer(canvas)
        self.dragManager = DragManager(canvas,1)
        self.node_event_binder = NodeEventBinder(canvas,self.dragManager.start_drag,self.on_drag,self.end_drag)
        self.edge_event_binder = EdgeEventBinder(canvas,self.delete_edge)
        self.context_menu_manager = ContextMenuManager(root,canvas,graphManager,self.edit_node,self.delete_node)

        self.setup_buttons(root)
        self.canvas.bind("<Button-1>", self.handle_canvas_click)

    def setup_buttons(self, root):
        frame = tk.LabelFrame(root, text="Controles", padx=5, pady=5)
        frame.pack()

        self.btn_process = tk.Button(
            frame, text="Novo Processo", command=self.toggle_process_mode
        )
        self.btn_resource = tk.Button(
            frame, text="Novo Recurso", command=self.toggle_resource_mode
        )
        self.btn_process.pack(side=tk.LEFT, padx=5)
        self.btn_resource.pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Detectar Deadlock", command=self.detect_deadlock).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(frame, text="Limpar", command=self.clear_canvas).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(frame, text="Salvar", command=self.salvar_data).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(frame, text="Carregar", command=self.carregar_data).pack(
            side=tk.LEFT, padx=5
        )

    def salvar_data(self):
        if not storeData(self.graphManager):
            messagebox.showinfo("Erro ao Salvar", "Não foi possível salvar o grafo")

    def carregar_data(self):
        self.clear_canvas()

        gm = loadData()
        if not gm:
            messagebox.showinfo("Erro ao Carregar", "Não foi possível carregar o grafo")
            return

        self.graphManager = gm

        for processo in self.graphManager.processos.values():
            self.node_renderer.draw(processo)
            self.node_event_binder.bind(processo)

        for processo in self.graphManager.recursos.values():
            self.node_renderer.draw(processo)
            self.node_event_binder.bind(processo)

        for edge in self.graphManager.edges.values():
            self.edge_renderer.draw(edge)
            self.edge_event_binder.bind(edge)

    def set_mode(self, mode: ETipoNode):
        if self.mode == mode:
            self.mode = None
        self.mode = mode
        self.update_button_states()

    def toggle_process_mode(self):
        self.set_mode(ETipoNode.PROCESSO)

    def toggle_resource_mode(self):
        self.set_mode(ETipoNode.RECURSO)

    def update_button_states(self):
        self.btn_process.config(
            bg="red" if self.mode == ETipoNode.PROCESSO else "SystemButtonFace"
        )
        self.btn_resource.config(
            bg="red" if self.mode == ETipoNode.RECURSO else "SystemButtonFace"
        )

    def handle_canvas_click(self, event):
        if self.graphManager.has_node_at_position(event.x, event.y):
            return

        if self.mode == ETipoNode.PROCESSO:
            node = self.graphManager.add_process(event.x, event.y)
            self.node_renderer.draw(node)
            self.node_event_binder.bind(node)

        elif self.mode == ETipoNode.RECURSO:
            max_allocs = ask_max_allocations()
            if max_allocs is not None:
                node = self.graphManager.add_resource(event.x, event.y, max_allocs)
                self.node_renderer.draw(node)
                self.node_event_binder.bind(node)

    def end_drag(self, event, node: Node):
        if not self.dragManager.has_moved():
            self.on_node_click(node) 

        self.dragManager.end_drag(event, node)

    def on_drag(self, event, node: Node):
        self.dragManager.do_drag(event, node)
        self.redraw_edges_for_node(node)

    def redraw_edges_for_node(self, node: Node):
        copy = node.edges.copy()
        node.delete_all_edges()

        for edge in copy:
            node.add_edge(edge)
            self.canvas.delete(edge.edgeElementId)
            self.edge_renderer.draw(edge)
            self.edge_event_binder.bind(edge)


    def on_node_click(self,node: Node):
        if self.graphManager.selected_node:
            if self.graphManager.can_add_edge(node):
                edge = self.graphManager.add_edge(node)
                self.edge_renderer.draw(edge)
                self.edge_event_binder.bind(edge)

            self.unhighlight_node()
        else:
            if not node.can_add_edge():
                messagebox.showwarning(
                    "Limite atingido", f"Máximo de alocações: {node.max_alocacoes}"
                )
                return

            self.highlight_node(node)

            self.mode = None
            self.update_button_states()

    def delete_node_edges(self, node: Node):
        for edge in node.edges.copy():
            self.delete_edge(edge)

    def delete_node(self, node: Node):
        self.delete_node_edges(node)
        self.canvas.delete(node.NodeId)
        self.canvas.delete(node.TextId)

        if node.MaxAlocacoesId:
            self.canvas.delete(node.MaxAlocacoesId)

        self.graphManager.delete_node(node)

    def delete_edge(self, edge: Edge):
        self.canvas.delete(edge.edgeElementId)
        self.graphManager.delete_edge(edge)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.graphManager.clear()

    def unhighlight_node(self):
        self.canvas.itemconfig(
            self.graphManager.selected_node.NodeId, outline="black", width=1
        )
        self.graphManager.selected_node = None

    def highlight_node(self, node: Node):
        self.canvas.itemconfig(node.NodeId, outline="red", width=2)
        self.graphManager.select_node(node)

    def detect_deadlock(self):
        deadlocked, liberaveis = (
            self.graphManager.detect_deadlock_with_terminable_edges()
        )
        self.remove_edges_step_by_step(liberaveis, deadlocked)

    def remove_edges_step_by_step(self, liberaveis, deadlocked, index=0):
        if index < len(liberaveis):
            node_id = liberaveis[index]
            node = self.graphManager.processos.get(node_id)
            if node:
                self.delete_node_edges(node)
            # Chama recursivamente o próximo passo após 500ms
            self.canvas.after(
                2000,
                lambda: self.remove_edges_step_by_step(
                    liberaveis, deadlocked, index + 1
                ),
            )
        else:
            # Após terminar a remoção, mostra a mensagem
            if deadlocked:
                messagebox.showwarning(
                    "Deadlock detectado",
                    f"Processos em deadlock: {', '.join(deadlocked)}",
                )
                self.highlight_deadlocked_processes(deadlocked)
            else:
                messagebox.showinfo("Sem Deadlock", "Nenhum deadlock foi detectado.")

    def highlight_deadlocked_processes(self, deadlocked_ids: list[str]):
        for pid in deadlocked_ids:
            processo = self.graphManager.processos.get(pid)
            if processo:
                self.canvas.itemconfig(processo.NodeId, fill="red")

    def edit_node(self, node: Node):
        max = ask_max_allocations(str(node.max_alocacoes))

        if max < node.get_alocados_size():
            messagebox.showwarning(
                "Não foi possível editar",
                "Você deve removar as alocações para diminuir o número máximo",
            )

        else:
            node.max_alocacoes = max
            self.canvas.itemconfig(node.MaxAlocacoesId, text=str(max))
