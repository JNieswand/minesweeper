#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:48:02 2020

@author: jacob
"""
import numpy as np
import matplotlib.pyplot as plt

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
        self.array = np.zeros((size, size))
    def is_mine(self, x,y):
        
        return False
    
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
        plt.imshow(self.board.overlay_mask + self.board.mines_field.array)
        plt.show()

if __name__ == "__main__":
    player = Player()
    board = Board(9, 3)
    player.click_board(board, 3,3)
    drawer = Drawer(board)
    drawer.draw()