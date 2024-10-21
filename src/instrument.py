import pygame
from Constants import *
from Text import Text
from Note import *

STRINGS = 6
FRETS = 6

EMPTY_STRINGS = [
    Note(NotesFrancais.Mi),
    Note(NotesFrancais.Si),
    Note(NotesFrancais.Sol),
    Note(NotesFrancais.Re),
    Note(NotesFrancais.La),
    Note(NotesFrancais.Mi)
]

class Fret :
    def __init__(self,string, fret, rect, note, is_selected=False) :
        self.is_selected = is_selected
        self.rect = rect
        self.string = string
        self.fret = fret
        self.note = note
        
    def is_hovered(self) :
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def draw(self, draw_hovered=False, write_notes=False, write_selected_note=False) :
        if (self.is_hovered() and draw_hovered) or self.is_selected :
            pygame.display.get_surface().blit(FRET_BUTTON_IMAGE, self.rect.topleft)
            if write_selected_note :
                Text(str(self.note), color=WHITE).center_on_rect(self.rect).write()
        if write_notes :
            Text(str(self.note), color=WHITE).center_on_rect(self.rect).write()

class String :
    def __init__(self) :
        self.frets = []
        
class FretBoard :
    def __init__(self, startingFret = 0) :
        self.set_starting_fret = startingFret
        self.image = FRETBOARD_5_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = pygame.display.get_surface().get_rect().centerx
        self.rect.top = 175
        self.strings = []
        self.show_notes = False
        for stringNumber in range(STRINGS) :
            note_to_add = EMPTY_STRINGS[stringNumber] #TODO : add startingFret
            string = String()
            for fretNumber in range(FRETS) :
                fretRect = pygame.Rect(
                    self.rect.left + (((self.rect.width-FRETBOARD_SCALING)/FRETS)*fretNumber),
                    self.rect.top + (((self.rect.height+FRETBOARD_SCALING)/STRINGS)*stringNumber),
                    self.rect.width/FRETS,
                    self.rect.height/STRINGS
                )
                fret = Fret(stringNumber, fretNumber, fretRect, note_to_add)
                string.frets.append(fret)
                note_to_add = note_to_add.get_next()
            self.strings.append(string)
    
    def select_random(self) :
        self.empty()
        random_fret = choice(choice(self.strings).frets)
        random_fret.is_selected = True
        return random_fret

    def set_starting_fret(self, startingFret) :
        self.startingFret = startingFret
        def set_frets(string) :
            pass
        for string in self.strings :
            set_frets(string, startingFret)
        return self

    def draw(self, draw_hovered_frets=False, write_selected_notes=False) :
        pygame.display.get_surface().blit(self.image, self.rect.topleft)
        for string in self.strings :
            for fret in string.frets :
                fret.draw(
                    draw_hovered=draw_hovered_frets, 
                    write_notes=self.show_notes,
                    write_selected_note=write_selected_notes
                    )

    def empty(self) -> object:
        for string in self.strings :
            for fret in string.frets :
                fret.is_selected = False
        return self

    def check_all(self, note) -> object:
        for string in self.strings :
            for fret in string.frets :
                if fret.note == note :
                    fret.is_selected = True
        return self

    def fret(self, stringNumber, fretNumber) :
        return self.strings[stringNumber, fretNumber]
    
    def has_one_selection(self) :
        for string in self.strings :
            for fret in string.frets :
                if fret.is_selected :
                    return True
        return False
    
    def selected_frets(self) :
        selected_frets = []
        for string in self.strings :
            for fret in string.frets :
                if fret.is_selected :
                    selected_frets.append(fret)
        return selected_frets

    def selected_notes(self) :
        selected_notes = []
        for fret in self.selected_frets() :
            selected_notes.append(fret.note)
        return selected_notes
    
    def selection_is_correct(self, note) :
        for string in self.strings :
            for fret in string.frets :
                if fret.note == note :
                    if not(fret.is_selected) :
                        return False
                else :
                    if fret.is_selected :
                        return False
        return True