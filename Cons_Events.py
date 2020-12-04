"""
Copyright 2020, Köhler Noah & Statz Andre, noah2472000@gmail.com andrestratz@web.de, All rights reserved.
"""

# Declare the different constant Event types and times

import pygame as pg

# USEREVENTS are event types where no input can influence the event
START_REST_TIME = pg.USEREVENT + 1         
FRIGHTEND_MODE = pg.USEREVENT + 2
DOT_HOURGLASS = pg.USEREVENT + 3

# Declare the different times in Milliseconds
TWO_SEC = 2 * 10**3
FOUR_SEC = 4 * 10**3
FIVE_SEC = 5 * 10**3
SEVEN_SEC = 7 * 10**3

# Declare times as Frames. The Game Framerate has to be 60 FPS
HALF_SEC_IN_FRAMES = 30
TWO_SEC_IN_FRAMES = 120
FOUR_SEC_IN_FRAMES = 240