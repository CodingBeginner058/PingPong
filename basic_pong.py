from curses import window

import pygame
import math
import random
import time

pygame.init()
pygame.mixer.init()

class Design:
    def __init__(self, screen, windowSize, bg_colour):
        self.screen = screen
        self.windowSize = windowSize
        self.drop_music = pygame.mixer.Sound("Python/PONG/music/drop.mp3")
        self.default_bg = bg_colour       

    def draw_words(self, words, loc, font = ["sys", True, ("font-name", 100, False, False)], spacing=(False, 0)):

        if font[1]:
            if font[0] == "file":
                font = pygame.font.Font(*font[2])
            elif font[0] == "sys":
                font = pygame.font.SysFont(*font[2])
        else:
            font = font[2]

        if spacing[0]:
            for letter in words:
                letterScreen = font.render(letter, True, (255, 255, 255))
                letterWidth = letterScreen.get_width()
                letterHeight = letterScreen.get_height()
                self.screen.blit(letterScreen, (loc[0], loc[1]))
                loc[0] += letterWidth + spacing[1]

                    
        else:
            wordScreen = font.render(words, True, (255, 255, 255))
            wordrWidth = wordScreen.get_width()
            wordHeight = wordScreen.get_height()
            self.screen.blit(wordScreen, loc)

    def draw_dropping_text(self, font = ["sys", True, ("font-name", 100, False, False)], x_loc = 860, y_bounds = (300, 900), words = "maybe, just maybe, enter what to print", speed = 1, skip_enable = False, drop_sound = False):
        anim_done = False
        self.draw_bg()

        if font[1]:
            if font[0] == "file":
                font = pygame.font.Font(*font[2])
            elif font[0] == "sys":
                font = pygame.font.SysFont(*font[2])
        else:
            font = font[2]


        for letter in words:
            letterScreen = font.render(letter, True, (255, 255, 255))
            letterWidth = letterScreen.get_width()
            letterHeight = letterScreen.get_height()
            for y in range(y_bounds[0] - letterHeight//2, y_bounds[1] + 1 - letterHeight//2, speed):

                #check for key press

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if skip_enable and event.type == pygame.KEYDOWN:
                        return True
                
                pygame.draw.rect(self.screen, self.default_bg, ((x_loc, y-speed, letterWidth, letterHeight+speed)))
                self.screen.blit(letterScreen, (x_loc, y))
                pygame.display.flip()
            x_loc += letterWidth + 20
            if drop_sound:
                self.drop_music.play()

        return True
  
    def draw_interactable_button(self, loc, dims, colour, font, text, mouse, flags):
       #possible flags: outline, 
        letterScreen = font.render(text, True, colour)
        textHitbox = pygame.rect.Rect(*loc, *dims)
        mouseHitbox = pygame.rect.Rect(*mouse, 1, 1)
        if not textHitbox.colliderect(mouseHitbox):
            self.screen.blit(letterScreen, *loc)
        else:
            self.screen.blit(letterScreen, (loc[0] - 10, loc[1] - 10))

    def draw_input_box(self, loc, dims, colour):
        pass

    def draw_bg(self):
        self.screen.fill(self.default_bg)

class Game:
    def __init__(self, windowSize = (1920, 1080)):
        pygame.mixer.music.load("Python/PONG/music/background.mp3")
        # define window
        self.windowSize = windowSize
        self.windowWidth, self.windowHeight = windowSize
        if windowSize == (1920, 1080):
            self.screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(windowSize)
        pygame.display.set_caption("PING-PONG 🏓🏐")

        # game variables
        self.running = True
        self.gameStarted = False
        self.menuScreen = False
        self.gameStartedAnim = False
        self.default_bg = "#061A52"
        self.Design = Design(self.screen, self.windowSize, self.default_bg)
        self.clock = pygame.time.Clock()
        self.fps = 60
        

        # fonts
        self.title_font = pygame.font.Font("Python/PONG/font/PressStart2P-Regular.ttf", 96)

    def GameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.gameStarted and not self.pause:
                pass

            self.Draw()

    def Draw(self):
        if not self.gameStarted:
            self.Design.draw_bg()
            self.GameStart()
        elif self.menuScreen:
            self.Design.draw_bg()
        else:
            self.Design.draw_bg()
        pygame.display.flip()

    def GameStart(self):
        font=self.title_font        
        if not self.gameStartedAnim:
            self.gameStartedAnim = self.Design.draw_dropping_text(  font=["file", False, font], 
                                                                    x_loc=self.windowWidth//5,
                                                                    y_bounds=(0, self.windowHeight//2),
                                                                    words="PING-PONG",
                                                                    speed= 2,
                                                                    skip_enable=True,
                                                                    drop_sound=True)
            self.startScreenTime = pygame.time.get_ticks()

        #clear and freeze the ping pong logo
        self.Design.draw_bg()
        self.Design.draw_words( "PING-PONG", [self.windowWidth//5, self.windowHeight//2], ["file", False, font], (True, 20))
        self.Design.draw_words( "press anything to continue", [self.windowWidth - 1000, self.windowHeight - 200])

        # Wait 1 second before accepting keyboard input
        currentTime = pygame.time.get_ticks()
        if currentTime - self.startScreenTime < 1000: return

        #check if key pressed then continue
        keys = pygame.key.get_pressed()
        if any(keys) and not( keys[pygame.K_LALT] and keys[pygame.K_TAB]):
            pass

            # self.gameStarted = True
            # pygame.mixer.music.set_volume(0.5)
            # pygame.mixer.music.play(-1)

    def Pause(self):
        design = Design(self.screen, self.windowSize, "black")
        font = self.title_font
        design.draw_bg()
        design.draw_words("PING PONG", (self.windowSize[0] // 10, self.windowSize[1] // 5), )

class Ball:
    def __init__(self):
        pass

class Paddle:
    def __init__(self, controls, dims, loc, colour = "white", speed = 10):
        #Contorls in order (True, UP, DOWN); where the first flag is for 2p, and mouse control
        self.controls = controls
        self.dims = dims
        self.loc = loc
        self.colour = colour
        self.hitbox = pygame.rect.Rect(*loc, *dims)
        self.speed = speed

    def checkMovement(self, keys, mouse = False):
        #Check if mouse is enabled()
        if not self.controls[0]:
            _, y = self.hitbox.center
            #move up or down based on mouse position
            if mouse[1] < y and mouse[1] > 0:
                self.hitbox.centery -= self.speed
            elif mouse[1] > y and mouse[1] < windowSize[1]:
                self.hitbox.centery += self.speed
        else:
            #move up or down based on what keys are pressed
            if keys[self.controls[1]]:
                self.hitbox.centery -= self.speed
            elif keys[self.controls[2]]:
                self.hitbox.centery += self.speed

    def draw_paddle(self, screen):
        pygame.draw.rect(screen, self.colour, self.hitbox)

global windowSize                             
windowSize = (1920, 1080)                
     
game = Game(windowSize)
game.GameLoop() 