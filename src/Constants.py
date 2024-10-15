from enum import Enum
from utils import load_image
import pygame

class States(Enum) :
    KILL = 1
    HOME = 2
    FIND_THE_NOTE = 3

class FindTheNoteState(Enum) :
    PLAY = 1
    SUCCESS = 2
    FAILURE = 3
    GAME_OVER = 4

class Difficulty(Enum) :
    EASY = 1
    HARD = 2

SECOND_EVENT = pygame.USEREVENT+1
TENTHSECOND_EVENT = pygame.USEREVENT+2

FIND_THE_NOTE_MAX_ROUNDS = 10

SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1366
BROWN = (130, 20, 0)
GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (215, 0, 0)

BUTTON_SCALING = 6
FRETBOARD_SCALING = 10
START_EXIT_BUTTON_HEIGHT = 500
QUESTION_COORDINATES = (20,20)
BASIC_SHIFT = 20

EASY_BUTTON_IMAGE = load_image("src/ressources/images/easy_button.png", BUTTON_SCALING)
EASY_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/easy_button_hovered.png", BUTTON_SCALING)

HARD_BUTTON_IMAGE =load_image("src/ressources/images/hard_button.png", BUTTON_SCALING)
HARD_BUTTON_HOVERED_IMAGE =load_image("src/ressources/images/hard_button_hovered.png", BUTTON_SCALING)

VALIDATE_BUTTON_IMAGE = load_image("src/ressources/images/validate_button.png", BUTTON_SCALING)
VALIDATE_BUTTON_GREYED_IMAGE = load_image("src/ressources/images/validate_button_greyed.png", BUTTON_SCALING)
VALIDATE_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/validate_button_hovered.png", BUTTON_SCALING)

START_BUTTON_IMAGE = load_image("src/ressources/images/start_button.png", BUTTON_SCALING)
START_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/start_button_hovered.png", BUTTON_SCALING)

EXIT_BUTTON_IMAGE = load_image("src/ressources/images/exit_button.png", BUTTON_SCALING)
EXIT_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/exit_button_hovered.png", BUTTON_SCALING)

FRETBOARD_IMAGE = load_image("src/ressources/images/guitar_fretboard.png", FRETBOARD_SCALING)

FRET_BUTTON_IMAGE = load_image("src/ressources/images/fret_button.png", FRETBOARD_SCALING)

HIGHSCORES_FILE = "data/highscores.txt"