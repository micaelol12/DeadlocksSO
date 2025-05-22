from UI.DragManager import DragManager
from components.Node import Node
import tkinter as tk


class NodeEventBinder:
    def __init__(self, canvas: tk.Canvas,on_button_press_callback,on_button_motion_callback,on_button_release_callback):
            self.canvas = canvas
            self.on_button_press_callback = on_button_press_callback
            self.on_button_motion_callback= on_button_motion_callback
            self.on_button_release_callback = on_button_release_callback

    def bind(self, node: Node):
        self.canvas.tag_bind(
            node.id, "<Button-3>", lambda e, n=node: self.context_menu_manager.show(n, e)
        )
        
        self.canvas.tag_bind(node.id, "<ButtonPress-1>", lambda e, n=node: self.on_button_press_callback(e, n))
        self.canvas.tag_bind(node.id, "<B1-Motion>", lambda e, n=node: self.on_button_motion_callback(e,n) )
        self.canvas.tag_bind(node.id, "<ButtonRelease-1>", lambda e, n=node: self.on_button_release_callback(e,n))