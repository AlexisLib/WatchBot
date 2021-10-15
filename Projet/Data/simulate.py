#!/usr/bin/env python
# coding: utf-8

# Importing Python Libraries
import random
import time
from datetime import datetime, timedelta
from Stream import *


# Function to simulate steps, heartbeat, bloodpressure and temperature data
def simulate(user, i, state):
    # Range for heartbeat, blood pressure and temperature

    iduser = user.ident
    age = user.age
    gender = user.gender
    height = user.height
    weight = user.weight
    speed_max_h = user.speed_max_h
    step_per_minute_resting = user.step_per_minute_resting
    step_per_minute_sport = user.step_per_minute_sport

    # Blood pressure au repos

    if age < 20:
        if gender == "m":
            values = [102, 66]
        else:
            values = [97, 62]
    if age > 19 and age < 30:
        if gender == "m":
            values = [107, 69]
        else:
            values = [101, 66]
    if age > 29 and age < 40:
        if gender == "m":
            values = [111, 74]
        else:
            values = [105, 69]
    if age > 39 and age < 50:
        if gender == "m":
            values = [115, 78]
        else:
            values = [108, 70]
    if age > 49 and age < 60:
        if gender == "m":
            values = [116, 77]
        else:
            values = [101, 72]
    if age > 59 and age < 70:
        if gender == "m":
            values = [120, 75]
        else:
            values = [101, 71]
    if age > 69:
        if gender == "m":
            values = [128, 70]
        else:
            values = [101, 70]

    blood_presure_dialostic = random.randint(values[0] - 3, values[0] + 3)
    blood_pressure_systolic = random.randint(values[1] - 2, values[1] + 2)

    # Fréquence cardiaque

    fcm = 207 - 0.7 * age
    max_resting = fcm / 2.2
    min_sport = max_resting * 1.2

    if age > 5 and age < 13:
        maxi = 125
        age_start = 6
        coeff = 11.6  # Déterminé suivant l'évolution des fréquences moyennes selon l'âge
    if age > 12:
        maxi = 80
        age_start = 12
        coeff = 0.4  # Déterminé suivant l'évolution des fréquences moyennes selon l'âge
    if age > 62:
        maxi = 70
        age_start = 62
        coeff = 0.3  # Déterminé suivant l'évolution des fréquences moyennes selon l'âge

    min_resting = maxi - (age - age_start) * coeff
    if min_resting < 60: min_resting == 60

    # Pas max
    steps_max = 1000 / (speed_max_h / 60)
    step_per_minute = [0, steps_max]
    resting_heartbeat = [min_resting, max_resting]
    sporting_hearbeat = [min_sport, fcm]

    now = datetime.now().replace(hour=0, minute=0)
    now = now + timedelta(minutes=i)
    date = str(now.strftime("%d-%m-%Y"))
    hour = str(now.strftime("%H:%M"))

    # Simulating Steps
    if state == 0:
        steps = 0
    if state == 1:
        steps = random.randint(step_per_minute_resting[0], step_per_minute_resting[1])
    if state == 2:
        steps = random.randint(step_per_minute_sport[0], step_per_minute_sport[1])

    # Blood pressure effort
    #  1 pas environ = 0.0006 km donc par minute = 0.036 km/h

    evol_pressure_dialostic = 10 * (steps * 0.036)
    evol_pressure_systolic = 2.5 * (steps * 0.036)
    blood_presure_dialostic += evol_pressure_dialostic
    blood_pressure_systolic += evol_pressure_systolic
    blood_pressure = str(round(blood_presure_dialostic, 2)) + "/" + str(round(blood_pressure_systolic, 2))

    # A changer en virgule
    temperature = round(random.uniform(36, 38), 2)

    if steps > 60:
        heartbeat = random.randint(int(sporting_hearbeat[0]), int(sporting_hearbeat[1]))

    else:
        heartbeat = random.randint(int(resting_heartbeat[0]), int(resting_heartbeat[1]))

    # Returning the simulated data
    return [iduser, gender, age, height, weight, steps, heartbeat, blood_pressure, temperature, date, hour]


# ## Types d'utilisateurs

# Détermination du temps d'inactivité
class Sportif:
    def __init__(self,ident,gender,age,height,weight,speed_max_h,
                 step_per_minute_resting,step_per_minute_sport,s_resting,e_resting):
        start = datetime.datetime.strptime(s_resting, '%H:%M')
        end = datetime.datetime.strptime(e_resting, '%H:%M')
        self.start_sleep = start.hour * 60 + start.minute
        self.end_sleep = end.hour * 60 + end.minute 
        self.normal_period = [1,1,1,1,2]
        self.resting_period = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,2]
        self.sport_period = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        self.random_inactive = [0,0,0,0,0,0,0,1,1,1]
        self.ident = ident
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.speed_max_h = speed_max_h
        self.step_per_minute_resting = step_per_minute_resting
        self.step_per_minute_sport = step_per_minute_sport
        
