from tkinter import simpledialog, messagebox
from utils.utils import validate_integer_input


def ask_max_allocations(initialvalue=None) -> int:
    while True:
        response = simpledialog.askstring(
            "Recurso", "Digite o número máximo de alocações:", initialvalue=initialvalue
        )
        if response is None:
            return None
        if validate_integer_input(response):
            return int(response)
        messagebox.showerror("Erro", "Digite apenas números inteiros.")
