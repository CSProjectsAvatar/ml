from abc import ABC, abstractmethod
from dataclasses import dataclass
from distutils.util import change_root
from tkinter import CHAR
from typing import List,Tuple, Optional


class AstNode(ABC):
    pass

@dataclass
class Identifier: # Abstract
    name:str

class VarName(Identifier):
    pass

class Literal(AstNode):
    pass

class NodeLabel(Identifier):
    pass

@dataclass
class Limit(AstNode):
    number: int

@dataclass
class NodePattern(AstNode):
    variable:  VarName
    nodeLabels: List[NodeLabel]
    properties: List[Tuple[VarName, Literal]]

@dataclass
class AttributeAccessor(AstNode):
    pass

@dataclass
class Order:
    ascending: bool
    attribute: AttributeAccessor

@dataclass
class RelationDetails(AstNode):
    details: List[Tuple[VarName, Literal]]
    relationNames: List[Identifier]

@dataclass
class Projection(AstNode):
    pass
@dataclass
class RelationPattern(AstNode):
    rarrow: bool
    larrow: bool
    relationDetails: RelationDetails

@dataclass
class Pattern(AstNode):
    node_pattern: NodePattern
    relations: List[Tuple[RelationPattern, NodePattern]] 


@dataclass
class Atom(AstNode):
    pass



@dataclass
class Comparison(AstNode):
    left: Atom
    right: Atom
    operation: CHAR

@dataclass
class Conjunction(AstNode):
    comparisons: List[Comparison]

@dataclass
class Condition(AstNode):
    conjunctions: List[Conjunction]

class Where(AstNode):
    condition: Condition

@dataclass
class Match(AstNode):
    optional: bool
    pattern: Pattern
    where_: Where 

class Return(AstNode):
    distinct: Optional[bool]
    limit: Optional[Limit]
    skip: Optional[Condition]
    projections: List[Projection]

@dataclass
class SingleQuery(AstNode):
    match: Match
    return_: Return