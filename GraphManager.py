from Enums import ETipoNode
from Node import Node
from Edge import Edge

class Graphmanager:
    def __init__(self,canvas):
        self.processos: dict[str,Node] = {}
        self.recursos: dict[str,Node] = {}
        self.edges: dict[str,Edge] = {}
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node:Node = None
        self.canvas = canvas

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

        node.delete()
        if self.selected_node == node:
            self.selected_node = None
    
    def delete_edge(self,edge:Edge):
        if edge.id in self.edges:
            edge.delete()

            edge.origem.delete_edge(edge)
            edge.destino.delete_edge(edge)

            del self.edges[edge.id]
    
    def has_node_at_position(self, x, y) -> bool:
        return any(node.is_in_position(x, y) for node in self.recursos.values()) or any(node.is_in_position(x, y) for node in self.processos.values())
    
    def add_edge(self,origem:Node,destino:Node)-> Edge:
        self.node_count['E'] += 1
        id = f"E{self.node_count['E']}"

        edge = Edge(id,origem,destino,self.canvas)

        origem.add_edge(edge)
        destino.add_edge(edge)

        self.edges[id] = edge

        return edge

    def try_add_edge(self,node:Node):
        if self.can_add_edge(node):
            edge = self.add_edge(self.selected_node,node)
            self.selected_node.unhighlight_node()
            self.selected_node = None
            return edge
        
    def can_add_edge(self,node:Node) -> bool:
        isDiferenteNode =  self.selected_node != node
        iDiferenteNodeType = self.selected_node.tipoNode != node.tipoNode   
        return isDiferenteNode and iDiferenteNodeType
        
    def seleciona_node(self,node:Node):
        node.highlight_node()
        self.selected_node = node
    
    def add_process(self,x,y) -> Node:
        self.node_count['P'] += 1
        name = f"Processo {self.node_count['P']}"
        id = f"P{self.node_count['P']}"

        node = Node(x,y,id,name,self.canvas,"blue",ETipoNode.PROCESSO)
        self.processos[node.id] = node
        node.print_node()

        return node
    
    def add_resource(self,x,y,max_alocations):
        if(max_alocations):
            self.node_count['R'] += 1
            name = f"Recurso {self.node_count['R']}"
            id = f"R{self.node_count['R']}"

            node = Node(x,y,id,name,self.canvas,"orange",ETipoNode.RECURSO,max_alocations)
            self.recursos[node.id] = node
            node.print_node()

            return node

