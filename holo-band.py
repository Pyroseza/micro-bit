import microbit as mb
import music

class Stepper():
    #steps = 0
    #make steps 4999 for testing
    steps = 4999
    shakes_since_last_check = 0
    calories_allowance_idle = 1500
    calories_burnt = 0
    calories_consumed = 0
    calories_allowed = 0
    all_meals = []
    stay_in_menu = True
    sleepInterval = 100
    #milliseconds = 0
    #make milliseconds 37200000 (time=10:20:00) for testing
    milliseconds = 37200000
    seconds = 0
    minutes = 0
    hours = 0
    secondsText = ''
    minutesText = ''
    hoursText = ''
    showAnimMain = True

    def __init__(self):
        self.all_meals.append({'name': 'Apple', 'KCal': 30})
        self.all_meals.append({'name': 'Banana', 'KCal': 50})
        self.all_meals.append({'name': 'Slice of Pizza', 'KCal': 70})
        self.all_meals.append({'name': 'Health wrap', 'KCal': 130})
        self.all_meals.append({'name': 'Chicken Salad', 'KCal': 170})
        self.all_meals.append({'name': 'Burger', 'KCal': 580})
        self.all_meals.append({'name': 'Chocolate', 'KCal': 800})
        return

    def updateValues(self):
        #10,000 steps per day to burn 500 calories
        #for every 20 steps = 1 calorie burnt 
        self.calories_burnt = int(self.steps * (1 / 20))
        #calculate how many calories are allowed now
        self.calories_allowed = self.calories_allowance_idle + self.calories_burnt
        return

    def checkAllowedMeals(self):
        #update values used in the calculations
        self.updateValues()
        #clear the allowed list
        self.allowed_meals = []
        #loop through all meals
        for meal in self.all_meals:
            #check what can be consumed does not go over the calory limit
            if (meal['KCal'] <= (self.calories_allowed - self.calories_consumed)):
                self.allowed_meals.append(meal)
        return

    def nom(self, index, meal):
        while True:
            mb.display.scroll(str(index+1) + '. ' + meal['name'])
            #mb.display.scroll('A: next, B: exit, A+B: eat')
            if mb.button_a.was_pressed() and mb.button_b.was_pressed():
                #eat the food!
                self.calories_consumed += meal['KCal']
                mb.display.scroll('Yum!')
                mb.display.show(mb.Image.PACMAN)
                self.snooze(self.sleepInterval * 5)
                #jump out the menu
                self.stay_in_menu = False
                break
            elif mb.button_a.was_pressed():
                break
            elif mb.button_b.was_pressed():
                self.stay_in_menu = False
                break
            self.snooze(self.sleepInterval)
        return
        
    def animMain(self, animLength):
        dotImage = mb.Image("00000:"
                            "00000:"
                            "00900:"
                            "00000:"
                            "00000")
        animLength = min(5, max(animLength, 1))
        mb.display.show(mb.Image.HAPPY)
        self.snooze(self.sleepInterval * 5)
        mb.display.show(mb.Image.HEART)
        self.snooze(self.sleepInterval * 5)
        for i in range(1,animLength):
            mb.display.show(mb.Image.DIAMOND)
            self.snooze(self.sleepInterval)
            mb.display.show(mb.Image.SQUARE)
            self.snooze(self.sleepInterval)
            mb.display.show(mb.Image.DIAMOND_SMALL)
            self.snooze(self.sleepInterval)
            mb.display.show(mb.Image.SQUARE_SMALL)
            self.snooze(self.sleepInterval)
            mb.display.show(dotImage)
            self.snooze(self.sleepInterval)
        mb.display.clear()
        return
    
    def animGoal(self, animLength):
        animLength = min(20, max(animLength, 1))
        for i in range(1,animLength):
            mb.display.show(mb.Image.HAPPY)
            self.snooze(self.sleepInterval * 5)
            mb.display.show(mb.Image.TARGET)
            self.snooze(self.sleepInterval * 5)
            mb.display.show(mb.Image.YES)
            self.snooze(self.sleepInterval * 5)
        mb.display.clear()
        return
        
    def checkGoals(self):
        #check for big victory every 5000 steps
        if (self.steps % 5000 == 0):
            music.play(music.PYTHON,wait=False)
            self.animGoal(9)
        elif (self.steps % 1000 == 0):
            #small victory for every 1000 steps
            mb.display.scroll(str(self.steps) + ' steps!')
            music.play(music.ENTERTAINER,wait=False)
            self.animGoal(9)

    def increaseTimeElapsed(self, tick):
        self.milliseconds += tick
            
    def snooze(self,timeToSnooze):
        mb.sleep(timeToSnooze)
        self.increaseTimeElapsed(timeToSnooze)

    def main(self):
        while True:
            
            if (self.showAnimMain == True):
                self.animMain(10)
                self.showAnimMain = False
                
            if mb.accelerometer.was_gesture('shake'):
                self.steps += 1
                self.checkGoals()
                
            if mb.button_a.was_pressed() and mb.button_b.was_pressed():
                #check what meals are allowed
                self.checkAllowedMeals()
                for index, meal in enumerate(self.allowed_meals):
                    if (self.stay_in_menu == True):
                        #show mini menu for single meal
                        self.nom(index, meal)
                    else:
                        self.stay_in_menu = True
                        #jump out entirely
                        break
                self.showAnimMain = True

            if mb.button_a.is_pressed():
                #update values used in the calculations
                #self.updateValues()
                mb.display.scroll('KCal: ' + str(self.calories_consumed) + '/' + str(self.calories_allowed))
                mb.display.scroll('Steps: ' + str(self.steps))
                self.showAnimMain = True

            if mb.button_b.is_pressed():
                #show a clock face for 50ms and then the "time"
                mb.display.show(mb.Image.ALL_CLOCKS,(self.sleepInterval//2),wait=True, loop=False, clear=True)
                self.increaseTimeElapsed(self.sleepInterval//2)
                self.seconds = self.milliseconds // 1000
                self.minutes = ((self.seconds % 3600) // 60)
                self.minutesText = ('0' if self.minutes < 10 else '') + str(self.minutes)
                self.hours = (self.seconds // 3600)
                self.hoursText = ('0' if self.hours < 10 else '') + str(self.hours)
                self.seconds = (self.seconds - (self.hours * 3600) - (self.minutes * 60))
                self.secondsText = ('0' if self.seconds < 10 else '') + str(self.seconds)
                mb.display.scroll(self.hoursText + ':' + self.minutesText + ':' + self.secondsText)
                self.showAnimMain = True
            self.snooze(self.sleepInterval)
        
if __name__=='__main__':
    app = Stepper()
    app.main()
