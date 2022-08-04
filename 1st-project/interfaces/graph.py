from abc import ABC, abstractmethod
from typing import List, Iterable

import more_itertools


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

    def rand_entity_labels(self, amount: int) -> Iterable[str]:
        """Returns the given number of random entity rabels."""
        raise NotImplementedError()

    def values_of(self, attribute: str) -> Iterable[str]:
        raise NotImplementedError()

    def rand_relation_labels(self, amount: int):
        raise NotImplementedError()


class FakeGraphInteract(GraphInteract):
    def __init__(self) -> None:
        self.entities = ['human', 'painting', 'apartment']
        self.relations = ['paints', 'lives', 'has']
        self.attr_dict = {
            'human': ['name', 'age', 'height'],
            'painting': ['height', 'style'],
            'apartment': ['price', 'length'],
            'lives': ['time'],
            'has': ['start_time']
        }

    def get_entities(self) -> List[str]:
        return self.entities

    def get_relations(self) -> List[str]:
        return self.relations

    def get_attributes(self) -> Iterable[str]:
        return more_itertools.flatten(self.attr_dict.values())

    def attrs(self, type_name: str) -> List[str]:
        """Returns attributes of type_name (relation or entity label) in lowercase."""
        return self.attr_dict[type_name]

    def rand_entity_labels(self, amount: int) -> Iterable[str]:
        labs = more_itertools.flatten([self.attrs(e) for e in self.get_entities()])
        return more_itertools.random_product(labs, repeat=amount)

    def values_of(self, attribute: str) -> Iterable[str]:
        return 'andy'  # todo @audit

    def rand_relation_labels(self, amount: int):
        labs = more_itertools.flatten([self.attrs(e) for e in self.get_relations()])
        return more_itertools.random_product(labs, repeat=amount)
