#!/usr/bin/env python
import sys,os
import pygame

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

import pygame
pygame.init()
#pygame.display.set_mode((200,100))
pygame.mixer.music.load("warning0.wav")
pygame.mixer.music.play(0)

#clock = pygame.time.Clock()
#clock.tick(10)
while pygame.mixer.music.get_busy():
    pygame.event.poll()
    #clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()