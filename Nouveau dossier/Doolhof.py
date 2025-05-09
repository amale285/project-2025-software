# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 09:48:08 2025

@author: eliag
"""
import pygame 
import random 



#elementen in het doolhof

    
def beweging_speler(speler_x, speler_y): 
    if event.type == pygame.KEYDOWN:
            toets = event.key
        #if 
        
def doolhof(screen):     
    y = 70
    leeg= ""
    mogelijke_knoppen = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d, leeg]
    elementen_doolhof = []
    
    for i in range(4): 
        x = 50
        rij = []
      
        willekeurige_elementen = random.choices(mogelijke_knoppen, k=30)
        elementen_doolhof.append(willekeurige_elementen)
        
        for k in willekeurige_elementen:
            if k == pygame.K_LEFT: 
                knopje = pygame.image.load("left_arrow.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_RIGHT: 
                knopje = pygame.image.load("right arrow.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje,(x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_UP: 
                knopje = pygame.image.load("pijltje_boven.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_DOWN: 
                knopje = pygame.image.load("pijltje_beneden.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_q: 
                knopje = pygame.image.load("q.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_z: 
                knopje = pygame.image.load("z.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_s: 
                knopje = pygame.image.load("s.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == pygame.K_d: 
                knopje = pygame.image.load("d.png")
                knopje = pygame.transform.scale(knopje, (20, 20))
                screen.blit(knopje, (x,y))
                rij.append(k)
                x+= 20
            elif k == leeg: 
                x+= 20
                rij.append(k)
        y += 50 
    return print(elementen_doolhof )
 
                
    
        
