import unittest
from bloxivora import Game,SHAPES
class Tests(unittest.TestCase):
 def test_shapes(self):
  for s in SHAPES:self.assertEqual(len(set(s)),4)
 def test_bag(self):
  g=Game(1);g.bag=[];self.assertEqual(set(g.draw() for _ in range(7)),set(range(7)))
 def test_boundary(self):
  g=Game();
  for _ in range(20):g.move(-1)
  self.assertFalse(g.move(-1));self.assertTrue(all(x>=0 for x,y in g.cells()))
 def test_rotate(self):
  g=Game(1);g.kind=2;g.shape=SHAPES[2];before=g.shape
  for _ in range(4):self.assertTrue(g.rotate())
  self.assertEqual(set(before),set(g.shape))
 def test_drop(self):
  g=Game(1);g.drop();self.assertEqual(len(g.board),4);self.assertGreater(g.score,0)
 def test_clear(self):
  g=Game();g.board={(x,17):1 for x in range(10)};g.board[2,16]=2;self.assertEqual(g.clear(),1);self.assertEqual(g.board,{(2,17):2});self.assertEqual(g.score,100)
 def test_four(self):
  g=Game();g.board={(x,y):1 for x in range(10) for y in range(14,18)};self.assertEqual(g.clear(),4);self.assertEqual(g.score,800)
 def test_over(self):
  g=Game();g.board={(x,y):1 for x in range(10) for y in range(4)};g.spawn();self.assertTrue(g.dead);self.assertFalse(g.down())
 def test_seed(self):self.assertEqual(Game(4).shape,Game(4).shape)
 def test_simulate(self):
  for i in range(20):
   g=Game(i)
   for _ in range(60):
    g.rotate();g.move(g.rng.choice([-1,1]));g.drop();self.assertTrue(all(0<=x<10 and 0<=y<18 for x,y in g.board))
class MoreTests(unittest.TestCase):
 def test_speed(self):
  g=Game();self.assertEqual(g.interval(),.7);g.lines=10;self.assertLess(g.interval(),.7);g.lines=10000;self.assertEqual(g.interval(),.12)
 def test_no_rotate_through(self):
  g=Game();g.kind=2;g.shape=SHAPES[2];g.x=3;g.y=4;g.board={(x,y):1 for x in range(10) for y in range(4,7) if (x,y) not in g.cells()};self.assertFalse(g.rotate())
 def test_double_compaction(self):
  g=Game();g.board={(x,y):1 for x in range(10) for y in (16,17)};g.board[2,15]=2;g.clear();self.assertEqual(g.board,{(2,17):2})
if __name__=='__main__':unittest.main()
