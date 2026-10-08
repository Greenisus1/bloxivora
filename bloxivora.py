#!/usr/bin/env python3
"""Bloxivora: terminal falling blocks with line clearing."""
import curses,random,time,argparse
from terminal_ui import setup,text,title
SHAPES=[((0,1),(1,1),(2,1),(3,1)),((1,0),(2,0),(1,1),(2,1)),((1,0),(0,1),(1,1),(2,1)),((1,0),(2,0),(0,1),(1,1)),((0,0),(1,0),(1,1),(2,1)),((0,0),(0,1),(1,1),(2,1)),((2,0),(0,1),(1,1),(2,1))]
class Game:
 width=10;height=18
 def __init__(self,seed=None):
  self.rng=random.Random(seed);self.board={};self.bag=[];self.score=0;self.lines=0;self.dead=False;self.next=self.draw();self.spawn()
 def draw(self):
  if not self.bag:self.bag=list(range(7));self.rng.shuffle(self.bag)
  return self.bag.pop()
 def spawn(self):
  self.kind=self.next;self.next=self.draw();self.shape=SHAPES[self.kind];self.x=3;self.y=0
  if not self.valid(self.shape,self.x,self.y):self.dead=True
 def cells(self,shape=None,x=None,y=None):return [(self.x+dx if x is None else x+dx,self.y+dy if y is None else y+dy) for dx,dy in (self.shape if shape is None else shape)]
 def valid(self,shape,x,y):return all(0<=cx<10 and 0<=cy<18 and (cx,cy) not in self.board for cx,cy in self.cells(shape,x,y))
 def move(self,dx):
  if self.dead:return False
  if self.valid(self.shape,self.x+dx,self.y):self.x+=dx;return True
  return False
 def rotate(self):
  if self.dead:return False
  if self.kind==1:return True
  size=4 if self.kind==0 else 3;shape=tuple((size-1-y,x) for x,y in self.shape)
  for kick in (0,-1,1,-2,2):
   if self.valid(shape,self.x+kick,self.y):self.shape=shape;self.x+=kick;return True
  return False
 def clear(self):
  rows={y for y in range(18) if all((x,y) in self.board for x in range(10))};n=len(rows)
  if n:
   self.board={(x,y+sum(r>y for r in rows)):v for (x,y),v in self.board.items() if y not in rows};self.lines+=n;self.score+=(0,100,300,500,800)[n]*(1+self.lines//10)
  return n
 def down(self):
  if self.dead:return False
  if self.valid(self.shape,self.x,self.y+1):self.y+=1;return True
  for p in self.cells():self.board[p]=self.kind+1
  self.clear();self.spawn();return False
 def drop(self):
  if self.dead:return
  while self.valid(self.shape,self.x,self.y+1):self.y+=1;self.score+=2
  self.down()
def run(stdscr,seed):
 setup(stdscr);stdscr.timeout(50);g=Game(seed);last=time.monotonic();paused=False
 while True:
  title(stdscr,'Bloxivora',f'Score {g.score} | Lines {g.lines} | '+('Game over' if g.dead else 'Paused' if paused else 'Playing'),'A/D move | W rotate | S soft | Space drop | P pause | R new | Q quit')
  h,w=stdscr.getmaxyx()
  if h<25 or w<82:text(stdscr,4,2,'Resize to 82x25. Board paused.',3);last=time.monotonic()
  else:
   active=set(g.cells())
   for y in range(18):
    text(stdscr,4+y,4,'|',1);text(stdscr,4+y,25,'|',1)
    for x in range(10):
     v=g.kind+1 if (x,y) in active else g.board.get((x,y),0);text(stdscr,4+y,5+x*2,'##' if v else ' .',((v-1)%6+1) if v else 0,True)
   text(stdscr,22,4,'+--------------------+',1);text(stdscr,5,30,'NEXT',1)
   for dx,dy in SHAPES[g.next]:text(stdscr,7+dy,30+dx*2,'##',g.next%6+1)
   if not paused and time.monotonic()-last>=max(.12,.7-.05*(g.lines//10)):g.down();last=time.monotonic()
  stdscr.refresh();k=stdscr.getch()
  if k==ord('q'):return
  if k==ord('r'):g=Game(seed);paused=False;last=time.monotonic()
  elif k==ord('p'):paused=not paused;last=time.monotonic()
  elif not paused and h>=25 and w>=82:
   if k in (curses.KEY_LEFT,ord('a')):g.move(-1)
   elif k in (curses.KEY_RIGHT,ord('d')):g.move(1)
   elif k in (curses.KEY_UP,ord('w')):g.rotate()
   elif k in (curses.KEY_DOWN,ord('s')):g.down();last=time.monotonic()
   elif k==32:g.drop();last=time.monotonic()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seed',type=int);p.add_argument('--demo',action='store_true');a=p.parse_args()
 if a.demo:
  g=Game(a.seed);print('BLOXIVORA\n'+ '\n'.join(''.join('#' if (x,y) in g.cells() else '.' for x in range(10)) for y in range(18)));return
 try:curses.wrapper(run,a.seed)
 except curses.error:print('Needs an interactive curses terminal (82x25 minimum).')
 except KeyboardInterrupt:pass
if __name__=='__main__':main()
