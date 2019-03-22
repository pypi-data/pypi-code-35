import pygame, sys, time, random
from pygame.locals import *

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    #pygame show text, then display
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


class ballgame():
    def __init__(self):
        self.leftplayer = leftplayer()
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

        self.player_vel_y = 3

        self.ballsize = 10

    def start(self,act):
        self.leftplayer.terminal = False
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        #clear screen
        self.screen.fill((0,0,0))

        #move ball
        self.ball_pos_x += self.vel_x
        self.ball_pos_y += self.vel_y

    # keep player within screen
        if self.leftplayer.y < 0 :
            self.leftplayer.y = 0
        elif self.leftplayer.y > self.screenheight - self.leftplayer.long:
            self.leftplayer.y = self.screenheight - self.leftplayer.long
        else:
            if act == 1:
                self.leftplayer.y -= self.player_vel_y
            else:
                self.leftplayer.y += self.player_vel_y

        if self.ball_pos_x < self.leftplayer.x:
            #right_win()
            self.leftplayer.score = 0
            self.ball_pos_x = random.randint(self.right_player_pos_x-45,self.right_player_pos_x-25)
            self.ball_pos_y = random.randint(0,self.screenheight-10)
            #self.vel_x = 0
            #self.vel_y = 0
            self.leftplayer.terminal = True

        if self.ball_pos_x >= self.right_player_pos_x - self.ballsize:
            self.vel_x = -self.vel_x
        if self.ball_pos_x <= self.leftplayer.x + self.leftplayer.thick \
            and self.leftplayer.y - self.ballsize <= self.ball_pos_y <= self.leftplayer.y + self.leftplayer.long + self.ballsize:
        #left player get ball
            self.leftplayer.score += 1
            self.vel_x = -self.vel_x


        if self.ball_pos_y > self.screenheight - self.ballsize or self.ball_pos_y < 0:
        # wall get ball
            self.vel_y = -self.vel_y

    # paint
        color = (255,255,255)
        ballpos = self.ball_pos_x,self.ball_pos_y, self.ballsize, self.ballsize
        pygame.draw.rect(self.screen, color, ballpos, 0)
    # draw player
        lplayer_pos = self.leftplayer.x, self.leftplayer.y, self.leftplayer.thick, self.leftplayer.long
        pygame.draw.rect(self.screen, color, lplayer_pos, 0)
    #
        rplayer_pos = self.right_player_pos_x, self.right_player_pos_y, self.right_player_thick, self.right_player_long
        pygame.draw.rect(self.screen, color, rplayer_pos, 0)
        pygame.display.flip()
        inputs = [self.ball_pos_x,self.ball_pos_y,self.leftplayer.y]
        return inputs,self.leftplayer.score,self.leftplayer.terminal
