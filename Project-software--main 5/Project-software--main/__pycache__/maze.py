# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:28:31 2025

@author: eliag
"""
import pygame 
import numpy as np 
import queue
import random 
def create_maze(dim1, dim2, saturation):
    maze = np.zeros((dim1, dim2))
    for i in range(1, dim1-1): 
        for j in range(1, dim2-1):
            if random.uniform(0.0,1.0)< saturation/100: 
                maze[i,j]=1
            
#make an edge around
    maze[:,0] = 1
    maze[0,:] = 1
    maze[:,-1] = 1
    maze[-1,:] = 1

#Create an exit
    maze[-2, -1] = 0
    maze[1, 0] = 0
    return maze


def draw_maze(screen, maze, x_0, y_0):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            x = j * 20 +x_0
            y = i * 20+y_0
            if maze[i, j] == 1:
                pygame.draw.rect(screen, (0,0,0), (x, y, 20, 20)) #zwart 
            else:
                pygame.draw.rect(screen, (255,255,255), (x, y, 20, 20)) #wit 


def BFS_oplossing_maze(maze): 
    begintoestand = {'pos': [1,0], 'parents': None}
    q = queue.Queue()
    q.put(begintoestand)
    visited = []
    visited.append(tuple(begintoestand['pos']))
    eindtoestand = (len(maze)-2, len(maze[0])-1)
    while not q.empty(): 
        puzzeltoestand = q.get() #puzzeltoestand uit queue nemen 
        huidige_pos = puzzeltoestand['pos']
        zetten = [(1,0), (0,1), (-1,0), (0,-1)]        
        for zet in zetten: 
            nieuwe_positie = [huidige_pos[0] + zet[0], huidige_pos[1] + zet[1]]
            nieuwe_positie_array = np.array(nieuwe_positie)
            if maze[nieuwe_positie[0], nieuwe_positie[1]] != 1 and tuple(nieuwe_positie) not in visited:
                if tuple(nieuwe_positie) == eindtoestand: 
                    return True 

                nieuwe_toestand = {'pos': nieuwe_positie, 'parent': puzzeltoestand} #zet toegepast op puzzeltoestand
                q.put(nieuwe_toestand)
                visited.append(tuple(nieuwe_positie))
    return False
    
def BFS_pad(maze):
    start = {'pos': [1, 0], 'parent': None}
    q = queue.Queue()
    q.put(start)
    visited = set()
    visited.add(tuple(start['pos']))
    einddoel = (len(maze) - 2, len(maze[0]) - 1)
    
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
            if (0 <= nieuwe_pos[0] < len(maze) and 0 <= nieuwe_pos[1] < len(maze[0]) and
                maze[nieuwe_pos[0], nieuwe_pos[1]] == 0 and
                tuple(nieuwe_pos) not in visited):
                nieuwe_toestand = {'pos': nieuwe_pos, 'parent': huidige}
                q.put(nieuwe_toestand)
                visited.add(tuple(nieuwe_pos))
    
    return []
