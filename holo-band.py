import microbit as mb
import collections as collects
    
class Stepper():
    steps = 0
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
        self.calories_burnt = self.steps * 150
        self.calories_allowed = self.calories_allowance_idle + self.calories_burnt

    def checkAllowedMeals(self):
        self.allowed_meals = []
        for meal in self.all_meals:
            if (meal['calories'] <= (self.calories_allowed - self.calories_consumed)):
                self.allowed_meals.append(meal)

    def nom(self):
        while True:
            mb.display.scroll(str(index+1) + '. ' + meal['name'])
            mb.display.scroll('A: next, B: exit, A+B: eat')
            if mb.button_a.is_pressed() and mb.button_b.is_pressed():
                self.calories_consumed += meal['calories']
                mb.display.scroll('Yum!')
                self.stay_in_menu = False
                break
            elif mb.button_a.is_pressed():
                break
            elif mb.button_b.is_pressed():
                self.stay_in_menu = False
                break
            mb.sleep(10)

    def main(self):
        while True:
            if mb.accelerometer.was_gesture('shake'):
                self.steps += 1         
            if mb.button_a.is_pressed():
                self.updateValues()
                mb.display.scroll('Steps: ' + str(self.steps))
                mb.display.scroll('Calories: ' + str(self.calories_consumed) + '/' + str(self.calories_allowed))
            elif mb.button_b.is_pressed():
                self.updateValues()
                self.checkAllowedMeals()
                for index, meal in enumerate(self.allowed_meals):
                    if (self.stay_in_menu == True):
                        self.nom()
                    else:
                        self.stay_in_menu = True
                        break
            mb.sleep(100)
        
if __name__=='__main__':
    app = Stepper()
    app.main()
