import math as m
from environment import track

max_snelheid = 0
max_rot_snelheid = 0
max_kracht = 0
max_torque = 0

class Car:#//cars are circles to make collision easy.
    def __init__(self, x=0, y=0, rot=0, momentum=0, ang_momentum=0, size=1):
        self.x, self.y, self.rot, self.momentum, self.ang_momentum, self.size = x, y, rot, momentum, ang_momentum, size
        self.reward = 0
        self.crashed = 0

        self.obs_angels = [-m.pi/3, 0, m.pi/3]#the angels we do observations on relative to the direction the car is facing.
        self.obs = [0, 0, 0]
        
    def Move(self):
        #TO DO
        speed = self.momentum/np.sqrt(1+(2*self.momentum/max_snelheid)**2) + max_snelheid/2
        ang_speed = self.ang_momentum/np.sqrt(1+(2*self.ang_momentum/max_rot_snelheid)**2) + max_rot_snelheid/2
        self.rot += self.ang_speed
        self.x += m.cos(self.rot)*speed
        self.y += m.sin(self.rot)*speed


    def Obs(self, env:track):#updates observations.
        self.obs = [env.distance((self.x, self.y), self.rot+angle) for angle in self.obs_angles]

    def Steer_user(self, kracht, torque):
        self.momentum += kracht
        self.ang_momentum += torque

    def Steer_ai(self):
        kracht, torque = 0, 0 #Get from AI
        self.momentum += kracht
        self.ang_momentum += torque

