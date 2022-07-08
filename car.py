import math as m
from environment import track
import numpy as np

max_snelheid = 100
max_rot_snelheid = 100
max_kracht = 100
max_draai = 0.2
max_torque = 100

class Car:#//cars are circles to make collision easy.
    def __init__(self, x=0, y=0, rot=0, momentum=0, ang_momentum=0, size=1):
        self.x, self.y, self.rot, self.momentum, self.ang_momentum, self.size = x, y, rot, momentum, ang_momentum, size
        self.reward = 0
        self.crashed = 0
        self.stop = False
        self.draai = 0

        self.obs_angles = [-m.pi/3, 0, m.pi/3]#the angels we do observations on relative to the direction the car is facing.
        self.obs = [0, 0, 0]
        
    def Move(self):
        #TO DO
        if self.momentum < 0:
            self.momentum = 0

        print(f"---{self.draai} | {max_draai}")
        if abs(self.draai) > max_draai:
            print("oko")
            self.draai = abs(self.draai)/self.draai*max_draai
        print(f"---{self.draai} | {max_draai}")
        speed = self.momentum/np.sqrt(1+(2*self.momentum/max_snelheid)**2) #+ max_snelheid/2
        self.rot += self.draai*speed
        self.x += m.cos(self.rot)*speed
        self.y += m.sin(self.rot)*speed


    def Obs(self, env:track):#updates observations.
        self.obs = [env.distance((self.x, self.y), self.rot+angle) for angle in self.obs_angles]

    def Steer_user(self, kracht, draai):
        self.momentum += kracht
        if draai == 0:
            self.draai = 0
        else:
            self.draai += draai

    def Steer_ai(self):
        kracht, draai = 0, 0 #Get from AI
        self.momentum += kracht
        if draai == 0:
            self.draai = 0

