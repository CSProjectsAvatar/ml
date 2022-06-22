from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List,Tuple, Optional, Union


class AstNode(ABC):
    pass

@dataclass
class Literal(AstNode):
    value: str


@dataclass
class NodePattern(AstNode):
    variable:  Optional[str]
    nodeLabels: Optional[List[str]]
    properties: Optional[List[Tuple[str, Literal]]]


@dataclass
class RelationDetails(AstNode):
    details: Optional[List[Tuple[str, Literal]]]
    relationNames: Optional[List[str]]


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
class AttributeAccessor(Atom):
    target: str
    property: str

@dataclass
class Order:
    ascending: Optional[bool]
    attribute: AttributeAccessor

@dataclass
class Comparison(AstNode):
    class Operator(Enum):
        GREATER = 1
        LESS = 2
        GEQ = 3
        LEQ = 4
        EQ = 5

    left: Atom
    right: Atom
    operation: Operator
    

@dataclass
class Conjunction(AstNode):
    comparisons: List[Comparison]

@dataclass
class Condition(AstNode):
    conjunctions: List[Conjunction]

@dataclass
class Match(AstNode):
    optional: bool
    pattern: Pattern
    where_: Optional[Condition]

@dataclass
class Return(AstNode):
    distinct: Optional[bool]
    limit: Optional[int]
    skip: Optional[Condition]
    projections: List[Union[str, AttributeAccessor]]
    order: Optional[Order]

@dataclass
class SingleQuery(AstNode):
    match: Match
    return_: Return
