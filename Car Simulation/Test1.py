import array # imports the array class to use for the stacks
import pygame
import time

pygame.init()

(width, height) = (1000,1000)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()


# tank object

class Tank():  # every variable that will be store on the tank itself will be stored here. 
    def __init__(self, width, height, dimen1 = 60, dimen2 = 80, rotation=0) -> None:
        #place the tank in the centre of the screen
        self.posX = width/2
        self.posY = height/2

        #defines the dimensions of the tank
        self.length = dimen1
        self.height = dimen2

        self.rotation = rotation # 

    def draw(self, surface): # call this to draw the tank 
        pygame.draw.rect(surface, (0,100,0), pygame.Rect(self.posX-0.5*(self.length), self.posY-0.5*(self.height), self.length, self.height))

    def search(): # the simple search algorithm (Left free, Right free, Turn either 90, -90 or 180)
        pass

    
## set up the sections of the sreen as an array

screen_array = []
    
for i in range(width):
    for j in range(height):
        


## main loop

myTank = Tank(width, height)

running = True
while running:
    time.sleep(1/60) # limits refresh rate
    screen.fill((255,255,255))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    myTank.draw(screen)

        
    

    pygame.display.flip()