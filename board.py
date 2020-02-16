#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:48:02 2020

@author: jacob
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm

overlay_dict = np.array(["visible", "hidden", "flagged"])

def is_in_bounds(size_x, size_y ,x,y):
        if ( x<0 or x>= size_x or
            y < 0 or y >= size_y):
            return False
        return True

class Player:
    def __init__(self):
        self.isAlive = True
    def click_board(self, board, x,y):
        if not board.field_pressed(x,y):
            return "Didn't press"
        if board.exploded:
            player.isAlive = False
    def flag_board(self, board, x, y):
        board
        
        
class MinesDistanceField:
    def __init__(self, size, nr_mines):
        self.size = size
        self.array = np.zeros((size, size))
        stackarray = np.full(size*size, 0)
        stackarray[:nr_mines] = -1
        np.random.shuffle(stackarray)
        self.array = np.reshape(stackarray, (self.size, self.size))
        print(self.array)
        for i in np.arange(size):
            for j in np.arange(size):
                if not self.is_mine(i, j):
                    self.array[i,j] = self.get_neighbouring_bombs(i,j)
                else: 
                    print("bomb on " + str(i) +", " + str(j))
        print(self.array)
                
    def is_mine(self, x,y):
        if self.array[x,y]==-1:
            return True
        return False
    def get_neighbour_count(self, x, y):
        return self.array[x,y]
    
    def get_neighbouring_bombs(self, x,y):
        borderx = np.array([-1, 1] , dtype = int)
        bordery = np.array([-1, 1] , dtype = int)
        if x==0:
            borderx[0] = 0
        if y == 0:
            bordery[0] = 0
        if x == self.size-1:
            borderx[1] = 0
        if y == self.size -1 :
            bordery[1] = 0
        ctr = 0
        for i in np.arange(borderx[0], borderx[1] +1):
            for j in np.arange(bordery[0], bordery[1] +1):
                if self.is_mine(x + i, y + j):
                    ctr += 1
        return ctr
    
class MineOverlayMask:
    def __init__(self, size):
        self.array = np.ones((size, size))
    def flag(self, x, y):
        self.array[x, y] = 2
    def is_flagged(self, x, y):
        return(self.array[x,y] == 2)
    def is_hidden(self, x, y):
        return(self.array[x,y] == 1)
    def is_visible(self, x, y):
        return(self.array[x,y] == 0)
    def make_visible(self, x, y):
        self.array[x,y] = 0
    
    
class Board:
    def __init__(self, size, nr_mines):
        self.overlay_mask = MineOverlayMask(size)
        self.mines_field = MinesDistanceField(size, nr_mines)
        self.exploded = False
        self.size = size
    def field_pressed(self, x, y):
        if not is_in_bounds(self.size, self.size, x,y):
            print("Coordinates not in bounds")
            return False
        if(self.overlay_mask.is_visible(x,y)):
            return False
        else:
            if self.mines_field.is_mine(x, y):
                self.exploded = True
                return True
        self.overlay_mask.make_visible(x,y)
        return True
    def field_flagged(self, x, y):
        if not is_in_bounds(self.size, self.size, x,y):
            print("Coordinates not in bounds")
            return False
        self.overlay_mask.flag(x,y)
        return True
        
    
   
class Drawer:
    def __init__(self, board):
        self.board = board
        self.draw_array = np.zeros(np.size(board))
        
    def draw(self):
        
        plt.imshow(self.board.overlay_mask.array, cmap = "Reds")
        for i in np.arange(self.board.size):
            for j in np.arange(self.board.size):
                if self.board.overlay_mask.is_visible(i,j):
                    plt.text(i, j, str(self.board.mines_field.get_neighbour_count(j, i)))
        plt.show()

class Game:
    def __init__(self):
        self.player = Player()
        self.board = Board(4, 1) 
        self.drawer = Drawer(self.board)
    def update(self):
        if not self.player.isAlive:
            print("GAME OVER")
            return
        drawer.draw()
if __name__ == "__main__":
   
    game = Game()
    game.player.click_board(game.board, 3,3)
    game.update()