from components.Node import Node
import tkinter as tk

class DragManager:
    drag_data = {"x": 0, "y": 0, "node": None,"moved": False}
    canvas = None

    def __init__(self,canvas:tk.Canvas):
        self.canvas = canvas

    def start_drag(self, event, node: Node):
        self.drag_data["node"] = node
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["moved"] = False

    def do_drag(self, event, node: Node):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        if abs(dx) > 1 or abs(dy) > 1:
            self.drag_data["moved"] = True

        self.canvas.move(node.NodeId, dx, dy)
        self.canvas.move(node.TextId, dx, dy)

        if node.MaxAlocacoesId:
            self.canvas.move(node.MaxAlocacoesId, dx, dy)

        node.position = (node.position[0] + dx, node.position[1] + dy)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def has_moved(self)->bool:
        return self.drag_data["moved"]

    def end_drag(self, event, node: Node):
        self.drag_data = {"x": 0, "y": 0, "node": None, "moved": False}