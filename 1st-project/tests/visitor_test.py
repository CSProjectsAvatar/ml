import unittest

from usecases.visitor import visitor


class A:
    pass


class B:
    pass


class C(B):
    pass


class D:
    def __init__(self, e, f):
        self.e = e
        self.f = f


class E:
    pass


class F:
    pass


class Visitor:
    @visitor(A)
    def visit(self, a):
        return 'a'

    @visitor(B)
    def visit(self, b):
        return 'b'

    @visitor(D)
    def visit(self, d):
        return 'd' + self.visit(d.e) + self.visit(d.f)

    @visitor(E)
    def visit(self, e):
        return 'e'

    @visitor(F)
    def visit(self, e):
        return 'f'


class V2:
    @visitor(F)
    def visit(self, f):
        return 'f2'


class VisitorTest(unittest.TestCase):
    def test_visit_target_class(self):
        v = Visitor()
        self.assertEqual(v.visit(A()), 'a')
        self.assertEqual(v.visit(B()), 'b')

    def test_recursion(self):
        v = Visitor()
        self.assertEqual(v.visit(D(E(), F())), 'def')

    def test_2_visitors_same_visit(self):
        v1 = Visitor()
        v2 = V2()
        f = F()
        self.assertEqual(v1.visit(f), 'f')
        self.assertEqual(v2.visit(f), 'f2')


if __name__ == '__main__':
    unittest.main()
