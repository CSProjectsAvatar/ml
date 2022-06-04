import unittest
from usecases.graphrole_interact import WordGraphClassf
from interfaces.graph import FakeGraphInteract
from domain.graphrole import GraphRole


class GraphRoleInteractTest(unittest.TestCase):
   def test_fake_none_result(self):
      ginter = FakeGraphInteract()
      wgc = WordGraphClassf(ginter)
      self.assertEqual(GraphRole.NONE, wgc.get_role('bla'))
      self.assertEqual(GraphRole.NONE, wgc.get_role('home'))
      self.assertEqual(GraphRole.ENTITY, wgc.get_role('human'))

   def test_fake_relation_result(self):
      ginter = FakeGraphInteract()
      wgc = WordGraphClassf(ginter)
      self.assertEqual(GraphRole.RELATION, wgc.get_role('lives'))

   def test_fake_lowercase(self):
      ginter = FakeGraphInteract()
      wgc = WordGraphClassf(ginter)
      self.assertEqual(GraphRole.ATTRIBUTE, wgc.get_role('AgE'))


if __name__ == "__main__":
   unittest.main()