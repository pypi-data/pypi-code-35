import pygame, sys, time, random
from pygame.locals import *
import numpy as np
from neuralNetworkGA import *
import shelve
import os

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color) 
    screen.blit(imgText, (x,y))

def left_win():
    text = "Left Player Won!"
    font1 = pygame.font.Font(None, 30)
    print_text(font1, 200, 100, text)

def right_win():
    text = "Right Player Won!"
    font1 = pygame.font.Font(None, 30)
    print_text(font1, 200, 100, text)

class leftplayer():
    def __init__(self):
        self.x = 95
        self.y = 275
        self.long = 50
        self.thick = 10
        self.score = 0
        self.terminal = False
        self.color = (255,255,255)
        

class ballgame():
    def __init__(self,gen,population):
        self.gen = gen
        self.leftplayer = []
        self.population = population
        #evolution.population
        for i in range(self.population):
            lp = leftplayer()
            if i % 3 == 0:
                lp.color = ( 256//(self.population//3) * (i//(self.population//3)) ,80,80)
            elif i % 3 == 1:
                lp.color = ( 80, 256//(self.population//3) * (i//(self.population//3)) ,80)
            else:
                lp.color = ( 80,80, 256//(self.population//3) * (i//(self.population//3)))
            self.leftplayer.append(lp)

        self.screenwidth = 800
        self.screenheight = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenwidth,self.screenheight))
        pygame.display.set_caption("ballgame")
        
        self.right_player_pos_x = 695
        self.right_player_pos_y = 0
        self.right_player_long = 600
        self.right_player_thick = 10

        self.ball_pos_x = random.randint(self.right_player_pos_x-45,self.right_player_pos_x-25)
        self.ball_pos_y = random.randint(0,self.screenheight-10)
        
        self.vel_x = 3
        self.vel_y = 2

        self.deadline = 85
        self.player_vel_y = 3

        self.ballsize = 10
        self.clock = pygame.time.Clock()

    def start(self):
        self.clock.tick(1000)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        
        self.screen.fill((0,0,0))
        
        
        self.ball_pos_x += self.vel_x
        self.ball_pos_y += self.vel_y

        
        for i in range(len(self.leftplayer)):
            res = self.gen[i].put_inputs([self.ball_pos_x,self.ball_pos_y,self.leftplayer[i].y])
            act = np.argmax(res)
            
            if self.leftplayer[i].y < 0 :
                self.leftplayer[i].y = 0
            elif self.leftplayer[i].y > self.screenheight - self.leftplayer[i].long:
                self.leftplayer[i].y = self.screenheight - self.leftplayer[i].long
            else:
                if act == 1:
                    self.leftplayer[i].y -= self.player_vel_y
                else:
                    self.leftplayer[i].y += self.player_vel_y

        
        if self.ball_pos_x < self.deadline:
            #right_win()
            self.vel_x = 0
            self.vel_y = 0
            for i in range(len(self.leftplayer)):
                self.leftplayer[i].terminal = True
        
        
        if self.ball_pos_x >= self.right_player_pos_x - self.ballsize:
            self.vel_x = -self.vel_x

    
        for i in range(len(self.leftplayer)):    
            if self.ball_pos_x <= self.leftplayer[i].x + self.leftplayer[i].thick:
                if self.leftplayer[i].y - self.ballsize <= self.ball_pos_y <= self.leftplayer[i].y + self.leftplayer[i].long + self.ballsize:
                
                    self.leftplayer[i].score += 1
                else:
                    self.leftplayer[i].terminal = True
        
        
        for i in range(len(self.leftplayer)):    
            if self.ball_pos_x <= self.leftplayer[i].x + self.leftplayer[i].thick \
                and self.leftplayer[i].y - self.ballsize <= self.ball_pos_y <= self.leftplayer[i].y + self.leftplayer[i].long + self.ballsize:        
                self.vel_x = -self.vel_x
                break

        if self.ball_pos_y > self.screenheight - self.ballsize or self.ball_pos_y < 0:
            self.vel_y = -self.vel_y

        color = (255,255,255)
        ballpos = self.ball_pos_x,self.ball_pos_y, self.ballsize, self.ballsize
        pygame.draw.rect(self.screen, color, ballpos, 0)
        
        for i in range(len(self.leftplayer)):
            if self.leftplayer[i].terminal == False:
                lplayer_pos = self.leftplayer[i].x, self.leftplayer[i].y, self.leftplayer[i].thick, self.leftplayer[i].long
                pygame.draw.rect(self.screen, self.leftplayer[i].color, lplayer_pos, 0)
        rplayer_pos = self.right_player_pos_x, self.right_player_pos_y, self.right_player_thick, self.right_player_long
        pygame.draw.rect(self.screen, color, rplayer_pos, 0)
        pygame.display.flip()

        score = []
        for i in range(len(self.leftplayer)):
            score.append(self.leftplayer[i].score)
        return score

population = 50
ai = NeuroGA(3,[32],2,population)
gen = ai.next_gen_networks()
generation = 0
while True:
    generation += 1
    game = ballgame(gen,population)
    alldead = False
    while not alldead:
        score = game.start()
        alldead = True
        alives = 0
        for i in range(len(game.leftplayer)):
            if game.leftplayer[i].terminal == False:
                alives += 1
                alldead = False
                #print(game.leftplayer[i].score)
                maxscore = game.leftplayer[i].score
        print("alive:{}, generation:{}, score:{}".format(alives, generation, maxscore), end='\r')
    for i in range(len(game.leftplayer)):
        if game.leftplayer[i].score > 50:
            print('adsf')
            savenet(gen[i],1)
        ai.mark_score(game.leftplayer[i].score,gen[i])
    gen = ai.next_gen_networks()