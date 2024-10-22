from Constants import *
from instrument import *
from Button import Button
from game import Game



class FindTheNote(Game) :
    def __init__(self, difficulty = Difficulty.EASY) :
        Game.__init__(self, difficulty=difficulty, fretboard_top=175)
        #Game
        self.note_to_find = None

        #Graphics
        self.text_rule = Text("Quelle est cette note ?")
        self.text_success = Text("Bien joué !")
        self.text_failure = Text("Raté...")
        
        #Buttons
        self.do_button = Button(DO_BUTTON_IMAGE, DO_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Do))
        #self.dod_button = Button(DOD_BUTTON_IMAGE, DOD_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Do, Modifiers.Diese))
        self.re_button = Button(RE_BUTTON_IMAGE, RE_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Re))
        #self.red_button = Button(RED_BUTTON_IMAGE, RED_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Re, Modifiers.Diese))
        self.mi_button = Button(MI_BUTTON_IMAGE, MI_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Mi))
        self.fa_button = Button(FA_BUTTON_IMAGE, FA_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Fa))
        #self.fad_button = Button(FAD_BUTTON_IMAGE, FAD_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Fa, Modifiers.Diese))
        self.sol_button = Button(SOL_BUTTON_IMAGE, SOL_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Sol))
        #self.sold_button = Button(SOLD_BUTTON_IMAGE, SOLD_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Sol, Modifiers.Diese))
        self.la_button = Button(LA_BUTTON_IMAGE, LA_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.La))
        #self.lad_button = Button(LAD_BUTTON_IMAGE, LAD_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.La, Modifiers.Diese))
        self.si_button = Button(SI_BUTTON_IMAGE, SI_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Si))

    def start() :
        state = States.FIND_THE_NOTE
        game_instance = FindTheNote()
        game_instance.start_round()
        while state == game_instance.get_supposed_state() :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                elif event.type == pygame.KEYDOWN and event.key == 27 :
                    return States.HOME
                else :
                    state = game_instance.manage_event(event)
                    pass
            game_instance.display()
            pygame.display.update()
        return state
        

    def start_round(self) :
        Game.start_round(self)
        allow_modifiers = self.difficulty==Difficulty.HARD
        self.note_to_find = self.fretboard.select_random(allow_modifiers).note

    def guess(self, note) :
        if note == self.note_to_find :
            self.won_rounds += 1
            self.game_state = InGameState.SUCCESS
        else :
            self.game_state = InGameState.FAILURE
        return States.FIND_THE_NOTE 

    def manage_play(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.do_button.is_selected() :
                self.guess(Note(NotesFrancais.Do))
            elif self.re_button.is_selected() :
                self.guess(Note(NotesFrancais.Re))
            elif self.mi_button.is_selected() :
                self.guess(Note(NotesFrancais.Mi))
            elif self.fa_button.is_selected() :
                self.guess(Note(NotesFrancais.Fa))
            elif self.sol_button.is_selected() :
                self.guess(Note(NotesFrancais.Sol))
            elif self.la_button.is_selected() :
                self.guess(Note(NotesFrancais.La))
            elif self.si_button.is_selected() :
                self.guess(Note(NotesFrancais.Si))
        return Game.manage_play(self, event)

    def display_play(self) :
        self.text_rule.write()
        self.fretboard.draw(write_question_mark=True)
        self.draw_buttons()
    def display_success(self) :
        self.text_success.write()
        self.fretboard.draw(write_selected_notes=True)
    def display_failure(self) :
        self.text_failure.write()
        self.fretboard.draw(write_selected_notes=True)

    def get_supposed_state(self) :
        return States.FIND_THE_NOTE

    def draw_buttons(self, hard_mode = False, spacing = BASIC_SHIFT) :
        height, width = -spacing, -spacing #Pour compenser le fait qu'on ne veuille pas ajouter d'espace inter-bouton à la première itération
        if not(hard_mode) :
            button_list = [[self.do_button, self.re_button, self.mi_button, self.fa_button],[self.sol_button, self.la_button, self.si_button]]
            line_widths = []
            for line in button_list :
                height += spacing+line[0].rect.height
                for button in line :
                    width += spacing+button.rect.width
                line_widths.append(width)
                width = -spacing
            for line_width in line_widths :
                width = max(line_width, width)
            total_rect = pygame.Rect(0, 0, width, height)
            total_rect.centerx = pygame.display.get_surface().get_rect().centerx
            total_rect.bottom = pygame.display.get_surface().get_rect().bottom - BASIC_SHIFT
            (x,y) = total_rect.topleft
            for line_index in range(len(button_list)) :
                line = button_list[line_index]
                line_rect = pygame.Rect(x, y, line_widths[line_index], line[0].rect.height)
                line_rect.centerx = pygame.display.get_surface().get_rect().centerx
                x = line_rect.left
                for button in line :
                    button.rect.topleft = (x,y)
                    x += spacing + button.rect.width
                    button.draw()
                x = total_rect.left
                y += spacing + button.rect.height

DO_BUTTON_IMAGE = load_image("src/ressources/images/do_button.png", BUTTON_SCALING)
DO_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/do_button_hovered.png", BUTTON_SCALING)
#DOD_BUTTON_IMAGE = load_image("", BUTTON_SCALING)
#DOD_BUTTON_HOVERED_IMAGE = load_image("", BUTTON_SCALING)
RE_BUTTON_IMAGE = load_image("src/ressources/images/re_button.png", BUTTON_SCALING)
RE_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/re_button_hovered.png", BUTTON_SCALING)
#RED_BUTTON_IMAGE = load_image("", BUTTON_SCALING)
#RED_BUTTON_HOVERED_IMAGE = load_image("", BUTTON_SCALING)
MI_BUTTON_IMAGE = load_image("src/ressources/images/mi_button.png", BUTTON_SCALING)
MI_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/mi_button_hovered.png", BUTTON_SCALING)
FA_BUTTON_IMAGE = load_image("src/ressources/images/fa_button.png", BUTTON_SCALING)
FA_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/fa_button_hovered.png", BUTTON_SCALING)
#FAD_BUTTON_IMAGE = load_image("", BUTTON_SCALING)
#FAD_BUTTON_HOVERED_IMAGE = load_image("", BUTTON_SCALING)
SOL_BUTTON_IMAGE = load_image("src/ressources/images/sol_button.png", BUTTON_SCALING)
SOL_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/sol_button_hovered.png", BUTTON_SCALING)
#SOLD_BUTTON_IMAGE = load_image("", BUTTON_SCALING)
#SOLD_BUTTON_HOVERED_IMAGE = load_image("", BUTTON_SCALING)
LA_BUTTON_IMAGE = load_image("src/ressources/images/la_button.png", BUTTON_SCALING)
LA_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/la_button_hovered.png", BUTTON_SCALING)
#LAD_BUTTON_IMAGE = load_image("", BUTTON_SCALING)
#LAD_BUTTON_HOVERED_IMAGE = load_image("", BUTTON_SCALING)
SI_BUTTON_IMAGE = load_image("src/ressources/images/si_button.png", BUTTON_SCALING)
SI_BUTTON_HOVERED_IMAGE = load_image("src/ressources/images/si_button_hovered.png", BUTTON_SCALING)