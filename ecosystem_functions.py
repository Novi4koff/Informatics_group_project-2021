from ecosystem_constants import *

def fill_list_of_walls_separate(body, num):
	"""
	Функция заполняющая список стен случайными стенами (горизонтальными и вертикальными) со 
	случайными координатами
	"""
	for i in range (num):
		type_of_wall = random.choice(TYPES_OF_WALLS)
		new_wall = body(screen, type_of_wall)
		list_of_walls.append(new_wall)

def fill_list_of_herbivore(body, TIME, time_to_die):
	"""
	Функция создающая травоядного со случайными координатами
	"""
	new_herbivore = body(screen, TIME, time_to_die)
	list_of_herbivore.append(new_herbivore)

def fill_list_of_pacmans(body, TIME, time_to_die):
	"""
	Функция создающая хищника с "умной" моделью поведения со случайными координатами
	"""
	new_pacman = body(screen, TIME, time_to_die)
	list_of_pacmans.append(new_pacman)

def fill_list_of_pacmans_direct(body, TIME, time_to_die):
	"""
	Функция создающая хищника с прямолинейной моделью поведения со случайными координатами
	"""
	new_pacman = body(screen, TIME, time_to_die)
	new_pacman.color = WHITE
	list_of_pacmans_direct.append(new_pacman)


def fill_list_of_foods(body, num):
	"""
	Функция заполняющая список еды для травоядных в количестве num
	"""
	for i in range(num):
		new_food = body(screen)
		list_of_foods.append(new_food)

def move_and_draw_all_object(TIME, time_to_die_herbivore, time_to_die_predator):
	"""
	Функция двигает все обьекты на экране и отрисовывает их (еду, травоядных, хищников и стены). Также проверяет
	размножение, смерть и поедание пищи
	"""
	for herbivore in list_of_herbivore:
		herbivore.move()
		herbivore.draw()
		herbivore.eat_check(TIME)
		herbivore.die_check()
		herbivore.reproduction_check(TIME, time_to_die_herbivore)
	for pacman in list_of_pacmans:
		pacman.move()
		pacman.draw()
		pacman.eat_check(TIME)
		pacman.die_check()
		pacman.reproduction_check(TIME, time_to_die_predator)
	for pacman in list_of_pacmans_child:
		pacman.draw()
		#pacman.move() FIXME# Написать движение pacman_child. Если будем использовать подкласс Pacman_child
	for pacman in list_of_pacmans_direct:
		pacman.move()
		pacman.draw()
		pacman.eat_check(TIME)
		pacman.die_check()
		pacman.reproduction_check(TIME, time_to_die_predator)
	for wall in list_of_walls:
		wall.draw()
	for food in list_of_foods:
		food.draw()
	#score(screen, 10, 30, 40)
	Rule_text(screen, 10, 35, 25, 20)
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

def born_new_pacman(body, TIME, x, y, time_to_die, list_ = list_of_pacmans, parent = None):
	"""
	Функция создающая хищника в данных координатах (x, y) в массиве list_
	с родителем parent
	"""
	new_pacman = body(screen, TIME, time_to_die)
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

def added_new_predator(body, TIME, x, y, time_to_die, list_ = list_of_pacmans):
	"""
	Функция добавляющая нового хищника типа body в точку (x, y).
	"""
	new_target = body(screen, TIME, time_to_die)
	if list_ is list_of_pacmans_direct:
		new_target.color = WHITE
	new_target.x = x
	new_target.y = y
	list_.append(new_target)

def added_new_herbivore(body, TIME, x, y, time_to_die):
	"""
	Функция добавляющая нового травоядного типа body в точку (x, y).
	"""
	new_target = body(screen, TIME, time_to_die)
	new_target.x = x
	new_target.y = y
	list_of_herbivore.append(new_target)

def added_new_wall(body, x, y, type_of_wall):
	"""
	Функция добавляющая новую стену типа type_of_wall в точку (x, y).
	"""
	new_target = body(screen, type_of_wall, x, y)
	list_of_walls.append(new_target)

def score(screen, x, y, font_size):
    """
    Функция показывает на экране количество очков, набранное каждым умным хищником
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

def Rule_text(screen, x, y, font_size, indent):
	"""
	Функция, выводящая кнопки управления на экран.
	"""
	font2 = pygame.font.Font(None, font_size)
	text1 = "Создать: W - траву  Q - травоядного"
	text2 = "A - горизонтальную стену  S - вертикальную стену"
	text3 = "Z - умный хищник  X - прямолинейный хищник"
	Rule_text1 = font2.render(text1, True, YELLOW)
	Rule_text2 = font2.render(text2, True, YELLOW)
	Rule_text3 = font2.render(text3, True, YELLOW)
	screen.blit(Rule_text1, [x, y])
	screen.blit(Rule_text2, [x, y + indent])
	screen.blit(Rule_text3, [x, y + 2 * indent])

def grov_new_food(body, TIME, num, period):
	"""
	Функция создающая новую еду каждые period_of_spawn_food единицу времени.
	"""
	global food_time_last
	food_time = TIME // 1000
	if not period == 0:	
		if food_time % period == 0 and not (food_time_last == food_time) :
			fill_list_of_foods(body, num)
			food_time_last = food_time

def grov_new_herbivor(body, TIME, num, period):
	"""
	Функция создающая новых травоядных каждые period единицу времени в количестве num штук
	"""
	global herbivore_time_last
	herbivore_time = TIME // 1000
	if not period == 0:
		if herbivore_time % period == 0 and not (herbivore_time_last == herbivore_time) :
			for i in range(num):
				fill_list_of_herbivore(body, TIME, num)
				herbivore_time_last = herbivore_time

def grov_new_smart_predator(body, TIME, num, period):
	"""
	Функция создающая новых умных хищников каждые period единицу времени в количестве num штук
	"""
	global smart_predator_time_last
	smart_predator_time = TIME // 1000
	if not period == 0:
		if smart_predator_time % period == 0 and not (smart_predator_time_last == smart_predator_time) :
			for i in range(num):
				fill_list_of_pacmans(body, TIME, num)
				smart_predator_time_last = smart_predator_time

def grov_new_direct_predator(body, TIME, num, period):
	"""
	Функция создающая новых прямолинейных хищников каждые period единицу времени в количестве num штук
	"""
	global direct_predator_time_last
	direct_predator_time = TIME // 1000
	if not period == 0:
		if direct_predator_time % period == 0 and not (direct_predator_time_last == direct_predator_time) :
			for i in range(num):
				fill_list_of_pacmans_direct(body, TIME, num)
				direct_predator_time_last = direct_predator_time

def write_data_for_graphic(TIME):
	"""
    Функция записывабщая данные для построения графика в соотвествующие массивы.
    """
	current_number_of_herbivore.append(len(list_of_herbivore))
	current_number_of_predator.append(len(list_of_pacmans))
	current_number_of_predator_direct.append(len(list_of_pacmans_direct))
	current_time_system_living.append(TIME // 10)

def draw_graphic(number_of_foods):
	"""
    Функция рисующая график зависимости числа особей (хищников и травоядных) от времени и сохраняющая
    его в папку Graphics под именем graphic_(number_of_foods)_food.
    """
	plt.plot(current_time_system_living, current_number_of_herbivore)
	plt.ylabel(r'Число особей')
	plt.xlabel(r'время')
	plt.title(r'Число особей от времени')
	plt.plot(current_time_system_living, current_number_of_predator)
	plt.plot(current_time_system_living, current_number_of_predator_direct)
	plt.savefig('Graphics/graphic_' + str(number_of_foods) + '_food')
	plt.show()
