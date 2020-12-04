"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import pygame as pg
import Colors
import Sound
from pygame.locals import *
from Cons_Events import *

def find_opposite(direction:str):
    """
        Finds the oppisite direction of the current direction

        :param direction: The current direction of which Pac-Man is currently moving
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

class Pacman(Sound.Sound):
    """Pac-Man eats points"""

    # A dictionary, in which Pacmans speed is declared depending on 1. Level, 2. Ghosts are frightened or not, 3. Pac-Man eats points or not
    level_speed = { 1:
                       {'f':
                        {'p':(2, 3, 3), 
                        'np':(3, 2, 4) 
                        },
                       'nf':
                        {'p':(2, 2, 3), 
                         'np':(2, 3, 3) 
                         }
                       },
                    2:
                       {'f':
                         {'p':(20, 4, 3), 
                         'np':(2, 3, 4)
                         },
                       'nf':
                         {'p':(2, 3, 3), 
                          'np':(3, 2, 4) 
                          }
                        },
                    5:
                       {'f':
                         {'p':(20, 4, 3), 
                         'np':(5, 2, 4) 
                         },
                       'nf':
                         {'p':(20, 4, 3), 
                          'np':(5, 2, 4) 
                          }
                        },
                    21:
                       {
                       'nf':
                         {'p':(3, 2, 4), 
                          'np':(2, 3, 3) 
                          }
                    },
                }

    life_counter = 5 #< Pacmans amount of lifes
    count_eaten_ghost = 200 #< The Score you get for the first ghost you eat in frightened mode, will get bigger with each ghost
    global_counter = dot_counter = 0 #< Counts how many dots Pac-Man has eaten already
    hourglass_counter = 0 #< Counts how many frames passed in which Pac-Man hasn't eaten a dot
    state = '' #< Pacmans state can be either 'm' = move or '' = stay
    speed = 3 #< Pacmans initial speed
    eat_ghost = False #< Flag if Pac-Man can eat a ghost when they collide
    energizer_flag = False #< Flag if Pac-Man has eaten a energizer dot
    last_dir = direction = 'l' #< The current and previous direction of Pac-Man, can be 'r' = right, 'l' = left, 'u' = up or 'd' = down
    eaten = False #< Flag if Pac-Man got eaten
    point_counter = 0 #< Counter for the points Pac-Man already has made
    first_eaten = False #< Flag if Pac-Man got eaten for the first time
    frightened_frame_counter = 0 #< Counts how many frames the ghosts are already in frigthened mode

    def __init__(self, grid_size, start_pos:list):
        """
            :param grid_size: Is the size of one square side in Pixel  
            :param start_pos: The start Position form Pac-Man in the Maze
        """

        Sound.Sound.__init__(self)
        self.pos = list(start_pos)
        self.start_pos = start_pos
        self.grid_size = grid_size
        self.radius = self.grid_size - 5
        self.eaten_counter = 0
  
    def draw(self, DISPLAYSURF, frame:int):
        """
            Draws Pac-Man during the Game for each frame

            :param DISPLAYSURF: The Graphicwindow in which the Game will be visualized
            :param frame: The current Frame from one second, has a value between 0 - 59
        """

        #Pac-Man gets drawn
        pg.draw.circle(DISPLAYSURF, Colors.colors['YELLOW'], (self.pos[0] + self.grid_size // 2, self.pos[1] + self.grid_size // 2), self.radius)


        #The rest of the function has to do with Pacmans mouth animation
        # The offsets are there so Pac-Man might look in the correct direction while moving
        x_offset = 0
        y_offset = 0
        x_offset2 = 0
        y_offset2 = 0

        frame %= 20 #< Frame is made %20 so Pac-Man opens and closes his mouth 3 times per second

        if self.direction == 'u':
            y_offset = -1
            x_offset2 = 1
        elif self.direction == 'd':
            y_offset = 1
            x_offset2 = 1
        elif self.direction == 'r':
            x_offset = 1
            y_offset2 = 1
        elif self.direction == 'l':
            x_offset = -1
            y_offset2 = 1

        pacman_center = (self.pos[0] + self.grid_size//2, self.pos[1] + self.grid_size // 2)

        # When Pac-Man moves, his mouth will open and close depending on the current frame number 
        if self.state == 'm' and (frame >= 5 and frame < 20):  
            length_open_mouth = 0 #< This variable sets the width of Pacmans mouth

            if (frame >= 5 and frame < 10) or (frame >= 15 and frame < 20):
                length_open_mouth = self.grid_size - 10

            elif frame >= 10 and frame < 15:
                length_open_mouth = self.grid_size

            # Pacmans mouth gets drawn
            triangle_p1 = (pacman_center[0] + x_offset * self.radius, pacman_center[1] + y_offset * self.radius)
            triangle_p2 = triangle_p1[0] + x_offset2 * length_open_mouth, triangle_p1[1] + y_offset2 * length_open_mouth
            triangle_p3 = triangle_p1[0] - x_offset2 * length_open_mouth, triangle_p1[1] - y_offset2 * length_open_mouth
            pg.draw.polygon(DISPLAYSURF, Colors.colors['BLACK'], (pacman_center, triangle_p2, triangle_p3))

    def update_dir(self, key):
        """
            Depending on the input from the keyboard the direction from Pac-Man will be updated

            :param key: The key that got pressed by the player
        """

        
        if key == K_UP:
            self.last_dir = 'u'           
        elif key == K_DOWN:
            self.last_dir = 'd'
        elif key == K_RIGHT:
            self.last_dir = 'r'           
        elif key == K_LEFT:
            self.last_dir = 'l'           
        pass

    def pre_or_post_turn(self, game_field, all_ghost_out:bool):
        """
            Regualtes the per- and postturns Pac-Man does

            :param game_field: The Gamefield on which Pac-Man will move on
            :param all_ghost_out: A bool that tells if all ghost are out of the ghost house already
        """

        reference_pos = self.pos[0] + self.grid_size // 2, self.pos[1] + self.grid_size // 2 #< Positon is set to center of Pac-Man so there is no difference in which direction he moves
        field = game_field.possible_way(reference_pos, self.last_dir)
        self.cnt_points(field, all_ghost_out)
        self.dist = reference_pos[0] % self.grid_size, reference_pos[1] % self.grid_size

        # Check if Pac-Man is moving to the right 
        if self.direction == 'r':

            # dist to the center of the crossing less then grid_size//2 -> it's a preturn
            if self.dist[0] < self.grid_size // 2:

                # Check if Pac-Man wants to move up after the crossing
                if self.last_dir == 'u':       
                    
                    # Check if the next field is a field Pac-Man can move to
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] += (self.grid_size - (self.pos[0] % self.grid_size))
                        self.pos[1] -= self.speed
                        self.direction = self.last_dir[:]

                # Check if Pac-Man wants to move down after the crossing
                if self.last_dir == 'd':

                    # Check if the next field is a field Pac-Man can move to
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] += (self.grid_size - (self.pos[0] % self.grid_size))
                        self.pos[1] += self.speed
                        self.direction = self.last_dir[:]

            # dist to the center of the crossing greater then grid_size//2 -> it's a postturn
            elif self.dist[0] > self.grid_size // 2:

                 # Check if Pac-Man wants to move up after the crossing
                if self.last_dir == 'u':   
                    
                    # Check if the next field is a field Pac-Man can move to
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] -= (self.pos[0] % self.grid_size)
                        self.pos[1] -= self.speed
                        self.direction = self.last_dir[:]

                # Check if Pac-Man wants to move down after the crossing
                if self.last_dir == 'd':

                    # Check if the next field is a field Pac-Man can move to
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] -= (self.pos[0] % self.grid_size)
                        self.pos[1] += self.speed
                        self.direction = self.last_dir[:]
       
        # The rest of the function does the same as above, just for the other three directions 

        elif self.direction == 'l':
            #Preturn left
            if self.dist[0] > self.grid_size // 2:
                if self.last_dir == 'u':
                       if field == None or (field[0] != 'r' and field != 'os'):
                           self.pos[0] -= (self.pos[0] % self.grid_size)
                           self.pos[1] -= self.speed
                           self.direction = self.last_dir[:]
                if self.last_dir == 'd':
                       if field == None or (field[0] != 'r' and field != 'os'):
                           self.pos[0] -= (self.pos[0] % self.grid_size)
                           self.pos[1] += self.speed
                           self.direction = self.last_dir[:]
            #Postturn left
            elif self.dist[0] < self.grid_size // 2:
                if self.last_dir == 'u':
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] += (self.grid_size - (self.pos[0] % self.grid_size))
                        self.pos[1] -= self.speed
                        self.direction = self.last_dir[:]
                if self.last_dir == 'd':
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] += (self.grid_size - (self.pos[0] % self.grid_size))
                        self.pos[1] += self.speed
                        self.direction = self.last_dir[:]
       
        elif self.direction == 'u':
            #Preturn up
            if self.dist[1] > self.grid_size // 2:
                if self.last_dir == 'l':
                       if field == None or (field[0] != 'r' and field != 'os'):
                           self.pos[0] -= self.speed
                           self.pos[1] -= (self.pos[1] % self.grid_size)
                           self.direction = self.last_dir[:]
                if self.last_dir == 'r':
                       if field == None or (field[0] != 'r' and field != 'os'):
                           self.pos[0] += self.speed
                           self.pos[1] -= (self.pos[1] % self.grid_size)
                           self.direction = self.last_dir[:]
            #Postturn up
            elif self.dist[1] < self.grid_size // 2:
                if self.last_dir == 'l':
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] -= self.speed
                        self.pos[1] += self.grid_size - (self.pos[1] % self.grid_size)
                        self.direction = self.last_dir[:]
                if self.last_dir == 'r':
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] += self.speed
                        self.pos[1] += (self.grid_size - (self.pos[1] % self.grid_size))
                        self.direction = self.last_dir[:]
       
        elif self.direction == 'd':
             #Preturn down
            if self.dist[1] < self.grid_size // 2:
                if self.last_dir == 'l':
                      if field == None or (field[0] != 'r' and field != 'os'):
                           self.pos[0] -= self.speed
                           self.pos[1] += (self.grid_size - (self.pos[1] % self.grid_size))
                           self.direction = self.last_dir[:]
                if self.last_dir == 'r':
                       if field == None or (field[0] != 'r' and field != 'os'):
                           self.pos[0] += self.speed
                           self.pos[1] += (self.grid_size - (self.pos[1] % self.grid_size))
                           self.direction = self.last_dir[:]
            #Postturn down
            elif self.dist[1] > self.grid_size // 2:
                if self.last_dir == 'l':
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] -= self.speed
                        self.pos[1] -= (self.pos[1] % self.grid_size)
                        self.direction = self.last_dir[:]
                if self.last_dir == 'r':
                    if field == None or (field[0] != 'r' and field != 'os'):
                        self.pos[0] += self.speed
                        self.pos[1] -= (self.pos[1] % self.grid_size)
                        self.direction = self.last_dir[:]
        pass

    def update_pos(self, game_field, all_ghost_out, windowsize):
        """
            Updates Pac-Man's position during the game

            :param game_field: The Gamefield on which Pac-Man will move on
            :param all_ghost_out: A bool that tells if all ghost are out of the ghost house already
            :param windowsize: The size of the gamewindow
        """

        # If Pac-Man wants to change the direction into a direction, that is not the same or the opposite of the current direction, it could possible be a pre- or postturn
        if self.direction != self.last_dir and find_opposite(self.last_dir) != self.direction and self.state != '':
            self.pre_or_post_turn(game_field, all_ghost_out)

        # If Pac-Man moves, update his position depending on his direction
        if self.state == 'm':
            fak = 1
            if self.direction == 'u':
                self.pos[1] -= fak * self.speed
            elif self.direction == 'd':
                self.pos[1] += fak * self.speed
            elif self.direction == 'l':
                self.pos[0] -= fak * self.speed
            elif self.direction == 'r':
                self.pos[0] += fak * self.speed

        ongrid = (self.pos[0] % self.grid_size == 0 and self.pos[1] % self.grid_size == 0)

        # When Pac-Man is on grid check the field type he's on and in front of him
        if ongrid :
            field = game_field.possible_way(self.pos, self.last_dir)
            self.cnt_points(field, all_ghost_out)

            # When the next field is a wall of the maze, make Pac-Man stop moving, otherwise let him continue moving
            if field != None and field[0] == 'r':
                field2 = game_field.possible_way(self.pos, self.direction)
                self.cnt_points(field2, all_ghost_out)
                if field2 != None and field2[0] == 'r':
                    self.state = ''
            else:
                self.state = 'm'

            # When the field in front of him is the end of a tunnel move Pac-Man to the other side
            if  field == 'os':
                if self.direction == 'l':
                    self.pos[0] = windowsize[0]            
                elif self.direction == 'r':
                    self.pos[0] = -self.grid_size

            # When the next field is a field Pac-Man can move on to, safe the latest direction in direction
            if (field == None or field[0] != 'r'):
                    self.direction = self.last_dir[:]

            # Force Pacmans direction to drive through the tunnel, just to avoid graphical bugs
            if self.pos[0] < 0:
                self.direction = 'r'
                self.last_dir = 'r'
            elif self.pos[0] > windowsize[0] - self.grid_size:
                self.direction = 'l'
                self.last_dir = 'l'
        
    def can_eat_ghost(self, ghosts : list, current_level:int):
        """
            Evaluates what happens when a ghost and Pac-Man collide under specific circumstances

            :param ghosts: Is a list, that contains all the ghosts in the game
            :param current_level: Shows in which level you currently are
        """

        pac_rect = pg.rect.Rect((self.pos[0], self.pos[1]), (self.grid_size, self.grid_size)) #< Hitbox from Pac-Man
        START_EAT = False
        ghost_cnt = 0
        to_last = length_ghost_list = len(ghosts)

        # Tim has to be in the end of the list
        if length_ghost_list > 4: 
           to_last = -1 

        # Do following Checks for each ghost except the clone of Tim
        for ghost in ghosts[:to_last]:
            ghost_rect = pg.rect.Rect((ghost.pos[0], ghost.pos[1]), (self.grid_size, self.grid_size)) #< Hitbox from a ghost
            colli = pac_rect.colliderect(ghost_rect) #< Look if Pac-Man and the ghost have collided

            # When current level > 20 ghosts can't be eaten anymore
            if current_level >= 21 and self.eat_ghost:
                ghost.cm_flag = True
                self.eat_ghost = False

            # When an energizer got eaten by Pac-Man while the ghosts still wear in frightened, make them vulnerbale for the same time again
            if self.energizer_flag and ghost.first == 1:
                    ghost.first = 0
                    ghost.frightend_frame_counter = 0

            # When Pac-Man ate an energizer and the ghosts are in Scatter, Chase or frightened put them in frightened mode
            if self.eat_ghost and (ghost.state == 's' or ghost.state == 'c' or ghost.state == 'f'):
                if ghost.first == 0:
                    ghost.change_mode('f')
                    ghost.first += 1

            # Check if ghost is in frightened
            if ghost.state == 'f':
                ghost_cnt += 1

                # When the ghost collides with Pac-Man, play the corresponding sounds, add the points, change the ghost mode and add a little extra time to the frightened mode
                if colli:
                    self.play_eatghost()
                    self.play_retreating()
                    self.point_counter += self.count_eaten_ghost
                    self.count_eaten_ghost += self.count_eaten_ghost
                    ghost.change_mode('e')
                    START_EAT = True
                    self.frightened_frame_counter -= HALF_SEC_IN_FRAMES

            # When the ghost collides with Pac-Man while in Scatter or Chase, he will lose a life  
            elif colli and (ghost.state == 'c' or ghost.state == 's') and self.eaten_counter == 0: #and False: #<And False to debugg
                self.play_death()
                self.pause_siren()
                self.eaten_counter += 1
                self.life_counter -= 1
                self.first_eaten = True

        # When no ghost from the list was in frightened mode stop the frightened mode music
        if ghost_cnt == 0:
            self.stop_powerpellet()
        return START_EAT

    def reset(self):
        """
            Resets the Pac-Man object to it's init values
        """
        pg.event.clear()
        self.stop_powerpellet()
        if not self.eaten:
            self.dot_counter = 0
        self.eaten = False
        self.eat_ghost = False
        self.reset_energizer_flag()
        self.last_dir = self.direction = 'l'
        self.count_eaten_ghost = 200
        self.pos = list(self.start_pos)[:]
        self.global_counter = 0
        self.hourglass_counter = 0

    def cnt_points(self, field:str, all_ghost_out:bool):
        """
            Counts Pac-Man's points during the game, when the field he's on is either a 'p' or an 'e' field

            :param field: The field Pac-Man moves towars to
            :param all_ghost_out: A bool that tells if all ghost are out of the ghost house already
        """

        eat_dot = False

        # When field is 'e' that means Pac-Man ate an energizer, so he can now eat ghosts and +50 will be added to his point counter
        if field == 'e':
            self.play_powerpellet()
            eat_dot = True
            self.eat_ghost = True
            self.energizer_flag = True
            self.point_counter += 50
            self.dot_counter += 1
            if self.first_eaten:
                self.global_counter += 1

        # When field is 'p' Pac-Man ate a normal point, which adds +10 to his point counter
        elif field != None and field[0] == 'p':   
            self.play_chomp()
            eat_dot = True
            self.point_counter += 10
            self.dot_counter += 1
            if self.first_eaten:
                self.global_counter += 1

        # If not all ghosts are out of the ghost house the hourglass will be reset
        if eat_dot and not all_ghost_out:
            self.hourglass_counter = 0

    def reset_energizer_flag(self):
        """
            Resets the energizer flag
        """ 
        self.energizer_flag = False

    def count_frames_in_frightened(self):
        """
            Counts the Frames passed since Pac-Man collected an enerigzer, and sets an event flag, if four seconds have passed, so Pac-Man gets vulnerbale again
        """
        if self.energizer_flag:
            self.count_eaten_ghost = 200
            self.frightened_frame_counter = 0
            self.reset_energizer_flag()

        if self.eat_ghost:
            self.frightened_frame_counter += 1

            if self.frightened_frame_counter == FOUR_SEC_IN_FRAMES:
                FRIGHTEND_EVENT = pg.event.Event(FRIGHTEND_MODE)
                pg.event.post(FRIGHTEND_EVENT)
                self.eat_ghost = False
                self.frightened_frame_counter = 0

        else:
            self.frightened_frame_counter = 0

    def eaten_frame_counter(self):
        """
            Counts up a counter, when Pac-Man got eaten, so there is a short break before you restart
        """
        if self.eaten_counter < 120:
            self.eaten_counter += 1
            self.eaten = False
        else: 
            self.eaten_counter = 0
            self.eaten = True