import music
import random

#letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
letters = ["B", "C", "D", "E"]
#numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
numbersLow = ["0", "1", "2"]
numbersHigh = ["3", "4", "5"]

def main():
    while True:
        note = str(random.choice(letters)) + str(random.choice(numbersHigh)) + ":" + str(random.choice(numbersLow))
        music.play(note)
        
if __name__ == "__main__":
    main()
