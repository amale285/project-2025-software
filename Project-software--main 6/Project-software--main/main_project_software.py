# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 20:00:03 2025

@author: eliag
"""

import pygame
import random 
from voorpagina_game import voorpagina, keuze
from maze import Maze, Teleporter 

pygame.init()  

screen = pygame.display.set_mode([1000, 500])
clock = pygame.time.Clock()

lengte_blokje= 20
maze_x_0 = 50 
maze_y_0 = 15
lengte_maze = 45
hoogte_maze = 23
voorpagina(screen)
screen.fill((255,255,255))
achtergrond, resultaat = keuze(screen)
pygame.mixer.music.load("never gonna give you up.mp3.mp3")
pygame.mixer.music.play(-1) 



class Figuur():     #code uit wpo6 
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

    def beweging(self, maze, snelheid): 
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
        nieuwe_x = self.x + vx * lengte_blokje
        nieuwe_y = self.y + vy * lengte_blokje
        rij = (nieuwe_y- maze_y_0) // lengte_blokje
        kolom = (nieuwe_x - maze_x_0) // lengte_blokje
        if 0 <= rij < len(maze.maze) and 0 <= kolom < len(maze.maze[0]):
            if maze.maze[rij][kolom] ==0: 
                self.x = nieuwe_x
                self.y = nieuwe_y
    
       
   
class BotSpeler(Figuur):
    def __init__(self, x, y, breedte, hoogte, pad, snelheid):
        super().__init__(x, y)
        self.breedte = breedte
        self.hoogte = hoogte
        self.pad = pad
        self.stap = 0
        self.timer = 0
        self.snelheid = snelheid
    def tekenenen(self):
        bot_img = pygame.image.load("cat bot.png")
        bot_img = pygame.transform.scale(bot_img, (self.breedte, self.hoogte)).convert_alpha()
        screen.blit(bot_img, (self.x, self.y))
        
    def beweging(self, maze,_): # _ = we ontvangen nog iets extra (bijv. toetsenbord-input), maar de bot gebruikt het NIET
        if self.stap < len(self.pad):
            self.timer += 1
            if self.timer % self.snelheid == 0:
                nieuwe_y, nieuwe_x = self.pad[self.stap]
                self.x = nieuwe_x * lengte_blokje + maze_x_0
                self.y = nieuwe_y * lengte_blokje + maze_y_0
                self.stap += 1
                

class Bal(Figuur): 
    def __init__(self, x,y, straal, snelheid): 
        super().__init__(x,y)
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
        self.breedte = lengte_blokje
        self.hoogte = lengte_blokje
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

maze = Maze(hoogte_maze, lengte_maze,  'muren')
pad = maze.BFS_pad()
speler = Speler(51, 35, 18, 18)

teleporter = Teleporter(lengte_blokje,  screen )


if resultaat == "MEDIUM":
    BotSpeler.snelheid = 4
elif resultaat == "EASY":
    BotSpeler.snelheid = 2
else:
    BotSpeler.snelheid = 1

bot = BotSpeler(maze_x_0, maze_y_0, 18, 18, pad, BotSpeler.snelheid)
lijst_personages = [speler, bot]
powerups = []
for i in range(5):  # 5 power-ups
    while True:
        kolom = random.randint(0, len(maze.maze[0])-1)
        rij = random.randint(0, len(maze.maze)-1)
        if maze.maze[rij][kolom] == 0:
            x = kolom * lengte_blokje + maze_x_0
            y = rij * lengte_blokje + maze_y_0
            soort = random.choice(["snelheid", "vertrager"])
            powerups.append(PowerUp(x, y, soort))
            break

running = True  
verandering_maze = False    


powerup_timer = 0
oude_maze = None 
while running:
    
    clock.tick(20)
    screen.blit(achtergrond, (0, 0))
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB and verandering_maze == False and speler.x != maze_x_0 +lengte_blokje+1 :
                
                kolom_speler_tab = (speler.x - maze_x_0 ) // lengte_blokje
                nieuwe_lengte =   lengte_maze - kolom_speler_tab    #als 44- kolom dan is een variable en veranderd als oneven vakje 
                print(nieuwe_lengte)
                nieuwe_maze = Maze(hoogte_maze, nieuwe_lengte, 'nieuw')   #moet geen while loop gebruiken maze heeft altijd een oplossing 
                oude_maze = maze 
                maze = nieuwe_maze 
                maze_x_0 = speler.x 
                speler.y = lengte_blokje + maze_y_0 #beginpositie 
                pad = maze.BFS_pad()
                bot = BotSpeler(maze_x_0, maze_y_0, 18, 18, pad, BotSpeler.snelheid)
                lijst_personages = [speler, bot]
                
                for powerup in powerups:
                    powerup.teken()
                verandering_maze = True 
                
      
    if verandering_maze == True: 
        oude_maze.draw_maze(screen,  50, maze_y_0 ,len(maze.maze), kolom_speler_tab )
        coordinaten_portalen  = teleporter.tekenen(oude_maze)
    maze.draw_maze(screen,  maze_x_0, maze_y_0,len(maze.maze), len(maze.maze[0]))  #screen, maze, x_0, y_0, rij , kolom           
    coordinaten_portalen  = teleporter.tekenen(maze )
      
    
    for obj in lijst_personages: 
        if hasattr(obj, "beweging"):
            obj.beweging(maze,7)
        if hasattr(obj, "tekenenen"):
            obj.tekenenen()
       
    for powerup in powerups:
        powerup.teken()
    
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


    kolom_speler = (speler.x - maze_x_0 ) // lengte_blokje
    rij_speler = (speler.y -maze_y_0) //lengte_blokje 
    kolom_bot = (bot.x -maze_x_0)//lengte_blokje
    blauwe_teleporter_co = blauwe_teleporter_co = (len(maze.maze) - 2, 1)
#(maze_x_0+ lengte_blokje,(len(maze.maze) - 1) * lengte_blokje + maze_y_0-lengte_blokje)
    if (rij_speler, kolom_speler) == blauwe_teleporter_co: 
        random_coordinaten = random.choice(coordinaten_portalen)
        gekozen_rij = random_coordinaten[0]
        gekozen_kolom = random_coordinaten[1]
        speler.x = gekozen_kolom * lengte_blokje + maze_x_0
        speler.y = gekozen_rij * lengte_blokje + maze_y_0
        
        
    
    if kolom_speler == len(maze.maze[0]) - 1:
        font_size = 50
        font = pygame.font.Font(None, size=font_size)
        screen.fill((0, 0, 0))
        gewonnen = pygame.image.load("duck.png")
        gewonnen = pygame.transform.scale(gewonnen, (350, 500))
        screen.blit(gewonnen, (325, 0))
        screen.blit(font.render('Gewonnen!', True, (0,0,0)),dest=(400,30))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False
    elif kolom_bot == len(maze.maze[0]) - 1:    
        font_size = 50
        font = pygame.font.Font(None, size=font_size)
        screen.fill((0, 0, 0))
        bot_win = pygame.image.load("bot gewonnen.png")     #bron: https://www.google.com/url?sa=i&url=https%3A%2F%2Ftenor.com%2Fview%2Firobot-i-robot-smile-gif-4750318732627893030&psig=AOvVaw3EqvQyvpJlxapEygyY6hyU&ust=1746352778000000&source=images&cd=vfe&opi=89978449&ved=0CBcQjhxqFwoTCMCU7P-Gh40DFQAAAAAdAAAAABAE
        bot_win = pygame.transform.scale(bot_win, (350, 500))
        screen.blit(bot_win, (325, 0))
        screen.blit(font.render('Ik heb gewonnen', True, (255,255,255)),dest=(350,400))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False
        running = False
    
    
    
    pygame.display.flip()
pygame.mixer.music.stop()
pygame.quit()
