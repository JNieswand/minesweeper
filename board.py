#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:48:02 2020

@author: jacob
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import time

overlay_dict = np.array(["visible", "hidden", "flagged"])

def is_in_bounds(size_x, size_y ,x,y):
        if ( x<0 or x>= size_x or
            y < 0 or y >= size_y):
            return False
        return True
    
def get_neighbour_intervals(size, x, y):
    borderx = np.array([x-1, x+1] , dtype = int)
    bordery = np.array([y-1, y+1] , dtype = int)
    if x==0:
        borderx[0] = 0
    if y == 0:
        bordery[0] = 0
    if x == size-1:
        borderx[1] = x
    if y == size -1 :
        bordery[1] = y
    return borderx, bordery
    
class Player:
    def __init__(self, board):
        self.board = board
    def click_board(self, x,y):
        if not self.board.field_pressed(x,y):
            return "Didn't press"
    def flag_board(self, x, y):
        self.board.field_flagged(x, y)
        return
    def interprete_input(self, inp):
        stringlist = inp.strip().split(" ")
        print(stringlist)
        if len(stringlist) ==1:
            stringlist = list(inp.strip())
        if(len(stringlist) == 2):
            try:
                self.click_board(int(stringlist[0]), int(stringlist[1]))
            except ValueError:
                print("Invalid Input")
            return
        elif (len(stringlist) > 2) and (stringlist[2] == "f" or stringlist[2] == "flag"):
            try:
                self.flag_board(int(stringlist[0]), int(stringlist[1]))
            except ValueError:
                print("Invalid Input")
        else:
            print("Invalid Nr of arguments")
        return
    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        if( event.button ==1):
            self.click_board(int(event.xdata+0.5), int(event.ydata+0.5))
        elif (event.button == 3):
            self.flag_board(int(event.xdata+0.5), int(event.ydata+0.5))
        
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
        borderx , bordery = get_neighbour_intervals(self.size, x, y)
        ctr = 0
        for i in np.arange(borderx[0], borderx[1] +1):
            for j in np.arange(bordery[0], bordery[1] +1):
                if self.is_mine(i, j):
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
    def get_visible_nr(self):
        return(np.sum(self.array == 0))
    def get_flagged_nr(self):
        return(np.sum(self.array == 2))
    
    
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
        
        if self.mines_field.is_mine(x, y):
            self.exploded = True
            return True

        self.overlay_mask.make_visible(x,y)

        if self.mines_field.get_neighbour_count(x,y) == 0:
            borderx , bordery = get_neighbour_intervals(self.size, x, y)
            for i in np.arange(borderx[0], borderx[1] +1):
                for j in np.arange(bordery[0], bordery[1] +1):
                    if(i == x and j == y):
                        continue
                    self.field_pressed(i, j)
            
        return True
    def field_flagged(self, x, y):
        if not is_in_bounds(self.size, self.size, x,y):
            print("Coordinates not in bounds")
            return False
        if self.overlay_mask.is_visible(x, y):
            print("Only hidden fields can be flagged")
            return False
        self.overlay_mask.flag(x,y)
        return True
        
    

   
class Drawer:
    def __init__(self, board):
        self.board = board
        self.draw_array = np.zeros(np.size(board))
        self.fig = plt.figure()
        
        self.ax = self.fig.add_subplot(111)
        self.ax.imshow(np.swapaxes(self.board.overlay_mask.array, 0, 1), cmap = "Reds", vmax = "2")
        plt.show()
    def draw(self):
#        self.ax.clear()
        self.ax.imshow(np.swapaxes(self.board.overlay_mask.array, 0, 1), cmap = "Reds", vmax = "2")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        for i in np.arange(self.board.size):
            for j in np.arange(self.board.size):
                if self.board.overlay_mask.is_visible(i,j):
                    self.ax.text(i, j, str(self.board.mines_field.get_neighbour_count(i, j)))
                elif self.board.overlay_mask.is_flagged(i, j):
                    self.ax.text(i, j, "F")
        plt.show() 
        self.fig.canvas.draw()
    def connect_clickevent(self, onclick):
        self.fig.canvas.mpl_connect('button_press_event', onclick)
class Game:
    def __init__(self):
        self.nr_bombs = 4
        self.size = 9
        self.board = Board(self.size, self.nr_bombs) 
        self.drawer = Drawer(self.board)
    def update(self):
        if self.board.exploded:
            print("GAME OVER")
            return
        elif (self.board.overlay_mask.get_visible_nr() == self.size *self.size - self.nr_bombs
        and self.board.overlay_mask.get_flagged_nr() == self.nr_bombs):
            print("GAME WON !!")
            return
        self.drawer.draw()
if __name__ == "__main__":
    game = Game()
    player = Player(game.board)
    game.drawer.connect_clickevent(player.onclick)
    game.update()
    plt.show()
    while( not game.board.exploded):
        plt.waitforbuttonpress()
#        inp = input("Format: '<x> <y> <optional: f/flag>")
#        if inp == "c":
#            break
#        player.interprete_input(inp)
        game.update()
