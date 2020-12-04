"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com & andrestratz@web.de, All rights reserved.
"""

import Ghost,Colors

class Blinky(Ghost.Ghost):
    """
        Follows Pac-Mans position
    """
    
    def __init__(self, grid_size:int, start_pos:tuple):
        """
            :param grid_size: Is the size of one square side in Pixel 
            :param start_pos: The position in the maze where Blinky will spwan 
        """ 
        # Initiliaze the Base class
        Ghost.Ghost.__init__(self, start_pos, Colors.colors['RED'], grid_size)
        self.orginal_color = Colors.colors['RED']  
        
    def update(self, pacman_pos:tuple, recent_mode:str, game_field, windowsize_x:int):  
        """
            Updates Blinky's state, direction, target and his position

            :param pacman_pos: Pac-Mans actual position
            :param recent_mode: The current mode in which the ghosts should be. It will be 's' (Scatter) or 'c' (Chase)
            :param game_field: The Gamefield on which Blinky will move on
            :param windowsize_x: The width of the game window 
        """
        # Check the different states from Blinky
        # Controlls the behavior of Blinky when his mode is Chase
        if self.state == 'c' :
            self.target = pacman_pos 
            self.set_direction(game_field)

        # Controlls the behavior of Blinky when his mode is Scatter
        elif self.state == 's':  
            self.target = (25 * self.grid_size, 0) #< His target will be the top right corner of the maze.
            self.set_direction(game_field)

        # Controlls the behavior of Blinky when his mode is Frightened
        elif self.state == 'f': 
            self.set_direction(game_field) #< His direction is set randomly

        # Controlls the behavior of Blinky when his mode is Eaten
        elif self.state == 'e': 
            if not self.arrived_home: #< Flag got set in the go_home function
                self.go_home(game_field)
            
            else:
                self.arrived_target = self.arrived_home = False 
                self.change_mode('o') #< Set the state to Out 

        # Controlls the behavior of Blinky when his mode is Out
        elif self.state == 'o': 
            self.target = (13 * self.grid_size, 14 * self.grid_size) #< Set his target to outside of the Ghost House
            self.set_direction(game_field) 
            if tuple(self.pos) == self.target: 
                self.change_mode(recent_mode) #< Set his state to the current Ghost state

        self.update_pos(windowsize_x)

    def reset(self):
        """
            This function will reset Blinky to his init values
        """
        Ghost.Ghost.reset(self) 
        self.direction = 'l'
        self.state = 's' 