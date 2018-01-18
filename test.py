import pyaudio
import numpy as np
import pygame
import random
import math
import time
from matplotlib.mlab import find

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=2,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0;

WIDTH = 640
HEIGHT = 480
LIMIT = 201

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
surf = pygame.Surface(screen.get_size(), 0, screen)
surf.fill(pygame.Color("black"))
screen.blit(surf, (0, 0))
random.seed()

circles = []

factors = []

def update_factors(tab):
    i = 0
    k = 0
    j = len(tab)-1
    while (i < j):
        tab[i] = tab[j] = k
        k = k + 2 / len(tab)
        i = i + 1
        j = j - 1
    if (i == j):
        tab[i] = 1



def getcolor(freq):
    if 668 <= freq:
        return (176, 9, 176)
    elif 631 <= freq:
        return (21, 101, 176)
    elif 606 <= freq:
        return (57, 219, 212)
    elif 526 <= freq:
        return (43, 240, 20)
    elif 508 <= freq:
        return (255, 243, 16)
    elif 484 <= freq:
        return (255, 171, 12)
    elif 400 <= freq:
        return (255, 27, 5)
    else:
        return (232,232,212)



while (1): #go for a few seconds
    time.sleep(1/30)
    surf.fill(pygame.Color("black"))
    screen.blit(surf, (0,0))
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    c = int(Pitch(stream.read(CHUNK)))
    col = pygame.Color(getcolor(c)[0], getcolor(c)[1], getcolor(c)[2])
    if (len(circles)>=LIMIT):
        circles.pop(0)
    else :
        factors.append(0)
        update_factors(factors)
    circles.append([screen, col, (surf.get_width()/2, surf.get_height()/2), int(500*abs(peak)/2**16)])

    surfaces = []
    for i in range(len(circles)):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        circles[i][1].a = 255 * factors[i]
        pygame.draw.circle(s, circles[i][1],circles[i][2],int(circles[i][3] * factors[i]), int(min(circles[i][3] * factors[i], 1)))
        surfaces.append(s)

    for i in range(len(surfaces)):
        screen.blit(surfaces[i], (0,0))

    print len(circles)
    pygame.display.flip()
    bars="#"*int(50*peak/2**16)
    print("%05d %s"%(peak,bars))


stream.stop_stream()
stream.close()
p.terminate()
