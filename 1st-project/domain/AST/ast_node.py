from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List,Tuple, Optional


class AstNode(ABC):
    pass

class Return(AstNode):
    pass

class Where(AstNode):
    pass

@dataclass
class Identifier: # Abstract
    name:str

class VarName(Identifier):
    pass

class NodeLabel(Identifier):
    pass

@dataclass
class NodePattern(AstNode):
    variable:  str
    nodeLabels: List[str]
    properties: 
    pass

class RelationPattern(AstNode):
    pass

class Pattern(AstNode):
    node_pattern:NodePattern
    relations:List[Tuple[RelationPattern, NodePattern]] 

@dataclass
class Match(AstNode):
    optional:bool
    pattern:Pattern
    where_: Optional[Where]









@dataclass
class SingleQuery(AstNode):
    match: Match
    return_: Return




