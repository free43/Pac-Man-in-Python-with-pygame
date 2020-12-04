"""
Copyright 2020, Köhler Noah & Statz Andre, <NoahsEmail> & andrestratz@web.de, All rights reserved.
"""
import pygame as pg
import Colors
class Game_Field(object):
    """
    Represents the Game-Field.
    """
    """
        The const_look_up_table represents the Game-Field. Each of the strings has his own meaning. 
        Explained in the following part.
        None      ->    Nothing will be drawn
        rx_y_side -> r  is a rectangle, x*grid_size is the size in x direction,
                        y*grid_size is the size in y direction 
                        side -> a black line that overdraws a side from the rectangle to make the walls in the game looking smoother
                                u for up and l for left side of the drawn rectangle.
                                w for white draws the door from the ghost house.
        r ->            r is a rectangle that won't be drawn, but still is a border for the different Figures (Pac-Man, Blinky,...)
        t ->            t describes the Tunnel on this field the ghosts drive slower
        n ->            n stands for not. If one string ending with n this means the ghosts are not allowed to drive up on this field.
        p ->            is one point, it can be collected from Pacman and adds 10 Points to the Score,
                        after collecting it will be a None
        e ->            is one power pellet, it can be collected from Pacman and adds 50 Points to the Score,
                        after collecting it will be a None. It also sets the Ghosts in Frightended Mode and Pac-Man can eat them.
        PACMAN ->       is the start position from Pac-Man
        INKY   ->       is the start position from Inky
        FUNKY  ->       is the start position from Funky
        TIM    ->       is the start position from Tim
        BLINKY ->       is the start position from Blinky
    """
    const_look_up_table = (
                     (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
                     (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
                     (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
                     ('r','r','r','r','r','r','r','r','r','r','r','r','r','r1_4_u','r','r','r','r','r','r','r','r','r','r','r','r','r','r'),
                     ('r','p','p','p','p','p','p','p','p','p','p','p','p','r','r','p','p','p','p','p','p','p','p','p','p','p','p','r'),
                     ('r','p','r3_2','r','r','r','p','r4_2','r','r','r','r','p','r','r','p','r4_2','r','r','r','r','p','r3_2','r','r','r','p','r'),
                     ('r','e','r',None,None,'r','p','r',None,None,None,'r','p','r','r','p','r',None,None,None,'r','p','r',None,None,'r','e','r'),
                     ('r','p','r','r','r','r','p','r','r','r','r','r','p','r','r','p','r','r','r','r','r','p','r','r','r','r','p','r'),
                     ('r','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','r'),
                     ('r','p','r3_1','r','r','r','p','r1_7','r','p','r7_1','r','r','r','r','r','r','r','p','r1_7','r','p','r3_1','r','r','r','p','r'),
                     ('r','p','r','r','r','r','p','r','r','p','r','r','r','r1_3_u','r','r','r','r','p','r','r','p','r','r','r','r','p','r'),
                     ('r','p','p','p','p','p','p','r','r','p','p','p','p','r1','r','p','p','p','p','r','r','p','p','p','p','p','p','r'),
                     ('r5_4','r','r','r','r','r','p','r','r3_1_l','r','r','r',None,'r','r',None,'r3_1','r','r','r_l','r','p','r5_4','r','r','r','r','r'),
                     (None,None,None,None,None,'r','p','r','r','r','r','r','n','r','r','n','r','r','r','r','r','p','r',None,None,None,None,None),
                     (None,None,None,None,None,'r','p','r','r',None,None,None,None,'BLINKY',None,None,None,None,None,'r','r','p','r',None,None,None,None,None),
                     (None,None,None,None,None,'r','p','r','r',None,'r7_4','r','r','rw','rw','r','r','r',None,'r','r','p','r',None,None,None,None,None),
                     ('r','r','r','r','r','r','p','r','r',None,'r',None,None,None,None,None,None,'r',None,'r','r','p','r','r','r','r','r','r'),
                     ('t','t','t','t','t',None,'p',None,None,None,'r','INKY',None,'FUNKY',None,'TIM',None,'r',None,None,None,'p',None,'t','t','t','t','t'),
                     ('r5_4','r','r','r','r','r','p','r1_4','r',None,'r',None,None,None,None,None,None,'r',None,'r1_4','r','p','r5_4','r','r','r','r','r'),
                     (None,None,None,None,None,'r','p','r','r',None,'r','r','r','r','r','r','r','r',None,'r','r','p','r',None,None,None,None,None),
                     (None,None,None,None,None,'r','p','r','r',None,None,None,None,None,None,None,None,None,None,'r','r','p','r',None,None,None,None,None),
                     (None,None,None,None,None,'r','p','r','r',None,'r7_1','r','r','r','r','r','r','r',None,'r','r','p','r',None,None,None,None,None),
                     ('r','r','r','r','r','r','p','r','r',None,'r','r','r','r1_3_u','r','r','r','r',None,'r','r','p','r','r','r','r','r','r'),
                     ('r','p','p','p','p','p','p','p','p','p','p','p','p','r','r','p','p','p','p','p','p','p','p','p','p','p','p','r'),
                     ('r','p','r3_1','r','r','r','p','r4_1','r','r','r','r','p','r','r','p','r4_1','r','r','r','r','p','r3_1','r','r','r','p','r'),
                     ('r','p','r','r','r1_3_u','r','p','r','r','r','r','r','pn','r','r','pn','r','r','r','r','r','p','r1_3_u','r','r','r','p','r'),
                     ('r','e','p','p','r','r','p','p','p','p','p','p','p',None,'PACMAN','p','p','p','p','p','p','p','r','r','p','p','e','r'),
                     ('r2_1_l','r','r','p','r','r','p','r1_3','r','p','r7_1','r','r','r','r','r','r','r','p','r1_3','r','p','r','r','p','r2_1','r','r_l'),
                     ('r','r','r','p','r','r','p','r','r','p','r','r','r','r1_3_u','r','r','r','r','p','r','r','p','r','r','p','r','r','r'),
                     ('r','p','p','p','p','p','p','r','r','p','p','p','p','r','r','p','p','p','p','r','r','p','p','p','p','p','p','r'),
                     ('r','p','r9_1','r','r','r','r','r_u','r','r','r','r','p','r','r','p','r9_1','r','r','r_u','r','r','r','r','r','r','p','r'),
                     ('r','p','r','r','r','r','r','r','r','r','r','r','p','r','r','p','r','r','r','r','r','r','r','r','r','r','p','r'),
                     ('r','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','r'),
                     ('r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r'),
                     (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),
                     (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None),                     
                     )
    
    is_init = False
    
    def __init__(self,  
                 grid_size:int, 
                 FontObj):
        """
        :param grid_size: Is the size of one square side in Pixel. 
        :param FontObj: Describes the displayed font
        """
        # Converting the const look up table to a list so it can be updated.
        self.look_up_table = list(map(convert_to_list, self.const_look_up_table))
        self.grid_size = grid_size
        self.radius = 4 #< Set the radius for the power pellet 
        self.width = self.radius #< Set the width for the rectangels 
        self.FontObj = FontObj
        
    
    def init(self, windowsize:tuple):
        """
        Creates the maze without the Points and Power Pellet. It's saved in self.maze as a pygame.Surface Obeject.
        self.maze will be constant and created just one time. 
        Function needs to be called before call draw function.

        :param windowsize: The size of the game window.
        """
        y_count, x_count = 3, 0 #< Set the starting counter for the look_up_table. y starts with three because the first three lines are just Nones
        # Creating the constant maze 
        maze_size = windowsize[0], windowsize[1] - 2 * self.grid_size
        self.maze = pg.Surface(maze_size) 
        
        
        
        # Draw the outermost rectangles on self.maze
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((0, 3 * self.grid_size), (28 * self.grid_size, 31 * self.grid_size)), 4)
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((0 + self.grid_size // 2, 3 * self.grid_size + self.grid_size // 2),(27 * self.grid_size, 30 * self.grid_size)), 4) 
        # Draw the inner rectangles
        for y in self.look_up_table[3 : -2]: #< y is a list of one row from the maze
            for x in y: #< x is a string that is decoded as already explained
                pos = [self.grid_size * x_count, self.grid_size * y_count]
                # Set reference position in the middle of one square
                pos[0] += self.grid_size // 2
                pos[1] += self.grid_size // 2
                x_count += 1
                # Check if x is rectangle
                if x != None and x[0] == 'r':
                    # When the size of the string is equal or greater than 4 it's rectangle with a specific size and not just a border.
                    if len(x) >= 4:
                        # get the x and y size of the rectangle. x will be something like 'rx1_y1' x1 resprestens the size in x direction and y1 in y direction.
                        xy_dim = x[1:].split("_")   
                        xy_dim[0] = int(xy_dim[0])
                        xy_dim[1] = int(xy_dim[1])
                        rect = tuple(pos), (xy_dim[0] * self.grid_size , xy_dim[1] * self.grid_size )
                        pg.draw.rect(self.maze, Colors.colors['BLUE'], rect, self.width)
                    # If the last char is a w (white), u (up) or l (left) a line gets draw one a specific position 
                    if x[-1] == 'w':
                        self.draw_line(self.maze, 'u', (x_count,y_count), True)
                    if x[-1] == 'u' or x[-1] == 'l':
                        if x_count == 0:
                            self.draw_line(self.maze, x[-1], (len(y), y_count))
                        else:
                            self.draw_line(self.maze, x[-1], (x_count, y_count))
                   
            y_count += 1
            x_count = 0
        # Just some cosmetic drawing
        pg.draw.rect(self.maze, Colors.colors['BLACK'], ((0, 12 * self.grid_size + self.grid_size // 2 + 4), (self.grid_size // 2 + 1, 10 * self.grid_size - 4)), 4)
        pg.draw.rect(self.maze, Colors.colors['BLACK'], ((28 * self.grid_size - self.grid_size // 2 - 1, 12 * self.grid_size + self.grid_size // 2 + 4), (self.grid_size // 2 + 1, 10 * self.grid_size - 4)), 4)
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((-self.width, 13 * self.grid_size), (5 * self.grid_size, 3 * self.grid_size)), self.width)
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((-self.width, 19 * self.grid_size), (5 * self.grid_size, 3 * self.grid_size)), self.width)
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((23 * self.grid_size, 13 * self.grid_size), (5 * self.grid_size + 10, 3 * self.grid_size)), self.width)
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((23 * self.grid_size, 19 * self.grid_size), (5 * self.grid_size + 10, 3 * self.grid_size)), self.width)
        pg.draw.rect(self.maze, Colors.colors['BLUE'], ((11 * self.grid_size, 16 * self.grid_size), (6 * self.grid_size, 3 * self.grid_size)), self.width)
        
        pg.draw.line(self.maze, Colors.colors['BLUE'], (0, 16 * self.grid_size + self.grid_size // 2 - 1), (self.grid_size // 2 + self.width, 16 * self.grid_size + self.grid_size // 2 - 1), self.width)
        pg.draw.line(self.maze, Colors.colors['BLUE'], (0, 18 * self.grid_size + self.grid_size // 2), (self.grid_size // 2 + self.width, 18 * self.grid_size + self.grid_size // 2), self.width)
        pg.draw.line(self.maze, Colors.colors['BLUE'], (self.grid_size * 28 - self.grid_size, 16 * self.grid_size + self.grid_size // 2 - 1), (self.grid_size * 28 + self.width, 16 * self.grid_size + self.grid_size // 2 - 1), self.width)
        pg.draw.line(self.maze, Colors.colors['BLUE'], (self.grid_size * 28 - self.grid_size, 18 * self.grid_size + self.grid_size // 2), (self.grid_size * 28 + self.width, 18 * self.grid_size + self.grid_size // 2), self.width)
        self.is_init = True
    
    def draw(self, DISP, life_counter:int, level:int):
        """
        Draws the maze, the dots in it and the number of Pac-Man's life.

        :param DISP: On which Display the game should be shown.
        :param life_counter: Number of Pac-Man's life.
        """
        assert self.is_init, 'Call first Game_Field.init() before draw game!'
        y_count,x_count = 3, 0
        start_maze = 0, 0
        
        DISP.fill(Colors.colors['BLACK'])
        # Maze get blit on the Screen of the game
        DISP.blit(self.maze, start_maze) 
        # Draw the numer of Pac-Mans's life
        self.draw_pacman_life(life_counter, DISP)   
        # Draw the actual level on the screen
        self.draw_level(DISP, level)
        for y in self.look_up_table[3 : -2]: #< y is a list of one row from the maze
            for x in y: #< x is a string that is decoded as already explained
                pos = [self.grid_size * x_count, self.grid_size * y_count]
                # Set reference position in the middle of one square
                pos[0] += self.grid_size // 2
                pos[1] += self.grid_size // 2
                x_count += 1
                # Check if x is a Dot or an Energizer
                if x != None and (x[0] == 'p' or x == 'e'):
                    radius = 6
                    if x == 'e':
                        radius = self.grid_size // 2 - 4
                        pg.draw.circle(DISP, Colors.colors['POINTS'], tuple(pos), radius)
                    elif x[0] == 'p':
                        pg.draw.rect(DISP, Colors.colors['POINTS'], ((pos[0] - radius // 2, pos[1] - radius // 2), (radius, radius)))
               
                   
            y_count += 1
            x_count = 0
           
    def possible_way(self, pos:tuple, direction:str, ispac = True):
        """
        Look for a value at pos + direction in the look up table and then return the value.

        :param pos: Position of a figure
        :param direction: Direction from a figure {'r', 'l', 'd', 'u'}
        :param ispac: True if the figure is Pac-Man else the Figure isn't Pac-Man
        :return string: The field value of the requested position + direction 
        """
        x_offset, y_offset = 0,0
        # Check the four different directions 
        if direction == 'u':
              y_offset = -1
        elif direction == 'd':
              y_offset = 1
        elif direction == 'r':
              x_offset = 1
        elif direction == 'l':
              x_offset = -1
        x = pos[0] // self.grid_size
        y = pos[1] // self.grid_size
        # If the x position is out of the gamefield that means the figure is at the end of the tunnel
        if x + x_offset >= len(self.look_up_table[1]) or x + x_offset < 0:
            return 'os' #< os: other side -> The figure has to spwan at the other side of the gamefield
        # Get the value from the look up table
        value = self.look_up_table[y + y_offset][x + x_offset] 
        # Check if the value is a dot or an Energizer 
        if value != None and (value[0] =='p' or value[0] == 'e') and ispac:
            # Check if the end of the value field is a 'n' (not). The 'n' shouldn't remove from the gamefield.
            if value[-1] == 'n':
                self.look_up_table[y + y_offset][x + x_offset] = 'n'
            else:
                # Remove the dot or the energizer from the gamefield if Pac-Man eats them.
                self.look_up_table[y + y_offset][x + x_offset] = None
        return value
    
    def find_startpos(self, searched_object:str):
        """

        Returns the spwan position of the asked Object.
        :param searched_object: The name of the searched object such as 'PACMAN' or 'BLINKY' ...
        :return tuple: Spawn position of the asked object. Format (x,y).
        """
        fak = 1 #< When the figure needs to be pushed to the right -> fak = 1 else fak = 0
        # The main figures spwan position beginns at index 14 and ends at size(self.look_up_table) - 9
        start_index = 14
        y = start_index 
        end_index = -9
        for x in self.look_up_table[start_index : end_index]:
            # When the serached object is in the row then get the index of it
            if searched_object in x:
                x = x.index(searched_object)
                break
            y += 1
        # Pac-Man does not need to push to the right
        if searched_object == 'PACMAN':
            fak = 0
        return x * self.grid_size + fak * self.grid_size // 2, y * self.grid_size
    
    def draw_line(self, DISP, side:str, indizes:tuple, pink = False):   
        """
        Draws a blackline (if pink is False otherwise the line will be pink) on the position (indizes[0] * grid_size, indizes[1] * grid_size).
        Side indicates whether the line should be drawn horizontally or vertically. Possible values {'u', 'l'} 'u' -> Up ; 'l' -> Left

        :param DISP: On wich Display the line should be drawn
        :param indizes: The scaled start position from the line
        :param pink: False -> line will be black. 
                     True -> line will be pink. 
        """
        offset = 1 #< Just to draw the line nicely
        pos = (indizes[0] - 1) * self.grid_size, indizes[1] * self.grid_size
        # Check if it's a pink line
        if pink:
            start_pos = pos[0], pos[1] + self.grid_size // 2
            end_pos = pos[0] + self.grid_size, pos[1] + self.grid_size // 2
        # Check if the line should be vertically. u for up
        elif side == 'u':
            start_pos = pos[0] + self.width - offset + self.grid_size // 2, pos[1] + self.grid_size // 2
            end_pos = pos[0] + self.grid_size + offset + self.grid_size // 2 - self.width, pos[1] + self.grid_size // 2
        # Check if the line should be horizontally. l for left
        elif side == 'l':
            start_pos = pos[0] + self.grid_size // 2, pos[1] + self.width - offset + self.grid_size // 2
            end_pos = pos[0] + self.grid_size // 2, pos[1] - self.width + self.grid_size + offset + self.grid_size // 2
        if not pink:
            pg.draw.line(DISP, Colors.colors['BLACK'], start_pos,end_pos, self.width + 2 * offset) 
        else:
            pg.draw.line(DISP, Colors.colors['PINK'], start_pos,end_pos, self.width + 2 * offset) 
    def draw_pacman_life(self, life_counter, DISP):
        """
        Draws Pac-Man's life amount in the bottom left.

        :param life_counter: The number of Pac-Man's life.
        :param DISP: On wich Display the life should be drawn.
        """
        for i in range(1, life_counter):
            # Position depends on the value i
            # Draw yellow circle
            pg.draw.circle(DISP, Colors.colors['YELLOW'], (i * self.grid_size * 2, self.grid_size * 35), 20)
            # Draw Pac-Man's mouth as a black triangle.
            pg.draw.polygon(DISP, Colors.colors['BLACK'], ((i * self.grid_size * 2, self.grid_size * 35), (i * self.grid_size * 2 - 20, self.grid_size * 35 - 20), ( 2 * i * self.grid_size - 20, self.grid_size * 35 + 20)))
    def draw_ready_lose(self, DISP, life_counter = 1):
        """
        Draws either 'READY!' or 'GAMER OVER!' on the screen depending on how much life Pac-Man has left.

        :param DISP: On which Display the text should be shown.
        :param life_counter: The number of Pac-Man's life.
        """
        # When the life_counter isn't 0 that means Pac-Man is still alive and 'READY!' will be drawn in yellow
        if life_counter != 0:
            string = 'READY!'
            color = Colors.colors['YELLOW']
        # When the life_counter is 0 that means Pac-Man isn't alive anymore and 'GAME OVER!' will be drawn in red 
        else:
            string = 'GAME OVER!'
            color = Colors.colors['RED']
        TextSurfObj = self.FontObj.render(string, True, color)
        Textrec = TextSurfObj.get_rect()
        windowsize = DISP.get_size()
        Textrec.centerx = windowsize[0] // 2
        Textrec.top = self.grid_size * 20
        DISP.blit(TextSurfObj, Textrec)
    def draw_level(self, DISP, level:int):
        """
        Shows the current level at the bottom right of the screen.

        :param DISP: On which Display the text should be shown.
        :param level: The current game level.
        """
        windowsize = DISP.get_size()
        Level_Text_Obj =  self.FontObj.render("LEVEL: " + str(level), True, Colors.colors['WHITE'])
        Level_Text_rec = Level_Text_Obj.get_rect()
        Level_Text_rec.top = windowsize[1] - Level_Text_rec.height
        Level_Text_rec.left = windowsize[0] - Level_Text_rec.width
        DISP.blit(Level_Text_Obj, Level_Text_rec)
    
    def reset(self):
        """
        Resets the look up table.
        """
        self.look_up_table = list(map(convert_to_list, self.const_look_up_table))
        

def convert_to_list(element):
    """
    Convertes the element to a list and return it.
    Is needed to convert the const_look_up_table to changeable list.
    """
    return list(element)

