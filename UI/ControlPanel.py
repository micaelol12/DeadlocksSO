import tkinter as tk

class ControlPanel:
    def __init__(self, root, on_process, on_resource, on_detect_deadlock, on_clear, on_save, on_load):
        self.frame = tk.LabelFrame(root, text="Controles", padx=5, pady=5)
        self.frame.pack()

        self.active_color = "SteelBlue3"
        self.disable_color = "SystemButtonFace"

        self.btn_process = tk.Button(self.frame, text="Novo Processo", command=on_process)
        self.btn_resource = tk.Button(self.frame, text="Novo Recurso", command=on_resource)

        self.btn_process.pack(side=tk.LEFT, padx=5)
        self.btn_resource.pack(side=tk.LEFT, padx=5)

        tk.Button(self.frame, text="Detectar Deadlock", command=on_detect_deadlock).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame, text="Limpar", command=on_clear).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame, text="Salvar", command=on_save).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame, text="Carregar", command=on_load).pack(side=tk.LEFT, padx=5)

    def get_color(self,active) -> str:
        return self.active_color if active else self.disable_color

    def highlight_process(self, active):
        self.btn_process.config(bg=self.get_color(active))

    def highlight_resource(self, active):
        self.btn_resource.config(bg=self.get_color(active))
