import pygame
import ctypes
import os
import sys
from pygame.draw import *
import math
import random
"""
При нажатии на левую кнопку мыши появляются цели в виде разноцветных шариков. При нажатии (на клавиатуре)
на нижнюю стрелку появляется желтый шар, преследующий цели, если он догоняет их, то "съедает". Оба вида
шариков отражаются от стен, появляющихся случайноым образом при запуске программы.
"""
pygame.init()
FPS = 60
if os.name=="nt":
	ctypes.windll.user32.SetProcessDPIAware()
	window_width = 1200
	window_height = 900
if os.name=="posix":
	window_height = 900
	window_width= 1200
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
TYPES_OF_WALLS = [-1, 1]
list_of_herbivore = []
list_of_pacmans = []
list_of_pacmans_child = []
list_of_walls = []
list_of_foods = []
number_of_walls = 40
number_of_foods = 30
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
	def __init__(self, screen, type_of_wall, x = None, y = None):
		self.screen = screen
		self.color = GREY
		self.type_of_wall = type_of_wall
		if self.type_of_wall == 1:
			self.x_size = walls_x_size
			self.y_size = walls_y_size
		else:
			self.x_size = walls_y_size
			self.y_size = walls_x_size
		if x == None:
			self.x = random.randint(x_borders[0], x_borders[1])
		else:
			self.x = x
		if y == None:
			self.y = random.randint(y_borders[0], y_borders[1])
		else: self.y = y
	def draw(self):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.x_size, self.y_size))

class Pacman:
	"""
	Тип данных, описывающий pacman'а.
	Содержит его координаты, размеры, скорость и направление скорости
	#FIXME Сделать разные виды pacman'ов (например преследующие шарики
	только одного конкретного цвета, или "предсказывающие" траектории шариков) 
	"""
	def __init__(self, screen):
		self.point = 0
		self.screen = screen
		self.color = YELLOW
		self.r = 10
		self.x = random.randint(x_borders[0] + self.r, x_borders[1] - self.r)
		self.y = random.randint(y_borders[0] + self.r, y_borders[1] - self.r)
		self.vx = 3
		self.vy = 3
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
		self.angle_speed = self.vy / self.vx

	def move(self):
		min_distance = 1000000
		min_time_to_targets = 1000000
		vx_per = None
		vy_per = None
		v_relativ_max = None
		sgnvx = 0
		sgnvy = 0
		if not list_of_herbivore == []:
			for targets in list_of_herbivore:
				vx_per = -targets.vx
				vy_per = -targets.vy
				v_per = ((vx_per)**2 + (vy_per)**2)**0.5
				distance = ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5
				cos_vper_distance = (((vx_per * (- self.x + targets.x) + vy_per * (- self.y + targets.y))/ (distance * v_per + 0.000001)))
				diskr = (v_per * cos_vper_distance)**2 - ((v_per)**2 - (self.v)**2)
				v_relativ = ((cos_vper_distance * v_per) + (diskr)**0.5)
				time_to_targets = distance / (v_relativ + 0.00001)
				if (0 < time_to_targets < min_time_to_targets):
					min_time_to_targets = time_to_targets
					v_relativ_max = v_relativ
					current_targets_vx = targets.vx
					current_targets_vy = targets.vy
					self.angle_speed = (targets.y - self.y) / (targets.x - self.x + 0.000001)
					if  targets.y - self.y >= 0:
						sgnvy = 1
					else:
						sgnvy = -1
					if  targets.x - self.x >= 0:
						sgnvx = 1
					else:
						sgnvx = -1
				self.vx = (sgnvx * (v_relativ_max / ((1 + (self.angle_speed)**2))**0.5)) #это скорость пакмана относительно цели
				self.vy = (sgnvy * (((v_relativ_max)**2 - (self.vx)**2)**0.5))			 #
				self.vx += current_targets_vx	# абсолютная скорость пакмана
				self.vy += current_targets_vy
			self.collision_check()
			self.reproduction()
			self.x += self.vx
			self.y += self.vy

	def draw(self):
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
				if wall.type_of_wall == -1:
					self.vy = -self.vy

	def eat_check(self):
		"""
		Функция, проверяющая догнал ли pacman цель. Если догнал, то цель удаляется и
		pacman'у начисляются очки
		"""
		for targets in list_of_herbivore:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r**2:
				list_of_herbivore.remove(targets)
				self.point += targets.point

	def reproduction(self, number_of_food = 3):
		"""
		Функция, создающая нового пакмана рядом с данным, если данный пакман набрал
		number_of_food очков
		"""
		if self.point >= number_of_food:
			added_new_pacman(self.x, self.y, list_of_pacmans_child)
			self.point = 0



