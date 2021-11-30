#Импортирование библиотек
import pygame
import sys
import os
import ctypes
from pygame.draw import *
import math
import random
"""
При нажатии на левую кнопку мыши появляются цели в виде разноцветных шариков. При нажатии (на клавиатуре)
на нижнюю стрелку появляется желтый шар, преследующий цели, если он догоняет их, то "съедает". Оба вида
шариков отражаются от стен, появляющихся случайноым образом при запуске программы.
"""
pygame.init()
FPS = 120
if os.name=="nt":
	ctypes.windll.user32.SetProcessDPIAware()
	window_width = 1200
	window_height = 900
if os.name=="posix":
	window_height = 600
	window_width= 600
screen = pygame.display.set_mode((window_width, window_height))
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
list_of_targets = []
list_of_pacmans = []
list_of_walls = []
number_of_walls = 20
walls_x_size = 4
walls_y_size = 60
x_borders = [0, window_width]
y_borders = [0, window_height]

class Walls:
	"""
	Тип данных, описывающий стену.
	Содержит координаты и размеры стены а также тип (1 - вертикальная стена, 
	2 - горизонтальная стена)
	"""
	def __init__(self, screen, type_of_wall):
		"""
		Функция задаёт значения параметров класса (поверхность, цвет, тип стены, ширину, высоту, координаты левой верхней вершины).
		"""
		self.screen = screen
		self.color = GREY
		self.type_of_wall = type_of_wall
		if self.type_of_wall == 1:
			self.x_size = walls_x_size
			self.y_size = walls_y_size
		else:
			self.x_size = walls_y_size
			self.y_size = walls_x_size
		self.x = random.randint(x_borders[0], x_borders[1])
		self.y = random.randint(y_borders[0], y_borders[1])
	def draw(self):
		"""
		Этот метод рисует стену в виде серого прямоугольника.
		"""
		pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.x_size, self.y_size))
class Pacman:
	"""
	Тип данных, описывающий pacman'а.
	Содержит его координаты, размеры, скорость и направление скорости
	#FIXME Сделать разные виды pacman'ов (например преследующие шарики
	только одного конкретного цвета, или "предсказывающие" траектории шариков) 
	"""
	def __init__(self, screen):
		"""
		Функция инициализации пакмана. Его параметры - счётчик очков, поверность, цвет, радиус, начальные координаты,
		начальная скорость, начальная общая скорость и тангенс угла наклона скорости к горизонту
		"""
		self.point = 0
		self.screen = screen
		self.color = YELLOW
		self.r = 10
		self.x = random.randint(x_borders[0] + self.r, x_borders[1] - self.r)
		self.y = random.randint(y_borders[0] + self.r, y_borders[1] - self.r)
		self.vx = 2
		self.vy = 2
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
		self.angle_speed = self.vy / self.vx

	def move(self):
		"""
		Данный метод описывает движение пакмана. Метод находит цель, которая находится на наименьшем расстоянии от пакмана,
		и изменяет его скорость так, чтобы он двигался к цели.
		"""
		distance = 1000000
		sgnvx = 0
		sgnvy = 0
		for targets in list_of_targets:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 < distance:
				distance = ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5
				self.angle_speed = (targets.y - self.y) / (targets.x - self.x + 0.000001)
				if  targets.y - self.y >= 0:
					sgnvy = 1
				else:
					sgnvy = -1
				if  targets.x - self.x >= 0:
					sgnvx = 1
				else:
					sgnvx = -1
		self.vx = sgnvx * (self.v / ((1 + (self.angle_speed)**2))**0.5)
		self.vy = sgnvy * (((self.v)**2 - (self.vx)**2)**0.5) 
		self.collision_check()
		if distance < 1000000:
			self.x += self.vx
			self.y += self.vy

	def draw(self):
		"""
		Метод рисует пакмана в виде жёлтого шарика
		"""
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )

	def collision_check(self):
		"""
		Функция, проверяющая столкновение pacman'а со стенами и границами экрана. В случае
		столкновения меняет скорости
		#FIXME Сделать разные виды еды (двигающиеся по разному и дающие другое количество очков)
		"""
		if not (x_borders[0] <= (self.x + self.vx) <= x_borders[1]):
			self.vx = -self.vx
		if not (y_borders[0] <= (self.y + self.vy) <= y_borders[1]):
			self.vy = -self.vy
		for wall in list_of_walls:
			if (wall.x) <= (self.x + self.vx) <= (wall.x + wall.x_size) and (wall.y) <= (self.y + self.vy) <= (wall.y + wall.y_size):
				if wall.type_of_wall == 1:
					self.vx = -self.vx
				if wall.type_of_wall == 2:
					self.vy = -self.vy

	def eat_check(self):
		"""
		Функция, проверяющая догнал ли pacman цель. Если догнал, то цель удаляется и
		pacman'у начисляются очки
		"""
		for targets in list_of_targets:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r:
				list_of_targets.remove(targets)
				self.point += targets.point
