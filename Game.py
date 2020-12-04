"""
Copyright 2020, Köhler Noah & Statz Andre, <NoahsEmail> andrestratz@web.de, All rights reserved.
"""

import pygame as pg
from pygame.locals import *
import sys
import Colors, Game_Field, Level_Counter, Player
import Pacman
import Blinky, Funky, Inky, Tim #<Ghosts
from  Cons_Events import *

class Game:
    """
        Creates and regulates the whole Game
    """

    # Constants
    grid_size = 24 #< Is the size of one square side in Pixel
    windowsize = 28 * grid_size, 36 * grid_size #< Windowsize
    FPS = 60 #< Frames per Second
    # Number of total dots (included the Energizer)   
    NUMB_OF_DOTS = 244

    def init(self):
        """
            Initialize the game.
        """
        
        pg.init()
        self.DISPLAYSURF = pg.display.set_mode(self.windowsize)
        pg.display.set_caption('PAC-MAN')
        pacman_icon = pg.image.load('.\\images\\Pac-Man_Icon.png')
        pg.display.set_icon(pacman_icon)
        self.FPS_Clock = pg.time.Clock()

        self.player_one = Player.Player(self.grid_size)
        self.game_field = Game_Field.Game_Field(self.grid_size, self.player_one.text_input.font_object)
        self.level_counter = Level_Counter.Level_Counter(self.FPS)
        self.game_field.init(self.windowsize)

        #Initiliase Figures
        self.pacman = Pacman.Pacman(self.grid_size, self.game_field.find_startpos('PACMAN'))
        self.blinky = Blinky.Blinky(self.grid_size, self.game_field.find_startpos('BLINKY'))
        self.funky = Funky.Funky(self.grid_size, self.game_field.find_startpos('FUNKY'))
        self.inky = Inky.Inky(self.grid_size, self.game_field.find_startpos('INKY'))
        self.tim = Tim.Tim(self.grid_size, self.game_field.find_startpos('TIM'))

        # Init the ghost list
        self.ghosts = [self.funky, self.blinky, self.inky, self.tim]
     
        # Init the counter
        self.eaten_counter = 0 #< Counts how long the uneaten figures aren't allowed to move
        self.start_counter = 0 #< Counts until the game starts

        # Init the Flags
        self.all_ghost_out = False #< Flag is set when all ghost are out of the house
        self.START = False #< Flag it set when the game has started
        self.PAUSE = False #< Flag is set when the game is in pause
        self.START_EAT = False #< Flag is set if Pac-Man has eaten a ghost
        self.BONUS_LIFE = False #< Flag is set if Pac-Man has 10,000 Points
        self.title_screen()

    def title_screen(self):
        """
            Display the title screen of the Game for four Seconds
        """

        pacman_title_screen = pg.image.load('.\images\\Pac-Man_title_screen.png')
        self.pacman.play_background_music()
        self.DISPLAYSURF.blit(pacman_title_screen, (0, 0)) #< start drawing the image from the position (0, 0)
        pg.display.update()
        finish = False

        # Finish in four Seconds
        while not finish:
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #< Quit the game
                    pg.quit()
                    sys.exit(0)

            # Check if the counter reaches the four seconds
            if self.start_counter == FOUR_SEC_IN_FRAMES:
                finish = True
                self.start_counter = 0
            self.start_counter += 1 #< increment every 1/60th second (if the Framerate is 60) 

            self.FPS_Clock.tick(self.FPS)

        self.start_screen()  

    def start_screen(self):
        """
            Display the start screen of the Game. This includes:
                - The Highscoretable 
                - Name input field
                - Pac-Man and the four Ghost of the game
        """

        pacman_start_screen = pg.image.load('.\\images\\Pac-Man_start_screen.png')
        enter_pressed = False

        # Loop until Player enters a valid name.
        while self.player_one.name == '':      
            self.DISPLAYSURF.blit(pacman_start_screen, (0, 0))
            events = pg.event.get()
            for event in events:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #< Quit the game
                    pg.quit()
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN: #< Check if the Enter key is pressed down
                    enter_pressed = True

            self.player_one.get_name(self.DISPLAYSURF, events, enter_pressed) #< Set the name of the Player
            enter_pressed = False
            self.player_one.draw_highscore(self.DISPLAYSURF)
            pg.display.update()
            self.FPS_Clock.tick(self.FPS)

        # Stop the background music and start the beginning Sound
        self.pacman.stop_background_music()
        self.pacman.play_beginning()

    def run(self):
        """
            Runs the game
        """ 
       
        #Game Loop
        while True:
            self.draw_game_field()
            self.regulate_pacmans_life()
            self.set_ghost_out()

            # Check if Pac-Man got eaten 
            if self.pacman.eaten_counter >= 1:
                self.pacman.eaten_frame_counter()

            #Reset: pacman could collect all 244 dots or he got eaten  
            if self.pacman.dot_counter == self.NUMB_OF_DOTS or self.pacman.eaten:
                self.reset_figures()
                
           
            # Event queue
            for event in pg.event.get():

                # Check if Player press the Escape key or the Player has pressed the x on the window 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #< Quit the game
                    self.player_one.update_highscoretable(self.pacman.point_counter)
                    pg.quit()
                    sys.exit(0)

                # Press the key 'p' to pause your game or to continue it. Only possible if the game started already.
                elif event.type == KEYDOWN and event.key == K_p and self.START: 
                    self.PAUSE = not self.PAUSE
                    if self.PAUSE:
                        self.pacman.pause_siren()
                        self.pacman.play_intermission()
                    else:
                        self.pacman.stop_intermission()
                        self.pacman.unpause_siren()

                # Check if the Ghost finished the frightened Mode
                elif event.type == FRIGHTEND_MODE:
                    pg.event.clear(FRIGHTEND_MODE) #< Delete the event from the queue
                    for g in self.ghosts:
                        g.first = 0 
                        if g.state == 'f':
                            # Set the ghost state to the previous mode of the ghosts
                            g.change_mode(self.level_counter.current_mode)
                    # Reset Pac-Man's flags and counter
                    self.pacman.eat_ghost = False
                    self.pacman.count_eaten_ghost = 200

                # Check if the start- or resttime is over
                elif event.type == START_REST_TIME:
                    pg.event.clear(START_REST_TIME) #< Delete the event from the queue
                    self.start_counter = 0 #< Reset the start counter
                    self.START = True
                    self.pacman.stop_beginning()
                    self.pacman.unpause_siren()

                # Check if Pac-Man didn't eat a dot in the last four seconds
                elif event.type == DOT_HOURGLASS:
                    # Ghost need to be in Home mode to change to Out
                    if self.funky.state == 'h':
                        self.funky.change_mode('o')
                    elif self.inky.state == 'h':
                        self.inky.change_mode('o')
                    elif self.tim.state == 'h':
                        self.tim.change_mode('o')
                        self.all_ghost_out = True #< If tim is out all ghost are out

                # Check if the Player presses one of the arrow keys
                elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_DOWN or event.key == K_RIGHT or event.key == K_LEFT):
                    self.pacman.update_dir(event.key)

            # Draw figures.
            if self.pacman.eaten_counter == 0: #<If Pac-Man is eaten no figure get drawn
                self.draw_figures()

            # Update figures
            if self.START and not self.pacman.eaten_counter: #< The game has started and Pac-Man hasn't been eaten
                self.pacman.start_siren(self.pacman.dot_counter) 

                # Check if the game got paused
                if not self.PAUSE:

                    # Check if Pac-Man hasn't eaten a ghost
                    if not self.START_EAT:
                        self.START_EAT = self.pacman.can_eat_ghost(self.ghosts, self.level_counter.level) 

                    # If all the ghosts are not outside the hourglass has to be started
                    if not self.all_ghost_out:
                        self.hourglass_timing()
                    self.update_figures()
                
            else: #< The game hasn't started or Pac-Man has been eaten
               self.start_counter += 1

               # When four seconds are up start the START_EVENT
               if self.start_counter == FOUR_SEC_IN_FRAMES:
                    START_EVENT = pg.event.Event(START_REST_TIME)
                    pg.event.post(START_EVENT)
                    
               self.game_field.draw_ready_lose(self.DISPLAYSURF)

            # If Pac-Man has eaten a ghost and it's not a break
            if self.START_EAT and not self.PAUSE:

                # Start counting until half of a second is over
                if self.eaten_counter <= HALF_SEC_IN_FRAMES:
                    self.eaten_counter += 1
                else:
                    # Reset the counter and that Pac-Man has eaten a Ghost
                    self.eaten_counter = 0
                    self.START_EAT = False

            pg.display.update()
            self.FPS_Clock.tick(self.FPS)

    def hourglass_timing(self):
        """
            Triggers the hourglass event 
            The counter counts until it has reached the four seconds (FPS = 60) and then triggers the hourglass event
        """

        # Checks if the counter reached the four seconds 
        if self.pacman.hourglass_counter == FOUR_SEC_IN_FRAMES:
            # Triggers the hourglass event
            DOT_HOURGLASS_EVENT = pg.event.Event(DOT_HOURGLASS)
            pg.event.post(DOT_HOURGLASS_EVENT)
            self.pacman.hourglass_counter = 0
        else:
            self.pacman.hourglass_counter += 1

    def update_figures(self):
        """
            Updates all figures: 
                Pac-Man, Blinky, Funky, Inky and Tim
        """

        self.pacman.count_frames_in_frightened()
        self.level_counter.update_figures_speed(self.game_field, self.pacman, self.ghosts)
        self.level_counter.update_states(self.ghosts)

        # Update the ghosts
        if not self.START_EAT or self.blinky.state == 'e': #< Is needed if Pac-Man eats a ghost and just the eaten Ghosts have to be updated. 
            self.blinky.update(tuple(self.pacman.pos), self.level_counter.current_mode,self.game_field, self.windowsize[0])

        if not self.START_EAT or self.funky.state == 'e': #< Same like above
            self.funky.update(tuple(self.pacman.pos), self.level_counter.current_mode, self.game_field,self.windowsize[0], self.level_counter.level)

        if not self.START_EAT or self.inky.state == 'e':#< Same like above
            self.inky.update(tuple(self.pacman.pos), self.pacman.direction, tuple(self.blinky.pos),self.level_counter.current_mode,self.game_field, self.windowsize[0])

        if not self.START_EAT or self.tim.state == 'e':#< Same like above
            self.tim.update(tuple(self.pacman.pos), self.level_counter.current_mode, self.game_field, self.windowsize[0])

        # Check if Tim has to stay
        if self.tim.stay:
            # Just append one new_tim in the ghosts list
            if self.ghosts.count(self.tim.new_tim) == 0:
                self.ghosts.append(self.tim.new_tim)
        else:
            # Just remove new_tim if there is one in the ghosts list
            if self.ghosts.count(self.tim.new_tim) > 0:
                self.ghosts.remove(self.tim.new_tim)

        if not self.START_EAT : #< Just update Pac-Man if he didn't eat a ghost
                self.pacman.update_pos(self.game_field, self.all_ghost_out, self.windowsize)
        pass

    def reset_figures(self):
        """
            Resets all figures to their init values
                Pac-Man, Blinky, Funky, Inky and Tim
        """
        
        self.pacman.pause_siren()
       
        # Check if Tim's clone is in the ghosts list
        if self.tim.new_tim in self.ghosts:
            # Remove the clone from the list
            self.ghosts.remove(self.tim.new_tim)

        # Check if Pac-Man hasn't got eaten
        if not self.pacman.eaten:
            self.game_field.reset()

        # Stop the power pellet sound
        self.pacman.stop_powerpellet()

        # Reset all figures to their init values
        self.blinky.reset()
        self.inky.reset()
        self.tim.reset()
        self.funky.reset()
        self.level_counter.reset()
        self.all_ghost_out = False #< Reset the flag, because the ghost spawn again in the ghost house

        # Check if Pac-Man eat all dots. There are 244 dots on the gameboard
        if self.pacman.dot_counter == self.NUMB_OF_DOTS:
            self.level_counter.level += 1 #< Increase the level by one
            self.pacman.first_eaten = False
            # Set the Ghost in the Out mode
            self.funky.state = 'o'
            self.inky.state = 'o' #< Inky switches directly to the out mode from level two 

            # Tim switches directly to the out mode from level three 
            if self.level_counter.level >= 3:
                self.tim.state = 'o'

        self.pacman.reset()
        # Reset the start flag so that another pause is made
        self.START = False 

    def draw_figures(self):
        """
            Draw all figures:
                Pac-Man, Blinky, Funky, Inky and Tim
        """

        self.pacman.draw(self.DISPLAYSURF, self.level_counter.frame_counter) 
        for ghost in self.ghosts:
            ghost.draw(self.DISPLAYSURF, self.level_counter.frame_counter)

    def set_ghost_out(self):
        """
            Sets the ghosts -> Funky, Inky and Tim in the Out mode
        """

        # checks whether Pac-Man has already been eaten in the level
        if not self.pacman.first_eaten: #< Pac-Man hasn't already been eaten

            # Check what level the game is at
            if self.level_counter.level == 1:
                # Level 1
                if  self.pacman.dot_counter == 30 and self.inky.state == 'h' : #< Pac-Man has already eaten 30 dots and Inky is still in the Home mode
                    self.inky.change_mode('o')        
                elif self.pacman.dot_counter == 60 and self.tim.state == 'h': #< Pac-Man has already eaten 60 dots and Tim is still in the Home mode
                    self.tim.change_mode('o')

            elif self.level_counter.level == 2:
                # Level 2
                if self.pacman.dot_counter == 50 and self.tim.state == 'h': #< Pac-Man has already eaten 50 dots and Tim is still in the Home mode
                    self.tim.change_mode('o')

        else: #< Pac-Man has already been eaten
            if self.pacman.global_counter == 7 and self.funky.state == 'h': #< Pac-Man has eaten 7 dots since he was respawned and Funky is still in the home mode
                self.funky.change_mode('o')
            elif self.pacman.global_counter == 14 and self.inky.state == 'h': #< Pac-Man has eaten 14 dots since he was respawned and Inky is still in the home mode
                self.inky.change_mode('o')        
            elif self.pacman.global_counter == 32 and self.tim.state == 'h': #< Pac-Man has eaten 32 dots since he was respawned and Tim is still in the home mode
                self.tim.change_mode('o')

    def regulate_pacmans_life(self):
        """
            Check if Pac-Man is still alive or if he won a Bonus life
        """

        # Check if Pac-Man has already 10,000 Points and that he has not already received the bonus life
        if self.pacman.point_counter >= 10000 and not self.BONUS_LIFE:
                self.pacman.play_extrapac()
                self.BONUS_LIFE = True
                self.pacman.life_counter += 1

        # Check whether Pac-man has no life left
        if self.pacman.life_counter == 0: 
            self.pacman.stop_siren()
            # Displays the Game Over screen
            self.game_field.draw_ready_lose(self.DISPLAYSURF, 0) 
            pg.display.update() 
            pg.time.wait(TWO_SEC) #< Wait for two seconds
            self.player_one.update_highscoretable(self.pacman.point_counter) #< Update the highscoretable
            # Initliaze the game again
            self.init() 

    def draw_game_field(self):
        """
            Draws gamefield without the figures
        """
        self.game_field.draw(self.DISPLAYSURF, self.pacman.life_counter, self.level_counter.level)
        self.player_one.draw_score(self.DISPLAYSURF, self.pacman.point_counter)
        
        