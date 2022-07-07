# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:20:57 2019

@author: Wouter Van Bastelaere en Sander De Meyer
"""
import pygame
import numpy as np
from collections.abc import Iterable



wit = r'afbeeldingen\wit.png'
zwart = r'afbeeldingen\zwart.png'
water = r'afbeeldingen\water.png'
zon = r'afbeeldingen\zon.png'
jupiter = r'afbeeldingen\jupiter.png'
Dame = r'afbeeldingen\dame.png'
Loper = r'afbeeldingen\loper.png'
Paard = r'afbeeldingen\paard.png'
Pion = r'afbeeldingen\pion.png'
aangevallen = r'afbeeldingen\aangevallen.png'
Toren = r'afbeeldingen\toren.png'
Koning = r'afbeeldingen\koning.png'
Dame2 = r'afbeeldingen\dame2.png'
Loper2 = r'afbeeldingen\loper2.png'
Paard2 = r'afbeeldingen\paard2.png'
Pion2 = r'afbeeldingen\pion2.png'
Toren2 = r'afbeeldingen\toren2.png'
Koning2 = r'afbeeldingen\koning2.png'
boek_initieel = {-1:aangevallen, 1:wit, 2:water, 3:zon, 4:zwart, 0:jupiter, 'Dame':{-1:Dame, 1:Dame2}, 'Koning':{-1:Koning, 1:Koning2}, 'Toren':{-1:Toren, 1:Toren2}, 'Pion':{-1:Pion, 1:Pion2}, 'Paard':{-1:Paard, 1:Paard2}, 'Loper':{-1:Loper, 1:Loper2}} 
boek = {}
bewogen = False
kleur = 1
N = 8
W = (4, 2)
w_vak = {i:(((not i%2)*4+(i%2)*1)*((i//N)%2)+((not i%2)*1+(i%2)*4)*(not (i//N)%2)) if i%N not in [j for j in range(W[1])] + [N-1-j for j in range(W[1])] or i//N in [j for j in range((N-W[0])//2)] + [N-1-j for j in range((N-W[0])//2)] else 2 for i in range(N**2)}
w_stuk = {i:['0', '0'] for i in range(N**2)}
bord1 = [w_vak[i] if w_stuk[i][1] == '0' else {1:w_vak[i], 2:w_stuk[i][1]} for i in range(N**2)]
bord = np.array(tuple([tuple(bord1[N*i:N*(i+1)]) for i in range(N)]))
schermgroote_x = 720
schermgroote_y = 720
plaats_tussen_2_vakjes = 2
plaats_tussen_rand_en_eerste_rij_vakjes = 10
titel_van_uw_window = 'Schaakspel'
kleur_achtergrond = [255, 0, 255]
kleur_achtergrond2 = [255, 0, 0]
bordgroote_x = N
bordgroote_y = N
groote_x_1_vakje = ((schermgroote_x-2*plaats_tussen_rand_en_eerste_rij_vakjes)/bordgroote_x)-2*plaats_tussen_2_vakjes
groote_y_1_vakje = ((schermgroote_y-2*plaats_tussen_rand_en_eerste_rij_vakjes)/bordgroote_y)-2*plaats_tussen_2_vakjes

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

def sander_to_wouter_coordinaten(get):
    global N
    return (get%N, get//N)

def wcord_to_scord(x):
    global N
    return N*x[0]+x[1]

def bordsandermethode(n, w):
    global N
    global W
    global w_vak
    global w_stuk
    global schermgroote_x
    global bordgroote_y
    global groote_x_1_vakje
    global groote_y_1_vakje
    N = n
    W = w
    w_vak = {i:(((not i%2)*4+(i%2)*1)*((i//N)%2)+((not i%2)*1+(i%2)*4)*(not (i//N)%2)) if i%N not in [j for j in range(W[1])] + [N-1-j for j in range(W[1])] or i//N in [j for j in range((N-W[0])//2)] + [N-1-j for j in range((N-W[0])//2)] else 2 for i in range(N**2)}
    w_stuk = {i:['0', '0'] for i in range(N**2)}
    bordgroote_x = N
    bordgroote_y = N
    groote_x_1_vakje = ((schermgroote_x-2*plaats_tussen_rand_en_eerste_rij_vakjes)/bordgroote_x)-2*plaats_tussen_2_vakjes
    groote_y_1_vakje = ((schermgroote_y-2*plaats_tussen_rand_en_eerste_rij_vakjes)/bordgroote_y)-2*plaats_tussen_2_vakjes

def omringende(vak):  # Exclusief vak zelf
    l = [-N-1, -N, -N+1, -1, 1, N-1, N, N+1]
    return [vak + i for i in l if 0 <= vak + i < N**2 and abs((vak+i)%N-vak%N) <= 1]

def product_omringende(vak):   # Exclusief vak zelf
    return np.prod([w_vak[omr] for omr in omringende(vak)])

def geef_vaknummers():
    return np.array([[i+N*j for i in range(N)] for j in range(N)])

def geef_vak():
    return np.array([[w_vak[i+N*j] for i in range(N)] for j in range(N)])

def geef_stuk():
    return np.array([[''.join(str(w_stuk[i+N*j][0]) + w_stuk[i+N*j][1]) for i in range(N)] for j in range(N)])

def Stukplaats(l):
    return [i for i in w_stuk if w_stuk[i] == l][0]
    
def Beweeg(vak, kleur):
    return eval('Beweeg_' + w_stuk[vak][1] + '(' + str(vak) + ',' + str(w_stuk[vak][0]) + ')')

    
def Controle_Beweeg(vak, lijst, kleur):
    return [i for i in lijst if Mogelijk(vak, i, kleur)]
# Beweegfuncties

def Beweeg_Hulp(vak, kleur, ran, vakje):
    lijst = []
    for i in range(1, eval(ran)):
        if w_stuk[eval(vakje)][0] == kleur:
            break
        elif w_stuk[eval(vakje)][0] == -kleur:
            lijst.append(eval(vakje))
            break
        lijst.append(eval(vakje))
    return lijst

def Beweeg_Toren(vak, kleur): # Exclusief beginvak
    lijst = []
    lijst.extend(Beweeg_Hulp(vak, kleur, 'N-vak%N', 'vak + i'))
    lijst.extend(Beweeg_Hulp(vak, kleur, '1 + vak%N', 'vak - i'))
    lijst.extend(Beweeg_Hulp(vak, kleur, 'N-vak//N', 'vak + N*i'))
    lijst.extend(Beweeg_Hulp(vak, kleur, '1 + vak//N', 'vak - N*i'))
    return lijst

def Beweeg_Loper(vak, kleur):  # Exclusief beginvak
    lijst = []
    lijst.extend(Beweeg_Hulp(vak, kleur, 'min(N-vak%N, 1+vak//N)', 'vak - (N-1)*i'))
    lijst.extend(Beweeg_Hulp(vak, kleur, 'min(1+vak%N, N-vak//N)', 'vak + (N-1)*i'))
    lijst.extend(Beweeg_Hulp(vak, kleur, 'min(1+vak%N, 1+vak//N)', 'vak - (N+1)*i'))
    lijst.extend(Beweeg_Hulp(vak, kleur, 'min(N-vak%N, N-vak//N)', 'vak + (N+1)*i'))
    return lijst

def Beweeg_Dame(vak, kleur):
    return Beweeg_Toren(vak, kleur) + Beweeg_Loper(vak, kleur)

def Check_Rokade(vak, kleur):
    global Rokade
    if w_stuk[vak][2] == 0:
        if w_stuk[vak + 3] == [kleur, 'Toren', 0] and w_stuk[vak + 1][1] == '0' and w_stuk[vak + 2][1] == '0':
            Rokade.append(vak + 2)
        if w_stuk[vak - 4] == [kleur, 'Toren', 0] and w_stuk[vak - 1][1] == '0' and w_stuk[vak - 2][1] == '0' and w_stuk[vak - 3][1] == '0':
            Rokade.append(vak - 2)
    return Rokade
        


    
    
def Beweeg_Koning(vak, kleur):
    lijst = [vakje for vakje in omringende(vak) if w_stuk[vakje][0] != kleur]
    lijst.extend(Check_Rokade(vak, kleur))
    return lijst
def Beweeg_Pion(vak, kleur):
    global Piontransformatie
    global Enpassant
    global Enpassantplaats
    lijst = [vak + N*kleur for _ in range(1) if w_stuk[vak + N*kleur][0] == '0']
    if w_stuk[vak][2] == 0 and w_stuk[vak + N*kleur][0] == '0' and w_stuk[vak + 2*N*kleur][0] == '0':
        lijst.extend([vak + 2*N*kleur])
    if vak%N != 0:
        lijst.extend([vak - 1 + N*kleur for _ in range(1) if w_stuk[vak - 1 + N*kleur][0] == -kleur])
    if vak%N != N-1:
        lijst.extend([vak + 1 + N*kleur for _ in range(1) if w_stuk[vak + 1 + N*kleur][0] == -kleur])
    if vak in Enpassant[kleur]:
        lijst.append(Enpassantplaats)
    return lijst

def Piontransformeer(gekozen_pion):
    global Piontransformatie
    w_stuk[Piontransformatie] = [-kleur, gekozen_pion, 0]
    bord[Piontransformatie//N, Piontransformatie%N] = {1:w_vak[Piontransformatie], 2:w_stuk[Piontransformatie][1]}
    Piontransformatie = None


def Beweeg_Paard(vak, kleur):
    l = [-2*N-1, -2*N+1, -N-2, -N+2, 0, N-2, N+2, 2*N-1, 2*N+1]
    return [vak + i for i in l if 0 <= vak + i < N**2 and abs((vak+i)%N - vak%N) <=2 and w_stuk[vak+i][0] != kleur]
"""
def Schaakmat(kleur):
    l = Beweeg_Koning(Stukplaats([kleur, 'Koning']), kleur) + [Stukplaats([kleur, 'Koning'])]
    print(l)
    q = []
    print([v for v in w_stuk if w_stuk[v][0] == -kleur])
    for i in [v for v in w_stuk if w_stuk[v][0] == -kleur]:
        q.extend(Beweeg(i))
    return (sum([0 for i in l if i in q]) == 0)