class Food:
	"""
	Тип данных, описывающий цели.
	Содержит его координаты, размеры, скорость и направление скорости
	"""
	def __init__(self, screen):
		"""
		Метод инициаоизрует парамеры цели (очки, поверхность, цвет, координаты, скорость, радиус)
		"""
		self.point = 1
		self.screen = screen
		self.color = random.choice(GAME_COLORS) 
		self.x = random.randint(x_borders[0], x_borders[1])
		self.y = random.randint(y_borders[0], y_borders[1])
		speed_Food = [-5, 5]
		self.vx = random.randint(speed_Food[0], speed_Food[1])
		self.vy = random.randint(speed_Food[0], speed_Food[1])
		self.r = 4
	def collision_check(self):
		"""
		Функция, проверяющая столкновение целей со стенами и границами экрана. В случае
		столкновения меняет скорости
		"""
		if not (x_borders[0] <= (self.x + self.vx) <= x_borders[1]):
			self.vx = -self.vx
		if not (y_borders[0] <= (self.y + self.vy) <= y_borders[1]):
			self.vy = -self.vy
		for wall in list_of_walls:
			if (wall.x) <= (self.x + self.vx) <= (wall.x + wall.x_size) and (wall.y) <= (self.y + self.vy) <= (wall.y + wall.y_size):
				if wall.type_of_wall == 1:
					self.vx = -self.vx
				if wall.type_of_wall == 2:
					self.vy = -self.vy
	def move(self):
		"""
		Метод, описывающий движение цели
		"""
		self.collision_check()
		self.x += self.vx
		self.y += self.vy
	def draw(self):
		"""
		Метод рисует цель в виде маленького шарика
		"""
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )
def fill_list_of_walls():
	"""
	Функция заполняющая список стен случайными стенами
	"""
	for i in range (number_of_walls):
		type_of_wall = random.randint(1, 2)
		new_wall = Walls(screen, type_of_wall)
		list_of_walls.append(new_wall)
def fill_list_of_targets():
	"""
	Функция заполняющая список целей случайными целями
	"""
	new_target = Food(screen)
	list_of_targets.append(new_target)
def fill_list_of_pacmans():
	"""
	Функция заполняющая список pacman'а
	"""
	new_pacman = Pacman(screen)
	list_of_pacmans.append(new_pacman)
def move_all_object():
	"""
	Функция, двигающая все обьекты на экране (еду и pacman'ов) и следящая за количество очков, полученных пакманом за поимку цели.
	"""
	for target in list_of_targets:
		target.move()
		target.draw()
	for pacman in list_of_pacmans:
		pacman.move()
		pacman.draw()
		pacman.eat_check()
	for wall in list_of_walls:
		wall.draw()
	score(screen, 100, 100, 40)
	pygame.display.update()
def score(screen, x, y, font_size):
    """
    Функция показывает количество очков, набранное каждым pacman'ом
    """
    font2 = pygame.font.Font(None, font_size)
    i = 0
    for pacman in list_of_pacmans:
    	i += 30
    	text = "СЧЕТ "+ str(i/30) + ": " + str(pacman.point)
    	score = font2.render(text, True, YELLOW)
    	screen.blit(score, [x, y + i])
fill_list_of_walls()
pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
	screen.fill(BLACK)
	clock.tick(FPS)
	move_all_object()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			fill_list_of_targets()
	keys = pygame.key.get_pressed()
	if keys[pygame.K_DOWN]:
		fill_list_of_pacmans()
	pygame.display.update()

pygame.quit()
