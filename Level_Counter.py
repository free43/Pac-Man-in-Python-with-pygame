"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import pygame as pg
from Cons_Events import *

class Level_Counter(object):
    """
        Regulate the speed of the different Figures and change the state from scatter to chase
    """
    level = 1
    frame_counter = 0
    current_mode = 's'
    frame_counter_states = 0
    cs_counter = 0

    # Depending on the level, the times in which the modes from the ghosts are changed between Scatter and Chase
    modi_chase_scatter = { 1:
                            (7,
                             20,
                             7,
                             20,
                             5,
                             20,
                             5,
                             1),
                           2:
                            (7,
                             20,
                             7,
                             20,
                             5,
                             1033,
                             1/60,
                             1),
                           5:
                            (5,                                
                             20,
                             5,
                             20,
                             5,
                             1037,
                             1/60,
                             1)
                    }
    def __init__(self, FPS:int ):
        """
            :param FPS: The Framerate per second from the Game
        """

        self.FPS = FPS

    def update_figures_speed(self, game_field, pacman, ghosts):
        """
            Updates the speed of all figures in the game, every Frame

            :param game_field: The Gamefield on which the figures will move on
            :param Pac-Man: The Pac-Man 
            :param ghosts: All ghosts from the game in a list
        """

        pacmans_field = game_field.possible_way(tuple(pacman.pos), pacman.direction, False)
        if self.level < 21:
            ghosts_states = []
            for g in ghosts:
                ghosts_states.append(g.state)
        level = self.level
        figures = [pacman]
        figures.extend(ghosts)
        
        # Because the speed of the figures doesn't change every level, they are summarized 
        if self.level >= 2 and self.level < 5:
            level = 2
        elif self.level >= 5 and self.level < 21:
            level = 5
        elif self.level >= 21:
            level = 21   

        # For all the ghosts in the list figures, the speed will be customized individually, depending on there mode and position
        for ghosts in figures[1:]:
            field = game_field.possible_way(tuple(ghosts.pos), ghosts.direction, False)

            # If a ghost gets eaten in a tunnel the speed doesn't depend on being in a tunnel anymore
            if field == 't' and ghosts.state != 'e': 

                # With the modulo calculation the speed can be regualted more presize, then moving at one constant speed
                if (self.frame_counter % ghosts.level_speed[level]['t'][0]) == 0: 
                   ghosts.speed = ghosts.level_speed[level]['t'][1]

                else:
                    ghosts.speed = ghosts.level_speed[level]['t'][2]

            else:

                if self.frame_counter % ghosts.level_speed[level][ghosts.state][0] == 0: 
                    ghosts.speed = ghosts.level_speed[level][ghosts.state][1]

                else:
                    ghosts.speed = ghosts.level_speed[level][ghosts.state][2]

        ghost_state_for_pacman = 'nf'
        pacman_eat_dot = 'np'

        # Check if the current level < 21 and there is a ghost in the list in state f  
        if self.level < 21 and ghosts_states.count('f'):
            ghost_state_for_pacman = 'f'

        # Check if Pac-Man is eating dots at the moment
        if pacmans_field != None and pacmans_field[0] == 'p': 
            pacman_eat_dot = 'p'

        if self.frame_counter % pacman.level_speed[level][ghost_state_for_pacman][pacman_eat_dot][0] == 0: 
            pacman.speed = pacman.level_speed[level][ghost_state_for_pacman][pacman_eat_dot][1]
        else:
            pacman.speed = pacman.level_speed[level][ghost_state_for_pacman][pacman_eat_dot][2]

        # update the positions from each figure 
        for f in figures:
            rest = f.pos[0] % f.grid_size, f.pos[1] % f.grid_size

            # if the distance between the figure and the next ongrid is less then the speed from the figure, the figure will move the remaining distance, and not the actual speed
            if rest[0] != 0: 
                if f.grid_size-rest[0] < f.speed and f.direction == 'r':
                    f.pos[0] = f.pos[0] + (f.grid_size - rest[0]) - f.speed  
                elif rest[0] < f.speed and f.direction == 'l':              
                    f.pos[0] = f.pos[0] - (rest[0]) + f.speed 
            if rest[1] != 0:
                if rest[1] < f.speed and f.direction == 'u':                               
                    f.pos[1] = f.pos[1] - (rest[1]) + f.speed 
                elif f.grid_size - rest[1] < f.speed and f.direction == 'd':                
                    f.pos[1] = f.pos[1] + (f.grid_size - rest[1]) - f.speed 

        if self.frame_counter == self.FPS:
            self.frame_counter = 0
        else:
            self.frame_counter += 1
            
    def update_states(self, ghosts):
        """
            The Chase and Scatter mode, the ghosts go in regulary after specific time, are being set here

            :param ghosts: All ghosts from the game in a list
        """

        # Because the time of the figures, beeing in Scatter or Chase, doesn't change every level, they are summarized 
        level = self.level
        if self.level >= 2 and self.level < 5:
            level = 2
        elif self.level >= 5 and self.level < 21:
            level = 5
        elif self.level >= 21:
            level = 21   

        # Check if the frame counter has reached the specific time from the dictionary, and change the modi when this is the case
        if self.frame_counter_states == int(self.FPS * self.modi_chase_scatter[level][self.cs_counter]):
            self.frame_counter_states = 0 
            if self.cs_counter == 7:
                self.current_mode = 'c'
                return
            if self.cs_counter <= 6:
                self.cs_counter += 1
            if self.cs_counter % 2 == 0:
                self.current_mode = 's'
            else:
                self.current_mode = 'c'
            for g in ghosts:
                if self.current_mode != g.state and (g.state == 's' or g.state == 'c'):
                    g.change_mode(self.current_mode)
            
            
        else:
            self.frame_counter_states += 1
       
        pass

    def reset(self):
        """
            Resets the Level_Counter to it's init values
        """
        self.current_mode = 's'
        self.frame_counter_states = 0
        self.cs_counter = 0
        self.frame_counter = 0
        self.is_finished = False
    