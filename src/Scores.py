import shelve
import os
from Constants import *

class Highscores :
    def __init__(self, key):
        self.key = key.name
        self.list = []
        if not(os.path.exists("data")) :
            os.mkdir("data")
        reader = shelve.open(HIGHSCORES_FILE)
        if self.key in reader :
            self.list = reader[self.key]
        reader.close()

    def save(self) :
        saver = shelve.open(HIGHSCORES_FILE)
        saver[self.key] = self.list
        saver.close()

    #Ajoute le score aux highscores si nécessaire et renvoie l'indice auquel il a été inséré (-1 si non inséré)
    def add(self, score) -> int :
        if len(self.list) <= 2 :
            self.list.append(score)
        elif score >= self.list[-1] :
            self.list[-1] = score
        else :
            return -1
        self.list.sort(reverse=True)
        self.save()
        return self.list.index(score)

class Score :
    def __init__(self, rounds, time):
        self.rounds = rounds
        self.time = time

    def __eq__(self, value) -> bool:
        if value == None :
            return False
        else :
            return ((self.rounds == value.rounds) and (self.time == value.time))
        
    def __lt__(self, value) :
        if self.rounds == value.rounds :
            return self.time > value.time
        else :
            return self.rounds < value.rounds

    def __le__(self, value) :
        return (self<value or self==value)

    def __gt__(self, value) :
        return not(self<=value)
    
    def __ge__(self, value) :
        return not(self<value)
    
    def __str__(self):
        return "Rounds gagnés : "+str(self.rounds)+". Temps : "+str(self.time)+" secondes." 