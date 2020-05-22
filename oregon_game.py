# -*- coding: utf-8 -*-
"""

"""
# Simulation game of traveling out west in 1800's

import random

welcome_text = """
Welcome to the Oregon Trail! The year is 1850 and Americans are
headed out West to populate the frontier. Your goal is to travel
by wagon train from Independence, MO to Oregon (2000 miles). You start
on March 1st, and your goal is to reach Oregon by December 31st.
The trail is arduous. Each day costs you food and health. You
can hunt and rest, but you have to get there before winter!
"""

help_text = """
Each turn you can take one of 3 actions:

  travel - moves you randomly between 30-60 miles and takes
           3-7 days (random).
  rest   - increases health 1 level (up to 5 maximum) and takes
           2-5 days (random).
  hunt   - adds 100 lbs of food and takes 2-5 days (random).

When prompted for an action, you can also enter one of these
commands without using up your turn:

  status - lists food, health, distance traveled, and day.
  help   - lists all the commands.
  quit   - will end the game.
  
You can also use these shortcuts for commands:

  't', 'r', 'h', 's', '?', 'q'
  
"""

good_luck_text = "Good luck, and see you in Oregon!"

# Model -- variables that collectivel represent the state
# of the game
miles_traveled = 0
food_remaining = 500
health_level = 5
month = 3
day = 1
date=""
sicknesses_suffered_this_month = 0
player_name = None
playing = True

# Constants -- parameters that define the rules of the game,
# but which don't change.
MIN_MILES_PER_TRAVEL = 30
MAX_MILES_PER_TRAVEL = 60
MIN_DAYS_PER_TRAVEL = 3
MAX_DAYS_PER_TRAVEL = 7

MIN_DAYS_PER_REST = 2
MAX_DAYS_PER_REST = 5
HEALTH_CHANGE_PER_REST = 1
MAX_HEALTH = 5

FOOD_PER_HUNT = 100
MIN_DAYS_PER_HUNT = 2
MAX_DAYS_PER_HUNT = 5

FOOD_EATEN_PER_DAY = 5
MILES_BETWEEN_NYC_AND_OREGON = 2000
MONTHS_WITH_31_DAYS = [1, 3, 5, 7, 8, 10, 12]
MONTHS_WITH_30_DAYS = [4, 6, 9, 11]
MONTHS_WITH_28_DAYS = [2]

# fake month is added so that January is at index 1
NAME_OF_MONTH = [
    'fake', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]

# Converts are numeric date into a string.
# input: m - a month in the range 1-12
# input: d - a day in the range 1-31
# output: a string like "December 24".
# Note: this function does not enforce calendar rules. It's happy to output
# impossible strings like "June 95" or "February 31"
def date_as_string(m, d):
    global miles_traveled
    if m<13:
        today = str(NAME_OF_MONTH[m])+" "+ str(d)
        return today
    elif(m<12 and miles_traveled>=2000):
        player_wins()
        return ""
    else:
        game_is_over
        return ""


def date_report():
    global day
    global month
    global date
    date = date_as_string(month,day)
    return date

def miles_remaining():
    global miles_traveled
    miles_rem = MILES_BETWEEN_NYC_AND_OREGON - miles_traveled
    print("Miles remaining are: ", miles_rem)
    
# Returns the number of days in the month (28, 30, or 31).
# input: an integer from 1 to 12. 1=January, 2=February, etc.
# output: the number of days in the month. If the input is not in
#   the required range, returns 0.
def days_in_month(m):
    if m in MONTHS_WITH_28_DAYS:
        return 28
    elif m in MONTHS_WITH_30_DAYS:
        return 30
    else:
        return 31

# Calculates whether a sickess occurs on the current day based
# on how many days remain in the month and how many sick days have
# already occured this month. If there are N days left in the month, then
# the chance of a sick day is either 0, 1 out of N, or 2 out of N, depending
# on whether there have been 2 sick days so far, 1 sick day so far, or no
# sick days so far.
#
# This system guarantees that there will be exactly
# 2 sick days each month, and incidentally that every day of the month
# is equally likely to be a sick day (proof left to the reader!)
def random_sickness_occurs():
    global health_level
    global sicknesses_suffered_this_month
    health_level = health_level - 1
    sicknesses_suffered_this_month+=1
    
def handle_sickness():
    global sicknesses_suffered_this_month
    global day
    global month
    global date
    #print("sstm: ", sicknesses_suffered_this_month)
    if sicknesses_suffered_this_month == 0:
        possible_sick_days_rem = 2
    elif sicknesses_suffered_this_month == 1:
        possible_sick_days_rem = 1
    else:
        possible_sick_days_rem = 0
        
    rem_days_month = days_in_month(month) - day
    
    if rem_days_month!=0:
        probability = possible_sick_days_rem / rem_days_month
    else:
        probability = 0
    
    generated_decimal_number = random.uniform(0, 1)
    
    if generated_decimal_number < probability:
        random_sickness_occurs()
        date = date_report()
        print("You got SICK on: ",date)

