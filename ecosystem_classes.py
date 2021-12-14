from ecosystem_constants import *
from ecosystem_functions import *

class Walls:
	"""
	Тип данных, описывающий стену.
	Содержит координаты(Walls.x и Walls.y) и размеры(Walls.x_size и Walls.y_size) стены а также тип (1 - вертикальная стена,
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
	Тип данных, описывающий хищника с умной моделью поведения.
	Содержит его координаты(Pacman_smart.x и Pacman_smart.y), размеры(Pacman_smart.r), скорость(Pacman_smart.vx и Pacman_smart.vy),
	направление скорости(Pacman_smart.angle_speed), время(Pacman_smart.time_without_food), которое он может прожить без еды, текущее количество
	очков сытости(self.point).
	"""
	def __init__(self, screen, TIME, time_to_die_predator):
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
		self.time_to_die = time_to_die_predator
		self.time_without_food = 0
		self.last_eat_time = TIME // 100

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
				if list_of_foods == []:
					targets.vx = targets.vy = 0
				vx_per = -targets.vx
				vy_per = -targets.vy
				distance = ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5
				if not ((vx_per == 0) and (vy_per == 0)): 
					v_per = ((vx_per)**2 + (vy_per)**2)**0.5
					cos_vper_distance = (((vx_per * (- self.x + targets.x) + vy_per * (- self.y + targets.y))/ (distance * v_per + 0.000001)))
					diskr = (v_per * cos_vper_distance)**2 - ((v_per)**2 - (self.v)**2)
					v_relativ = ((cos_vper_distance * v_per) + (diskr)**0.5)
					time_to_targets = distance / (v_relativ + 0.00001)
				else:
					v_relativ = self.v
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

	def eat_check(self, TIME):
		"""
		Функция, проверяющая догнал ли pacman цель. Если догнал, то цель удаляется и
		pacman'у начисляются очки сытости
		"""
		for targets in list_of_herbivore:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r**2:
				list_of_herbivore.remove(targets)
				self.point += targets.satiety
				self.time_without_food = 0
				self.last_eat_time = TIME // 100
				self.point += targets.point
			self.time_without_food = (TIME // 100) - self.last_eat_time

	def die_check(self):
		"""
		Функция, убивающая хищника, если оно не ело self.time_to_die времени.
		"""
		if (self.time_to_die * 10) <= self.time_without_food:
			list_of_pacmans.remove(self)

	def reproduction_check(self, TIME, time_to_die, number_of_food = 3):
		"""
		Функция, создающая нового пакмана рядом с данным, если данный пакман набрал
		number_of_food очков сытости
		"""
		if self.point >= number_of_food:
			born_new_pacman(Pacman_smart, TIME, self.x, self.y, time_to_die)
			self.point = 0

class Pacman_direct(Pacman_smart):
	"""
	Тип данных, описывающий хищника с прямолинейной моделью поведения. В отличии от Pacman_smart просто следует за целью
	в любой ситуации, отвлекаясь лишь на огибание препятствия.
	"""
	def move(self):
		"""
		Данный метод описывает движение хищника. Метод находит цель, которая находится на наименьшем расстоянии от хищника,
		и изменяет его скорость так, чтобы он двигался к цели.
		"""
		distance = 1000000
		sgnvx = 0
		sgnvy = 0
		if not list_of_herbivore == []:
			for targets in list_of_herbivore:
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

	def die_check(self):
		"""
		Функция, убивающая хищника, если оно не ело self.time_to_die времени.
		"""
		if (self.time_to_die * 10) <= self.time_without_food:
			list_of_pacmans_direct.remove(self)

	def reproduction_check(self, TIME, time_to_die, number_of_food = 3):
		"""
		Функция, создающая нового хищника рядом с данным, если данный пакман набрал
		number_of_food очков сытости
		"""
		if self.point >= number_of_food:
			born_new_pacman(Pacman_direct, TIME, self.x, self.y, time_to_die, list_of_pacmans_direct)
			self.point = 0

class herbivore:
	"""
	Тип данных, описывающий травоядных.
	Содержит его координаты (herbivore.x и herbivore.y), размеры(herbivore.r), скорость (herbivore.vx и herbivore.vy),
	время(herbivore.time_without_food), которое он может прожить без еды, текущее количество количество
	очков сытости(herbivore.point), которое ему необходимо для размножения, его сытность для хищника(herbivore.satiety).
	"""
	def __init__(self, screen, TIME, time_to_die_herbivore):
		self.parent = None
		self.point = 0
		self.satiety = 1
		self.screen = screen
		self.color = BLUE
		self.r = 4
		self.x = random.randint(x_borders[0] + self.r, x_borders[1] - self.r)
		self.y = random.randint(y_borders[0] + self.r, y_borders[1] - self.r)
		speed_herbivore = [-2, -1, 1, 2]
		self.vx = random.choice(speed_herbivore)
		self.vy = random.choice(speed_herbivore)
		self.v = ((self.vx)**2 + (self.vy)**2)**0.5
		self.time_to_die = time_to_die_herbivore
		self.time_without_food = 0
		self.last_eat_time = TIME // 100

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

	def eat_check(self, TIME):
		"""
		Функция, проверяющая догнал ли травоядный цель. Если догнал, то цель удаляется и
		травоядному начисляются очки сытости
		"""
		for targets in list_of_foods:
			if ((self.x - targets.x)**2 + (self.y - targets.y)**2)**0.5 <= targets.r**2:
				list_of_foods.remove(targets)
				self.time_without_food = 0
				self.last_eat_time = TIME // 100
				self.point += targets.point
			self.time_without_food = (TIME // 100) - self.last_eat_time

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
		Функция отрисовывающая травоядного.
		"""
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.r )

	def die_check(self):
		"""
		Функция, убивающая травоядного, если оно не ело self.time_to_die времени.
		"""
		if (self.time_to_die * 10) <= self.time_without_food:
			list_of_herbivore.remove(self)

	def reproduction_check(self, TIME, time_to_die, number_of_food = 3):
		"""
		Функция, создающая нового травоядного рядом с данным, если данный травоядный набрал
		number_of_food очков сытости
		"""
		if self.point >= number_of_food:
			new_herbivore = herbivore(screen, TIME, time_to_die)
			new_herbivore.x = self.x + random.choice([20, -20])
			new_herbivore.y = self.y + random.choice([20, -20])
			list_of_herbivore.append(new_herbivore)
			self.point = 0

class Food:
	"""
	Класс еды для траводяных (зеленые шарики). При поедании дают травоядному Food.point очков сытости. Обладают
	радиусом Food.r и координатами Food.x b Food.y
	"""
	def __init__(self, screen):
		self.point = 1
		self.screen = screen
		self.color = GREEN
		self.r = 3
		self.x = random.randint(x_borders[0] + 3 * self.r, x_borders[1] - 3 * self.r)
		self.y = random.randint(y_borders[0] + 3 * self.r, y_borders[1] - 3 * self.r)

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
