import tkinter as tk


class Menu:
    def __init__(self,root,on_save,on_load):
        self.root = root
        self.on_save = on_save
        self.on_load = on_load

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Salvar", command=self.on_save)
        file_menu.add_command(label="Carregar", command=self.on_load)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        self.root.config(menu=menu_bar)