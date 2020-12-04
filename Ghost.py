"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import pygame as pg
import math,random
import Colors

def find_opposite(direction:str):
    """
        Finds the oppisite direction of the current direction

        :param direction: The current direction of which a Ghost is currently moving
        :return string: Returns the opposite direction of the parameter direction
    """

    if direction == 'u':
        return 'd'                      
    if direction == 'l':                  
        return 'r'                      
    if direction == 'r':                  
        return 'l'                      
    if direction == 'd':                  
        return 'u'   
    



class Ghost(object):
    """Enemy from Pac-Man, try's to catch him"""
    
    # A dictionary in which a ghosts speed is declared depending on 1. Level, 2. Mode/Field they are in/on
    level_speed = { 1: 
                     {'s': (3,2,3),
                      'c':(3,2,3), 
                      'f':(5,1,2), 
                      'h':(2,2,2), 
                      'e':(3,4,4), 
                      'o':(3,2,3), 
                      't':(2,1,2) 
                      }, 
                    2:
                     {'s':(20,4,3),
                      'c':(20,4,3),
                      'f':(2,2,2),
                      'h':(2,2,2),
                      'e':(3,4,4),
                      'o':(3,2,3),
                      't':(3,1,2)
                         },
                    5:
                     {'s':(2,3,4),
                      'c':(2,3,4),
                      'f':(6,3,2),
                      'h':(2,2,2),
                      'e':(3,4,4),
                      'o':(3,2,3),
                      't':(5,1,2)
                         },
                    21:
                     {'s':(2,3,4),
                      'c':(2,3,4),            
                      'h':(2,2,2),                  
                      'o':(3,2,3),
                      't':(5,1,2)
                         }
                
        }
    arrived_target = False

    def __init__(self, start_pos:tuple, color, grid_size):
        """
            :param start_pos: The start Position form a Ghost in the Maze
            :param color: The Color, the ghost is getting displayed in
            :param grid_size: Is the size of one square side in Pixel  
        """

        self.pos = list(start_pos)
        self.start_pos = start_pos
        self.color = color
        self.target = None
        self.orginal_color = None
        self.grid_size = grid_size
        self.radius = self.grid_size - 5
        self.diameter = 2 * self.radius

        self.direction = 'l' #< The current direction of the Ghost, can be 'u' = up, 'd' = down, 'r' = right, 'l' = left
        self.state = 's' #< The current state of the ghost, can be 's' = scatter, 'c' = chase, 'f' = frightened, 'e' = eaten, 'o' = out, 'h' = home
        self.speed = 3 #< A Ghosts initial speed
        self.setpos_to_otherside = False #< A Flag to show, that the ghost is at the end of a tunnel and has to be moved to the other side
        self.first = 0 #< A value to say that a ghost was already eaten in the current frigthened mode
        self.arrived_home = False #< A flag to show that a ghost has arrived his home position
        self.cm_flag = False #< A flag to show, that his mode has changed
        self.frightend_frame_counter = 0 #<Counts the frames during the frightend Mode, gets reseted on 240 so at a FPS of 60, 4 seconds are over.

    def draw(self, DISP, frame:int):
        """
            Draws a ghost during the Game for each frame

            :param DISP: The Graphicwindow in which the Game will be visualized
            :param frame: The current Frame from one second, has a value between 0 - 59
        """

        frame %= 30 #< frame is made % 30 so they're "feet animation" changes four times per second

        ghost_center = self.pos[0] + self.grid_size // 2, self.pos[1] + self.grid_size // 2
        EYES_SIZE = 7
        SPACE_BETWEEN_EYES = 8
        eye0_start_pos = ghost_center[0] - SPACE_BETWEEN_EYES, ghost_center[1] - 4
        eye1_start_pos = ghost_center[0] + SPACE_BETWEEN_EYES , ghost_center[1] - 4

        # AS long as a ghost isn't eaten, his body will be drawn
        if self.state != 'e':
            self.draw_body(DISP, frame, ghost_center)

        # As long as a ghost isn't in frightened mode his eyes will be drawn normal
        if self.state != 'f':
            self.draw_eyes_normal_mode(DISP, frame, eye0_start_pos, eye1_start_pos, EYES_SIZE)
        else:
           self.draw_frightend_mode(DISP, frame, ghost_center, EYES_SIZE, eye0_start_pos, eye1_start_pos)

	    # Little help, to see the target a ghost has
        #if self.state != 'f' and self.target != None:
        #    pg.draw.rect(DISP, self.color,((self.target[0] + self.grid_size // 2, self.target[1] + self.grid_size // 2), (8, 8)))

    def draw_body(self, DISP, frame:int, ghost_center:tuple):
        """
            Drawing the ghost's body and legs, while the Color depends on the state of the ghost

            :param DISP: The Graphicwindow in which the Game will be visualized
            :param frame: The current Frame from one second, has a value between 0 - 59
            :param ghost_center: A X-Y-coordinate tuple, that contains the ghost's body center in Pixel
        """

        # Draws the body shape of a ghost
        pg.draw.circle(DISP, self.color, ghost_center, self.radius)
        ghost_rect = ghost_center[0] - self.radius, ghost_center[1], self.diameter, self.radius
        pg.draw.rect(DISP, self.color, ghost_rect)
        
        # When a ghost isn't eaten, his body and eyes will be drawn 
        if self.state != 'e':

            # For the first and third quarter of a second the first foot animation will be drawn
            if frame >= 0 and frame < 15:
                TRIANGLE_SIZE = 8

                #First triangle
                tr1_start_pos = ghost_rect[0] , ghost_rect[1]  + self.radius
                tr1_end_pos0 = tr1_start_pos[0] + TRIANGLE_SIZE, tr1_start_pos[1] - TRIANGLE_SIZE
                tr1_end_pos1 = tr1_start_pos[0] + 2 * TRIANGLE_SIZE, tr1_start_pos[1]
                triangle1 = (tr1_start_pos, tr1_end_pos0, tr1_end_pos1)

                #Second triangle
                tr2_start_pos = tr1_start_pos[0] + self.diameter, tr1_start_pos[1]
                tr2_end_pos0 = tr2_start_pos[0] - TRIANGLE_SIZE, tr2_start_pos[1] - TRIANGLE_SIZE
                tr2_end_pos1 = tr2_start_pos[0] - 2 * TRIANGLE_SIZE, tr2_start_pos[1]
                triangle2 = (tr2_start_pos, tr2_end_pos0, tr2_end_pos1)
                
                #Rectangle in the middle of the ghost feet
                RECTANGLE_SIZE = 6
                rect_start_pos = tr1_end_pos0[0] + TRIANGLE_SIZE, tr1_end_pos0[1]

                pg.draw.polygon(DISP, Colors.colors['BLACK'], triangle1)
                pg.draw.polygon(DISP, Colors.colors['BLACK'], triangle2)
                pg.draw.rect(DISP, Colors.colors['BLACK'], (rect_start_pos, (RECTANGLE_SIZE, TRIANGLE_SIZE)))
            
            # The second and fourth quarter of a second, the other feet animation will be drawn
            elif frame >= 15 and frame < 30:
                TRIANGLE_SIZE = 6

                #First triangle
                tr1_start_pos = ghost_rect[0] + 1 , ghost_rect[1]  + self.radius
                tr1_end_pos0 = tr1_start_pos[0] + TRIANGLE_SIZE, tr1_start_pos[1] - TRIANGLE_SIZE - 2
                tr1_end_pos1 = tr1_start_pos[0] + 2 * TRIANGLE_SIZE, tr1_start_pos[1]
                triangle1 = (tr1_start_pos, tr1_end_pos0, tr1_end_pos1)

                #Second triangle
                tr2_start_pos = tr1_start_pos[0] + self.diameter - 1, tr1_start_pos[1]
                tr2_end_pos0 = tr2_start_pos[0] - TRIANGLE_SIZE ,tr2_start_pos[1] - TRIANGLE_SIZE - 2
                tr2_end_pos1 = tr2_start_pos[0] - 2 * TRIANGLE_SIZE ,tr2_start_pos[1]
                triangle2 = (tr2_start_pos, tr2_end_pos0, tr2_end_pos1)

                #Third triangle
                tr3_start_pos = tr1_end_pos1[0], tr1_start_pos[1]
                tr3_end_pos0 = tr3_start_pos[0] + TRIANGLE_SIZE, tr3_start_pos[1] - TRIANGLE_SIZE - 2
                tr3_end_pos1 = tr3_start_pos[0] + 2 * TRIANGLE_SIZE, tr3_start_pos[1]
                triangle3 = (tr3_start_pos, tr3_end_pos0, tr3_end_pos1)

                pg.draw.polygon(DISP, Colors.colors['BLACK'], triangle1)
                pg.draw.polygon(DISP, Colors.colors['BLACK'], triangle2)
                pg.draw.polygon(DISP, Colors.colors['BLACK'], triangle3)
    
    def draw_eyes_normal_mode(self, DISP, frame:int, eye0_start_pos:tuple, eye1_start_pos:tuple, EYES_SIZE:int):
        """
            Drawing the eyes for every state except frightened mode
            
            :param DISP: The Graphicwindow in which the Game will be visualized
            :param frame: The current Frame from one second, has a value between 0 - 59
            :param eye0_start_pos: The start position for drawing the first eye
            :param eye1_start_pos: The start position for drawing the second eye
            :param EYES_SIZE: The radius of an eye
        """

        self.frightend_frame_counter = 0 #< Reset the frightend frame counter when ghost is not in frightend mode

        # Drawing the White from the eyes
        pg.draw.circle(DISP, Colors.colors['WHITE'], eye0_start_pos, EYES_SIZE)
        pg.draw.circle(DISP, Colors.colors['WHITE'], eye1_start_pos, EYES_SIZE)


        x_y_factors = [0, 0] #< The factors later decide where to draw the Iris, so a ghost looks in the direction he moves

        if self.direction == 'u':
            x_y_factors[1] = -1
        elif self.direction == 'd':
            x_y_factors[1] = 1
        elif self.direction == 'r':
            x_y_factors[0] = 1
        elif self.direction == 'l':
            x_y_factors[0] = -1

        IRIS_SIZE = 4
        
        # Calculates and draws the Iris of a ghost
        iris0_start_pos = eye0_start_pos[0]  + x_y_factors[0] * EYES_SIZE - x_y_factors[0] * IRIS_SIZE, eye0_start_pos[1] + x_y_factors[1] * EYES_SIZE - x_y_factors[1] * IRIS_SIZE
        iris1_start_pos = eye1_start_pos[0]  + x_y_factors[0] * EYES_SIZE - x_y_factors[0] * IRIS_SIZE, eye1_start_pos[1] + x_y_factors[1] * EYES_SIZE - x_y_factors[1] * IRIS_SIZE
        pg.draw.circle(DISP, Colors.colors['BLUE'], iris0_start_pos, IRIS_SIZE)
        pg.draw.circle(DISP, Colors.colors['BLUE'], iris1_start_pos, IRIS_SIZE)
    
    def draw_frightend_mode(self, DISP, frame:int, ghost_center:tuple, EYES_SIZE:int, eye0_start_pos:tuple, eye1_start_pos:tuple):
        """
            Draws the eyes and the mouth of the ghost in frightend mode, and also changes the color of his body from blue to white.
        
            :param DISP: The Graphicwindow in which the Game will be visualized
            :param frame: The current Frame from one second, has a value between 0 - 59
            :param eye0_start_pos: The start position for drawing the first eye
            :param eye1_start_pos: The start position for drawing the second eye
            :param EYES_SIZE: The radius of an eye
        """

        self.frightend_frame_counter += 1 #< Increments the frames already in frightened mode

        # Changes the Colors from the Eyes and the body
        frigthened_color_eyes = Colors.colors['POINTS']
        self.color = Colors.colors['BLUE']

        # When the time has reached two seconds, the ghosts will start blinking
        if self.frightend_frame_counter >= 120:
            if frame < 15:
                frigthened_color_eyes = Colors.colors['RED']
                self.color = Colors.colors['WHITE']          
        
        # Calculates the Eyes position and draws them, and the mouth
        rect_eye0 = ((eye0_start_pos[0] - EYES_SIZE//2, eye0_start_pos[1] - EYES_SIZE//2), (EYES_SIZE,EYES_SIZE))
        rect_eye1 = ((eye1_start_pos[0] - EYES_SIZE//2, eye1_start_pos[1] - EYES_SIZE//2), (EYES_SIZE,EYES_SIZE))
        pg.draw.rect(DISP, frigthened_color_eyes, rect_eye0)
        pg.draw.rect(DISP, frigthened_color_eyes, rect_eye1)
        pg.draw.circle(DISP, frigthened_color_eyes, (ghost_center[0], ghost_center[1] + EYES_SIZE), 3 * EYES_SIZE // 4)

    def set_direction(self, game_field):
        """
            Sets the direction in which a ghost moves to get to as fast as possible to it's target
            
            :param game_field: The Gamefield on which the ghost will move on
        """

        # The ghost just need to be on grid on the y position during the states Home and outside home
        ongrid = ((self.pos[0] % self.grid_size == 0 or self.state == 'h' or self.state == 'o') and self.pos[1] % self.grid_size == 0)
        
        # Only when on grid, the ghost can change direction
        if ongrid:

            # When a ghost changes it's mode, it turns in the opposite direction of the current direction
            if  self.cm_flag:
                self.cm_flag = False
                direction = find_opposite(self.direction)
                field = game_field.possible_way(tuple(self.pos), direction, False)

                #When the opposite direction is not possible because of a wall
                if not (field != None and field[0] == 'r'): 
                    self.direction = direction

                return

            possible_dir = ['d', 'r', 'l', 'u'] #< A list with every possible direction a ghost can possibly move
            possible_dir.remove(find_opposite(self.direction)) #< The oppisite direction gets deleted, because a ghost regulary isn't allowed to move in that direction

            offset_y,offset_x = 0, 0
            dist = {} #< A dictionary later filled like "distance to Pac-Man : possible direction "

            # For every possible direction there will be checked if the next field in that direction is a field a ghost can move to, if so this direction stays remaining in the dicitonary
            for p in possible_dir:
                value = game_field.possible_way(tuple(self.pos), p, False)

                # If field is 'os' the flag will be set, that tells the ghost he is at the end of a tunnel and will change the side 
                if value == 'os':
                    self.setpos_to_otherside = True
                
                # The field gets checked if it is a field the ghost can move to or not
                if value == None or value[0] != 'r' or (value != None and value[-1] == 'w' and ((self.state == 'e' and p == 'd') or p == 'u')):

                    # Direction 'u' gets a special check because there are 4 fields where they could move up but aren't allowed
                    if p == 'u':
                        if value != None and value[-1] == 'w':
                            self.direction = 'u'
                            return
                        if value == None or value[-1] != 'n':
                            offset_x = 0
                            offset_y = -self.grid_size
                        else:
                            continue

                    # Check the other directions and adjust the offsets
                    elif p == 'd':
                        offset_x = 0
                        offset_y = self.grid_size
                    elif p == 'r':
                        offset_x = self.grid_size
                        offset_y = 0
                    elif p == 'l':
                         offset_x = -self.grid_size
                         offset_y = 0

                    # Now for the checked direction, the distance to the target gets calculated, so in the end the ghost knows the distance to it's target if he would pick that direction
                    dist[math.sqrt((self.pos[0] - self.target[0] + offset_x)**2 + (self.pos[1] - self.target[1] + offset_y)**2)] = p
         
            # When a ghost is frightened he will pick a random direction from the possible directions
            if self.state == 'f':
                self.direction = random.choice(list(dist.values()))

            # In any other mode he will pick the direction, that is the shortest to it's current target
            else:
                minimum = min(dist.keys())
                self.direction = dist[minimum]

    def update_pos(self, windowsize_x:int):
        """
            Depedning on the chosen direction, the ghost will move in that direction with it's current speed
            
            :param windowsize_x: The width of the gamewindow
        """

        # Checks what direction the ghost should move to, and changes it's position
        if self.direction == 'u':
            self.pos[1] -= self.speed

        elif self.direction == 'd':
            self.pos[1] += self.speed

        # When moving left or right the ghost might be at the end of a tunnel and has to change sides, he knows that by looking at the flag state
        elif self.direction == 'r':
            if  self.setpos_to_otherside:
                self.pos[0] = 0
                self.setpos_to_otherside = False
            self.pos[0] += self.speed

        elif self.direction == 'l':
            if  self.setpos_to_otherside:
                self.pos[0] = windowsize_x - self.grid_size
                self.setpos_to_otherside = False
            self.pos[0] -= self.speed

    def go_home(self, game_field):
        """
            When a ghost got eaten he has to return home, which is taken care of here
        """

        # As long as the ghost isn't at home his target is target is in front of the "door" from the ghost house
        if not self.arrived_target:
            self.target = 13 * self.grid_size, 16 * self.grid_size
            self.set_direction(game_field) 
            self.arrived_target = self.pos == list(self.target)

        # When the ghost has reached it's target, he will then move in the ghost house
        else:
            if self.pos[1] != 17 * self.grid_size:
                self.direction = 'd'

            # When he is in the ghost house the flag that he arrived at home is set to true
            else:
                self.arrived_home = True  

    def change_mode(self, mode:str, cm_flag = True):
        """
            Changes the mode from a ghost

            :param mode: The mode, the ghost should change to
            :param cm_flag: Is set on true by default when function is called, but can be set to false when needed
        """

        if self.state != 'o':
            self.cm_flag = cm_flag
        self.state = mode

        # When the mode changes from 'f' or 'e' to another, the ghost will turn back to it's original color
        if self.state == 'c' or self.state == 's' or self.state == 'o':
            self.color = self.orginal_color
        
    def reset(self):
        """
            Resets Ghost to it's init values
        """
        self.pos = list(self.start_pos)[:]
        self.color = self.orginal_color
        self.first = 0
        self.arrived_home = False 
        self.arrived_target = False

    def stay_home(self, game_field):
        """
            Tells the ghost has to stay home

            :param game_field: The Gamefield on which Pac-Man will move on
        """
        self.cm_flag = True
        self.set_direction(game_field)
        
    
            