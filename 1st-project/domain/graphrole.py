from enum import Enum, auto


class GraphRole(Enum):
    NONE = auto()
    ENTITY = auto()
    RELATION = auto()
    ATTRIBUTE = auto()
