import numpy as np
import math as m
import csv

class track:
    def __init__(self):
        self.matrix = np.zeros((0,0))
        self.max_x = 0
        self.max_y = 0
    
    def read_track(self, link):#reads tracks from csv file
        lijst = []
        with open(link) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                lijst.append(row)
        lengte = len(lijst)
        breedte = len(lijst[0])
        self.matrix = np.zeros((lengte, breedte))
        for i in range(lengte):
            for j in range(breedte):
                self.matrix[i, j] = lijst[i][j]
        self.max_x = lengte
        self.max_y = breedte

    def get_xy(self, x, y):
        if(x < 0 or x > self.max_x or y < 0 or y > self.max_y):
            return -1
        return self.matrix[int(x), int(y)]
    
    def distance(self, start, dir):
        return self.get_distance_to_zero(start, dir, 0.1)

    def get_distance_to_zero(self, start, dir, frequency):
        #start is (x, y)
        #dir = angel
        #frequency = how ofter we check
        x, y = start
        dirx = m.cos(m.pi/2-dir)
        print("dir x = ", dirx)
        diry = m.sin(m.pi/2-dir)
        print("dir y = ", diry)

        hit = 1
        while(hit not in [0, -1]):
            hit = self.get_xy(x, y)
            if(hit not in [0, -1]):
                x += dirx*frequency
                y += diry*frequency
        return m.sqrt((start[0]-x)**2 + (start[1]-y)**2)

a = track()
a.read_track(f"C:\\Users\\woute\\Documents\\wiskunde\\raceai_py\\track2.txt")
#print(a.matrix)

print(a.get_distance_to_zero((0.43, 0), m.pi/3, 0.1))


