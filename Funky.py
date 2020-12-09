"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import Ghost, Colors
import math, random

class Funky(Ghost.Ghost):
    """
       From the level 1 to 20 Funky jumps to the closest Power Pellet from Pac-Man and
       From level 21 Funky protects the tunnel
    """

    # The coordinates of the different ENERGIZER in the look up table 
    # Meaning: U for Upper, L for Left or Lower, R for Right 
    ENERGIZER_UL = (1, 6)
    ENERGIZER_UR = (26, 6)
    ENERGIZER_LL = (1, 26)
    ENERGIZER_LR = (26, 26)

    # The coordinates of the tunnel entrance
    TUNNEL_L = (5, 17) 
    TUNNEL_R = (22, 17) 

    # frame_counter: to change funky's target every second when there are no more energizers
    frame_counter = 0

    def __init__(self, grid_size:int, start_pos:tuple):
        """
            :param gird_size: Is the size of one square side in Pixel
            :param start_pos: The position in the maze where Funky will spwan
        """

        # Set Funkys init values
        Ghost.Ghost.__init__(self, start_pos, Colors.colors['GREEN'], grid_size)
        self.orginal_color = Colors.colors['GREEN']
        self.state = 'o'
        self.direction = 'u'
        self.target = self.ENERGIZER_UL[0] * self.grid_size, self.ENERGIZER_UL[1] * self.grid_size #< Set his target to the Upper Left Energizer
        self.target_reached = True

    def set_target(self, pacman_pos:tuple, game_field, level:int):
        """
            Set Funkys target depending on the level of the game and Pac-Mans position

            :param pacman_pos: The current position from Pac-Man
            :param game_field: The Gamefield on which Funky will move on
            :param level: The current level of the game
        """

        # During the level 1 to 20 Funky jumps to the closest Power Pellet from Pac-Man. 
        if level < 21:
            positon_of_all_energizer = self.ENERGIZER_UL, self.ENERGIZER_UR, self.ENERGIZER_LL, self.ENERGIZER_LR
            dist_en = {}  #< Dictionary: key is the distance from Pac-Man to a Energizer e. value is the postion of the Energizer e

            # Searches the closest Energizer from Pac-Mans position
            for energizer_pos in positon_of_all_energizer:
                if game_field.look_up_table[energizer_pos[1]][energizer_pos[0]] == 'e':
                    distance = math.sqrt((energizer_pos[0] * self.grid_size - pacman_pos[0])**2 + (energizer_pos[1] * self.grid_size - pacman_pos[1])**2)
                    dist_en[distance] = energizer_pos

            # When there is no more Energizer on the Gamefield
            # Funky's target is set randomly in a radius of 4 * grid_size around Pacmans position 
            # A new randomly target is set every second (Game Framerate is 60)
            if not dist_en:
                self.frame_counter = (self.frame_counter % 60) + 1
                if self.frame_counter == 60:
                    RADIUS = 4 * self.grid_size
                    target_x = random.randint(pacman_pos[0] - RADIUS, pacman_pos[0] + RADIUS)
                    target_y = random.randint(pacman_pos[1] - RADIUS, pacman_pos[1] + RADIUS) 
                    self.target = target_x, target_y

            # When there is still an Energizer on the Gamefield. Funkys target will set to closest Power Pellet from Pac-Man. 
            else:
                self.frame_counter = 0
                minimum = min(dist_en.keys())
                new_target = dist_en[minimum][0] * self.grid_size, dist_en[minimum][1] * self.grid_size

                # When Pacman is closer to a Power Pellet and that Power Pellet position is not Funky's target 
                if self.target != new_target:
                    self.direction = 'd'
                    self.pos = list(new_target) #< Funky jumps to the closest Power Pellet from Pac-Man
                    self.target = new_target[:]
                
        # From level 21 Funky protects the tunnel   
        else:
            actual_pacman_pos = pacman_pos[0] // self.grid_size, pacman_pos[1] // self.grid_size 
            # Save if Funkys target is the entrance from the right or left tunnel
            target_tunnel_R = self.target[0] == self.TUNNEL_R[0] * self.grid_size
            target_tunnel_L = self.target[0] == self.TUNNEL_L[0] * self.grid_size
            reached_target = False

            # When Funky's target is the left or right tunnel entrance. 
            if target_tunnel_L or target_tunnel_R:
                # Save if Funky reached his target
                reached_target = (self.pos[0] // self.grid_size  == self.TUNNEL_L[0] or self.pos[0] // self.grid_size == self.TUNNEL_R[0]) and self.pos[1] // self.grid_size == self.TUNNEL_L[1]
            # When his target isn't the tunnel
            else:
                reached_target = True

            if reached_target:

                # Check if Pac-Man could be in the tunnel
                if actual_pacman_pos[1] == self.TUNNEL_L[1]:

                    # Check if Pac-Man is in the left tunnel
                    if actual_pacman_pos[0] <= self.TUNNEL_L[0]:
                        self.target = self.TUNNEL_R[0] * self.grid_size, self.TUNNEL_R[1] * self.grid_size #< Set Funky's target to the right entrance of the tunnel

                    # Check if Pac-Man is in the right tunnel
                    elif actual_pacman_pos[0] >= self.TUNNEL_R[0]:
                        self.target = self.TUNNEL_L[0] * self.grid_size, self.TUNNEL_L[1] * self.grid_size #< Set Funky's target to the left entrance of the tunnel
                    
                    # Pac-Man is not in the tunnel
                    else:
                        # Set the target from Funky in the ghost house
                        self.target = 14 * self.grid_size, 16 * self.grid_size 

                # Pac-Man is not in line with the tunnel
                else:
                    #Set the target from Funky in the ghost house
                    self.target = 14 * self.grid_size, 16 * self.grid_size 

    def update(self, pacman_pos:tuple, recent_mode:str, game_field, windowsize_x:int, level:int):
        """
            Updates Funky's state, direction, target and his position

            :param pacman_pos: The current position from Pac-Man
            :param recent_mode: The current mode in which the ghosts should be. It will be s (Scatter) or c (Chase)
            :param game_field: The Gamefield on which Funky will move on
            :param level: The current level of the game
        """

        # Check the different states from Funky

        # Controlls the behavior of Funky when his mode is Chase
        if self.state == 'c' :
            self.set_target(pacman_pos, game_field, level)
            self.set_direction(game_field)

        # Controlls the behavior of Funky when his mode is Scatter
        elif self.state == 's':            
            self.set_direction(game_field) #< Funky drives around his actual target

        # Controlls the behavior of Funky when his mode is Frightened.
        elif  self.state == 'f':
            self.set_direction( game_field) #< His direction is set randomly

        # Controlls the behavior of Blinky when his mode is Eaten
        elif self.state == 'e':
            if not self.arrived_home: #< Flag got set in the go_home function
                self.go_home(game_field)
            else:
                self.arrived_target = self.arrived_home = False
                self.change_mode('o')

        # Controlls the behavior of Blinky when his mode is Out
        elif self.state == 'o':
            self.direction = 'u'
            self.target = (13 * self.grid_size, 14 * self.grid_size)  #< Set his target to outside of the Ghost House

            # When Funky is outside of the ghost house his state is set to the recent ghost state
            if self.pos[1] == 14 * self.grid_size:
                self.pos[0] -= self.pos[0] % self.grid_size #< Put Funky on grid
                self.target = self.ENERGIZER_UL[0] * self.grid_size, self.ENERGIZER_UL[1] * self.grid_size
                self.change_mode(recent_mode, False)
                self.direction = 'l'

        # Controlls the behavior of Blinky when his mode is Home
        elif self.state == 'h':
            # Funky drives just up and down in the middle of the ghost house
            if self.pos[1] == 16 * self.grid_size:
                self.target = 13 * self.grid_size, 18 * self.grid_size
            elif self.pos[1] == 18 * self.grid_size:
                self.target = 13 * self.grid_size, 16 * self.grid_size
            self.stay_home(game_field) #< Regulate that Funky stays at home

        self.update_pos(windowsize_x)

    def reset(self):
        """
            This function will reset Funky to his init values
        """
        Ghost.Ghost.reset(self)
        self.direction = 'u'
        self.state = 'h'
        
    
         
         

