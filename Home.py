from Constants import *
import pygame
from Button import Button
from FretBoard import *

class Home :
    def __init__(self) :
        self.start_button = Button(START_BUTTON_IMAGE, START_BUTTON_HOVERED_IMAGE)
        self.exit_button = Button(EXIT_BUTTON_IMAGE, EXIT_BUTTON_HOVERED_IMAGE)
        self.start_button.center().shift(x = 300, y = -200)
        self.exit_button.center().shift(x = 300, y = 200)
        self.fretboard = FretBoard().select_random()
        self.text_title = Text("Taff ta gratt !!!").stick_to_top(50).centerx()

    def start() :
        home = Home()
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                    if home.start_button.is_selected() :
                        return States.FIND_THE_NOTE
                    if home.exit_button.is_selected() :
                        return States.KILL
                elif event.type == TIMER_EVENT :
                    home.fretboard.select_random()

            home.display()
            pygame.display.update()

    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        self.text_title.write()
        self.fretboard.draw(write_selected_notes=True)
        self.start_button.draw()
        self.exit_button.draw()