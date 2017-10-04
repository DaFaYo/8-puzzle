"""
Clone of 2048 game.

In CodeSkulptor: http://www.codeskulptor.org/#user34_NH9gi03yqa_1.py
Testsuite - merge: http://www.codeskulptor.org/#user34_mp6Ri7FKvY_1.py

To play the Game go to:

In CodeSkulptor: http://www.codeskulptor.org/#user34_KQovN5hjdbufLJF.py

"""

import random

# uncomment next line for GUI
#import poc_2048_gui        

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # An auxiliary function 
    def aux(lst, res, index, flag):
        """
        Helper function that that is recursive over line
        """
        if not lst:
            return res
        elif lst[0] == 0:
            return aux(lst[1:], res, index, flag)
        elif index == 0:
            res[index] = lst[0]
            index += 1
            return aux(lst[1:], res, index, flag)
        elif res[index - 1] == lst[0] and not flag:
            res[index - 1] += lst[0]
            flag = True
            return aux(lst[1:], res, index, flag)
        else:
            res[index] = lst[0]
            flag = False
            index += 1
            return aux(lst[1:], res, index, flag)

    result = [0] * len(line)    
    return aux(line, result, 0, False)

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):

        self.grid_height = grid_height
        self.grid_width = grid_width
        self._grid = []
        self.reset()

        # computea dictionary of the indices for the initial tiles
        # in the corresponding directions
        list_up = []
        list_down = []
        list_left = []
        list_right = []
        for j in range(grid_width):
            list_up.append(tuple([0, j]))
            list_down.append(tuple([grid_height - 1, j]))

        for i in range(grid_height):    
            list_left.append(tuple([i, 0]))
            list_right.append(tuple([i, grid_width - 1]))
    
        # dictionary
        self._tiles_dict = {}
        self._tiles_dict[UP]    = list_up
        self._tiles_dict[DOWN]  = list_down 
        self._tiles_dict[LEFT]  = list_left
        self._tiles_dict[RIGHT] = list_right 
            
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        
        for dummy_loop_counter in range(self.grid_height):
            self._grid.append([0] * self.grid_width)
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        #use boundary in case width is not the same as the height
        if direction == UP or direction == DOWN:
            boundary = self.grid_height
        else:
            boundary = self.grid_width        
        
        #retrieve the tile values from entries, and store them
        #in a temporary list            
        temp_tile_vals = []        
        init_list = self._tiles_dict[direction] #e.g. [(0, 0), (0, 1), (0, 2)]        
        length_side = len(init_list)
        
        for i in range(length_side):
            pair = init_list[i]
            values = []
            for j in range(boundary):
                row = pair[0] + j * OFFSETS[direction][0]
                col = pair[1] + j * OFFSETS[direction][1]
                
                values.append(self._grid[row][col])
                
            temp_tile_vals.append(values)

        #use merge function to merge the tile values in the temp list
        for i in range(length_side):
            temp_tile_vals[i] = merge(temp_tile_vals[i])
            
        #iterate over the entries in the row or column again and
        #store the merged tile values back into the grid. Also,
        #determine if any tiles have moved
        make_new_tile = False    
        for i in range(length_side):
            pair = init_list[i]
            for j in range(boundary):
                row = pair[0] + j * OFFSETS[direction][0]
                col = pair[1] + j * OFFSETS[direction][1]
                value_old = self._grid[row][col]
                value_new = temp_tile_vals[i][j]
                if value_old != value_new:
                    make_new_tile = True
               
                self._grid[row][col] = value_new
            
        if make_new_tile:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        #compute tiles with value zero
        zeroes = []
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self._grid[i][j] == 0:
                    zeroes.append([i, j])

         # if there are such tiles pick a random one
         # and a random value too.
        if zeroes: 
            index = random.randrange(len(zeroes))
            rand_tile_x = zeroes[index][0]
            rand_tile_y = zeroes[index][1]
           
            # pick 2 90% and 4 10% of the time
            value = 2
            pick_num = random.random() * 100
            if pick_num > float(90):
                value = 4
                
            # set the value
            self._grid[rand_tile_x][rand_tile_y] = value
                
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """

        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        

        return self._grid[row][col]

import poc_twenty_forty_eight_testsuite
poc_twenty_forty_eight_testsuite.run_test(merge, TwentyFortyEight)

#import poc_2048_gui
#poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
