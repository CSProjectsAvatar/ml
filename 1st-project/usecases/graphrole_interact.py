from domain.graphrole import GraphRole
from interfaces.graph import GraphInteract


class WordGraphClassf:
    def __init__(self, graph_interact: GraphInteract) -> None:
        self.graph = graph_interact

    def get_role(self, word: str) -> GraphRole:
        word = word.lower()

        if word in self.graph.get_entities():
            return GraphRole.ENTITY
        elif word in self.graph.get_relations():
            return GraphRole.RELATION
        elif word in self.graph.get_attributes():
            return GraphRole.ATTRIBUTE

        return GraphRole.NONE



        