class herbivore:
	"""
	Тип данных, описывающий цели.
	Содержит его координаты, размеры, скорость и направление скорости
	"""
	def __init__(self, screen):
		self.parent = None
		self.point = 1
		self.screen = screen
		self.color = BLUE
		self.x = random.randint(x_borders[0], x_borders[1])
		self.y = random.randint(y_borders[0], y_borders[1])
		speed_Food = [-2, 2]
		self.vx = random.randint(speed_Food[0], speed_Food[1])
		self.vy = random.randint(speed_Food[0], speed_Food[1])
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
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
				if wall.type_of_wall == -1:
					self.vy = -self.vy

	def eat_check(self):
		"""
		Функция, проверяющая догнал ли травоядный цель. Если догнал, то цель удаляется и
		pacman'у начисляются очки
		"""
		for targets in list_of_foods:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r**2:
				list_of_foods.remove(targets)
				self.point += targets.point

	def move(self):
		"""
		Данный метод описывает движение пакмана. Метод находит цель, которая находится на наименьшем расстоянии от пакмана,
		и изменяет его скорость так, чтобы он двигался к цели.
		"""
		distance = 1000000
		sgnvx = 0
		sgnvy = 0
		for targets in list_of_foods:
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
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )

class Food:
	def __init__(self, screen):
		self.parent = None
		self.point = 1
		self.screen = screen
		self.color = GREEN
		self.x = random.randint(x_borders[0], x_borders[1])
		self.y = random.randint(y_borders[0], y_borders[1])
		speed_Food = [-2, 2]
		self.vx = random.randint(speed_Food[0], speed_Food[1])
		self.vy = random.randint(speed_Food[0], speed_Food[1])
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
		self.r = 3

	def draw(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )




class Pacman_smart(Pacman):
	'''
	По сравнение со своим родителем умеет огибать препятствия.
	#FIXME Иногда застревает при попытки обойти препятствие, также не может их преодолеть если два
	препятствия находятся рядом
	'''
	def collision_check(self):
		"""
		Функция, проверяющая столкновение pacman'а со стенами и границами экрана. В случае
		столкновения меняет скорости
		#FIXME Сделать разные виды еды (двигающиеся по разному и дающие другое количество очков)
		"""
		if not (x_borders[0] <= (self.x + self.vx + self.r) <= x_borders[1]):
			self.vx = -self.vx
		if not (y_borders[0] <= (self.y + self.vy + self.r) <= y_borders[1]):
			self.vy = -self.vy
		for wall in list_of_walls:
			if (wall.x - (self.r / 2)) <= (self.x + self.vx) <= (wall.x + wall.x_size + (self.r / 2)) and (wall.y - (self.r / 2)) <= (self.y + self.vy) <= (wall.y + wall.y_size + (self.r / 2)):
				if wall.type_of_wall == 1:
					if (self.y - wall.y)**2 <= (self.y - (wall.y + wall.y_size))**2:
						self.vy = -self.v
					else:
						self.vy = self.v
					self.vx = 0 
				if wall.type_of_wall == -1:
					if (self.x - wall.x)**2 <= (self.x - (wall.x + wall.x_size))**2:
						self.vx = -self.v
					else:
						self.vx = self.v
					self.vy = 0 



class Pacman_child(Pacman_smart):
	'''
	Только что появившийся от другого пакмана, всюду следует за родителем, пока не вырастет
	#FIXME Заготовка на будущее, пока не придумал как это будет работать. Дети не должны гнаться
	за едой, они следуют за родителямиб через определенное время они вырастают иначинают
	двигаться самостоятельно
	'''
	def growing_up(self):
		'''
		Функция, переводящая данный обьект из списка детей в список взрослых
		'''
		added_new_pacman(self.x, self.y, list_of_pacmans_child)
		list_of_pacmans_child.remove(self)
	def move(self):
		"""
		Данный метод описывает движение пакмана. Метод находит родителя и изменяет его скорость так, чтобы он двигался к цели.
		"""
		distance = ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5
		self.angle_speed = (self.parent - self.y) / (self.parent - self.x + 0.000001)
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
		self.x += self.vx
		self.y += self.vy

