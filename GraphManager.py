from Enums import ETipoEdge, ETipoNode
from Node import Node
from Edge import Edge

class Graphmanager:
    def __init__(self):
        self.processos: dict[str,Node] = {}
        self.recursos: dict[str,Node] = {}
        self.edges: dict[str,Edge] = {}
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node:Node = None

    def clear(self):
        self.processos.clear()
        self.recursos.clear()
        self.edges.clear()
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node = None
    
    def delete_node(self, node:Node):
        if node.id in self.recursos:
            del self.recursos[node.id]
        else:
            del self.processos[node.id]

        if self.selected_node == node:
            self.selected_node = None
    
    def delete_edge(self,edge:Edge):
        if edge.id in self.edges:
            edge.origem.delete_edge(edge)
            edge.destino.delete_edge(edge)

            del self.edges[edge.id]
    
    def has_node_at_position(self, x, y) -> bool:
        return any(node.is_in_position(x, y) for node in self.recursos.values()) or any(node.is_in_position(x, y) for node in self.processos.values())
    
    def add_edge(self,destino:Node)-> Edge:
        self.node_count['E'] += 1
        id = f"E{self.node_count['E']}"
        
        if not self.selected_node:
            raise ValueError("Nenhum nó selecionado para origem da aresta.")

        origem = self.selected_node
        edge = Edge(id,origem,destino)

        origem.add_edge(edge)
        destino.add_edge(edge)

        self.edges[id] = edge

        return edge
        
    def can_add_edge(self,node:Node) -> bool:
        isDiferenteNode =  self.selected_node != node
        iDiferenteNodeType = self.selected_node.tipoNode != node.tipoNode 

        return isDiferenteNode and iDiferenteNodeType
        
    def select_node(self, node: Node):
        self.selected_node = node
    
    def add_process(self,x,y) -> Node:
        self.node_count['P'] += 1
        name = f"Processo {self.node_count['P']}"
        id = f"P{self.node_count['P']}"

        node = Node(x,y,id,name,"blue",ETipoNode.PROCESSO)
        self.processos[node.id] = node

        return node
    
    def add_resource(self,x,y,max_alocations):
        self.node_count['R'] += 1
        name = f"Recurso {self.node_count['R']}"
        id = f"R{self.node_count['R']}"

        node = Node(x,y,id,name,"orange",ETipoNode.RECURSO,max_alocations)
        self.recursos[node.id] = node

        return node
    
    def detect_deadlock_with_terminable_edges(self):
        import copy

        # Vetor de recursos disponíveis
        available = {}
        # Total de recursos por tipo
        total = {}
        # Atribuição atual de recursos a cada processo
        allocation = {pid: {} for pid in self.processos}
        # Necessidades restantes de cada processo
        request = {pid: {} for pid in self.processos}

        # Inicializar total de instâncias e allocation
        for recurso in self.recursos.values():
            total[recurso.id] = recurso.max_alocacoes
            available[recurso.id] = recurso.max_alocacoes

        for edge in self.edges.values():
            if edge.tipo == ETipoEdge.ALOCADO:
                pid = edge.destino.id  # processo
                rid = edge.origem.id   # recurso

                allocation[pid][rid] = allocation[pid].get(rid, 0) + 1
                available[rid] -= 1  # recurso já alocado
            elif edge.tipo == ETipoEdge.PEDIDO:
                pid = edge.origem.id
                rid = edge.destino.id

                request[pid][rid] = request[pid].get(rid, 0) + 1

        # Cópia dos dados para simular execução
        finished = {pid: False for pid in self.processos}
        safe_edges = []

        changed = True
        while changed:
            changed = False
            for pid in self.processos:
                if finished[pid]:
                    continue

                # O processo pode terminar?
                can_finish = True
                for rid, amount in request[pid].items():
                    if available.get(rid, 0) < amount:
                        can_finish = False
                        break

                if can_finish:
                    finished[pid] = True
                    changed = True

                    # Libera os recursos alocados pelo processo
                    for rid, amount in allocation[pid].items():
                        available[rid] += amount

                    # Arestas alocadas que podem ser removidas
                    for edge in self.edges.values():
                        if (
                            edge.tipo == ETipoEdge.ALOCADO
                            and edge.destino.id == pid
                        ):
                            safe_edges.append(edge.id)

        # Processos não finalizados estão em deadlock
        deadlocked = [pid for pid, done in finished.items() if not done]

        return deadlocked, safe_edges



