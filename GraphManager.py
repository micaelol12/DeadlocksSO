from Enums import ETipoNode
from Node import Node
from Edge import Edge

class Graphmanager:
    def __init__(self,canvas):
        self.nodes: dict[str,Node] = {}
        self.edges: dict[str,Edge] = {}
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node:Node = None
        self.canvas = canvas

    def clear(self):
        self.nodes.clear()
        self.edges.clear()
        self.node_count = {'P': 0, 'R': 0, 'E': 0}
        self.selected_node = None
    
    def delete_node(self, node:Node):
        if node.id in self.nodes:
            node.delete()

            del self.nodes[node.id]

            if self.selected_node == node:
                self.selected_node = None
    
    def delete_edge(self,edge:Edge):
        if edge.id in self.edges:
            edge.delete()

            edge.origem.delete_edge(edge)
            edge.destino.delete_edge(edge)

            del self.edges[edge.id]
    
    def has_node_at_position(self, x, y) -> bool:
        return any(node.is_in_position(x, y) for node in self.nodes.values())
    
    def add_edge(self,origem:Node,destino:Node)-> Edge:
        self.node_count['E'] += 1
        id = f"E{self.node_count['E']}"

        edge = Edge(id,origem,destino,self.canvas)

        origem.add_edge(edge)
        destino.add_edge(edge)

        self.edges[id] = edge

        return edge


    def try_add_edge(self,node:Node):
        isDiferenteNode =  self.selected_node != node
        iDiferenteNodeType = self.selected_node.tipoNode != node.tipoNode

        if isDiferenteNode and iDiferenteNodeType:
                edge = self.add_edge(self.selected_node,node)
                self.selected_node.unhighlight_node()
                self.selected_node = None
                return edge
        
    def seleciona_node(self,node:Node):
        node.highlight_node()
        self.selected_node = node
    
    def add_process(self,x,y) -> Node:
        self.node_count['P'] += 1
        name = f"Processo {self.node_count['P']}"
        id = f"P{self.node_count['P']}"
        
        return self.create_node(name,id, "blue",x,y,ETipoNode.PROCESSO)
    
    
    def add_resource(self,x,y,max_alocations):
        if(max_alocations):
            self.node_count['R'] += 1
            name = f"Recurso {self.node_count['R']}"
            id = f"R{self.node_count['R']}"
            return self.create_node(name,id,"orange",x,y,ETipoNode.RECURSO,max_alocations)

    def create_node(self, name, id , color, x, y,tipo: ETipoNode,max_edges:int = None) -> Node:
        node = Node(x,y,id,name,self.canvas,color,tipo,max_edges)

        node.print_node()
        self.nodes[id] = node

        return node
