import pickle
from tkinter import filedialog

from services.GraphManager import Graphmanager

def storeData(graphManager:Graphmanager) -> bool:
    caminho_arquivo = filedialog.asksaveasfilename(
        title="Salvar arquivo como...",
        defaultextension=".pkl",
        filetypes=[("Arquivo Pickle", "*.pkl"), ("Todos os arquivos", "*.*")]
    )

    if not caminho_arquivo:
        return False

    try:
        with open(caminho_arquivo, 'wb') as dbfile:
            pickle.dump(graphManager, dbfile)
        return True
    except Exception as e:
        return False

def loadData() -> Graphmanager:
    caminho_arquivo = filedialog.askopenfilename(
        title="Abrir arquivo",
        defaultextension=".pkl",
        filetypes=[("Arquivo Pickle", "*.pkl"), ("Todos os arquivos", "*.*")]
    )

    if not caminho_arquivo:
        return None

    try:
        with open(caminho_arquivo, 'rb') as dbfile:
            graphManager = pickle.load(dbfile)
        return graphManager
    except Exception as e:
        return None
    
  