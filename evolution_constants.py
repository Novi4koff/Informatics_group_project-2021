import os
import ctypes
import pygame
import random
import pygame
import random
import math
import matplotlib.pyplot as plt

window_width = 0
window_height = 0
if os.name == "nt":
	ctypes.windll.user32.SetProcessDPIAware()
	window_width = 1200
	window_height = 900
elif os.name == "posix":
	window_height = 900
	window_width = 1200
screen = pygame.display.set_mode((window_width, window_height))
x_borders = [0, window_width]
y_borders = [0, window_height]
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
TYPES_OF_WALLS = [-1, 1]
list_of_herbivore = []
list_of_pacmans = []
list_of_pacmans_child = []
list_of_pacmans_direct = []
list_of_walls = []
list_of_foods = []
current_number_of_herbivore = []
current_number_of_predator = []
current_time_system_living = []
current_number_of_predator_direct = []
food_time_last = -1
walls_x_size = 4
walls_y_size = 60
'''
Начальные условия
'''
number_of_walls = 0
number_of_foods = 20
period_of_spawn_food = 1
time_draw_graphic = 30
time_to_die_herbivore = 200
time_to_die_predator = 200
