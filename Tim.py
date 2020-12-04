"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import Ghost, Colors, math, copy

class Tim(Ghost.Ghost):
    """ 
        Follows Pac-Man, except he's closer then 5 fields,
        then he will hold his position and clone himself, 
        the clone will follow Pac-Man the same as Tim, but can't hurt Pac-Man
    """

    stay = False #< Flag that tells Tim to stay on his position
    new_tim = None #< Clone from Tim

    def __init__(self, grid_size:int, start_pos:tuple):
        """
            :param grid_size: Is the size of one square side in Pixel  
            :param start_pos: the position in the maze where Tim will spawn
        """
        Ghost.Ghost.__init__(self, start_pos, Colors.colors['BROWN'], grid_size)
        self.orginal_color = Colors.colors['BROWN']

        # Movement relevant vars:
        self.state = 'h'
        self.old_state = 'o'
        self.direction = 'u'
        
    def update(self, pacman_pos:tuple, recent_mode:str, game_field, windowsize_x:int):
        """
            Updates Tim's state, direction, Position and Target

            :param pacman_pos: The current position from Pac-Man
            :param recent_mode: The current mode in which Tim is
            :param game_field: The Gamefield on which Tim will move on
            :param windowsize_x: The biggest possible X-Coordinate
        """

        # When Tim has to stay his clone will be updated, he won't
        if self.stay:
            self.clone_update(windowsize_x, game_field) 

        # Controlls the behavior of Tim when his mode is Chase
        if self.state == 'c' :
            self.target = pacman_pos
            dist = math.sqrt((self.pos[0] - pacman_pos[0])**2 + (self.pos[1] - pacman_pos[1])**2) #< distance from Tim to Pac-Man

            # Distance < 5 * grid size, so Tim has to stay if possible
            if dist < 5 * self.grid_size: 

                # Checks if Tim isn't moving already or if he just got near Pac-Man
                if not self.stay: 
                    self.stay = self.pos[0] % self.grid_size == 0 and self.pos[1] % self.grid_size == 0 
                    
                    # Self.stay must be true so that Tim is on grid, stops moving and sends out his clone
                    if self.stay: 
                        self.new_tim =  copy.deepcopy(self)

            # Distance > 10 * gridsize so Tim starts moving again
            elif dist > 10 * self.grid_size:               
                self.stay = False
            self.set_direction(game_field)        

        # Controlls the behavior of Tim when he is in Scatter mode
        elif self.state == 's':
            self.stay = False
            self.target = (0, 35 * self.grid_size)
            self.set_direction(game_field)

        # Controlls the behavior of Tim when he is in Frightened mode
        elif self.state == 'f':
            self.stay = False #< Tim won't stay if he is frightened
            self.set_direction(game_field)

        # Controlls the behavior of Tim when he is in Eaten mode
        elif self.state == 'e':
            self.stay = False

            # As long as Tim isn't home he will want to go home
            if not self.arrived_home:
                self.go_home(game_field)

            else:

                # When Tim is home he will move to the right side in the ghost house
                if self.pos[0] != 15 * self.grid_size:
                    self.direction = 'r'

                # When he reached the right side, he has reached home and his mode is changed to Out
                elif self.pos[0] == 15 * self.grid_size:
                    self.arrived_target = self.arrived_home = False
                    self.change_mode('o')

        # Controlls the behavior of Tim when he is in Out mode
        elif self.state == 'o':

            # As long as Tim isn't in the X-Center of the ghost house he will move to the left
            if self.pos[0] != 13 * self.grid_size:
                self.direction = 'l'

            # When Tim is in the X-Center he will then move up to get out of the ghost house
            if self.pos[0] == 13 * self.grid_size:
                self.direction = 'u'

                # When Tim reached the outside of the ghost house he will move left and turn back to his recent mode
                if self.pos[1] == 14 * self.grid_size:
                    self.change_mode(recent_mode, False)
                    self.direction = 'l'

        # Controlls the behavior when Tim is in home mode
        elif self.state == 'h':
            self.stay = False
            if self.pos[1] == 16 * self.grid_size:
                self.target = (15 * self.grid_size, 18 * self.grid_size)
            elif self.pos[1] == 18 * self.grid_size:
                self.target = (15 * self.grid_size, 16 * self.grid_size)
            self.stay_home(game_field)

        # When Tim doesn't have to stay he will be updated
        if not self.stay:
            self.update_pos(windowsize_x) 
            
    def clone_update(self, windowsize_x, game_field):
        """
            Calls the update function for the clone from Tim

            :param windowsize_x: The biggest possible X-Coordinate
            :param gamefield: The Gamefield on which the clone will move
        """
        self.new_tim.set_direction(game_field)
        self.new_tim.update_pos(windowsize_x)

    def reset(self):
        """
            This function will reset Tim to his init values
        """
        Ghost.Ghost.reset(self)
        self.stay = False
        self.state = 'h'
        self.direction = 'u'
                 