import shelve
saver = shelve.open('score.txt')  # here you will save the score variable   
#saver['score'] = [(10, 2), (10, 100), (9, 1)]            # thats all, now it is saved on disk.
#saver.close()

score = saver['score']
saver.close()

print(score)