"""
def niet_bewogen(bord):
    for i in range(N):
        for j in range(N):
            try:
                del bord[i, j][3]
            except:
                pass


def aangevallen(vakje, kleur):
    lijst = []
    if w_stuk[vakje][1] == '0':
        w_stuk[vakje] = [kleur, 'Fout']
    for vak in [vak for vak in w_stuk if w_stuk[vak][0] == -kleur]:
        lijst.extend(Beweeg(vak, kleur))
    if w_stuk[vakje][1] == 'Fout':
        w_stuk[vakje] = [kleur, '0']
    return vakje in lijst
            
def Schaak(kleur):
    vak = [vakje for vakje in w_stuk if w_stuk[vakje][:2] == [kleur, 'Koning']][0]
    return aangevallen(vak, kleur)
        
def Mogelijk(vak, zet, kleur):
    vorige = w_stuk[zet]
    w_stuk[zet] = w_stuk[vak]
    w_stuk[vak] = ['0', '0']
    controle = not Schaak(kleur)
    w_stuk[vak] = w_stuk[zet]
    w_stuk[zet] = vorige
    return controle
    
        
def Speel(bord, vakje):
    vak = vakje[1] + N*vakje[0]
    global kleur
    global bewogen
    global lijst_beweeg
    global aangeklikte_stuk
    global aangeklikte_stuk2
    global Rokade
    global Piontransformatie
    global Enpassant
    global Enpassantplaats
    Schaakmat_lijst = [stuk for stuk in w_stuk if w_stuk[stuk][0] == kleur]
    Bewegingsmogelijkheden = []
    for stuk in Schaakmat_lijst:
        Bewegingsmogelijkheden.extend(Controle_Beweeg(stuk, Beweeg(stuk, kleur), kleur))
    if Bewegingsmogelijkheden == []:
        print('Schaakmat')
    if bewogen:
        if vak in lijst_beweeg:
            if w_stuk[aangeklikte_stuk2][1] in ['Koning', 'Pion']:
                w_stuk[aangeklikte_stuk2][2] = 1
            if vak in Rokade:
                if vak - aangeklikte_stuk2 == 2:
                    w_stuk[vak - 1] = [kleur, 'Toren']
                    w_stuk[vak + 1] = ['0', '0']
                    bord[(vak//N, vak%N + 1)] = w_vak[vak + 1]
                    bord[(vak//N, vak%N - 1)] = {1:w_vak[vak - 1], 2:w_stuk[vak - 1][1]}
                if vak - aangeklikte_stuk2 == -2:
                    w_stuk[vak + 1] = [kleur, 'Toren']
                    w_stuk[vak - 2] = ['0', '0']
                    bord[(vak//N, vak%N - 2)] = w_vak[vak - 2]
                    bord[(vak//N, vak%N + 1)] = {1:w_vak[vak - 1], 2:w_stuk[vak + 1][1]}
            if vak - aangeklikte_stuk2 == 2*N*kleur and w_stuk[aangeklikte_stuk2][1] == 'Pion':
                Enpassantplaats = vak - N*kleur
                l = []
                if vak%N != 0:
                    l.append(vak - 1)
                if vak%N != N-1:
                    l.append(vak + 1)
                Enpassant[-kleur] = l
            if w_stuk[aangeklikte_stuk2][1] == 'Pion' and Enpassantplaats == vak:
                w_stuk[vak - N*kleur] = ['0', '0']
                bord[((vak-N*kleur)//N, (vak-N*kleur)%N)] = w_vak[vak - N*kleur]
            w_stuk[vak] = w_stuk[aangeklikte_stuk2]
            w_stuk[aangeklikte_stuk2] = ['0', '0']
            bord[(aangeklikte_stuk2//N,aangeklikte_stuk2%N)] = w_vak[aangeklikte_stuk2]
            bord[vakje] = {1:w_vak[vak], 2:w_stuk[vak][1]}
            if w_stuk[vak][1] == 'Pion' and vak//N == (kleur+1)*(N-1)/2:
                Piontransformatie = vak
            niet_bewogen(bord)
            bewogen = False
            kleur = -kleur
            Rokade = []
            #bord1 = [w_vak[i] if w_stuk[i][1] == '0' else {1:w_vak[i], 2:w_stuk[i][1]} for i in range(256)]
            #bord = np.array(tuple([tuple(bord1[N*i:N*(i+1)]) for i in range(N)]))
        else:
            bewogen = False
            niet_bewogen(bord)
    else:
        if w_stuk[vak][0] == kleur:
            bewogen = True
            aangeklikte_stuk = vakje
            aangeklikte_stuk2 = vak
            lijst_beweeg = Controle_Beweeg(vak, Beweeg(vak, kleur), kleur)
            for i in lijst_beweeg:
                if isinstance(bord[i//N, i%N], int):
                    bord[i//N, i%N] = {1:w_vak[i], 3:-1}
                else:
                    bord[i//N, i%N][3] = -1                
    return bord
    
def boekklaarmaken(boek_initieel):
    global boek
    for i in boek_initieel:
        if isinstance(boek_initieel[i], dict) is True:
            boek[i]={-1:image(boek_initieel[i][-1]), 1:image(boek_initieel[i][1])}
        else:
            boek[i] = image(boek_initieel[i])

def gewoonschaakbordstart():
    global Rokade
    Rokade = []
    bordsandermethode(8, (0, 0))
    boekklaarmaken(boek_initieel)
    w_stuk[0] = [1, 'Toren', 0]
    w_stuk[1] = [1, 'Paard', 0]
    w_stuk[2] = [1, 'Loper', 0]
    w_stuk[3] = [1, 'Dame', 0]
    w_stuk[4] = [1, 'Koning', 0]
    w_stuk[5] = [1, 'Loper', 0]
    w_stuk[6] = [1, 'Paard', 0]
    w_stuk[7] = [1, 'Toren', 0]
    w_stuk[8] = [1, 'Pion', 0]
    w_stuk[9]= [1, 'Pion', 0]
    w_stuk[10]= [1, 'Pion', 0]
    w_stuk[11]= [1, 'Pion', 0]
    w_stuk[12]= [1, 'Pion', 0]
    w_stuk[13]= [1, 'Pion', 0]
    w_stuk[14]= [1, 'Pion', 0]
    w_stuk[15]= [1, 'Pion', 0]
    w_stuk[63] = [-1, 'Toren', 0]
    w_stuk[62] = [-1, 'Paard', 0]
    w_stuk[61] = [-1, 'Loper', 0]
    w_stuk[59] = [-1, 'Dame', 0]
    w_stuk[60] = [-1, 'Koning', 0]
    w_stuk[58] = [-1, 'Loper', 0]
    w_stuk[57] = [-1, 'Paard', 0]
    w_stuk[56] = [-1, 'Toren', 0]
    w_stuk[55] = [-1, 'Pion', 0]
    w_stuk[54]= [-1, 'Pion', 0]
    w_stuk[53]= [-1, 'Pion', 0]
    w_stuk[52]= [-1, 'Pion', 0]
    w_stuk[51]= [-1, 'Pion', 0]
    w_stuk[50]= [-1, 'Pion', 0]
    w_stuk[49]= [-1, 'Pion', 0]
    w_stuk[48]= [-1, 'Pion', 0]

def spel16start():
    
    bordsandermethode(16, (4, 2))
    boekklaarmaken(boek_initieel)
    w_stuk[20] = [1, 'Toren', 0]
    w_stuk[21] = [1, 'Paard', 0]
    w_stuk[22] = [1, 'Loper', 0]
    w_stuk[23] = [1, 'Dame', 0]
    w_stuk[24] = [1, 'Koning', 0]
    w_stuk[25] = [1, 'Loper', 0]
    w_stuk[26] = [1, 'Paard', 0]
    w_stuk[27] = [1, 'Toren', 0]
    w_stuk[36] = [1, 'Pion', 0]
    w_stuk[37]= [1, 'Pion', 0]
    w_stuk[38]= [1, 'Pion', 0]
    w_stuk[39]= [1, 'Pion', 0]
    w_stuk[40]= [1, 'Pion', 0]
    w_stuk[41]= [1, 'Pion', 0]
    w_stuk[42]= [1, 'Pion', 0]
    w_stuk[43]= [1, 'Pion', 0]
    w_stuk[228] = [-1, 'Toren', 0]
    w_stuk[229] = [-1, 'Paard', 0]
    w_stuk[230] = [-1, 'Loper', 0]
    w_stuk[231] = [-1, 'Dame', 0]
    w_stuk[232] = [-1, 'Koning', 0]
    w_stuk[233] = [-1, 'Loper', 0]
    w_stuk[234] = [-1, 'Paard', 0]
    w_stuk[235] = [-1, 'Toren', 0]
    w_stuk[212] = [-1, 'Pion', 0]
    w_stuk[213]= [-1, 'Pion', 0]
    w_stuk[214]= [-1, 'Pion', 0]
    w_stuk[215]= [-1, 'Pion', 0]
    w_stuk[216]= [-1, 'Pion', 0]
    w_stuk[217]= [-1, 'Pion', 0]
    w_stuk[218]= [-1, 'Pion', 0]
    w_stuk[219]= [-1, 'Pion', 0]


gamedisplay = pygame.display.set_mode((schermgroote_x, schermgroote_y))#gamedisplay is basicaly gewoon een matrix waarin pixels opgeslagen zijn, er zijn functies die gemakkelijk uit onze afbeeldingen(ook matrixen met pixels) op specifieke locaties in display pixels veranderen. daarom dat we pygame gebruiken, voor de ingebouwde pixel verandering functies, en de time klasse(zie later) en de handige manier van dingen op het scherm te projecteren.
pygame.display.set_caption(titel_van_uw_window)#zet de titel van uw window.

class image(object):#classe die immages bijhoud.
    def __init__(self, image):
        self.im = pygame.transform.scale(pygame.image.load(image), (int(groote_x_1_vakje), int(groote_y_1_vakje)))
    def pri(self, a): #a staat voor een tuple die de locatie voorsteld. (x, y)
        gamedisplay.blit(self.im, a)
class game(object):
    def __init__(self, n, w, speelfunctie, startbord):
        self.n, self.w, self.speelfunctie, self.startbord =  n, w, speelfunctie, startbord
    def speel(self):
        self.speelfunctie()
    def afbeeldingenklaarmaken(self):
        self.startbord()
        global N
        global bord
        global w_vak
        global w_stuk
        N = self.n
        bord1 = [w_vak[i] if w_stuk[i][1] == '0' else {1:w_vak[i], 2:w_stuk[i][1]} for i in range(self.n**2)]
        bord = np.array(tuple([tuple(bord1[self.n*i:self.n*(i+1)]) for i in range(self.n)]))



def welk_vakje(pos, bord):
    for i, ii in enumerate(bord):
        for e, ee in enumerate(ii):
            if abs(plaats_tussen_rand_en_eerste_rij_vakjes+(plaats_tussen_2_vakjes+groote_x_1_vakje)*i-pos[0]) < groote_x_1_vakje and abs(plaats_tussen_rand_en_eerste_rij_vakjes+(plaats_tussen_2_vakjes+groote_y_1_vakje)*e-pos[1]) < groote_y_1_vakje:
            #if abs((plaats_tussen_2_vakjes+groote_x_1_vakje)*i-pos[0]) < groote_x_1_vakje and abs((plaats_tussen_2_vakjes+groote_y_1_vakje)*e-pos[1]) < groote_y_1_vakje:
                return (e, i)
    return 'no found'

def scherm_klaarmaken(bord, boek=boek):
    for i, ii in enumerate(bord):
        for e, ee in enumerate(ii):
            x = plaats_tussen_rand_en_eerste_rij_vakjes+(plaats_tussen_2_vakjes+groote_x_1_vakje)*i
            y = plaats_tussen_rand_en_eerste_rij_vakjes+(plaats_tussen_2_vakjes+groote_y_1_vakje)*e
            te_printen = bord[e, i]
            if isinstance(te_printen, Iterable):
                for iii in sorted(te_printen):
                    if isinstance(boek[te_printen[iii]], image):
                        boek[te_printen[iii]].pri((x, y))
                    else:
                        boek[te_printen[iii]][w_stuk[wcord_to_scord((e, i))][0]].pri((x, y))
            else:
                boek[te_printen].pri((x, y))


pygame.display.update() #update uw scherm wordt al 1 keer voor de lus gedaan omdat je dan iets ziet vooraleer je een 1e keer geklikt hebt.
clock = pygame.time.Clock() #initieert dat je tijd gaat willen gebruiken als (pygame.time.Clock()) is een klasse zonder variabelen in de init voor zover ik het snap.
stop = False #wordt niet echt als stop gebruikt


def gewoonspel():
    global N
    global w_vak
    global w_stuk
    global bord1
    global bord
    while not stop: #de stop zit in het if event.type == pygame.QUIT: pygame.quit()
        gamedisplay.fill(kleur_achtergrond) # reset de achtergrond van uw scherm zodat opnieuw alle stukken erop kunnen gezet worden. filler is gelijk aan een lijst van 3 groot die een kleur representeert. 
        if Piontransformatie:
            pionnen = ['Dame', 'Paard', 'Loper', 'Toren', 'Paard', 'Loper', 'Toren', 'Paard', 'Loper', 'Toren', 'Paard', 'Loper', 'Toren', 'Paard', 'Loper', 'Toren', 'Paard', 'Loper', 'Toren']
            for i, e in enumerate(pionnen):
                boek[e][kleur].pri((plaats_tussen_rand_en_eerste_rij_vakjes+(plaats_tussen_2_vakjes+groote_x_1_vakje)*(i%N), plaats_tussen_rand_en_eerste_rij_vakjes+(plaats_tussen_2_vakjes+groote_y_1_vakje)*(i//N) ))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #als je op kruisje gedrukt hebt.
                    pygame.quit() #sluit uw game af, laat spider open.
                
                if event.type == pygame.MOUSEBUTTONUP:
                    print('mousebutton')
                    pos = pygame.mouse.get_pos() #positie is nu de positie van de muis waar laatst geklikt is.
                    print(pos)
                    vakje = welk_vakje(pos, bord) #dit was mijn functie om dan het vakje te bepalen.
                    if vakje is not None: #als er geklikt was deze frame doe dan
                        print(vakje)
                        if len(pionnen) >= wcord_to_scord(vakje):
                            Piontransformeer(pionnen[wcord_to_scord(vakje)])
                            print('gepromoveerd')
                        
                
                
                

        else:
            scherm_klaarmaken(bord)
            for event in pygame.event.get(): #overloopt elke klik die je gedaan hebt en steekt die in een lijst.
                if event.type == pygame.QUIT: #als je op kruisje gedrukt hebt.
                    pygame.quit() #sluit uw game af, laat spider open.
                if event.type == pygame.MOUSEBUTTONUP: #als je uw muis loslaat.
                    pos = pygame.mouse.get_pos() #positie is nu de positie van de muis waar laatst geklikt is.
                    vakje = welk_vakje(pos, bord) #dit was mijn functie om dan het vakje te bepalen.
                    if vakje is not None: #als er geklikt was deze frame doe dan
                        Speel(bord, vakje) #functie die iets doet met uw klik.

        pygame.display.update()#het vlak display wordt op uw pc_scherm gezet.
        clock.tick(10) #10 keer per seconde is de maximale frame rate. als uw ding rapper klaar is dan 1/10 van een seconde weg van de vorige zal ik wachten tot dit wel 1/10 * 1sec weg is van de vorige.
    pygame.quit() #hier wordt nooit gekomen door de infinite loop maarja, moest die toch ooit eindigen stopt uw programma hier ook.
def spel16():
    global N
    global w_vak
    global w_stuk
    global bord1
    global bord
    while not stop: #de stop zit in het if event.type == pygame.QUIT: pygame.quit()
        for event in (pygame.event.get()): #overloopt elke klik die je gedaan hebt en steekt die in een lijst.
            if event.type == pygame.QUIT: #als je op kruisje gedrukt hebt.
                pygame.quit() #sluit uw game af, laat spider open.
            if event.type == pygame.MOUSEBUTTONUP: #als je uw muis loslaat.
                pos = pygame.mouse.get_pos() #positie is nu de positie van de muis waar laatst geklikt is.
                vakje = welk_vakje(pos, bord) #dit was mijn functie om dan het vakje te bepalen.
                if vakje is not None: #als er geklikt was deze frame doe dan
                    Speel(bord, vakje) #functie die iets doet met uw klik. doe je maar zelf.
            gamedisplay.fill(kleur_achtergrond) # reset de achtergrond van uw scherm zodat opnieuw alle stukken erop kunnen gezet worden. filler is gelijk aan een lijst van 3 groot die een kleur representeert. 
            scherm_klaarmaken(bord)
            if Piontransformatie:
                pass
            pygame.display.update()#het vlak display wordt op uw pc_scherm gezet.
        clock.tick(10) #10 keer per seconde is de maximale frame rate. als uw ding rapper klaar is dan 1/10 van een seconde weg van de vorige zal ik wachten tot dit wel 1/10 * 1sec weg is van de vorige.
    pygame.quit() #hier wordt nooit gekomen door de infinite loop maarja, moest die toch ooit eindigen stopt uw programma hier ook.
Rokade = []
Piontransformatie = None
Enpassant = {1: [], -1: []}
Enpassantplaats = None
spel16game = game(16, (4, 2), spel16, spel16start)
gewoonspelgame = game(8, (0, 0), gewoonspel, gewoonschaakbordstart)


def startscherm():
    kleur = kleur_achtergrond2
    gamedisplay.fill(kleur)
    while True:
        for event in (pygame.event.get()):
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP: #als je uw muis loslaat.
                pos = pygame.mouse.get_pos() #positie is nu de positie van de muis waar laatst geklikt is.
                if pos[0] >= schermgroote_x/2-schermgroote_x/8 and pos[0] <= schermgroote_x/2+schermgroote_x/8:
                    if pos[1] >= schermgroote_y/7 and pos[1] <= 2*schermgroote_y/7:
                        spel16game = game(16, (4, 2), spel16, spel16start)
                        spel16game.afbeeldingenklaarmaken()
                        spel16game.speel()
                        pygame.quit
                    if pos[1] >= 3*schermgroote_y/7 and pos[1] <= 4*schermgroote_y/7:
                        gewoonspelgame = game(8, (0, 0), gewoonspel, gewoonschaakbordstart)
                        gewoonspelgame.afbeeldingenklaarmaken()
                        gewoonspelgame.speel()
                        pygame.quit
                    if pos[1] >= 5*schermgroote_y/7 and pos[1] <= 6*schermgroote_y/7:
                        print('nog niet gemaakt')
                if kleur == kleur_achtergrond2:
                    kleur = kleur_achtergrond
                else:
                    kleur = kleur_achtergrond2
            gamedisplay.fill(kleur)
            textsurface = myfont.render('16x16', False, (0, 255, 0))
            pygame.draw.rect(gamedisplay, [0, 0, 0], [schermgroote_x/2-schermgroote_x/8, schermgroote_y/7, schermgroote_x/4,schermgroote_y//7], 0)
            gamedisplay.blit(textsurface,(schermgroote_x/2-15*5, schermgroote_y//7))
            textsurface = myfont.render('normaal', False, (0, 255, 0))
            pygame.draw.rect(gamedisplay, [0, 0, 0], [schermgroote_x/2-schermgroote_x/8, 3*schermgroote_y/7, schermgroote_x/4,schermgroote_y//7], 0)
            gamedisplay.blit(textsurface,(schermgroote_x/2-15*5, 3*schermgroote_y//7))
            textsurface = myfont.render('custom', False, (0, 255, 0))
            pygame.draw.rect(gamedisplay, [0, 0, 0], [schermgroote_x/2-schermgroote_x/8, 5*schermgroote_y/7, schermgroote_x/4,schermgroote_y//7], 0)
            gamedisplay.blit(textsurface,(schermgroote_x/2-15*5, 5*schermgroote_y//7))
            pygame.display.update()
        clock.tick(10)
startscherm()
pygame.quit()