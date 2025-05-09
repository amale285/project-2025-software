# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 15:13:57 2025

@author: eliag
"""
import pygame 

class Knop(): 
    def __init__(self,positieX_knop, positieY_knop,  breedte, hoogte, text): 
        self.breedte = breedte
        self.hoogte = hoogte 
        self.text = str(text)
        self.positieY_knop = positieY_knop
        self.positieX_knop = positieX_knop
    def teken(self, screen): 
        pygame.draw.rect(screen, (255, 204, 255), (self.positieX_knop, self.positieY_knop,self.breedte,self.hoogte))
        font_size = 35
        font = pygame.font.Font(None, size=font_size)
        screen.blit(font.render(self.text, True, (0,0,0)),dest=(self.positieX_knop + self.breedte // 2- 20, self.positieY_knop + self.hoogte // 2-15))
    def klik(self, pos): 
         if self.positieX_knop <= pos[0] <= self.positieX_knop + self.breedte and self.positieY_knop <= pos[1] <= self.positieY_knop + self.hoogte:
            return True     
        
        
        
def voorpagina(screen):
    running = True
    clock = pygame.time.Clock()
    achtergrond = pygame.image.load("pachtergrond_voorpagina.png")
    achtergrond = pygame.transform.scale(achtergrond, (1000, 500))
    start_knop = Knop(375,250,200,75, "Start")
    while running:
        clock.tick(20)
        screen.blit(achtergrond, (0,0))
        start_knop.teken(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if start_knop.klik(pos): 
                        running = False
        pygame.display.flip()

   
def keuze(screen):
    running = True
    clock = pygame.time.Clock()
    achtergrond = pygame.image.load("pachtergrond_voorpagina.png")
    achtergrond = pygame.transform.scale(achtergrond, (1000, 500))
    gemakkelijk_knop = Knop(375,100,200,75, "EASY")
    MID_knop = Knop(375,250,200,75, "niet zo moeilijk")
    moeilijke_knop = Knop(375,400,200,75, "HARDCORE")
    resultaat = ""
    while running:
        clock.tick(20)
        screen.blit(achtergrond, (0,0))
        gemakkelijk_knop.teken(screen)
        MID_knop.teken(screen)
        moeilijke_knop.teken(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if gemakkelijk_knop.klik(pos):
                        achtergrond = pygame.image.load("achtergrond_gemakkelijk.png")
                        achtergrond = pygame.transform.scale(achtergrond, (1000, 500))
                        resultaat = "EASY"
                        screen.blit(achtergrond, (0,0))
                        running = False
                    elif MID_knop.klik(pos): 
                        achtergrond = pygame.image.load("achtergrond_gemiddeld.png")
                        achtergrond = pygame.transform.scale(achtergrond, (1000, 500))
                        resultaat = "MEDIUM"
                        running = False
                    elif moeilijke_knop.klik(pos): 
                        achtergrond = pygame.image.load("achtergrond_moeilijk.png")
                        achtergrond = pygame.transform.scale(achtergrond, (1000, 500))
                        resultaat = "MOEILIJK"
                        running = False
        pygame.display.flip()                 
    return achtergrond, resultaat      
       
  
