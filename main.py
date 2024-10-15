import pygame
from Home import *
from FindTheNote import *
from Constants import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Taff ta Gratt")
state = States.HOME
pygame.time.set_timer(TIMER_EVENT, 1000)

while state != States.KILL :
    if state == States.HOME :
        state = Home.start()
    if state == States.FIND_THE_NOTE :
        state = FindTheNote.start()

pygame.quit()