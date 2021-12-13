from evolution_variables import *

def fill_list_of_walls_separate(body):
	"""
	Функция заполняющая список стен случайными стенами
	"""
	for i in range (number_of_walls):
		type_of_wall = random.choice(TYPES_OF_WALLS)
		new_wall = body(screen, type_of_wall)
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

def fill_list_of_herbivore(body, TIME):
	"""
	Функция заполняющая список травоядных
	"""
	new_herbivore = body(screen, TIME)
	list_of_herbivore.append(new_herbivore)

def fill_list_of_pacmans(body, TIME):
	"""
	Функция заполняющая список хищников с "умной" моделью поведения
	"""
	new_pacman = body(screen, TIME)
	list_of_pacmans.append(new_pacman)

def fill_list_of_pacmans_direct(body, TIME):
	"""
	Функция заполняющая список хищников с "прямой"" моделью поведения
	"""
	new_pacman = body(screen, TIME)
	new_pacman.color = WHITE
	list_of_pacmans_direct.append(new_pacman)

def fill_list_of_foods(body):
	"""
	Функция заполняющая список еды для травоядных
	"""
	for i in range(number_of_foods):
		new_food = body(screen)
		list_of_foods.append(new_food)

def move_and_draw_all_object(TIME):
	"""
	Функция двигает все обьекты на экране и отрисовывает их (еду, травоядных, хищников и стены). Также проверяет
	размножение, смерть и поедание пищи
	"""
	for herbivore in list_of_herbivore:
		herbivore.move()
		herbivore.draw()
		herbivore.eat_check(TIME)
		herbivore.die_check()
		herbivore.reproduction_check(TIME)
	for pacman in list_of_pacmans:
		pacman.move()
		pacman.draw()
		pacman.eat_check(TIME)
		pacman.die_check()
		pacman.reproduction_check(TIME)
	for pacman in list_of_pacmans_child:
		pacman.draw()
		#pacman.move() FIXME# Написать движение pacman_child. Если будем использовать подкласс Pacman_child
	for pacman in list_of_pacmans_direct:
		pacman.move()
		pacman.draw()
		pacman.eat_check(TIME)
		pacman.die_check()
		pacman.reproduction_check(TIME)
	for wall in list_of_walls:
		wall.draw()
	for food in list_of_foods:
		food.draw()
	score(screen, 10, 30, 40)
	time_count(TIME, screen, 10, 10, 40)
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

def born_new_pacman(body, TIME, x, y, list_ = list_of_pacmans, parent = None):
	"""
	Функция создающая хищника в данных координатах (x, y) в массиве list_
	с родителем parent
	"""
	new_pacman = body(screen, TIME)
	if list_ is list_of_pacmans_direct:
		new_pacman.color = WHITE
	if list_ is list_of_pacmans_child:
		new_pacman = Pacman_child(screen)
		new_pacman.color = RED
		new_pacman.r = 8
		new_pacman.parent = parent
	new_pacman.x = x + random.choice([50, -50])
	new_pacman.y = y + random.choice([50, -50])
	list_.append(new_pacman)

def added_new_food(body, x, y, vx = 0, vy = 0):
	"""
	Функция добавляющая новую еду в точку (x, y).
	"""
	new_target = body(screen)
	new_target.x = x
	new_target.y = y
	new_target.vx = vx
	new_target.vy = vy
	list_of_foods.append(new_target)

def added_new_predator(body, TIME, x, y, list_ = list_of_pacmans):
	"""
	Функция добавляющая нового хищника типа body в точку (x, y).
	"""
	new_target = body(screen, TIME)
	if list_ is list_of_pacmans_direct:
		new_target.color = WHITE
	new_target.x = x
	new_target.y = y
	list_.append(new_target)

def added_new_wall(body, x, y, type_of_wall):
	"""
	Функция добавляющая новую стену типа type_of_wall в точку (x, y).
	"""
	new_target = body(screen, type_of_wall, x, y)
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

def time_count(TIME, screen, x, y, font_size):
	"""
	Функция, выводящая прошедшее со старта программы время на экран.
	"""
	font2 = pygame.font.Font(None, font_size)
	time_text = "Прошло времени: " + str(round(TIME // 1000))
	Time = font2.render(time_text, True, YELLOW)
	screen.blit(Time, [x, y])

def grov_new_food(body, TIME):
	"""
	Функция создающая новую еду каждые period_of_spawn_food единицу времени.
	"""
	global food_time_last
	food_time = TIME // 1000
	if food_time % period_of_spawn_food == 0 and not (food_time_last == food_time) :
		fill_list_of_foods(body)
		food_time_last = food_time

def write_data_for_graphic(TIME):
	"""
    Функция записывабщая данные для построения графика в соотвествующие массивы.
    """
	current_number_of_herbivore.append(len(list_of_herbivore))
	current_number_of_predator.append(len(list_of_pacmans))
	current_number_of_predator_direct.append(len(list_of_pacmans_direct))
	current_time_system_living.append(TIME // 10)

def draw_graphic():
	"""
    Функция рисующая график зависимости числа особей (хищников и травоядных) от времени.
    """
	plt.plot(current_time_system_living, current_number_of_herbivore)
	plt.ylabel(r'Число особей')
	plt.xlabel(r'время')
	plt.title(r'Число особей от времени')
	plt.plot(current_time_system_living, current_number_of_predator)
	plt.plot(current_time_system_living, current_number_of_predator_direct)
	plt.show()