from enum import Enum
from random import choice
from Constants import *

class Modifiers(Enum) :
    Empty = 0
    Diese = 1
    Bemol = 2

#Enums
class NotesAnglais(Enum) :
    C = 0
    D = 1
    E = 2
    F = 3
    G = 4
    A = 5
    B = 6

class NotesFrancais(Enum) :
    Do = 0
    Re = 1
    Mi = 2
    Fa = 3
    Sol = 4
    La = 5
    Si = 6

class Note :
    def random() -> object:
        noteAliases = choice(suiteNotes)
        note = choice(noteAliases)
        return note
    
    def random_easy() -> object:
        note = choice(choice(suiteNotes))
        while note.modifier != Modifiers.Empty :
            note = choice(choice(suiteNotes))
        return note

    def index(self) :
        for notes in suiteNotes :
            for note in notes:
                if note == self :
                    return notes.index(note)
        return None

    def __init__(self, name, modifier = Modifiers.Empty) :
        self.name = name
        self.modifier = modifier

    def get_note_francais(self) -> NotesFrancais:
        return (NotesFrancais(self.name.value), self.Modifiers)
    
    def get_next(self) -> object:
        for i in range(len(suiteNotes)) :
            for note_alias in suiteNotes[i] :
                if note_alias == self :
                    next_index = (i+1)%len(suiteNotes)
                    next_note = suiteNotes[next_index]
                    return choice(next_note)


    def __eq__(self, note: object) -> bool:
        if not(isinstance(note, Note)) :
            return False
        for noteAliases in suiteNotes :
            containsSelf = False
            containsNote = False
            for noteAlias in noteAliases :
                if (noteAlias.name.value == self.name.value) and (noteAlias.modifier == self.modifier) :
                    containsSelf = True
                if (noteAlias.name.value == note.name.value) and (noteAlias.modifier == note.modifier) :
                    containsNote = True
            if containsNote and containsSelf :
                return True
        return False
    
    def __str__(self) -> str:
        string_to_return = self.name.name
        if self.modifier == Modifiers.Bemol :
            string_to_return += "b"
        elif self.modifier == Modifiers.Diese :
            string_to_return += "#"
        return string_to_return
    
#Constantes
suiteNotes = [
    [Note(NotesFrancais.Do)],
    [Note(NotesFrancais.Do, Modifiers.Diese),Note(NotesFrancais.Re, Modifiers.Bemol)],
    [Note(NotesFrancais.Re)],
    [Note(NotesFrancais.Re, Modifiers.Diese),Note(NotesFrancais.Mi, Modifiers.Bemol)],
    [Note(NotesFrancais.Mi)],
    [Note(NotesFrancais.Fa)],
    [Note(NotesFrancais.Fa, Modifiers.Diese),Note(NotesFrancais.Sol, Modifiers.Bemol)],
    [Note(NotesFrancais.Sol)],
    [Note(NotesFrancais.Sol, Modifiers.Diese),Note(NotesFrancais.La, Modifiers.Bemol)],
    [Note(NotesFrancais.La)],
    [Note(NotesFrancais.La, Modifiers.Diese),Note(NotesFrancais.Si, Modifiers.Bemol)],
    [Note(NotesFrancais.Si)]
]