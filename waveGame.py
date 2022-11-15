import pygame
import math
import random

# feel free to change these in case the pygame window doesn't fit, or if you want to make the window bigger
screen_width  = 500
screen_height = 500

class Player:
  '''
  attributes:
      x,y : coordinates of the player
      w,h : width and height of the player rectangle
      rect: draw the player rectangle

  methods:
    __init__: initializes the x,y,w,h attributes along with rectangle
    update_rectangle: recreates the pygame Rect
  '''
  def __init__(self):
    '''
    initializes the player at the top-left corner of the screen
    along with the pygame.Rect object
    '''
    self.x = 0
    self.y = 0
    self.w = 50
    self.h = 50
    self.update_rectangle() # creates a pygame.Rect object as self.rect attribute

    self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

    self.image = pygame.image.load('piper.png')
    self.image = pygame.transform.scale( self.image , (self.w,self.h) )

  def update_rectangle(self):
    '''
    updates the pygame Rect object according to the current dimensions: x,y,w,h
    this should be called whenever the position of the Player object is modified
    
    input: None (other than the self Player object)
    return: None
    '''
    self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

class Wave:
  '''
  A class to create a wave object
  '''
  def __init__(self):
    '''
    Initializes the wave, goes to half way across the screen
    '''
    self.x = 250
    self.y = 0
    self.w = 500
    self.h = 500
    self.update_rectangle() # creates a pygame.Rect object as self.rect attribute

  

  def update_rectangle(self):
    '''
    Updates the player rectangle
    '''
    self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

class Clam:

  def __init__(self,x,y):
    '''
    Initialize the clam and makes it the image of the clam
    '''
    self.w = 25
    self.h = 25
    self.x = x
    self.y = y
    self.update_clam()
    self.visible = True


    self.image = pygame.image.load('clam.gif')
    self.image = pygame.transform.scale( self.image , (self.w,self.h) )

  def update_clam(self):
    '''
    Update the clam rectangle 
    '''
    self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

# initialize pygame and set up the screen
pygame.init()
screen = pygame.display.set_mode( (screen_width,screen_height) )

# initialize the clock and font objects
clock = pygame.time.Clock()
font  = pygame.font.SysFont('Arial',14)
player = Player() # initialize player
wave = Wave() #initialize the wave

#initialize the clams
nclams=10
clams=[]
for i in range(nclams):
  x = random.randint( screen_width//2 , screen_width - 50)
  y = random.randint( 0 , screen_height - 50 )
  clam = Clam(x,y)
  clams.append(clam)

# initialize some variables to keep track of time
FPS  = 60
dt   = 1/FPS
time = 0
NumberofClams = 0

#game loop
while True:
    
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    print('quit the game!')
    break
  
  if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_RIGHT:
      player.x += 50
    if event.key == pygame.K_LEFT:
      player.x -= 50
    if event.key == pygame.K_DOWN:
      player.y += 50
    if event.key == pygame.K_UP:
      player.y -= 50

  #make the wave move back and forth
  wave.x = (0.75 * screen_width)- (0.25 * screen_width) * (math.sin(time))

  #deal with collision of wave and player
  collision = False

  if player.rect.colliderect(wave.rect) == 1:
    collision = True
  
  if collision == True:
    print('bruh, watch out fo da wave')
    break

  # clear the screen
  screen.fill( (255,255,255) )
  
  # draw the player as piper
  player.update_rectangle()
  screen.blit( player.image , (player.x,player.y) )

  #draw clams
  for clam in clams:
    if clam.visible == True:
      screen.blit(clam.image, (clam.x, clam.y))

  #draw wave as a blue rectangle
  wave.update_rectangle()
  pygame.draw.rect(screen, (0,200,230), wave.rect)
  
  #regenerate the clams after each wave 
  newclams = [] # list of clams
  if wave.x < 250.005:
    for clam in clams:
      # create new box object
      x = random.randint( screen_width//2 , screen_width - 50)
      y = random.randint( 0 , screen_height - 50 )
      clam = Clam(x,y)
      newclams.append(clam)
    clams=newclams

  #Collision of clams and player and adding scores
  for clam in clams:
    if clam.rect.colliderect(player.rect) == 1:
      print('ay, you got a clam')
      clam.visible = False
      clam.x = 1000
      clam.y = 1000
      clam.update_clam()
      NumberofClams += 1

  # update time
  time = time + dt
  score = NumberofClams / time

  # draw the time and score 95% down the screen height
  text = font.render( 'time = ' + str(round(time,1)) + ' seconds' + '   Clams = ' + str(NumberofClams),True,(0,0,0) )
  screen.blit( text , (10,0.95*screen_height) )
  
  pygame.display.update()
  clock.tick(FPS) # force pygame to update at desired FPS
  
print('game over!')
print('Score = ' + str(score))
print('you got '+ str(NumberofClams) + ' clams')
pygame.quit()
