import pygame
import ctypes
import os
import sys
from pygame.draw import *
import math
import matplotlib.pyplot as plt
import numpy as np
import random
"""
При запуске программы появляется number_of_walls стен. Раз в period_of_spawn_food единиц времени появляется 
number_of_foods зеленых шариков (еды) в случайном месте на экране. 
При нажатии на левую кнопку мыши появляются синие шарики (травоядные), которые движутся до ближайшей еды и 
едят ее. При нажатии на клавиатуре на нижнюю стрелку появляется желтый шар (хищник), преследующий травоядных,
если он догоняет их, то ест. Оба вида шариков не могут пройти через стены стен. Через time_draw_graphic спустя
запуска программы рисуется график зависимости числа особей (хищников и травоядных) от времени.
При нажатии на w создает еду там, где находится курсор мыши. Аналогично для a (вертикальная стена) и s (горизонатльная
стена)
"""

FPS = 45
if os.name=="nt":
	ctypes.windll.user32.SetProcessDPIAware()
	window_width = 1200
	window_height = 900
if os.name=="posix":
	window_height = 900
	window_width= 1200
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
list_of_walls = []
list_of_foods = []
current_number_of_herbivore = []
current_number_of_predator = []
current_time_system_living = []
food_time_last = -1
walls_x_size = 4
walls_y_size = 60

'''Начальные условия'''
number_of_walls = 50
number_of_foods = 30
period_of_spawn_food = 1
time_draw_graphic = 50

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
		"""
		Функция, отрисовывающая стены
		"""
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.x_size, self.y_size))

