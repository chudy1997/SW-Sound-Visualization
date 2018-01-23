import random
import struct
import sys

import numpy as np
import pyaudio
import pygame
import time

CHUNK = 2 ** 11
RATE = 44100
FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
nFFT = 512
WIDTH = 960
HEIGHT = 720
LIMIT = 11
CHANNELS = 1
CONSTANCE = 700


def get_color(freq):
    if 700 <= freq:
        return (176, 9, 176)
    elif 600 <= freq:
        return (21, 101, 176)
    elif 500 <= freq:
        return (57, 219, 212)
    elif 400 <= freq:
        return (43, 240, 20)
    elif 300 <= freq:
        return (255, 243, 16)
    elif 200 <= freq:
        return (255, 171, 12)
    elif 100 <= freq:
        return (255, 27, 5)
    else:
        return (232, 232, 212)


def get_freq(signal, max_y):
    y = np.array(struct.unpack("%dh" % (len(signal) / SAMPLE_SIZE), signal)) / max_y
    
    if (CHANNELS == 2):
        y_L = y[::2]
        y_R = y[1::2]
        Y_L = np.fft.fft(y_L, nFFT)
        Y_R = np.fft.fft(y_R, nFFT)

        Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))
        
        return (RATE / 2.0) * (abs(np.argmax(Y) - len(Y) / 2.0)) / (len(Y) / 2.0)  
            
    else:
        Y = np.fft.fft(y, nFFT)
        Y = abs(Y)
        
    
        print ((RATE / 2.0) * np.argmax(Y) / len(Y))
        
        return (RATE / 2.0) * np.argmax(Y) / len(Y)
        
        
def update_factors(tab):
    for i in range(len(tab)):
        tab[i] = (1.0 * i) / len(tab)


def update_factors1(tab):
    i = 0
    k = 0
    j = len(tab) - 1
    while i < j:
        tab[i] = tab[j] = k
        k = k + 2 / len(tab)
        i = i + 1
        j = j - 1
    if i == j:
        tab[i] = 1


def init():
    pya = pyaudio.PyAudio()
    pygame.init()
    stream = pya.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    max_y = 2.0 ** (pya.get_sample_size(FORMAT) * 8 - 1)
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render("Hello, say or play something to see magic!", True, (0, 128, 0))
    screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
    pygame.display.flip()
    time.sleep(3)
    surf = pygame.Surface(screen.get_size(), 0, screen)
    surf.fill(pygame.Color("black"))
    screen.blit(surf, (0, 0))
    random.seed()
    circles = []
    factors = []
    
    return pya, stream, max_y, screen, surf, circles, factors, font


def close(pya, stream):
    screen.fill((0, 0, 0))
    screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
    pygame.display.flip()
    stream.stop_stream()
    stream.close()
    pya.terminate()
    time.sleep(1)
    pygame.quit()
    sys.exit()


def loop(surf, screen, circles, factors, max_y):
    surf.fill(pygame.Color("black"))
    screen.blit(surf, (0, 0))
    raw_data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.fromstring(raw_data, dtype=np.int16)
    peak = np.average(np.abs(data)) * 2
    c = int(get_freq(raw_data, max_y))
    col = pygame.Color(get_color(c)[0], get_color(c)[1], get_color(c)[2])
    if len(circles) >= LIMIT:
        circles.pop(0)
    else:
        factors.append(0)
        update_factors(factors)
    
    circles.append(
        [screen, col, (int(surf.get_width() / 2), int(surf.get_height() / 2)), int(CONSTANCE * abs(peak) / 2 ** 16)])

    surfaces = []
    for i in range(len(circles)):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        circles[i][1].a = int(255 * factors[i])
        pygame.draw.circle(s, circles[i][1], circles[i][2], int(circles[i][3] * factors[i]),
                           int(min(circles[i][3] * factors[i], 1)))
        surfaces.append(s)

    for i in range(len(surfaces)):
        screen.blit(surfaces[i], (0, 0))

    pygame.display.flip()


if __name__ == "__main__":
    pya, stream, max_y, screen, surf, circles, factors, font = init()
    text = font.render("See you again!", True, (0, 128, 0))

    while (1):
        # for event in pygame.event.get():
          #   if event.type == pygame.QUIT:
            #     close(pya, stream)
        loop(surf, screen, circles, factors, max_y)
