import tkinter as tk
from DeadlockSimulator import DeadlockSimulator

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockSimulator(root)
    root.mainloop()
