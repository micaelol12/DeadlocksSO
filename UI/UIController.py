import tkinter as tk
from tkinter import messagebox
from UI.Renderers import EdgeRenderer,NodeRenderer
from UI.Binders import NodeEventBinder,EdgeEventBinder
from components import Edge,Node
from services import GraphManager as GM
from services.File import loadData, storeData

from UI.ControlPanel import ControlPanel
from UI.DeadlockVisualizer import DeadlockVisualizer
from UI.ContextMenuManager import ContextMenuManager
from UI.Managers.DragManager import DragManager
from utils.Enums import  ETipoNode
from utils.dialog import ask_max_allocations


class UIController:
    def __init__(self, root, canvas: tk.Canvas, graphManager: GM):
        self.root = root
        self.canvas = canvas
        self.graphManager = graphManager
        self.mode: ETipoNode = False
        self.node_renderer = NodeRenderer(self.canvas)
        self.edge_renderer = EdgeRenderer(self.canvas)
        self.dragManager = DragManager(self.canvas,1)
        self.context_menu_manager = ContextMenuManager(root,canvas,self.graphManager,self.edit_node,self.delete_node)
        self.node_event_binder = NodeEventBinder(self.canvas,self.dragManager.start_drag,self.on_drag,self.end_drag,self.context_menu_manager.show)
        self.edge_event_binder = EdgeEventBinder(self.canvas,self.delete_edge)
        self.deadlock_visualizer = DeadlockVisualizer(self.canvas,self.graphManager,self.delete_node_edges)
        self.control_panel = ControlPanel(
            root,
            self.toggle_process_mode,
            self.toggle_resource_mode,
            self.deadlock_visualizer.detect_deadlock,
            self.clear_canvas,
            self.salvar_data,
            self.carregar_data
        )

        self.canvas.bind("<Button-1>", self.handle_canvas_click)


    def salvar_data(self):
        if not storeData(self.graphManager):
            messagebox.showinfo("Erro ao Salvar", "Não foi possível salvar o grafo")

    def carregar_data(self):
        self.clear_canvas()

        gm = loadData()

        if not gm:
            messagebox.showinfo("Erro ao Carregar", "Não foi possível carregar o grafo")
            return

        self.set_graph_manager(gm)

        for processo in self.graphManager.processos.values():
            self.draw_and_bind_node(processo)

        for recurso in self.graphManager.recursos.values():
           self.draw_and_bind_node(recurso)

        for edge in self.graphManager.edges.values():
            self.draw_and_bind_edge(edge)

    def set_graph_manager(self, new_gm: GM):
        self.graphManager = new_gm
        self.context_menu_manager.graphManager = new_gm
        self.deadlock_visualizer.graphManager = new_gm


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
      self.control_panel.highlight_process(self.mode == ETipoNode.PROCESSO)
      self.control_panel.highlight_resource(self.mode == ETipoNode.RECURSO)

    def handle_canvas_click(self, event):
        if self.graphManager.has_node_at_position(event.x, event.y):
            return

        if self.mode == ETipoNode.PROCESSO:
            node = self.graphManager.add_process(event.x, event.y)
            self.draw_and_bind_node(node)


        elif self.mode == ETipoNode.RECURSO:
            max_allocs = ask_max_allocations()
            if max_allocs is not None:
                node = self.graphManager.add_resource(event.x, event.y, max_allocs)
                self.draw_and_bind_node(node)

    def draw_and_bind_node(self, node: Node):
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
            self.draw_and_bind_edge(edge)

    def on_node_click(self,node: Node):
        if self.graphManager.selected_node:
            if self.graphManager.can_add_edge(node):
                edge = self.graphManager.add_edge(node)
                self.draw_and_bind_edge(edge)

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

    def draw_and_bind_edge(self,edge:Edge):
        self.edge_renderer.draw(edge)
        self.edge_event_binder.bind(edge)

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
