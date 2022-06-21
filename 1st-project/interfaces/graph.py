from abc import ABC, abstractmethod
from typing import List


class GraphInteract(ABC):
    """Graph interactor."""
    @abstractmethod
    def get_entities(self) -> List[str]:
        """Returns entities names in lowercase."""
        raise NotImplementedError()

    @abstractmethod
    def get_relations(self) -> List[str]:
        """Returns relations names in lowercase."""
        raise NotImplementedError()

    @abstractmethod
    def get_attributes(self) -> List[str]:
        """Returns attributes names in lowercase."""
        raise NotImplementedError()

    @abstractmethod
    def attrs(self, type_name: str) -> List[str]:
        """Returns attributes of type_name (relation or entity label) in lowercase."""
        raise NotImplementedError()


class FakeGraphInteract(GraphInteract):
    def __init__(self) -> None:
        self.entities = ['human', 'painting', 'apartment']
        self.relations = ['paints', 'lives', 'has']
        self.attributes = ['name', 'age', 'height', 'weight', 'color']

    def get_entities(self) -> List[str]:
        return self.entities

    def get_relations(self) -> List[str]:
        return self.relations

    def get_attributes(self) -> List[str]:
        return self.attributes

    def attrs(self, type_name: str) -> List[str]:
        """Returns attributes of type_name (relation or entity label) in lowercase."""
        raise NotImplementedError()
