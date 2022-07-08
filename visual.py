import pygame
from environment import track
from car import Car
import math

schermgroote_x = 500
schermgroote_y = 500
titel_van_uw_window = "race ai"
groote_x_1_vakje = groote_y_1_vakje = 10
kleur_achtergrond = [50, 200, 50]
racecar_picture = r'racecar.jpg'#https://flyclipart.com/th-red-racing-car-top-view-race-car-png-210070
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
gamedisplay = pygame.display.set_mode((schermgroote_x, schermgroote_y))#gamedisplay is basicaly gewoon een matrix waarin pixels opgeslagen zijn, er zijn functies die gemakkelijk uit onze afbeeldingen(ook matrixen met pixels) op specifieke locaties in display pixels veranderen. daarom dat we pygame gebruiken, voor de ingebouwde pixel verandering functies, en de time klasse(zie later) en de handige manier van dingen op het scherm te projecteren.
pygame.display.set_caption(titel_van_uw_window)#zet de titel van uw window.
clock = pygame.time.Clock() #initieert dat je tijd gaat willen gebruiken als (pygame.time.Clock()) is een klasse zonder variabelen in de init voor zover ik het snap.
clock.tick(60)
pygame.display.update()
class image(object):#classe die immages bijhoud.
    def __init__(self, image):
        self.im = pygame.transform.scale(pygame.image.load(image), (int(groote_x_1_vakje), int(groote_y_1_vakje)))
    def pri(self, a): #a staat voor een tuple die de locatie voorsteld. (x, y)
        gamedisplay.blit(self.im, a)

def draw_board(env:track):
    lengte, breete = env.matrix.shape
    for i in range(lengte):
        for j in range(breete):
            height = 5
            width = 5
            pygame.draw.rect(gamedisplay, get_color(env.matrix[i, j]), [j*height, i*width, (j+1)*height,(i+1)*width], 0)

def draw_car(car:Car, image_:image):
    image_.pri((car.x, -car.y), car.rot)

def get_color(space:int):
    if(space < 0):
        return [255, 0, 0]
    if(space == 0):
        return [50, 50, 50]
    if(space == 1):
        return [0, 255, 0]

def startscherm():
    kleur = kleur_achtergrond
    gamedisplay.fill(kleur)

def last_loop():
    while(True):
        for event in (pygame.event.get()):
            if event.type == pygame.QUIT:
                pygame.quit()
def update():
    pygame.display.update()

class image(object):#classe die immages bijhoud.
    def __init__(self, image):
        self.im = pygame.transform.scale(pygame.image.load(image), (int(groote_x_1_vakje*10), int(groote_y_1_vakje*10)))
    def pri(self, a, angle): #a staat voor een tuple die de locatie voorsteld. (x, y)
        gamedisplay.blit(self.rot_center(angle), a)
    def rot_center(self, angle):
        """rotate an image over [angle] radians while keeping its center and size"""
        orig_rect = self.im.get_rect()
        rot_image = pygame.transform.rotate(self.im, angle*180/math.pi-90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
# a = track()
# a.read_track("track1.txt")
# #print(a.matrix)
# startscherm()
# draw_board(a)
# race_car = image(racecar_picture)
# car = Car()
# car.x = 6
# car.y = 12
# draw_car(car, race_car)
# update()






# last_loop()