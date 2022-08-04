import unittest

import more_itertools

from domain.AST.ast_node import SingleQuery, Match, Pattern, NodePattern, Literal, RelationPattern, RelationDetails, \
    Return, AttributeAccessor
from interfaces.graph import FakeGraphInteract
from usecases.cypher_visitors import QueryGen, AstGen


class EnglishQueryGenerator(unittest.TestCase):
    def test_something(self):
        v = QueryGen(FakeGraphInteract())
        print('\n', v.visit(
            SingleQuery(
                match=Match(
                    optional=False,
                    pattern=Pattern(
                        node_pattern=NodePattern(
                            'p', ['human'], [('name', Literal('Andy Ledesma'))]
                        ),
                        relations=[(
                            RelationPattern(
                                larrow=False, rarrow=True,
                                relationDetails=RelationDetails(
                                    relationNames=['lives'],
                                    details=None, variable=None
                                )
                            ),
                            NodePattern(
                                None, ['apartment'], [('price', Literal('23k'))]
                            )
                        )]
                    ),
                    where_=None
                ),
                return_=Return(
                    distinct=False, limit=0, skip=None, order=None,
                    projections=[AttributeAccessor('p', 'age')]
                )
            )
        ))

    def test_ast_gen(self):
        g = FakeGraphInteract()
        v = AstGen(g)
        en_v = QueryGen(g)
        print(list(map(lambda ast: en_v.visit(ast), more_itertools.take(5, v.visit(SingleQuery(None, None))))))


if __name__ == '__main__':
    unittest.main()
