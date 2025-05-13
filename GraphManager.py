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
        # Mapear índices
        processo_ids = list(self.processos.keys())
        recurso_ids = list(self.recursos.keys())

        index_proc = {pid: i for i, pid in enumerate(processo_ids)}
        index_recurso = {rid: j for j, rid in enumerate(recurso_ids)}

        process_len = len(processo_ids)
        recurso_len = len(recurso_ids)

        # Inicializar matrizes
        allocation = [[0]*recurso_len for _ in range(process_len)]
        request = [[0]*recurso_len for _ in range(process_len)]
        available = [0]*recurso_len

        # 1. Preencher a matriz de alocação
        for edge in self.edges.values():
            if edge.tipo == ETipoEdge.ALOCACAO:
                i = index_proc[edge.destino.id]
                j = index_recurso[edge.origem.id]
                allocation[i][j] += 1
            
            elif edge.tipo == ETipoEdge.REQUISACAO:
                i = index_proc[edge.origem.id]
                j = index_recurso[edge.destino.id]
                request[i][j] += 1

        # 2. Vetor de disponíveis
        for rid, node in self.recursos.items():
            j = index_recurso[rid]
            allocated = sum(allocation[i][j] for i in range(process_len))
            available[j] = node.max_alocacoes - allocated

        # 3. Algoritmo de detecção de deadlock
        work = available[:]
        finish = [False]*process_len
        liberaveis = []

        while True:
            progress = False
            for i in range(process_len):
                if not finish[i]:
                    # Verifica se o processo i pode terminar com os recursos disponíveis
                    if all(request[i][j] <= work[j] for j in range(recurso_len)):
                        # Processo pode terminar: libera os recursos
                        for j in range(recurso_len):
                            work[j] += allocation[i][j]

                        for edge in self.edges.values():
                            if (
                                edge.destino.id == processo_ids[i]
                                or edge.origem.id == processo_ids[i]
                            ):
                                liberaveis.append(edge.id)


                        finish[i] = True
                        progress = True
            if not progress:
                break  # Nenhum processo pôde terminar nesta iteração → parar

        processos_em_deadlock = [
            processo_ids[i] for i in range(process_len) if not finish[i]
        ]

        return processos_em_deadlock,liberaveis

        



