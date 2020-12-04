"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import pygame as pg
import Colors
import pygame_textinput #< Extern Code

class Player:
    """
        This class outputs Graphical content on the Display such as:
            - Highscore table in the start screen
            - Own Points while playing
            - Next Highscore that you can reach
        It also reads the Highscore table file and writes in it when beating a highscore
    """
    MAX_SCORE_NAME_LENGTH = 30 #< Max length of a line when the Highscore table gets drawn on the screen
    FONT_SIZE_HIGHSCORETABLE = 18 #< Size of the characters written
    CURSOR_POS = (92, 389) #< In Pixel
    text_input = pygame_textinput.TextInput(font_family = "ocraextended", 
                                            font_size = 20,
                                            text_color = Colors.colors['WHITE'],
                                            cursor_color = Colors.colors['WHITE'],
                                            max_string_length = 10)

    def __init__(self, grid_size):
        """
            :param grid_size: Is the size of one square side in Pixel 
        """

        # Try to open the file and read from it
        try:
            f = open('.\\etc\\Name_Highscore.txt', "r")
            self.NAME_HIGHSCORE_TABLE = {} 
            text = f.readline()

            # Fill the upper dictionary like "Player : Score" as long as there are data that can be read from the file
            while text != '':
                temp = text.split(' ') #< Split the text in two parts (Player : Score), sepperated by ' ' 
                self.NAME_HIGHSCORE_TABLE[temp[0]] = int(temp[1])
                text = f.readline()
            f.close() #< After done reading close the file
            self.scores = tuple(self.NAME_HIGHSCORE_TABLE.values())
            self.names = tuple(self.NAME_HIGHSCORE_TABLE.keys())

        # When the file can't be opened print out the Error 
        except OSError as err:
            print("OS error: {0}".format(err))

        self.name = ''
        self.highscore_counter = 5
        self.grid_size = grid_size

    def get_name(self, DISP, events, enter_pressed: bool):
        """
            Gets the name the Player Enters, but has following restrictionsto the name:
                - has to be 1-10 chars
                - no ' ' are allowed

            :param DISP: The Graphicwindow in which the Game will be visualized
            :param events: The events from the keyboard, e.g. when a key gets pressed
            :param enter_pressed: A bool that tells if the event was the Enter Key getting pressed
        """

        windowsize = DISP.get_size()
        self.text_input.update(events)
        DISP.blit(self.text_input.get_surface(), self.CURSOR_POS)

        # If enter got pressed set the name of the player to the input
        if enter_pressed:
            name = self.text_input.get_text()

            # No spaces allowed in the Name of the Player
            if name.find(' ') == -1: 
                self.name = name
        pass

    def draw_highscore(self, DISP):
        """
            Will draw the Highscoretable that can be seen in the start screen

            :param DISP: The Graphicwindow in which the Game will be visualized
        """

        start_pos = [80, 514]
        
        # Output the dictionary with the Highscores from other Players on the Display
        for name, score in self.NAME_HIGHSCORE_TABLE.items():
            score_str = str(score)
            multiplier = self.MAX_SCORE_NAME_LENGTH - len(score_str) - len(name) #< The rest space between Name and Score will be filled up with dots
            output = name + multiplier*'.' + score_str
            table_line = self.text_input.font_object.render(output, True, Colors.colors['WHITE'])
            table_line_rect = table_line.get_rect()
            table_line_rect.left = start_pos[0]
            table_line_rect.top = start_pos[1]
            DISP.blit(table_line, table_line_rect) #< Output on the Display like "Name.........Score"
            start_pos[1] += 2 * self.FONT_SIZE_HIGHSCORETABLE #< Go to the next line
        pass

    def draw_score(self, DISP, points:int):
        """
            Draws the next beatable Highscore in the upper right croner and your own score in the upper left corner
            
            :param DISP: The Graphicwindow in which the Game will be visualized
            :param points: The currrent Score Player reached while playing
        """

        Text_Surf_Obj = self.text_input.font_object.render('HIGH SCORE', True, Colors.colors['WHITE'])
        Score_Surf_Obj = self.text_input.font_object.render(self.name + ' ' + str(points), True, Colors.colors['WHITE'])  
        index = self.highscore_counter - 1

        # When the highscore_counter reaches zero the current Player has the highest Score
        if self.highscore_counter == 0:
            index = 0

        highscore_name = self.names[index] #< The Name of the Player with the next possible Highscore
        highscore = str(self.scores[index]) #< The Score of the Player with the next possible Highscore

        # Checks if the Points from the current Player are greater then the next best Highscore
        if points > self.scores[index]:

            # Decreases the highscore_counter by 1 when the highscore_counter > 0
            if self.highscore_counter > 0:
                self.highscore_counter -= 1
                
            # If the current Player already has the highest score, his name and score will be printed on the display
            elif self.highscore_counter == 0:
                highscore = str(points)
                highscore_name = self.name

        # The rest of the function is making the output on the screen, for further details what the functions do visit https://www.pygame.org/docs/
        High_Score_Surf_Obj = self.text_input.font_object.render(highscore_name+ ' ' + highscore, True, Colors.colors['WHITE'])
        Textrec = Text_Surf_Obj.get_rect()
        score_rec = Score_Surf_Obj.get_rect()
        highscore_rec = High_Score_Surf_Obj.get_rect()
        windowsize = DISP.get_size()
        Textrec.centerx = windowsize[0] - highscore_rec.width // 2 - 3 * self.grid_size
        Textrec.top = 0
        score_rec.left = 3 * self.grid_size
        score_rec.top = self.grid_size
        highscore_rec.right = windowsize[0] - 3 * self.grid_size
        highscore_rec.top = self.grid_size
        DISP.blit(Text_Surf_Obj, Textrec)
        DISP.blit(Score_Surf_Obj, score_rec)
        DISP.blit(High_Score_Surf_Obj, highscore_rec)

    def update_highscoretable(self, points : int):
        """
            Updates the Highscore file, by writing the new top five highscores in the table

            :param points: The currrent Score Player reached while playing
        """

        score_is_higher = False

        # Check if the Player's Name already is in the file
        if self.name in self.names: 

            # When the Score of the current Player is less then the Score he already reached, set Flag
            if points <= self.NAME_HIGHSCORE_TABLE[self.name]:
                score_is_higher = True

            # Else put the curent Players Highscore out of the table
            else:
                self.NAME_HIGHSCORE_TABLE.pop(self.name)

        # When the current Player wasn't in the table already
        else:

           # When highscore_counter < 5 remove the lowest score from the highscore table
           if self.highscore_counter < 5:
               self.NAME_HIGHSCORE_TABLE.pop(self.names[-1])

        # When the current Player has beaten his own highscore, or he got a highscore better than one of the top 5, open and write name and reached score in the file
        if not score_is_higher:
            f = open('.\\etc\\Name_Highscore.txt', "w")
            counter = 0

            # Name and Score will be written in the .txt file in decreasing order (by points)
            for name, score in self.NAME_HIGHSCORE_TABLE.items():
            
                if self.highscore_counter == counter:
                    if points > score:
                         f.write(self.name + ' ' + str(points) + '\n')
                    else:
                         f.write(self.name + ' ' + str(score) + '\n')
                f.write(name + ' ' + str(score) + '\n')
                counter += 1
            if self.highscore_counter == 4:
                f.write(self.name + ' ' + str(points) + '\n')
            f.close()
            