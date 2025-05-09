# -*- coding: utf-8 -*-
"""
Created on Sat May  3 09:03:28 2025

@author: eliag
"""

"""
    def BFS_oplossing_maze(self):
        begintoestand = {'pos': [1,0], 'parents': None}
        q = queue.Queue()
        q.put(begintoestand)
        visited = []
        visited.append(tuple(begintoestand['pos']))
        eindtoestand = (len(self.maze)-2, len(self.maze[0])-1)
        while not q.empty(): 
            puzzeltoestand = q.get() #puzzeltoestand uit queue nemen 
            huidige_pos = puzzeltoestand['pos']
            zetten = [(1,0), (0,1), (-1,0), (0,-1)]        
            for zet in zetten: 
                nieuwe_positie = [huidige_pos[0] + zet[0], huidige_pos[1] + zet[1]]
                nieuwe_positie_array = np.array(nieuwe_positie)
                if self.maze[nieuwe_positie[0], nieuwe_positie[1]] != 1 and tuple(nieuwe_positie) not in visited:
                    if tuple(nieuwe_positie) == eindtoestand: 
                        return True 
                    nieuwe_toestand = {'pos': nieuwe_positie, 'parent': puzzeltoestand}
                    q.put(nieuwe_toestand)
                    visited.append(tuple(nieuwe_positie))
        return False
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:28:31 2025

@author: eliag
"""
import pygame 
import numpy as np 
import queue
import random 

"""
bron: https://en.wikipedia.org/wiki/Maze_generation_algorithm
Given a current cell as a parameter ===> fucntie definieren 
Mark the current cell as visited
While the current cell has any unvisited neighbour cells
Choose one of the unvisited neighbours
Remove the wall between the current cell and the chosen cell
Invoke the routine recursively for the chosen cell
"""

class Maze():
    def __init__(self, dim1, dim2, variable):
        self.dim1 = dim1
        self.dim2 = dim2
        self.variable = variable #variable = muren of nieuw
        self.maze = self.create_maze()

    def create_maze(self):   
        maze = np.ones((self.dim1, self.dim2))
        #muren maken 
        if self.variable == 'nieuw': 
            maze[:,0] = 0 #links
        else: 
            maze[:,0] = 1 
        maze[0,:] = 1       #boven
        maze[:,-1] = 1      #rechts
        maze[-1,:] = 1      #beneden 
        maze[self.dim1-2, self.dim2-1] = 0      #uitgang
        maze[1, 0] = 0      #ingang 
        visited = [] 
        
        def DFS_maze(rij, kolom): 
            visited.append((rij, kolom))
            richtingen = [(2,0), (0,2), (-2,0), (0,-2)]  #stapjes van 2 anders muren zijn geplakt aan elkaar
            random.shuffle(richtingen)  #uit for loop! 
            for zet in richtingen: 
                nieuwe_rij = rij + zet[0]
                nieuwe_kolom = kolom + zet[1]
                if 0 < nieuwe_rij < self.dim1-1 and  0 < nieuwe_kolom < self.dim2-1:  #moet in maze zijn
                    if (nieuwe_rij, nieuwe_kolom) not in visited and maze[nieuwe_rij][ nieuwe_kolom]==1: 
                        maze[nieuwe_rij][nieuwe_kolom] = 0
                        muur_rij = rij + zet[0]//2
                        muur_kolom = kolom + zet[1]//2 
                        maze[muur_rij][muur_kolom] = 0
                        DFS_maze(nieuwe_rij, nieuwe_kolom)
        maze[1,1] =0       
        DFS_maze(1,1)
        return maze     

    def draw_maze(self, screen, x_0, y_0, aantal_rijen, aantal_kolommen):
        for i in range(len(self.maze)):
            for j in range(aantal_kolommen):
                x = int(j * 20 +x_0)
                y = int( i * 20+y_0)
                if self.maze[i, j] == 1:
                    pygame.draw.rect(screen, (0,0,0), (x, y, 20, 20)) #zwart 
                else:
                    pygame.draw.rect(screen, (255,255,255), (x, y, 20, 20)) #wit 


    def BFS_pad(self):
        start = {'pos': [1, 0], 'parent': None}
        q = queue.Queue()
        q.put(start)
        visited = set()
        visited.add(tuple(start['pos']))
        einddoel = (len(self.maze) - 2, len(self.maze[0]) - 1)
        
        while not q.empty():
            huidige = q.get()
            huidige_pos = huidige['pos']
            
            if tuple(huidige_pos) == einddoel:
                pad = []
                while huidige:
                    pad.append(huidige['pos'])
                    huidige = huidige['parent']
                return pad[::-1]  # pad van start naar eind
            
            richtingen = [(1,0), (0,1), (-1,0), (0,-1)]
            for dx, dy in richtingen:
                nieuwe_pos = [huidige_pos[0] + dx, huidige_pos[1] + dy]
                if (0 <= nieuwe_pos[0] < len(self.maze) and 0 <= nieuwe_pos[1] < len(self.maze[0]) and
                    self.maze[nieuwe_pos[0], nieuwe_pos[1]] == 0 and
                    tuple(nieuwe_pos) not in visited):
                    nieuwe_toestand = {'pos': nieuwe_pos, 'parent': huidige}
                    q.put(nieuwe_toestand)
                    visited.add(tuple(nieuwe_pos))
        
        return []
maze_x_0 = 50 
maze_y_0 = 15
class Teleporter(): 
    def __init__(self, lengte,    screen): 
        self.lengte= lengte 
        self.screen = screen 
        self.paarse_portaal = pygame.image.load("paarse portaal.png")
        self.paarse_portaal = pygame.transform.scale(self.paarse_portaal, (self.lengte, self.lengte))
        self.blauwe_portaal = pygame.image.load("blauwe portaal.png")
        self.blauwe_portaal = pygame.transform.scale(self.blauwe_portaal, (self.lengte, self.lengte))
    def tekenen(self, maze):
        coordinaten_portalen = []
        #coordianten van de portalen 
        co_begin = (0 * self.lengte + maze_x_0, self.lengte + maze_y_0)
        co_boven_rechts = ((len(maze.maze[0]) - 1) * self.lengte + maze_x_0-self.lengte,0 * self.lengte + maze_y_0+self.lengte)
        co_links_onder = (0 * self.lengte + maze_x_0+self.lengte, (len(maze.maze) - 1) * self.lengte + maze_y_0-self.lengte)
        #x_co = rij y_co = kolom
        coordinaten_portalen.append((1,1)) #begin maze 
        coordinaten_portalen.append((1, len(maze.maze[0]) - 2)) #-2 want moet voorlaatste kolom zijn => anders muur 
        
        #middel portaal mag niet op zwarte vakje zijn 
        x_midden = len(maze.maze[0]) // 2
        y_midden = len(maze.maze) // 2
        portaal_getekend = False 
        while portaal_getekend is False:
            if maze.maze[y_midden][x_midden] == 0:
                x_midden_kolom = x_midden * self.lengte + maze_x_0
                y_midden_rij = y_midden * self.lengte + maze_y_0
                self.screen.blit(self.paarse_portaal, (x_midden_kolom, y_midden_rij))
                coordinaten_portalen.append((x_midden, y_midden))
                portaal_getekend = True 
            else: 
                x_midden += 1
    # portalen tekenen
        self.screen.blit(self.paarse_portaal, co_begin)
        self.screen.blit(self.paarse_portaal, co_boven_rechts)
        self.screen.blit(self.blauwe_portaal, co_links_onder)
        return coordinaten_portalen

