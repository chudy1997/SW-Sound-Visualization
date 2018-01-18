import pyaudio as pya
import numpy as np
import time
import math
import struct
import pygame
import random
from matplotlib.mlab import find

CHUNK = 2048 # number of data points to read at a time
RATE = 44100# time resolution of the recording device (Hz)
WIDTH = 640
HEIGHT = 480
LIMIT = 10


def init():
    pa=pya.PyAudio()
    sIn=pa.open(format=pya.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    surf = pygame.Surface(screen.get_size(), 0, screen)
    screen.blit(surf, (0, 0))
    random.seed()
    circles = []
    factors = []
    
    return pa, sIn, screen, surf, circles, factors    
	

def clean(pa, sIn):
	sIn.stop_stream()
	sIn.close()
	pa.terminate()
	
	
def pitch(signal):
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing))
    return int(round(len(index) *RATE /(2*np.prod(len(signal)))))


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
    elif 200 <= freq:
        return (255, 27, 5)
    else:
        return (232,232,212)
        
    
def loop(sIn, screen, surf, circles, factors):
    surf.fill(pygame.Color("black"))
    screen.blit(surf, (0,0))
    
    data = np.fromstring(sIn.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
    freq = pitch(data)
    peak = np.average(np.abs(data))*2
    color = pygame.Color(getcolor(freq)[0], getcolor(freq)[1], getcolor(freq)[2])
    
    if (len(circles) >= LIMIT):
        circles.pop(0)
        
    circles.append([screen, color, (surf.get_width()/2, surf.get_height()/2), int(500*abs(peak)/2**15)])
    surfaces = []
    for i in range(len(circles)):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        circles[i][1].a = 255 * i/len(circles)
        pygame.draw.circle(s, circles[i][1],circles[i][2], circles[i][3], 1)
        
        surfaces.append(s)

    for i in range(len(surfaces)):
        screen.blit(surfaces[i], (0,0))

    pygame.display.flip()
    bars="#"*int(50*peak/2**15)


if __name__ == "__main__":
    #init
    pa, sIn, screen, surf, circles, factors = init()

    #read, process and visualize
    while True:
        loop(sIn, screen, surf, circles, factors)

    #clean
    clean(pa, sIn)
    