class Pacman_smart:
	"""
	Тип данных, описывающий pacman'а (хищник).
	Содержит его координаты, размеры, скорость, направление скорости, время, которое он может прожить без еды, количество
	очков сытости, которое ему необходимо для размножения.
	"""
	def __init__(self, screen):
		self.point = 0
		self.screen = screen
		self.color = YELLOW
		self.r = 10
		self.x = random.randint(x_borders[0] + self.r, x_borders[1] - self.r)
		self.y = random.randint(y_borders[0] + self.r, y_borders[1] - self.r)
		self.vx = 3
		self.vy = 2
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
		self.angle_speed = self.vy / self.vx
		self.time_to_die = 2.5
		self.time_without_food = 0
		self.food_level = 0
		self.last_eat_time = time // 100

	def move(self):
		"""
		Функция, задающая скорость хищника так, чтобы он просчитал кратчайший по времени маршрут до ближайщего травоядного
		и двигающая хищника к нему.
		"""
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
			self.x += self.vx
			self.y += self.vy

	def draw(self):
		"""
		Функция, отрисовывающая хищника в виде желтого шарика
		"""
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )

	def collision_check(self):
		"""
		Функция, проверяющая столкновение pacman'а со стенами и границами экрана. В случае
		столкновения огибает препятствие по кратчайшему пути. 
		#FIXME Застревает в случае столкновения с узкой границей стены
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

	def eat_check(self):
		"""
		Функция, проверяющая догнал ли pacman цель. Если догнал, то цель удаляется и
		pacman'у начисляются очки сытости
		"""
		for targets in list_of_herbivore:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r**2:
				list_of_herbivore.remove(targets)
				self.point += targets.satiety
				self.time_without_food = 0
				self.last_eat_time = time // 100
				self.point += targets.point
			self.time_without_food = (time // 100) - self.last_eat_time 

	def die_check(self):
		"""
		Функция, убивающая хищника, если оно не ело self.time_to_die времени.
		"""
		if (self.time_to_die * 10) <= self.time_without_food:
			list_of_pacmans.remove(self)

	def reproduction_check(self, number_of_food = 3):
		"""
		Функция, создающая нового пакмана рядом с данным, если данный пакман набрал
		number_of_food очков сытости
		"""
		if self.point >= number_of_food:
			added_new_pacman(self.x, self.y)
			self.point = 0



class herbivore:
	"""
	Тип данных, описывающий травоядных.
	Содержит его координаты, размеры, скорость, направление скорости, время, которое он может прожить без еды, количество
	очков сытости, которое ему необходимо для размножения, его сытность для хищника.
	"""
	def __init__(self, screen):
		self.parent = None
		self.point = 0
		self.satiety = 1
		self.screen = screen
		self.color = BLUE
		self.x = random.randint(x_borders[0], x_borders[1])
		self.y = random.randint(y_borders[0], y_borders[1])
		speed_herbivore = [-1, -2, 1, 2]
		self.vx = random.choice(speed_herbivore)
		self.vy = random.choice(speed_herbivore)
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
		self.r = 4
		self.time_to_die = 2.0
		self.time_without_food = 0
		self.food_level = 0
		self.last_eat_time = time // 100

	def collision_check(self):
		"""
		Функция, проверяющая столкновение целей со стенами и границами экрана. В случае
		столкновения меняет скорости так, чтобы травоядных огибал препятсвие
		"""
		if not (x_borders[0] <= (self.x + self.vx) <= x_borders[1]):
			self.vx = -self.vx
		if not (y_borders[0] <= (self.y + self.vy) <= y_borders[1]):
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
	def eat_check(self):
		"""
		Функция, проверяющая догнал ли травоядный цель. Если догнал, то цель удаляется и
		травоядному начисляются очки сытости
		"""
		for targets in list_of_foods:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r**2:
				list_of_foods.remove(targets)
				self.time_without_food = 0
				self.last_eat_time = time // 100
				self.point += targets.point
			self.time_without_food = (time // 100) - self.last_eat_time 

	def move(self):
		"""
		Данный метод описывает движение травоядного. Метод находит цель, которая находится на наименьшем расстоянии от травоядного,
		и изменяет его скорость так, чтобы он двигался к цели.
		"""
		distance = 1000000
		sgnvx = 0
		sgnvy = 0
		if not list_of_foods == []:
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
		"""
		Функция отрисовфвабщая травоядного.
		"""
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )

	def die_check(self):
		"""
		Функция, убивающая травоядного, если оно не ело self.time_to_die времени.
		"""
		if (self.time_to_die * 10) <= self.time_without_food:
			list_of_herbivore.remove(self)

	def reproduction_check(self, number_of_food = 3):
		"""
		Функция, создающая нового травоядного рядом с данным, если данный травоядный набрал
		number_of_food очков сытости
		"""
		if self.point >= number_of_food:
			new_herbivore = herbivore(screen)
			new_herbivore.x = self.x + random.choice([20, -20])
			new_herbivore.y = self.y + random.choice([20, -20])
			list_of_herbivore.append(new_herbivore)
			self.point = 0

class Food:
	"""
	Класс еды для траводяных (зеленые шарики). При поедании дают травоядному Food.point очков сытости 
	"""
	def __init__(self, screen):
		self.point = 1
		self.screen = screen
		self.color = GREEN
		self.x = random.randint(x_borders[0], x_borders[1])
		self.y = random.randint(y_borders[0], y_borders[1])
		self.r = 3

	def draw(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )


class Pacman_child(Pacman_smart): #FIXME Пока никак не используется в программе. Скорее всего и не будет, но пока оставлю
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
	"""
	Функция создающая непрерывную стену 
	#FIXME не работает, впрочем пока и не используется
	"""
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
	Функция заполняющая список хищников
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
	Функция двигает все обьекты на экране и отрисовывает их (еду, травоядных, хищников и стены). Также проверяет
	размножение, смерть и поедание пищи
	"""
	for herbivore in list_of_herbivore:
		herbivore.move()
		herbivore.draw()
		herbivore.eat_check()
		herbivore.die_check()
		herbivore.reproduction_check()
	for pacman in list_of_pacmans:
		pacman.move()
		pacman.draw()
		pacman.eat_check()
		pacman.die_check()
		pacman.reproduction_check()
	for pacman in list_of_pacmans_child:
		pacman.draw()
		#pacman.move() FIXME# Написать движение pacman_child. Если будем использовать подкласс Pacman_child
	for wall in list_of_walls:
		wall.draw()
	for food in list_of_foods:
		food.draw()
	score(screen, 10, 30, 40)
	time_count(screen, 10, 10, 40)
	pygame.display.update()

