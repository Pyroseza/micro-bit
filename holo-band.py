from microbit import *
from collections import *

steps = 0
all_meals = []
allowed_meals = []
calories_allowance_idle = 1500
calories_burnt = 0
calories_consumed = 0
calories_allowed=0
stay_in_menu=True

all_meals.append({'name': 'Burger', 'calories': 580})
all_meals.append({'name': 'Slice of Pizza', 'calories': 70})
all_meals.append({'name': 'Apple', 'calories': 30})
all_meals.append({'name': 'Chicken Salad', 'calories': 170})
all_meals.append({'name': 'Banana', 'calories': 50})
all_meals.append({'name': 'Chocolate', 'calories': 800})
all_meals.append({'name': 'Health wrap', 'calories': 130})

while True:
    if 'shake' in accelerometer.get_gestures():
    #if accelerometer.was_gesture("shake"):
        steps += 10
        calories_burnt = steps * 15
        calories_allowed = (calories_allowance_idle + calories_burnt) - calories_consumed
    if button_a.is_pressed():
        display.scroll(str(calories_consumed) + '/' + str(calories_allowance_idle + calories_burnt))
    elif button_b.is_pressed():
        allowed_meals = []
        for meal in all_meals:
            if (meal['calories'] <= calories_allowed):
                allowed_meals.append(meal)
        for index, meal in enumerate(allowed_meals):
            if (stay_in_menu == True):
                while True:
                    display.scroll(str(index+1) + '. ' + meal['name'])
                    display.scroll('A: next, B: exit, A+B: consume')
                    if button_a.is_pressed() and button_b.is_pressed():
                        calories_consumed += meal['calories']
                        stay_in_menu = False
                        break
                    elif button_a.is_pressed():
                        break
                    elif button_b.is_pressed():
                        stay_in_menu = False
                        break
                    sleep(10)
            else:
                stay_in_menu = True
                break
    sleep(10)
