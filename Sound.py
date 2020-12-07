"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

import pygame as pg
import Cons_Events

class Sound(object):
    """
        This class contains the different Sounds used during the Game.
    """

    CHOMP_ID = 0
    POWERPELLET_ID = 1
    BEGINNING_ID = 2
    DEATH_ID = 3
    EATGHOST_ID = 4
    EXTRAPAC_ID = 5
    INTERMISSION_ID = 6
    RETREATING_ID = 7
    
    next_siren_music = False #< Check if the next siren sound should be played
    
    def __init__(self):
        """
            All the Sounds will be loaded into a specific Channel that has a number from 0 to 8
        """

        pg.mixer.music.load(".\\sounds\\8-bitDetective.wav")
        self.beginning_sound = pg.mixer.Sound(".\\sounds\\game_start.wav")
        self.chomp_sound = pg.mixer.Sound(".\\sounds\\munch_1.wav")
        var = self.chomp_sound.get_length()
        self.death_sound = pg.mixer.Sound(".\\sounds\\death_1.wav")
        self.eatghost_sound = pg.mixer.Sound(".\\sounds\\eat_ghost.wav")
        self.extrapac_sound = pg.mixer.Sound(".\\sounds\\extend.wav")
        self.intermission_sound = pg.mixer.Sound(".\\sounds\\intermission.wav")
        self.powerpellet_sound = pg.mixer.Sound(".\\sounds\\power_pellet.wav")
        self.powerpellet_sound.set_volume(0.85)
        self.retreating_sound = pg.mixer.Sound(".\\sounds\\retreating.wav")
        
        pg.mixer.set_reserved(self.CHOMP_ID)
        pg.mixer.set_reserved(self.POWERPELLET_ID)
        pg.mixer.set_reserved(self.BEGINNING_ID)
        pg.mixer.set_reserved(self.DEATH_ID)
        pg.mixer.set_reserved(self.EATGHOST_ID)
        pg.mixer.set_reserved(self.EXTRAPAC_ID)
        pg.mixer.set_reserved(self.INTERMISSION_ID)
        pg.mixer.set_reserved(self.RETREATING_ID)

        self.channel_chomp = pg.mixer.Channel(self.CHOMP_ID)
        self.channel_powerpellet = pg.mixer.Channel(self.POWERPELLET_ID)
        self.channel_beginning = pg.mixer.Channel(self.BEGINNING_ID)
        self.channel_death = pg.mixer.Channel(self.DEATH_ID)
        self.channel_eatghost = pg.mixer.Channel(self.EATGHOST_ID)
        self.channel_extrapac = pg.mixer.Channel(self.EXTRAPAC_ID)
        self.channel_intermission = pg.mixer.Channel(self.INTERMISSION_ID)
        self.channel_retreating = pg.mixer.Channel(self.RETREATING_ID)



    # play_example make music/sounds get played
    # stop_example make music/sounds get stopped
    # pause_example make music pause at the specific point they got paused at
    # unpause_example make music play again from where it left off when got paused

    def play_background_music(self):
        pg.mixer.music.play(loops = -1) #<Infinity loop
        pass

    def stop_background_music(self):
        pg.mixer.music.stop()

    def play_beginning(self):
        self.channel_beginning.play(self.beginning_sound) 

    def stop_beginning(self):
        self.channel_beginning.stop()

    def play_chomp(self):
        if not self.channel_chomp.get_busy():
            self.channel_chomp.play(self.chomp_sound)

    def play_death(self):
        self.channel_death.play(self.death_sound)

    def play_eatghost(self):
        self.channel_eatghost.play(self.eatghost_sound)

    def play_extrapac(self):
        self.channel_extrapac.play(self.extrapac_sound)

    def play_intermission(self):
        self.channel_intermission.play(self.intermission_sound, loops = -1) 
    def stop_intermission(self):
        self.channel_intermission.stop()

    def start_siren(self, counter):
        """
            Depending on how many dots already got eaten the siren will get faster and higher piched

            :param counter: The Number of Dots already eaten by Pacman
        """
        
        play = False #< Play for new music
        # Load the different music depending on how much dots are left on the maze        
        if 0 <= counter < 49 and not self.next_siren_music:
            play = not play
            self.next_siren_music = True
            pg.mixer.music.load(".\sounds\siren_1.wav")
        elif 49 <= counter < 98 and self.next_siren_music:
            play = not play
            self.next_siren_music = False
            pg.mixer.music.load(".\sounds\siren_2.wav")
        elif 98 <= counter < 137 and not self.next_siren_music:
            play = not play
            self.next_siren_music = True
            pg.mixer.music.load(".\sounds\siren_3.wav")
        elif 137 <= counter < 186 and self.next_siren_music:
            play = not play
            self.next_siren_music = False
            pg.mixer.music.load(".\sounds\siren_4.wav")
        elif 186 <= counter < 245 and not self.next_siren_music:
            play = not play
            self.next_siren_music = True
            pg.mixer.music.load(".\sounds\siren_5.wav")


        if play:
            pg.mixer.music.stop()
            pg.mixer.music.play(loops = -1)

    def stop_siren(self):
        pg.mixer.music.stop()

    def pause_siren(self):  
        pg.mixer.music.pause()

    def unpause_siren(self):  
        pg.mixer.music.unpause()

    def play_retreating(self):
        self.channel_retreating.play(self.retreating_sound)

    def play_powerpellet(self):
        self.channel_powerpellet.play(self.powerpellet_sound, loops = -1)
        
    def stop_powerpellet(self):
        self.channel_powerpellet.stop()
pass