class Big_Sportif:
    def __init__(self,ident,gender,age,height,weight,speed_max_h,
                 step_per_minute_resting,step_per_minute_sport,s_resting,e_resting):
        start = datetime.datetime.strptime(s_resting, '%H:%M')
        end = datetime.datetime.strptime(e_resting, '%H:%M')
        self.start_sleep = start.hour * 60 + start.minute
        self.end_sleep = end.hour * 60 + end.minute 
        self.normal_period = [1,1,1,1,2]
        self.resting_period = [0,0,0,0,0,0,0,0,0,0,0,0,0,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
        self.sport_period = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        self.random_inactive = [0,0,0,0,0,0,1,1,1,1]
        self.ident = ident
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.speed_max_h = speed_max_h
        self.step_per_minute_resting = step_per_minute_resting
        self.step_per_minute_sport = step_per_minute_sport
        
class Not_Sportif:
    def __init__(self,ident,gender,age,height,weight,speed_max_h,
                 step_per_minute_resting,step_per_minute_sport,s_resting,e_resting):
        start = datetime.datetime.strptime(s_resting, '%H:%M')
        end = datetime.datetime.strptime(e_resting, '%H:%M')
        self.start_sleep = start.hour * 60 + start.minute
        self.end_sleep = end.hour * 60 + end.minute 
        self.normal_period = [1,1,1,1,2]
        self.resting_period = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,2]
        self.sport_period = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        self.random_inactive = [0,0,0,0,0,0,1,1]
        self.ident = ident
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.speed_max_h = speed_max_h
        self.step_per_minute_resting = step_per_minute_resting
        self.step_per_minute_sport = step_per_minute_sport
        

class Very_Not_Sportif:
    def __init__(self,ident,gender,age,height,weight,speed_max_h,
                 step_per_minute_resting,step_per_minute_sport,s_resting,e_resting):
        start = datetime.datetime.strptime(s_resting, '%H:%M')
        end = datetime.datetime.strptime(e_resting, '%H:%M')
        self.start_sleep = start.hour * 60 + start.minute
        self.end_sleep = end.hour * 60 + end.minute 
        self.normal_period = [1,1,1,1,2]
        self.resting_period = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                               1,1,1,1,1,1,1,1,1,2]
        self.sport_period = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        self.random_inactive = [0,0,0,0,0,0,0,0,1,1]
        self.ident = ident
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.speed_max_h = speed_max_h
        self.step_per_minute_resting = step_per_minute_resting
        self.step_per_minute_sport = step_per_minute_sport



# ## Création User


# Création d'un utilisateur en y indiquant la période de fin de journée : il ne se déplace plus vraiment
user1 = Big_Sportif(1, "m", 25, "175", "75", 30, [0, 100], [100, 400], "21:00", "08:00")
user2 = Very_Not_Sportif(2, "m", 22, "177", "77", 30, [0, 50], [50, 200], "23:30", "12:30")
user3 = Very_Not_Sportif(3, "f", 48, "168", "65", 30, [0, 70], [50, 220], "21:30", "07:00")
user4 = Sportif(4, "f", 33, "175", "98", 30, [0, 40], [40, 180], "21:30", "07:00")
users = [user1, user2, user3, user4]

result = []
select = 0
select2 = 0

#Init stream flux
kinesis_helper = KinesisFireHose(StreamName="WatchBotStream")

for user in users:
    for i in range(1440):
        stop = 0
        if i >= user.start_sleep or i <= user.end_sleep:
            select = 0
            select2 = 0
        if i > user.end_sleep and i < user.start_sleep:
            if select == 0:
                select = random.choice(user.random_inactive)
                if select == 0:
                    select2 = -10
                    stop = 1
                else:
                    select2 = random.choice(user.normal_period)
            if select == 1:
                # On rentre dans une période sans sport
                select2 = random.choice(user.resting_period)
            if select == 2:
                # On rentre dans une période de sport
                select2 = random.choice(user.sport_period)
            if select < 0:
                select2 = select + 1
                stop = 1
        if stop == 1:
            result.append(simulate(user, i, 0))
        else:
            result.append(simulate(user, i, select2))
        select = select2

    data = []
    for row in result:
        row = {"iduser": str(row[0]), "gender": str(row[1]), "age": str(row[2]), "height": str(row[3]), "weight": str(row[4]), "steps": str(row[5]), "heartbeat": str(row[6]), "blood_pressure": str(row[7]), "temperature": str(row[8]), "date": str(row[9]), "hour": str(row[10])}
        data.append(row)

    for x in data:
        response = kinesis_helper.post(payload=x)

    result = []

    print("Data streamed to Kinesis !")

    time.sleep(200)