def groving_up_check(list_of_creatures = list_of_pacmans_child):
	"""
	Функция проверяющая условия взросления существ в массиве list_of_creatures
	#FIXME необходимо придумать и реализовать условие взросления, если решим использовать
	подкласс Pacman_child в программе
	"""
	for children in list_of_creatures:
		if True is False:
			children.growing_up()

def added_new_pacman(x, y, list_ = list_of_pacmans, parent = None):
	"""
	Функция создающая хищника в данных координатах (x, y) в массиве list_
	с родителем parent
	"""
	if list_ is list_of_pacmans:
		new_pacman = Pacman_smart(screen)
	if list_ is list_of_pacmans_child:
		new_pacman = Pacman_child(screen)
		new_pacman.color = RED
		new_pacman.r = 8
		new_pacman.parent = parent
	new_pacman.x = x + random.choice([50, -50])
	new_pacman.y = y + random.choice([50, -50])
	list_.append(new_pacman)

def added_new_food(x, y, vx = 0, vy = 0):
	"""
	Функция добавляющая новую еду в точку (x, y).
	"""
	new_target = Food(screen)
	new_target.x = x
	new_target.y = y
	new_target.vx = vx
	new_target.vy = vy
	list_of_foods.append(new_target)

def added_new_wall(x, y, type_of_wall):
	"""
	Функция добавляющая новую стену типа type_of_wall в точку (x, y).
	"""
	new_target = Walls(screen, type_of_wall, x, y)
	list_of_walls.append(new_target)

def score(screen, x, y, font_size):
    """
    Функция показывает количество очков, набранное каждым pacman'ом
    """
    font2 = pygame.font.Font(None, font_size)
    i = 0
    for pacman in list_of_pacmans:
    	i += 30
    	text = text = "скорость "+ str(round(((pacman.vx)**2+(pacman.vy)**2)**0.5, 2)) + " СЧЕТ "+ str(round(i/30)) + ": " + str(pacman.point)
    	score = font2.render(text, True, YELLOW)
    	screen.blit(score, [x, y + i])

def time_count(screen, x, y, font_size):
	"""
	Функция, выводящая прошедшее со старта программы время на экран.
	"""
	font2 = pygame.font.Font(None, font_size)
	time_text = "Прошло времени: " + str(round(time // 1000))
	Time = font2.render(time_text, True, YELLOW)
	screen.blit(Time, [x, y])

def grov_new_food():
	"""
	Функция создающая новую еду каждые period_of_spawn_food единицу времени.
	"""
	global food_time_last
	food_time = time // 1000
	if food_time % period_of_spawn_food == 0 and not (food_time_last == food_time) :
		fill_list_of_foods()
		food_time_last = food_time

def write_data_for_graphic():
	"""
    Функция записывабщая данные для построения графика в соотвествующие массивы.
    """
	current_number_of_herbivore.append(len(list_of_herbivore))
	current_number_of_predator.append(len(list_of_pacmans))
	current_time_system_living.append(time // 10)

def draw_graphic():
	"""
    Функция рисующая график зависимости числа особей (хищников и травоядных) от времени.
    """
	plt.plot(current_time_system_living, current_number_of_herbivore)
	plt.ylabel(r'Число особей') 
	plt.xlabel(r'время') 
	plt.title(r'Число особей от времени')
	plt.plot(current_time_system_living, current_number_of_predator)
	plt.show() 

pygame.init()
fill_list_of_walls_separate()
pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
	clock.tick(FPS)
	time = pygame.time.get_ticks()
	pos = pygame.mouse.get_pos()
	screen.fill(BLACK)
	grov_new_food()
	move_and_draw_all_object()
	groving_up_check()
	write_data_for_graphic()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			fill_list_of_herbivore()
	keys = pygame.key.get_pressed()
	if keys[pygame.K_DOWN]:
		fill_list_of_pacmans()
	elif keys[pygame.K_w]:
		added_new_food(pos[0], pos[1])
	elif keys[pygame.K_s]:
		added_new_wall(pos[0], pos[1], 1)
	elif keys[pygame.K_a]:
		added_new_wall(pos[0], pos[1], -1)
	if time // 1000 == time_draw_graphic:
		draw_graphic()
	pygame.display.update()

pygame.quit()