import microbit
import music
import random

#letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
letters = ["B", "C", "D", "E"]
#numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
numbersLow = ["0", "1", "2"]
numbersHigh = ["3", "4", "5"]

def main():
    dots = [ [0]*5, [0]*5, [0]*5, [0]*5, [0]*5 ]
    while True:
        dots[random.randrange(5)][random.randrange(5)] = 8
        for i in range(5):
            for j in range(5):
                microbit.display.set_pixel(i, j, dots[i][j])
                dots[i][j] = max(dots[i][j] - 1, 0)
        #microbit.sleep(10)
        note = str(random.choice(letters)) + str(random.choice(numbersHigh)) + ":" + str(random.choice(numbersLow))
        music.play(note)
  
if __name__ == "__main__":
    main()
