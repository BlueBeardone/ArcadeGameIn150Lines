import pygame,random,asyncio
pygame.init()
W,H,GS=600,600,20
GW,GH=W//GS,H//GS
FPS=10
C={0:(0,0,0),1:(255,255,255),2:(0,255,0),3:(255,0,0),4:(0,120,255),5:(255,255,0),6:(180,0,255),7:(100,100,100)}
D=[(0,-1),(0,1),(-1,0),(1,0)]
class S:
 def __init__(self):
  self.positions=[(GW//2,GH//2)]
  self.direction=random.choice(D)
  self.score=self.grow_to=3
  self.speed_boost=self.invincible=0
 def get_head_position(self):return self.positions[0]
 def turn(self,point):
  if self.grow_to>3 and (point[0]*-1,point[1]*-1)==self.direction:return
  self.direction=point
 def move(self):
  head=self.get_head_position()
  x,y=self.direction
  new=((head[0]+x)%GW,(head[1]+y)%GH)
  if not self.invincible and new in self.positions[1:]:
   self.__init__();return True
  self.positions.insert(0,new)
  if len(self.positions)>self.grow_to:self.positions.pop()
  if self.speed_boost>0:self.speed_boost-=1
  return False
 def draw(self,s):
  for i,p in enumerate(self.positions):
   r=pygame.Rect((p[0]*GS,p[1]*GS),(GS,GS))
   c=C[6]if self.invincible else C[4]if self.speed_boost else C[2]
   pygame.draw.rect(s,c,r);pygame.draw.rect(s,C[0],r,1)
class F:
 def __init__(self):self.position=(0,0);self.randomize_position()
 def randomize_position(self):
  self.position=(random.randint(0,GW-1),random.randint(0,GH-1))
  r=random.random();self.type="n"if r<0.7 else"s"if r<0.9 else"i"
 def draw(self,s):
  r=pygame.Rect((self.position[0]*GS,self.position[1]*GS),(GS,GS))
  c=C[3]if self.type=="n"else C[5]if self.type=="s"else C[6]
  pygame.draw.rect(s,c,r);pygame.draw.rect(s,C[0],r,1)
async def main():
 screen=pygame.display.set_mode((W,H))
 pygame.display.set_caption('Snake Game')
 clock=pygame.time.Clock()
 s,f=S(),F()
 font=pygame.font.SysFont('Arial',20)
 game_over=False
 cs=FPS
 obstacles=[]
 for _ in range(5):
  p=(random.randint(0,GW-1),random.randint(0,GH-1))
  while p in obstacles:p=(random.randint(0,GW-1),random.randint(0,GH-1))
  obstacles.append(p)
 while True:
  for e in pygame.event.get():
   if e.type==pygame.QUIT:return
   elif e.type==pygame.KEYDOWN:
    if e.key==pygame.K_UP:s.turn(D[0])
    elif e.key==pygame.K_DOWN:s.turn(D[1])
    elif e.key==pygame.K_LEFT:s.turn(D[2])
    elif e.key==pygame.K_RIGHT:s.turn(D[3])
    elif e.key==pygame.K_r and game_over:s,f=S(),F();game_over=False;cs=FPS
  if not game_over:
   cs=FPS*2 if s.speed_boost else FPS
   game_over=s.move()
   if not s.invincible and s.get_head_position() in obstacles:s,f=S(),F();game_over=True
   if s.get_head_position()==f.position:
    if f.type=="n":s.grow_to+=1
    s.score+=1 if f.type=="n"else 2 if f.type=="s"else 3
    if f.type=="s":s.speed_boost=15
    if f.type=="i":s.invincible=True
    f.randomize_position()
    while f.position in s.positions or f.position in obstacles:f.randomize_position()
  screen.fill(C[0])
  for y in range(0,H,GS):
   for x in range(0,W,GS):pygame.draw.rect(screen,C[1],pygame.Rect((x,y),(GS,GS)),1)
  for p in obstacles:pygame.draw.rect(screen,C[7],pygame.Rect((p[0]*GS,p[1]*GS),(GS,GS)))
  s.draw(screen);f.draw(screen)
  screen.blit(font.render(f'Score: {s.score}',1,C[1]),(5,5))
  if s.speed_boost:screen.blit(font.render(f'Speed: {s.speed_boost}',1,C[5]),(5,30))
  if s.invincible:screen.blit(font.render('Invincible!',1,C[6]),(5,55))
  if game_over:screen.blit(font.render('Game Over! Press R',1,C[3]),(W//2-100,H//2))
  pygame.display.update();clock.tick(cs);await asyncio.sleep(0)
asyncio.run(main())