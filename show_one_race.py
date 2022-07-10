from matplotlib.pyplot import show
import pygame
from car import Car
from environment import track
from visual import image, update, draw_car, draw_board, racecar_picture


MAX_GEN = 1
MAX_CARS = 10
MAX_ITT = 10000
START_X = 3
START_Y = 3

def get_steer_parameters():
    return (1e-2, 1e-2, 1e-2, 1e-1)


def show_one_race():
    car = Car()
    env = track()
    env.read_track("tracks\\track1.txt")

    gen = 0
    max_itt = MAX_ITT
    itt = 0

    Left, Right, Up, Down = get_steer_parameters()

    race_car = image(racecar_picture)
    car.x = START_X
    car.y = START_Y

    pygame.key.set_repeat(1, 10)

    update()


    while(gen < MAX_GEN):
        draw_board(env)
        gen += 1
        itt = 0
        while(not car.stop and itt <= max_itt):
            print(itt)
            draw_board(env)
            draw_car(car, race_car)
            update()
            itt += 1
            car.Obs(env)
            # car.Steer_ai()
            user_key = [0,0,0,0]
            for event in (pygame.event.get()):
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    user_key[0] += Left
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    user_key[1] += Right
                if pygame.key.get_pressed()[pygame.K_UP]:
                    user_key[2] += Up
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    user_key[3] += Down
                if event.type == pygame.QUIT:
                    pygame.quit()
            car.Steer_user(user_key[2]-user_key[3], user_key[0]-user_key[1])
            print(car.x, car.y, car.rot, car.ang_momentum, car.momentum)
            car.Move()
            print(car.x, car.y, car.rot, car.ang_momentum, car.momentum)

show_one_race()
        
    
