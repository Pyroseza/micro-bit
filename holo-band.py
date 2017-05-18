import microbit as mb
#import collections as collects
import music as ms
    
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

    def __init__(self):
        self.all_meals.append({'name': 'Burger', 'calories': 580})
        self.all_meals.append({'name': 'Slice of Pizza', 'calories': 70})
        self.all_meals.append({'name': 'Apple', 'calories': 30})
        self.all_meals.append({'name': 'Chicken Salad', 'calories': 170})
        self.all_meals.append({'name': 'Banana', 'calories': 50})
        self.all_meals.append({'name': 'Chocolate', 'calories': 800})
        self.all_meals.append({'name': 'Health wrap', 'calories': 130})
        return

    def updateValues(self):
        #10,000 steps per day to burn 500 calories
        #for every 20 steps = 1 calorie burnt 
        self.calories_burnt = int(self.steps * (1 / 20))
        #calculate how many calories are allowed now
        self.calories_allowed = self.calories_allowance_idle + self.calories_burnt

    def checkAllowedMeals(self):
        #update values used in the calculations
        self.updateValues()
        #clear the allowed list
        self.allowed_meals = []
        #loop through all meals
        for meal in self.all_meals:
            #check what can be consumed does not go over the calory limit
            if (meal['calories'] <= (self.calories_allowed - self.calories_consumed)):
                self.allowed_meals.append(meal)

    def nom(self, index, meal):
        while True:
            mb.display.scroll(str(index+1) + '. ' + meal['name'])
            mb.display.scroll('A: next, B: exit, A+B: eat')
            if mb.button_a.is_pressed() and mb.button_b.is_pressed():
                #eat the food!
                self.calories_consumed += meal['calories']
                mb.display.scroll('Yum!')
                mb.display.show(mb.Image.PACMAN)
                mb.sleep(500)
                #jump out the menu
                self.stay_in_menu = False
                break
            elif mb.button_a.is_pressed():                
                break
            elif mb.button_b.is_pressed():
                self.stay_in_menu = False
                break
            mb.sleep(10)
    
    def checkGoals(self):
        #check for big victory every 5000 steps
        if (self.steps % 5000 == 0):
            ms.play(ms.PYTHON,wait=False)
            mb.display.show(mb.Image.HAPPY)
            mb.sleep(500)
            mb.display.show(mb.Image.TARGET)
            mb.sleep(500)
            mb.display.show(mb.Image.YES)
            mb.sleep(500)
            mb.display.show(mb.Image.HAPPY)
            mb.sleep(500)
            mb.display.show(mb.Image.TARGET)
            mb.sleep(500)
            mb.display.show(mb.Image.YES)
            mb.sleep(500)
            mb.display.clear()
        elif (self.steps % 1000 == 0):
            #small victory for every 1000 steps
            mb.display.scroll(str(self.steps) + ' steps!')
            ms.play(ms.ENTERTAINER,wait=False)
            mb.display.show(mb.Image.HAPPY)
            mb.sleep(500)
            mb.display.show(mb.Image.TARGET)
            mb.sleep(500)
            mb.display.show(mb.Image.YES)    
            mb.sleep(500)        
            mb.display.clear()

    def main(self):
        while True:
            if mb.accelerometer.was_gesture('shake'):
                self.steps += 1
                self.checkGoals()
            if mb.button_a.is_pressed():
                #update values used in the calculations
                self.updateValues()
                mb.display.scroll('Steps: ' + str(self.steps))
                mb.display.scroll('Calories: ' + str(self.calories_consumed) + '/' + str(self.calories_allowed))
            elif mb.button_b.is_pressed():            
                #check what meals are allowed
                self.checkAllowedMeals()
                for index, meal in enumerate(self.allowed_meals):
                    if (self.stay_in_menu == True):
                        #show mini menu for single meal
                        self.nom(index, meal)
                    else:
                        #jump out entirely
                        self.stay_in_menu = True
                        break
            mb.sleep(100)
        
if __name__=='__main__':
    app = Stepper()
    app.main()
