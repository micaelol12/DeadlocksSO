from tkinter import messagebox,Canvas
from services.GraphManager import Graphmanager

class DeadlockVisualizer:
    def __init__(self,canvas: Canvas, graphManager: Graphmanager,on_node_fine_callback):
        self.canvas = canvas
        self.graphManager = graphManager
        self.on_node_fine_callback = on_node_fine_callback

    def detect_deadlock(self):
        deadlocked, liberaveis = self.graphManager.detect_deadlock_with_terminable_edges()
        self.remove_edges_step_by_step(liberaveis, deadlocked)

    def remove_edges_step_by_step(self, liberaveis, deadlocked, index=0):
        if index < len(liberaveis):
            node_id = liberaveis[index]
            node = self.graphManager.processos.get(node_id)

            if node:
                self.on_node_fine_callback(node)
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
