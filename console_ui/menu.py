''' 
Classes and functions relating to the menu for the console version of the 
user interface.
'''
from typing import Optional, Any

listicle = Optional[list[Any] | tuple[Any, ...]]



class Node:

    def __init__(self,
                 parent_node: 'Node | Tree'
                 ) -> None:
        
        self.parent: 'Node | Tree' = parent_node
        parent_node.attach(self)
        self.root = 
        self.children: list['Node'] = []


    def fetch_root(self) -> Tree:
        

    def nodes_to_root(self, node_list: list['Node'] | None = None) -> list['Node']:
        if node_list is None:
            node_list = []
        node_list.append(self)
        if isinstance(self.parent, Tree):
            return node_list
        else:
            return self.parent.nodes_to_root(node_list)
        
    


    def detach(self, child: 'Node') -> None:
        '''
        _summary_

        Parameters
        ----------
        child : Node
            _description_
        '''
        if child in self.children:
            self.children.remove(child)


    def attach(self, child: 'Node') -> None:
        '''
        _summary_

        Parameters
        ----------
        child : Node
            _description_
        '''
        if child not in self.children:
            self.children.append(child)


class Tree:

    def __init__(self,
                  nodes: listicle = None
                  ) -> None:
        
        self.nodes = []
        if nodes is not None:
            self.nodes: list[Node] = list(filter(lambda x : isinstance(x, Node), nodes))

        self.current_node: Node
        self.next_nodes: list[Node]


    def attach(self, node: Node) -> None:
        if node not in self.nodes:
            self.nodes.append(node)


    def detach(self, node: Node, sever: bool = False) -> None:
        if sever is False:
            for ch_node in self.nodes:
                if ch_node.parent == node:
                    ch_node.parent = node.parent
                    if not isinstance(node.parent, Tree):
                        node.parent.attach(ch_node)
        self.nodes.remove(node)

    


    

    
    
