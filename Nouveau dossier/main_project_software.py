# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 20:00:03 2025

@author: eliag
"""

import pygame
#from Doolhof import doolhof 
import random 
from voorpagina_game import voorpagina, keuze
from maze import draw_maze, create_maze, BFS_oplossing_maze

pygame.init()  

screen = pygame.display.set_mode([1000, 500])
clock = pygame.time.Clock()

voorpagina(screen)
screen.fill((255,255,255))
achtergrond = keuze(screen)
pygame.mixer.music.load("never gonna give you up v2.mp3")
pygame.mixer.music.play(-1) 
#achter = pygame.image.load("spel_achtergrond.png")
#achter = pygame.transform.scale(achter, (1000, 500))


class Figuur():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def botsing(self, andereFiguur):
        
        
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.breedte
        y2 = self.y + self.hoogte
            
        andereFiguurx1 = andereFiguur.x
        andereFiguury1 = andereFiguur.y
        andereFiguurx2 = andereFiguur.x + andereFiguur.breedte
        andereFiguury2 = andereFiguur.y + andereFiguur.hoogte
        # https://silentmatt.com/rectangle-intersection/

        if x1 < andereFiguurx2 and x2 > andereFiguurx1 and y1 < andereFiguury2 and y2 > andereFiguury1:
            return True #enkel gedefinieerd tussen 2 rechthoeken 
        else:
            return False

class Speler(Figuur): 
    def __init__(self, x, y, breedte, hoogte):  
        super().__init__(x, y)
        self.breedte = breedte 
        self.hoogte = hoogte

    def tekenenen(self):
        #pygame.draw.rect(screen, (255, 204, 255), (self.x, self.y, self.breedte, self.hoogte))
        player = pygame.image.load("player2.png")
        player = pygame.transform.scale(player, (self.breedte, self.hoogte)).convert_alpha()
        screen.blit(player, (self.x, self.y))
    def beweging(self,  maze, snelheid): 
        vx = 0
        vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            vx += snelheid 
        if keys[pygame.K_q]:
            vx -= snelheid
        if keys[pygame.K_s]:
            vy += snelheid
        if keys[pygame.K_z]:
            vy -= snelheid
        print(vx)
        nieuwe_x = self.x + vx
        nieuwe_y = self.y + vy
        kolom = (nieuwe_x - 50) // 20  
        rij = (nieuwe_y - 15) // 20 

        if 0 <= rij < len(maze) and 0 <= kolom < len(maze[0]):
            if maze[rij][kolom] == 0:  
                self.x = nieuwe_x
                self.y = nieuwe_y
    #        if speler.botsing(maze) == True: 
    #           vx = 0
    #           vy = 0
    # FOUT MOET blokje per blokje bewegen 
    
    """ nieuw_x = (self.x + vx) //20
        nieuw_y = (self.y + vy) //20
        if maze[nieuw_x, nieuw_y] == 0: 
            self.x += vx
            self.y += vy"""
    

        

 

        
#doolhof(screen)

running = True
speler = Speler(51,35, 18,18)
lijst_personages = [speler]

maze = create_maze(23,38,30)
while not BFS_oplossing_maze(maze): 
    maze = create_maze(23,38,30)
    

while running:
    clock.tick(20)
    screen.blit(achtergrond, (0, 0))
    draw_maze(screen, maze, 50, 15)
    pygame.draw.rect(screen, (255, 204, 255), (len(maze)-2, len(maze[0])-1, 20, 20))

    for object in lijst_personages: 
        if hasattr(object, "beweging"):
            object.beweging( maze, 7)
        if hasattr(object, "tekenenen"):
            object.tekenenen()
       
   
    if speler.x//20 == (len(maze)-2) and speler.y//20== (len(maze[0])-1): 
        print("gewonnen")
        screen.fill((255,204,255))
         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN:
            
        
   
    
    pygame.display.flip()
pygame.mixer.music.stop()
pygame.quit()