from enum import Enum, auto


class GraphRole(Enum):
    """Role of a word in the graph."""
    NONE = auto()
    ENTITY = auto()
    RELATION = auto()
    ATTRIBUTE = auto()
