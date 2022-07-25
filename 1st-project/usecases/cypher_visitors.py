import itertools
from typing import Iterable

import more_itertools

from domain.AST.ast_node import SingleQuery, Match, Pattern, NodePattern, RelationPattern, RelationDetails, Return, \
    Condition, Conjunction, Comparison, Literal, AttributeAccessor, Order, AstNode, Atom
from interfaces.graph import GraphInteract
from usecases.visitor import visitor


class AstCtx:
    """Context for AST traversal."""

    def __init__(self):
        self._labels = {}
        self._varid = 0

    def labels(self) -> Iterable[str]:
        """Gets all defined labels till now."""
        return more_itertools.flatten(self._labels.values())

    def labels_of(self, variable: str) -> Iterable[str]:
        """Gets all types (labels) of a variable."""
        return self._labels[variable]

    def define(self, name: str, labels: Iterable[str]):
        self._labels[name] = labels

    def var_name(self):
        self._varid += 1
        return f'var{self._varid}'

    def defined_vars(self) -> Iterable[str]:
        return map(lambda name: f'var{name}', range(1, self._varid))


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
                pstr = 'all from any entity under the categor' \
                       + ('ies' if more_itertools.quantify(types) > 1 else 'y') + ' '
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


class Projection(AstNode):
    """For the sole purpose of AstGen visit."""
    pass


