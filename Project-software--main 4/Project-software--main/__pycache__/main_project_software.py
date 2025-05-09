# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 20:00:03 2025

@author: eliag
"""

import pygame
import random 
from voorpagina_game import voorpagina, keuze
from maze import draw_maze, create_maze, BFS_oplossing_maze, BFS_pad
pygame.init()  

screen = pygame.display.set_mode([1000, 500])
clock = pygame.time.Clock()

voorpagina(screen)
screen.fill((255,255,255))
achtergrond, resultaat = keuze(screen)
pygame.mixer.music.load("never gonna give you up.mp3.mp3")
pygame.mixer.music.play(-1) 



class Figuur():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def botsing(self, andereFiguur):
        if(isinstance(self,Bal)): #x,y is midden van de cirkel en voor de   botsing willen we linker en rechter bovenhoek.
            x1 = self.x-self.radius
            y1 = self.y-self.radius
            x2 = self.x + self.radius
            y2 = self.y + self.radius
        else: #voor een rechthoek is x en y de linkerbovenhoek
            x1 = self.x
            y1 = self.y
            x2 = self.x + self.breedte
            y2 = self.y + self.hoogte
        if(isinstance(andereFiguur,Bal)):
            andereFiguurx1 = andereFiguur.x-andereFiguur.radius
            andereFiguury1 = andereFiguur.y-andereFiguur.radius
            andereFiguurx2 = andereFiguur.x + andereFiguur.radius
            andereFiguury2 = andereFiguur.y + andereFiguur.radius
        else:
            andereFiguurx1 = andereFiguur.x
            andereFiguury1 = andereFiguur.y
            andereFiguurx2 = andereFiguur.x + andereFiguur.breedte
            andereFiguury2 = andereFiguur.y + andereFiguur.hoogte
            # https://silentmatt.com/rectangle-intersection/
        if x1 < andereFiguurx2 and x2 > andereFiguurx1 and y1 < andereFiguury2 and y2 > andereFiguury1:
            return True
        else:
            return False


class Speler(Figuur): 
    def __init__(self, x, y, breedte, hoogte):  
        super().__init__(x, y)
        self.breedte = breedte 
        self.hoogte = hoogte

    def tekenenen(self):
        player = pygame.image.load("hamburger.png")
        player = pygame.transform.scale(player, (self.breedte, self.hoogte)).convert_alpha()
        screen.blit(player, (self.x, self.y))

    def beweging(self,  maze, snelheid): 
        vx = 0
        vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  
            vx = 1
        if keys[pygame.K_q]:  
            vx = -1
        if keys[pygame.K_s]: 
            vy = 1
        if keys[pygame.K_z]:
            vy = -1
        nieuwe_x = self.x + vx * 20
        nieuwe_y = self.y + vy * 20
        rij = (nieuwe_y- 15) // 20
        kolom = (nieuwe_x - 50) // 20
        if 0 <= rij < len(maze) and 0 <= kolom < len(maze[0]):
            if maze[rij][kolom] ==0: 
                self.x = nieuwe_x
                self.y = nieuwe_y
        #if 0 <= rij < len(maze) and 0 <= kolom < len(maze[0]):
        #    if maze[rij][kolom] == 0:  
        #        self.x = nieuwe_x
         #       self.y = nieuwe_y
    #        if speler.botsing(maze) == True: 
    #           vx = 0
    #           vy = 0
    # FOUT MOET blokje per blokje bewegen 
    
    """ nieuw_x = (self.x + vx) //20
        nieuw_y = (self.y + vy) //20
        if maze[nieuw_x, nieuw_y] == 0: 
            self.x += vx
            self.y += vy"""
    
class BotSpeler(Figuur):
    def __init__(self, x, y, breedte, hoogte, pad, snelheid):
        super().__init__(x, y)
        self.breedte = breedte
        self.hoogte = hoogte
        self.pad = pad
        self.index = 0
        self.timer = 0
        self.snelheid = snelheid

    def tekenenen(self):
        try:
            bot_img = pygame.image.load("cat bot.png")
            bot_img = pygame.transform.scale(bot_img, (self.breedte, self.hoogte)).convert_alpha()
            screen.blit(bot_img, (self.x, self.y))
        except:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.breedte, self.hoogte))

    def beweging(self, maze, _): 
        if self.index < len(self.pad):
            self.timer += 1
            if self.timer % self.snelheid == 0:
                i, j = self.pad[self.index]
                self.x = j * 20 + 50
                self.y = i * 20 + 15
                self.index += 1
                
class Bal(Figuur): 
    def __init__(self, x,y, straal, snelheid): 
        super.__init__(x,y)
        self.straal = straal
        self.snelheid = snelheid
    def draw_bal(self): 
        pygame.draw.rect(screen, (225, 204, 255), (self.x, self.y, self.straal))
    def beweging_bal(self):
        
        
        x_0 = 19
        y_0 = 11
class PowerUp(Figuur):
    def __init__(self, x, y, soort):
        super().__init__(x, y)
        self.breedte = 20
        self.hoogte = 20
        self.soort = soort  # "snelheid" of "vertrager"
        self.actief = True

    def teken(self):
        if self.actief:
            if self.soort == "snelheid":
                kleur = (0, 255, 0)  # Groen
            else:
                kleur = (255, 0, 0)  # Rood
            pygame.draw.rect(screen, kleur, (self.x, self.y, self.breedte, self.hoogte))

    def controleer_botsing(self, speler):
        return (
            speler.x < self.x + self.breedte and
            speler.x + speler.breedte > self.x and
            speler.y < self.y + self.hoogte and
            speler.y + speler.hoogte > self.y
        )


maze = create_maze(23,44, 30) #hoogte , lengte, blokje 
while not BFS_oplossing_maze(maze): 
    maze = create_maze(23,44,30)

pad = BFS_pad(maze)
speler = Speler(51, 35, 18, 18)

if resultaat == "MEDIUM":
    BotSpeler.snelheid = 8
elif resultaat == "EASY":
    BotSpeler.snelheid = 100
else:
    BotSpeler.snelheid = 100

bot = BotSpeler(50, 15, 18, 18, pad, BotSpeler.snelheid)
lijst_personages = [speler, bot]
powerups = []
for i in range(5):  # 5 power-ups
    while True:
        kolom = random.randint(0, len(maze[0])-1)
        rij = random.randint(0, len(maze)-1)
        if maze[rij][kolom] == 0:
            x = kolom * 20 + 50
            y = rij * 20 + 15
            soort = random.choice(["snelheid", "vertrager"])
            powerups.append(PowerUp(x, y, soort))
            break

verandering_maze = False 
running = True
           
powerup_timer = 0
while running:
    clock.tick(20)
    screen.blit(achtergrond, (0, 0))
    draw_maze(screen, maze, 50, 15)  #screen, maze, x_0, y_0
    
    for obj in lijst_personages: 
        if hasattr(obj, "beweging"):
            obj.beweging(maze, 7)
        if hasattr(obj, "tekenenen"):
            obj.tekenenen()
    for powerup in powerups:
        powerup.teken()

    if speler.x ==200 and not verandering_maze: 
        maze = create_maze(23, 23, 30)
        while not BFS_oplossing_maze(maze): 
            maze = create_maze(23, 23, 30)
            draw_maze(screen, maze, 200, 15) 
        verandering_maze = True 
    for powerup in powerups:
        if powerup.actief and powerup.controleer_botsing(speler):
            if powerup.soort == "snelheid":
                speler.snelheid = 2
                powerup_timer = pygame.time.get_ticks()
            elif powerup.soort == "vertrager":
                bot.snelheid += 5
                powerup_timer = pygame.time.get_ticks()
            powerup.actief = False

    # Powerup effecten resetten na 5 seconden
    if powerup_timer != 0 and pygame.time.get_ticks() - powerup_timer > 5000:
        speler.snelheid = 1
        if bot.snelheid > 5:
            bot.snelheid -= 5
        powerup_timer = 0

      
    speler_kolom = (speler.x - 15) // 20
    speler_rij = (speler.y - 50) // 20
    if speler_kolom == len(maze)-1 and speler_rij == len(maze[0])-1:
        print("Gewonnen!")
        screen.fill((100, 255, 100))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN:
            
        
   
    
    pygame.display.flip()
pygame.mixer.music.stop()
pygame.quit()
