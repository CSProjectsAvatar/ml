from typing import Iterable

import more_itertools

from domain.AST.ast_node import SingleQuery, Match, Pattern, NodePattern, RelationPattern, RelationDetails, Return, \
    Condition, Conjunction, Comparison, Literal, AttributeAccessor, Order
from interfaces.graph import GraphInteract
from usecases.visitor import visitor


class AstCtx:
    def __init__(self):
        self._labels = {}

    """Context for AST traversal."""
    def labels(self) -> Iterable[str]:
        """Gets all defined labels till now."""
        return more_itertools.flatten(self._labels.values())

    def labels_of(self, variable: str) -> Iterable[str]:
        """Gets all types (labels) of a variable."""
        return self._labels[variable]

    def define(self, name: str, labels: Iterable[str]):
        self._labels[name] = labels


class QueryGen:
    def __init__(self, graph: GraphInteract):
        self.ctx = AstCtx()
        self.graph = graph

    @visitor(SingleQuery)
    def visit(self, sq: SingleQuery) -> str:
        return 'From ' + self.visit(sq.match) + '; ' + self.visit(sq.return_) + '.'

    @visitor(Match)
    def visit(self, m: Match) -> str:
        ans = ', if found, ' if m.optional else ''
        ans += self.visit(m.pattern)

        if m.where_:
            return ans + '; where ' + self.visit(m.where_)

        return ans

    @visitor(Pattern)
    def visit(self, p: Pattern) -> str:
        ans = self.visit(p.node_pattern)
        for (r, n) in p.relations:
            ans += 'in a relation ' + self.visit(r) + 'with ' + self.visit(n)

        return ans

    @visitor(NodePattern)
    def visit(self, n: NodePattern) -> str:
        ans = ''

        if n.nodeLabels:
            ans = 'any entity under the categor' + ('ies' if len(n.nodeLabels) > 1 else 'y') + ' '
            ans += ', '.join(map(lambda l: f'\"{l}\"', n.nodeLabels))
            self.ctx.define(n.variable, n.nodeLabels)

        if n.properties:
            ans += ', which '
            kvs = (f'{key} is \"{literal.value}\"' for (key, literal) in n.properties)
            ans += ', '.join(kvs)

        return ans + ' '

    @visitor(RelationPattern)
    def visit(self, r: RelationPattern) -> str:
        ans = ''
        # larrow and rarrow can't be on at the same time
        if r.larrow:
            ans = 'from right to left '
        elif r.rarrow:
            ans = 'from left to right '

        return ans + self.visit(r.relationDetails)

    @visitor(RelationDetails)
    def visit(self, r: RelationDetails) -> str:
        ans = ''
        if r.relationNames:
            ans = 'called ' + ' or '.join(map(lambda l: f'\"{l}\"', r.relationNames))
            self.ctx.define(r.variable, r.relationNames)

        if r.details:
            ans += ', which '
            kvs = (f'{key} is \"{literal.value}\"' for (key, literal) in r.details)
            ans += ', '.join(kvs)

        return ans + ' '

    @visitor(Condition)
    def visit(self, cond: Condition) -> str:
        return ' or '.join(map(lambda c: self.visit(c), cond.conjunctions)) + ' '

    @visitor(Conjunction)
    def visit(self, conj: Conjunction) -> str:
        return ' and '.join(map(lambda c: self.visit(c), conj.comparisons)) + ' '

    @visitor(Comparison)
    def visit(self, cmp: Comparison) -> str:
        op_str = {
            Comparison.Operator.EQ: '=',
            Comparison.Operator.GEQ: '>=',
            Comparison.Operator.LEQ: '<=',
            Comparison.Operator.GREATER: '>',
            Comparison.Operator.LESS: '<'
        }
        return f'{self.visit(cmp.left)} {op_str[cmp.operation]} {self.visit(cmp.right)} '

    @visitor(Literal)
    def visit(self, lit: Literal) -> str:
        return f'\"{lit.value}\"'

    @visitor(AttributeAccessor)
    def visit(self, a: AttributeAccessor) -> str:
        attr = a.property.lower()
        count = 0  # holds in how many types the attribute is
        for t in self.ctx.labels():
            if attr in self.graph.attrs(t):
                count += 1
            if count == 2:
                break

        assert 0 < count <= 2, f'Attribute {attr} appears {count} times and that\'s not possible.'

        ans = attr
        if count == 2:  # if the attribute is found in 2 or more types, we need to add the type name
            target_attr_type = (t for t in self.ctx.labels_of(a.target) if attr in self.graph.attrs(t))
            ans += ' of ' + next(target_attr_type)

        return ans + ' '

    @visitor(Return)
    def visit(self, r: Return) -> str:
        ans = ''

        if r.skip:
            ans += 'don\'t take when ' + self.visit(r.skip) + 'and '

        ans += 'give me '
        if r.limit > 1:
            ans += f'{r.limit} '

        if r.distinct:
            ans += 'distinct '

        projs_str = []
        for p in r.projections:
            if isinstance(p, AttributeAccessor):
                projs_str.append(self.visit(p))
            elif isinstance(p, str):
                types = self.ctx.labels_of(p)
                types_str = ', '.join(map(lambda t: f'\"{t}\"', types))
                pstr = 'all from any entity under the categor' + ('ies' if more_itertools.quantify(types) > 1 else 'y') + ' '
                projs_str.append(pstr + types_str)

        ans += ', '.join(projs_str) + ' '

        if r.order:
            ans += self.visit(r.order) + ' '

        return ans

    @visitor(Order)
    def visit(self, o: Order) -> str:
        ans = 'sorted by ' + self.visit(o.attribute) + ' '

        if not o.ascending:
            ans += 'in descending order '

        return ans

