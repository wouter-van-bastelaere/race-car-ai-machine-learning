MAX_GEN = 10
MAX_CARS = 10
MAX_ITT = 10
START_X = 3
START_Y = 3

def reward(env, car, neuraal):#werkt nog niet
    print("reward not completely implemented")
    gen = 0
    max_itt = MAX_ITT
    itt = 0
    car.x = START_X
    car.y = START_Y
    while(gen < MAX_GEN):
        gen += 1
        itt = 0
        while(not car.stop and itt <= max_itt):
            itt += 1
            car.Obs(env)
            car.Steer_ai(neuraal)
            car.Move()

    return car.reward