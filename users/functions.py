import datetime
import random

def get_date():
    now = datetime.datetime.now()
    nday = datetime.timedelta(days = 1)
    due_time = now + nday
    print(due_time)
    return now, due_time


def get_percentage(amount):
    percentage = 0.008
    try:
        interest = int(amount)*percentage
        return interest
    except Exception as er:
        return er


def make_new_deposit():
    now = datetime.datetime.now()
    time_str = ''.join(ch for ch in str(now) if ch.isalnum())
    num1 = time_str[3:8]
    print(num1)
    num2 = time_str[8:17]
    print(f'{num2}{num1}')
    return f'{num2}{num1}GT'


def get_game_time():
    now = datetime.datetime.now()
    nday = datetime.timedelta(minutes= 1)
    due_time = now + nday
    print(due_time)

    return due_time
    
def get_user_id():
    now = datetime.datetime.now()
    time_str = ''.join(ch for ch in str(now) if ch.isalnum())
    num1 = time_str[5:8]
    print(num1)
    num2 = time_str[8:15]
    print(f'{num2}{num1}')
    return f'{num2}{num1}'

def get_rand_user():
    num = [5,6,7,20,32,30,1,2,3,]
    return random.choice(num)