from Constants import *
from instrument import *
from Button import Button



class FindTheNote :
    def __init__(self) :
        #Game
        self.game_timer = 0
        self.game_state = InGameState.PLAY
        self.note_to_find = None
        self.won_rounds = 0
        self.round = 0
        self.max_rounds = 10

        #Graphics
        self.fretboard = FretBoard()
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
        self.sol_button = Button(SOL_BUTTON_IMAGE, SOL_BUTTON_HOVERED_IMAGE), Note(NotesFrancais.Sol)
        #self.sold_button = Button(SOLD_BUTTON_IMAGE, SOLD_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Sol, Modifiers.Diese))
        self.la_button = Button(LA_BUTTON_IMAGE, LA_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.La))
        #self.lad_button = Button(LAD_BUTTON_IMAGE, LAD_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.La, Modifiers.Diese))
        self.si_button = Button(SI_BUTTON_IMAGE, SI_BUTTON_HOVERED_IMAGE, Note(NotesFrancais.Si))

    def start() :
        state = States.FIND_THE_NOTE
        game_instance = FindTheNote()
        game_instance.start_round()
        while state == States.FIND_THE_NOTE :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                elif event.type == pygame.KEYDOWN and event.key == 27 :
                    return States.HOME
                else :
                    state = game_instance.manage_event(event)

    def start_round(self) :
        self.note_to_find = self.fretboard.select_random()
        round += 1

    def guess(self, note) :
        if note == self.note_to_find :
            score += 1
            self.game_state = InGameState.SUCCESS
        else :
            self.game_state = InGameState.FAILURE
        return States.FIND_THE_NOTE

    def manage_event(self, event) :
        match self.game_state :
            case InGameState.PLAY :
                return self.manage_event_play(event)
            case InGameState.SUCCESS :
                return self.manage_event_success_or_failure(event)
            case InGameState.FAILURE :
                return self.manage_event_success_or_failure(event)
            case InGameState.GAME_OVER :
                return self.manage_event_game_over(event)    

    def manage_event_play(self, event) :
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
        return States.FIND_THE_NOTE

    def manage_event_success_or_failure(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.round < FIND_THE_FRETS_MAX_ROUNDS :
                self.start_round()
                self.game_state = InGameState.PLAY
            else :
                self.game_state = InGameState.GAME_OVER
        return States.FIND_THE_NOTE
            
    def manage_event_game_over(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            return States.HOME
        else : 
            return States.FIND_THE_NOTE

    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        match self.game_state :
            case InGameState.PLAY :
                self.display_play()
            case InGameState.SUCCESS :
                self.display_success()
            case InGameState.FAILURE :
                self.display_failure()
            case InGameState.GAME_OVER :
                self.display_game_over()

    def display_play(self) :
        self.fretboard.draw()
    def display_success(self) :
        self.fretboard.draw(write_selected_notes=True)
    def display_failure(self) :
        self.fretboard.draw(write_selected_notes=True)
    def display_game_over(self) :
        pass

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