from car import Car
from environment import track
from visual import image, update, draw_car, draw_board, racecar_picture


MAX_GEN = 10
MAX_CARS = 10
MAX_ITT = 10
START_X = 3
START_Y = 3

def show_one_race():
    car = Car()
    env = track()
    env.read_track(f"C:\\Users\\woute\\Documents\\wiskunde\\raceai_py\\track1.txt")

    gen = 0
    max_itt = MAX_ITT
    itt = 0


    race_car = image(racecar_picture)
    car.x = START_X
    car.y = START_Y

    update()


    while(gen < MAX_GEN):
        draw_board(env)
        gen += 1
        itt = 0
        while(not car.stop and itt <= max_itt):
            draw_board(env)
            draw_car(car, race_car)
            update()
            itt += 1
            car.Obs(env)
            car.Steer_ai()
            car.Move()
        
    