def fill_list_of_walls_separate():
	"""
	Функция заполняющая список стен случайными стенами
	"""
	for i in range (number_of_walls):
		type_of_wall = random.choice(TYPES_OF_WALLS)
		new_wall = Walls(screen, type_of_wall)
		list_of_walls.append(new_wall)

def fill_list_of_walls_continous():
	for i in range (number_of_walls):
		type_of_wall = random.choice(TYPES_OF_WALLS)
		if i == 0:
			new_wall = Walls(screen, type_of_wall, 450, 450)
			list_of_walls.append(new_wall)
		else:
			last_wall = list_of_walls[-1]
			type_of_wall = -(last_wall.type_of_wall)
			COORDINATE_X = [last_wall.x, last_wall.x + last_wall.x_size]
			x_new_wall = random.choice(COORDINATE_X)
			COORDINATE_Y = [last_wall.y, last_wall.y + last_wall.y_size]
			y_new_wall = random.choice(COORDINATE_Y)
			new_wall = Walls(screen, type_of_wall, x_new_wall, y_new_wall)
			list_of_walls.append(new_wall)


def fill_list_of_herbivore():
	"""
	Функция заполняющая список травоядных
	"""
	new_herbivore = herbivore(screen)
	list_of_herbivore.append(new_herbivore)
def fill_list_of_pacmans():
	"""
	Функция заполняющая список pacman'а
	"""
	new_pacman = Pacman_smart(screen)
	list_of_pacmans.append(new_pacman)

def fill_list_of_foods():
	"""
	Функция заполняющая список еды для травоядных
	"""
	for i in range(number_of_foods):
		new_food = Food(screen)
		list_of_foods.append(new_food)

def move_and_draw_all_object():
	"""
	Функция двигающая все обьекты на экране и отрисовывает их (еду и pacman'ов)
	"""
	for herbivore in list_of_herbivore:
		herbivore.move()
		herbivore.draw()
		herbivore.eat_check()
	for pacman in list_of_pacmans:
		pacman.move()
		pacman.draw()
		pacman.eat_check()
	for pacman in list_of_pacmans_child:
		pacman.draw()
		#pacman.move() FIXME# Написать движение pacman_child
	for wall in list_of_walls:
		wall.draw()
	for food in list_of_foods:
		food.draw()
	score(screen, 100, 100, 40)
	pygame.display.update()

def groving_up_check(list_of_creatures = list_of_pacmans_child):
	"""
	Функция проверяющая условия взросления существ в массиве list_of_creatures
	#FIXME необходимо придумать и реализовать условие взросления
	"""
	for children in list_of_creatures:
		if True is False:
			children.growing_up()

def added_new_pacman(x, y, list_ = list_of_pacmans, parent = None):
	"""
	Функция создающая пакмана (или один из его подклассов) в данных координатах (x, y) в массиве list_
	с родителем parent
	"""
	if list_ is list_of_pacmans:
		new_pacman = Pacman_smart(screen)
	if list_ is list_of_pacmans_child:
		new_pacman = Pacman_child(screen)
		new_pacman.color = RED
		new_pacman.r = 8
		new_pacman.parent = parent
	new_pacman.x = x + 10
	new_pacman.y = y + 10
	list_.append(new_pacman)

def added_new_target(x, y, vx = 0, vy = 0):
	new_target = Food(screen)
	new_target.x = x
	new_target.y = y
	new_target.vx = vx
	new_target.vy = vy
	list_of_targets.append(new_target)

def score(screen, x, y, font_size):
    """
    Функция показывает количество очков, набранное каждым pacman'ом
    """
    font2 = pygame.font.Font(None, font_size)
    i = 0
    for pacman in list_of_pacmans:
    	i += 30
    	text = text = "скорость "+ str(round(((pacman.vx)**2+(pacman.vy)**2)**0.5, 2)) + "СЧЕТ "+ str(round(i/30)) + ": " + str(pacman.point)
    	score = font2.render(text, True, YELLOW)
    	screen.blit(score, [x, y + i])
fill_list_of_walls_separate()
fill_list_of_foods()
pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
	pos = pygame.mouse.get_pos()
	screen.fill(BLACK)
	clock.tick(FPS)
	move_and_draw_all_object()
	groving_up_check()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			fill_list_of_herbivore()
	keys = pygame.key.get_pressed()
	if keys[pygame.K_DOWN]:
		fill_list_of_pacmans()
	elif keys[pygame.K_w]:
		added_new_target(pos[0], pos[1])

	pygame.display.update()

pygame.quit()