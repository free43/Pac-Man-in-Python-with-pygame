"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import Ghost,Colors

class Inky(Ghost.Ghost):
    """
        Depends on the position from Blinky and Pac-Man, as also on the direciton Pac-Man is looking
    """

    def __init__(self, grid_size:int, start_pos:tuple):
        """
            :param grid_size: Is the size of one square side in Pixel  
            :param start_pos: the position in the maze where Inky will spawn
        """

        Ghost.Ghost.__init__(self, start_pos, Colors.colors['CYAN'], grid_size)
        self.orginal_color = Colors.colors['CYAN']
        self.state = 'h'
        self.old_state = 's'
        self.direction = 'u'

    def set_target(self, pacman_pos:tuple, pacman_direction:str, blinky_pos:tuple):
        """
            Sets the target that Inky wants to reach

            :param pacman_pos: The current position from Pac-Man
            :param pacman_direction: The current direction Pac-Man is looking in
            :param blinky_pos: The current position from Blinky
        """

        x_offset,y_offset = 0, 0

        # Sets the value of the offset depending on Pac-Man direction
        if pacman_direction == 'u':
            y_offset = -2 * self.grid_size
        elif pacman_direction == 'd':
            y_offset = 2 * self.grid_size
        elif pacman_direction == 'l':
             x_offset = -2 * self.grid_size
        elif pacman_direction == 'r':
             x_offset = 2 * self.grid_size       

        ref_point = pacman_pos[0] + x_offset, pacman_pos[1] + y_offset #< Sets a point two fields in front of Pac-Man
        vec_ref_point = (ref_point[0] - blinky_pos[0]), (ref_point[1] - blinky_pos[1])
        self.target = (ref_point[0] + vec_ref_point[0], ref_point[1] + vec_ref_point[1])

    def update(self, pacman_pos:tuple, pacman_direction:str, blinky_pos:tuple, recent_mode:str, game_field, windowsize_x:int):
        """
            Updates Inky's state, position, direction and target

            :param pacman_pos: The current position from Pac-Man
            :param pacman_direction: The current direction Pac-Man is looking in
            :param blinky_pos: The current position from Blinky
            :param recent_mode:
            :param game_field: The Gamefield on which Tim will move on
            :param windowsize_x: The biggest possible X-Coordinate
        """

        # Controlls the behavior of Inky when his mode is Chase
        if self.state == 'c':
            self.set_target(pacman_pos, pacman_direction, blinky_pos)

        # Controls the direction setting when Inky is in Chase- or Frightened mode
        if (self.state == 'c' or self.state == 'f'):
            self.set_direction(game_field)

        # Controlls the behavior of Inky when he is in Scatter mode
        elif self.state == 's':
            self.target = (27 * self.grid_size, 35 * self.grid_size)
            self.set_direction(game_field)

        # Controlls the behavior of Inky when he is in Eaten mode
        elif self.state == 'e':

            # As long as Inky isn't home he will want to go home
            if not self.arrived_home:
                self.go_home(game_field)

            else:

                # When Inky is home he will move to the left side in the ghost house
                if self.pos[0] != 11 * self.grid_size:
                    self.direction = 'l'

                # When he reached the left side, he has reached home and his mode is changed to Out
                elif self.pos[0] == 11 * self.grid_size:
                    self.arrived_target = self.arrived_home = False
                    self.change_mode('o')

        # Controlls the behavior of Inky when he is in Out mode
        elif self.state == 'o':

            # As long as Inky isn't in the X-Center of the ghost house he will move to the right
            if self.pos[0] != 13 * self.grid_size:
                self.direction = 'r'

            # When Inky is in the X-Center he will then move up to get out of the ghost house
            if self.pos[0] == 13 * self.grid_size:
                self.direction = 'u'

                # When Inky reached the outside of the ghost house he will move left and turn back to his recent mode
                if self.pos[1] == 14 * self.grid_size:
                    self.change_mode(recent_mode, False)
                    self.direction = 'l'

        # Controlls the behavior when Tim is in home mode
        elif self.state == 'h':
            if self.pos[1] == 16 * self.grid_size:
                self.target = 11 * self.grid_size, 18 * self.grid_size
            elif self.pos[1] == 18 * self.grid_size:
                self.target = 11 * self.grid_size, 16 * self.grid_size
            self.stay_home(game_field)
        self.update_pos(windowsize_x)

    def reset(self):
        """
            This function will reset Inky to his init values
        """
        Ghost.Ghost.reset(self)
        self.direction = 'u'
        self.state = 'h'