def consume_food():
    global food_remaining
    food_remaining = food_remaining - FOOD_EATEN_PER_DAY
    
# Repairs problematic values in the global (month, day) model where the day is
# larger than the number of days in the month. If this happens, advances to the next
# month and knocks the day value down accordingly. Knows that different months have
# different numbers of days. Doesn't handle cases where the day is more than 28
# days in excess of the limit for that month -- could still end up with an
# impossible date after this function is called.
#
# Returns True if the global month/day values were altered, else False.
def maybe_rollover_month():
    global day
    global month
    global sicknesses_suffered_this_month
    
    if(month in MONTHS_WITH_28_DAYS and day>28):
        day = day-28
        month += 1
        sicknesses_suffered_this_month=0
    
    if day >= 30:
        if month not in MONTHS_WITH_31_DAYS:
            if day > 30:
                day -= 30
                month += 1
                sicknesses_suffered_this_month=0
        else:
            if day > 31:
                day -= 31
                month += 1
                sicknesses_suffered_this_month=0
                
# Causes a certain number of days to elapse. The days pass one at a time, and each
# day brings with it a random chance of sickness. The sickness rules are quirky: player
# is guaranteed to fall ill a certain number of times each month, so illness
# needs to keep track of month changes.
#
# input: num_days - an integer number of days that elapse.
def advance_game_clock(num_days):
    global day
    global playing
    global miles_traveled
    global food_remaining
    
    if miles_traveled>=2000:
        player_wins()
    elif health_level <= 0:
        game_is_over()
    elif food_remaining <= 0:
        game_is_over()
    elif(month>=12 and miles_traveled>=2000):
        player_wins()
    elif(month==13):
        game_is_over()
    
    for i in range(1,num_days+1):
        day +=1
        consume_food()
        handle_sickness()
    maybe_rollover_month()
    miles_traveled=miles_traveled+num_miles   
    miles_remaining()

def handle_travel():
    global num_days
    global num_miles
    num_days = random.randint(MIN_DAYS_PER_TRAVEL, MAX_DAYS_PER_TRAVEL)
    num_miles = random.randint(MIN_MILES_PER_TRAVEL, MAX_MILES_PER_TRAVEL)
    advance_game_clock(num_days)

def travel():
    handle_travel()
    handle_status()

def handle_rest():
    global num_days
    global num_miles
    global health_level

    num_days = random.randint(MIN_DAYS_PER_REST,MAX_DAYS_PER_REST)
    num_miles=0
    advance_game_clock(num_days)
    if(health_level<5):
        health_level+=1
    
def rest():
    handle_rest()
    handle_status()

def handle_hunt():
    global num_days
    global num_miles
    global food_remaining
    num_days = random.randint(MIN_DAYS_PER_HUNT,MAX_DAYS_PER_HUNT)
    num_miles=0
    food_remaining += 100
    advance_game_clock(num_days)
    
    
def hunt():
    handle_hunt()
    handle_status()

def handle_status():
    date = date_report()
    print("Food remaining: %d   Health level: %d   Miles traveled: %d  Date: %s"%(food_remaining,health_level,miles_traveled,date))    

def status():
    handle_status()
    
def handle_help():
    print(help_text)
    
def help():
    handle_help()

def handle_quit():
    global playing
    playing = False

def handle_invalid_input(response):
    print("%s is Invalid. Please enter a valid input. Enter 'help' for more information"%response)


def game_is_over():
    global health_level
    global food_remaining
    global month 
    if health_level<=0:
        return True
    elif food_remaining<=0:
        return True
    elif month>12:
        return True
    else:
        return False
    
    

def player_wins():
    global day
    global month
    global miles_traveled
    
    if miles_traveled>=2000:
        return True
    elif(miles_traveled>=2000 and month>=12):
        return True
    else:
        return False

def loss_report():
    global health_level
    global food_remaining
    global month 
    if health_level<=0:
        print("Your health is 0 !")
    elif food_remaining<=0:
        print("You don't have any food left !")
    elif month>12:
        print("Time's up")
        
print(welcome_text + help_text + good_luck_text)
player_name = input("\nWhat is your name, player?")

playing = True
handle_status()
while playing:
    print()
    action = input("Choose an action " + player_name)
    if action == "travel" or action == "t":
        travel()
    elif action == "rest" or action == "r":
        rest()
    elif action == "hunt" or action == "h":
        hunt()
    elif action == "quit" or action == "q":
        handle_quit()
    elif action == "help" or action == "?":
        help()
    elif action == "status" or action == "s":
        status()
    else:
        handle_invalid_input(action)

    if game_is_over():
        playing = False
        
    elif player_wins():
        playing = False
        print("\n\nCongratulations you made it to Oregon alive!")
        handle_status()
if player_wins()==False:
    print("\n\nAlas! You lose.")
    handle_status()
    print(loss_report())
    