class AstGen:
    def __init__(self, graph_mngr: GraphInteract):
        self.graph = graph_mngr
        self.ctx = AstCtx()

    """Generates all the valid ASTs."""
    @visitor(SingleQuery)
    def visit(self, sq: SingleQuery) -> Iterable[SingleQuery]:
        for match in self.visit(Match(False, None, None)):
            for return_ in self.visit(Return(False, None, None, None, None)):
                yield SingleQuery(match=match, return_=return_)

    @visitor(Match)
    def visit(self, m: Match) -> Iterable[Match]:
        for p in self.visit(Pattern(None, None)):
            for w in self.visit(Condition(None)):
                yield Match(False, pattern=p, where_=w)
                yield Match(True, pattern=p, where_=w)

    @visitor(Return)
    def visit(self, _) -> Iterable[Return]:
        proj_take = 3  # max projections to create
        limit_top = 10  # limit property will take values from 1 to limit_top

        for ptake in range(proj_take+1):
            projs = more_itertools.take(ptake, self.visit(Projection()))

            yield Return(distinct=True, projections=projs, order=None, skip=None, limit=None)
            yield Return(distinct=False, projections=projs, order=None, skip=None, limit=None)

            for o in self.visit(Order(False, None)):
                yield Return(distinct=True, projections=projs, order=o, skip=None, limit=None)
                yield Return(distinct=False, projections=projs, order=o, skip=None, limit=None)

                for s in self.visit(Condition(None)):  # skip
                    yield Return(distinct=True, projections=projs, order=o, skip=s, limit=None)
                    yield Return(distinct=False, projections=projs, order=o, skip=s, limit=None)

                    for limit in range(1, limit_top+1):
                        yield Return(distinct=True, projections=projs, order=o, skip=s, limit=limit)
                        yield Return(distinct=False, projections=projs, order=o, skip=s, limit=limit)

    @visitor(Pattern)
    def visit(self, _) -> Iterable[Pattern]:
        relation_node_take = 3
        for fst_node in self.visit(NodePattern('', [], properties=None)):
            for rntake in range(relation_node_take+1):
                rand_prod = more_itertools.random_product(self.visit(NodePattern('', [], properties=None)), self.visit(RelationPattern(larrow=False, rarrow=False, relationDetails=None)), repeat=rntake)
                tail = [(rand_prod[2*i], rand_prod[2*i+1]) for i in range(rntake)]

                yield Pattern(fst_node, tail)

    @visitor(NodePattern)
    def visit(self, _) -> Iterable[NodePattern]:
        label_take = 3
        props_take = 3
        varname = self.ctx.var_name()  # next available variable number
        for labtake in range(label_take+1):
            labels = self.graph.rand_entity_labels(labtake)

            yield NodePattern(nodeLabels=list(labels), variable=None, properties=None)

            for ptake in range(props_take+1):
                props = more_itertools.flatten((self.graph.attrs(l) for l in labels))
                val_iters = (self.graph.values_of(p) for p in props)
                vals = more_itertools.random_product(*val_iters, repeat=ptake)
                for vals_for_props in more_itertools.grouper(vals, ptake):
                    yield NodePattern(nodeLabels=list(labels), variable=varname,
                                  properties=list(zip(props, map(lambda vs: Literal(vs), vals_for_props))))

    @visitor(RelationPattern)
    def visit(self, _) -> Iterable[RelationPattern]:
        for detail in self.visit(RelationDetails(None, None, None)):
            yield RelationPattern(larrow=False, relationDetails=detail, rarrow=False)
            yield RelationPattern(larrow=True, relationDetails=detail, rarrow=False)
            yield RelationPattern(larrow=False, relationDetails=detail, rarrow=True)

    @visitor(RelationDetails)
    def visit(self, _) -> Iterable[RelationDetails]:
        label_take = 3
        props_take = 3
        varname = self.ctx.var_name()  # next available variable number
        for labtake in range(label_take+1):
            labels = self.graph.rand_relation_labels(labtake)

            yield RelationDetails(relationNames=labels, variable=None, details=None)

            for ptake in range(props_take+1):
                props = more_itertools.flatten((self.graph.attrs(l) for l in labels))
                val_iters = (self.graph.values_of(p) for p in props)
                vals = more_itertools.random_product(*val_iters, repeat=ptake)
                for vals_for_props in more_itertools.grouper(vals, ptake):
                    yield RelationDetails(relationNames=labels, variable=varname,
                                      details=list(zip(props, map(lambda v: Literal(v), vals_for_props))))

    @visitor(Condition)
    def visit(self, _) -> Iterable[Condition]:
        max_conjs = 3
        for conj_take in range(max_conjs+1):
            yield Condition(more_itertools.random_product(self.visit(Conjunction()), repeat=conj_take))

    @visitor(Conjunction)
    def visit(self, _) -> Iterable[Conjunction]:
        max_cmps = 3
        for cmps_take in range(max_cmps+1):
            yield Conjunction(more_itertools.random_product(self.visit(Comparison()), repeat=cmps_take))

    @visitor(Comparison)
    def visit(self, _) -> Iterable[Comparison]:
        operators = [
            Comparison.Operator.EQ,
            Comparison.Operator.LEQ,
            Comparison.Operator.LESS,
            Comparison.Operator.GEQ,
            Comparison.Operator.GREATER,
        ]
        for op in operators:
            for left in self.visit(Atom()):
                for right in self.visit(Atom()):
                    yield Comparison(left=left, operation=op, right=right)

    @visitor(Atom)
    def visit(self, _) -> Iterable[Atom]:
        return map(lambda v: Literal(str(v)), itertools.chain(['New York', 5, 'Havana', 23, 35, 'Texas'], self.visit(AttributeAccessor(None, None))))

    @visitor(Projection)
    def visit(self, _) -> Iterable[Projection]:
        return itertools.chain(self.ctx.defined_vars(), self.visit(AttributeAccessor(None, None)))

    @visitor(AttributeAccessor)
    def visit(self, _) -> Iterable[AttributeAccessor]:
        for v in self.ctx.defined_vars():
            for l in self.ctx.labels_of(v):
                for attr in self.graph.attrs(l):
                    yield AttributeAccessor(target=v, property=attr)

    @visitor(Order)
    def visit(self, _) -> Iterable[Order]:
        yield Order(False, None)  # todo @audit tas pasan2 None
        yield Order(True, None)
