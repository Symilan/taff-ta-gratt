import pygame
from Home import Home
from FindTheFrets import FindTheFrets
#from FindTheNote import FindTheNote
from Constants import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Taff ta Gratt")
state = States.HOME
pygame.time.set_timer(SECOND_EVENT, 1000)
pygame.time.set_timer(TENTHSECOND_EVENT, 100)

while state != States.KILL :
    if state == States.HOME :
        state = Home.start()
    if state == States.FIND_THE_FRETS :
        state = FindTheFrets.start()
#    if state == States.FIND_THE_NOTE :
#        state = FindTheNote.start()

pygame.quit()