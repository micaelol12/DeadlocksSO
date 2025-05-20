from services.GraphManager import Graphmanager

def teste_add_process():
    manager = Graphmanager()
    manager.add_process(10,20)
    assert len(manager.processos) == 1

def test_add_resource():
    manager = Graphmanager()
    manager.add_resource(10,20,2)
    assert len(manager.recursos) == 1
