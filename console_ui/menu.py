''' 
Classes and functions relating to the menu for the console version of the 
user interface.
'''
from typing import Optional, Any

listicle = Optional[list[Any] | tuple[Any, ...]]



class Node:

    def __init__(self,
                 parent_node: 'Node | Tree',
                 child_nodes: listicle = None
                 ) -> None:
        
        self.parent: 'Node | Tree' = parent_node
        self.children: list['Node'] = []


    def steps_to_root(self, counter: int) -> int:
        '''
        _summary_

        Parameters
        ----------
        counter : int
            _description_

        Returns
        -------
        int
            _description_
        '''
        counter += 1
        if isinstance(self.parent, Tree):
            return counter
        else:
            return self.parent.steps_to_root(counter)


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


    def remove_node(self, node: Node, sever: bool = False) -> None:
        if sever == True:
            if node in self.nodes:
                self.nodes.remove(node)
        else:
            for child in node.children:
                child.parent = node.parent
                if not isinstance(node.parent, Tree):
                    node.parent.attach(child)

    


    

    
    

