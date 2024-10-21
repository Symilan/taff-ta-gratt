from Constants import *
import pygame
from Button import Button
import instrument
from Text import *

class HomeState(Enum) :
    HOME = 1
    GAME_CHOICE = 2
class Home :
    def __init__(self) :
        #Buttons
        self.start_button = Button(START_BUTTON_IMAGE, START_BUTTON_HOVERED_IMAGE).center().shift(x = 300, y = -200)
        self.exit_button = Button(EXIT_BUTTON_IMAGE, EXIT_BUTTON_HOVERED_IMAGE).center().shift(x = 300, y = 200)
        self.find_the_notes_button = Button(FIND_THE_NOTE_BUTTON_IMAGE, FIND_THE_NOTE_BUTTON_HOVERED_IMAGE).center().stick_to_left(10)
        self.find_the_frets_button = Button(FIND_THE_FRETS_BUTTON_IMAGE, FIND_THE_FRETS_BUTTON_HOVERED_IMAGE).center().stick_to_right(10)

        #Graphics
        self.fretboard = instrument.FretBoard()
        self.fretboard.select_random()
        self.text_title = Text("Taff ta gratt !!!").stick_to_top(50).centerx()

        #Game
        self.home_state = HomeState.HOME
        
    def start() :
        home = Home()
        state = States.HOME
        while state == States.HOME :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                else :
                    state = home.manage(event)
            home.display()
            pygame.display.update()
        return state

    def manage(self, event) :
        match self.home_state :
            case HomeState.HOME :
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                    if self.start_button.is_selected() :
                        self.home_state = HomeState.GAME_CHOICE
                    elif self.exit_button.is_selected() :
                        return States.KILL
                elif event.type == SECOND_EVENT :
                    self.fretboard.select_random()
            case HomeState.GAME_CHOICE :
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                    if self.find_the_notes_button.is_selected() :
                        return States.FIND_THE_NOTE
                    elif self.find_the_frets_button.is_selected() :
                        return States.FIND_THE_FRETS
                if event.type == pygame.KEYDOWN and event.key == 27 :
                    self.home_state = HomeState.HOME
        return States.HOME

    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        match self.home_state :
            case HomeState.HOME :
                self.text_title.write()
                self.fretboard.draw(write_selected_notes = True)
                self.start_button.draw()
                self.exit_button.draw()
            case HomeState.GAME_CHOICE :
                self.find_the_frets_button.draw()
                self.find_the_notes_button.draw()
                