import pygame.time
from ecosystem_constants import *
from ecosystem_classes import *
from ecosystem_functions import *
from tkinter import *

"""
При запуске программы появляется number_of_walls стен. Раз в period_of_spawn_food единиц времени появляется 
number_of_foods зеленых шариков (еды) в случайном месте на экране. 
При нажатии на левую кнопку мыши появляются синие шарики (травоядные), которые движутся до ближайшей еды и 
едят ее. При нажатии на клавиатуре на нижнюю стрелку появляется желтый шар (умный хищник), преследующий травоядных,
если он догоняет их, то ест. При нажатии на верхнюю стрелку появляется белый шар (прямолинейный хищник), который
движется прямо к цели. Все виды шариков не могут пройти через стены. Через time_draw_graphic спустя
запуска программы рисуется график зависимости числа особей (хищников и травоядных) от времени.
При нажатии на w создает еду там, где находится курсор мыши. Аналогично для A (вертикальная стена), S (горизонтальная
стена), Z (умный хищник), X (прямолинейный хищник).
"""


'''Начальные условия (настройки по умолчанию)'''
FPS = 45
number_of_walls = 50
number_of_foods = 30

number_of_herb = 6
period_of_spawn_herb = 10
number_of_smart_predator = 1
period_of_spawn_smart_predator = 5
number_of_direct_predator = 1
period_of_spawn_direct_predator = 5

period_of_spawn_food = 1
time_draw_graphic = 30
time_to_die_herbivore = 2
time_to_die_predator = 2.5

def submit(opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12):
	global number_of_walls, number_of_foods, period_of_spawn_food, time_draw_graphic, time_to_die_predator, time_to_die_herbivore, \
	number_of_herb, period_of_spawn_herb, number_of_smart_predator, period_of_spawn_smart_predator, number_of_direct_predator, \
	period_of_spawn_direct_predator

	number_of_walls = int(opt1)
	number_of_foods = int(opt2)
	period_of_spawn_food = int(opt3)
	number_of_smart_predator = int(opt4)
	period_of_spawn_smart_predator = int(opt5)
	number_of_direct_predator = int(opt6)
	period_of_spawn_direct_predator = int(opt7)
	number_of_herb = int(opt11)
	period_of_spawn_herb = int(opt12)
	time_draw_graphic = int(opt8)
	time_to_die_predator = int(opt9)
	time_to_die_herbivore = int(opt10)


def free_mode():
	"""
	Функция устанавливает все параметры из настроек на 0, кроме time_draw_graphic = 10000
	time_to_die_predator = 100
	time_to_die_herbivore = 100
	"""
	global number_of_walls, number_of_foods, period_of_spawn_food, time_draw_graphic, time_to_die_predator, time_to_die_herbivore, \
	number_of_herb, period_of_spawn_herb, number_of_smart_predator, period_of_spawn_smart_predator, number_of_direct_predator, \
	period_of_spawn_direct_predator
	number_of_walls = 0
	number_of_foods = 0
	period_of_spawn_food = 0
	number_of_smart_predator = 0
	period_of_spawn_smart_predator = 0
	number_of_direct_predator = 0
	period_of_spawn_direct_predator = 0
	number_of_herb = 0
	period_of_spawn_herb = 0
	time_draw_graphic = 10000
	time_to_die_predator = 100
	time_to_die_herbivore = 100

def settings():
	def clicked():
		submit(txt1.get(), txt2.get(), txt3.get(), txt4.get(), txt5.get(), txt6.get(), txt7.get(), txt8.get(), txt9.get(), txt10.get(),
			txt11.get(), txt12.get())
		options.destroy()
	options = Tk()
	options.title("Settings")
	options.geometry('320x320')
	lbl1 = Label(options, text="number of walls")
	lbl2 = Label(options, text="number of foods")
	lbl3 = Label(options, text="period of spawn food")
	lbl4 = Label(options, text="number of smart predators")
	lbl5 = Label(options, text="period of spawn smart ptedators")
	lbl6 = Label(options, text="number of direct predators")
	lbl7 = Label(options, text="period of spawn direct predators")
	lbl8 = Label(options, text="time draw graphic")
	lbl9 = Label(options, text="time live without food predator")
	lbl10 = Label(options, text="time live without food herbivore")
	lbl11 = Label(options, text="number of herbivore")
	lbl12 = Label(options, text="period of spawn herbivore")
	txt1 = Entry(options, width=10)
	txt2 = Entry(options, width=10)
	txt3 = Entry(options, width=10)
	txt4 = Entry(options, width=10)
	txt5 = Entry(options, width=10)
	txt6 = Entry(options, width=10)
	txt7 = Entry(options, width=10)
	txt8 = Entry(options, width=10)
	txt9 = Entry(options, width=10)
	txt10 = Entry(options, width=10)
	txt11 = Entry(options, width=10)
	txt12 = Entry(options, width=10)
	lbl1.grid(column=0, row=0)
	lbl2.grid(column=0, row=1)
	lbl3.grid(column=0, row=2)
	lbl4.grid(column=0, row=3)
	lbl5.grid(column=0, row=4)
	lbl6.grid(column=0, row=5)
	lbl7.grid(column=0, row=6)
	lbl8.grid(column=0, row=7)
	lbl9.grid(column=0, row=8)
	lbl10.grid(column=0, row=9)
	lbl11.grid(column=0, row=10)
	lbl12.grid(column=0, row=11)
	txt1.grid(column=1, row=0)
	txt2.grid(column=1, row=1)
	txt3.grid(column=1, row=2)
	txt4.grid(column=1, row=3)
	txt5.grid(column=1, row=4)
	txt6.grid(column=1, row=5)
	txt7.grid(column=1, row=6)
	txt8.grid(column=1, row=7)
	txt9.grid(column=1, row=8)
	txt10.grid(column=1, row=9)
	txt11.grid(column=1, row=10)
	txt12.grid(column=1, row=11)

	btn4 = Button(options,
				  text="Submit",
				  background="#555",
				  foreground="#ccc",
				  padx="20",
				  pady="8",
				  font="16",
				  command=clicked
				  )
	btn4.grid(column=1, row=12)

def start():
	pygame.init()
	fill_list_of_walls_separate(Walls, number_of_walls)
	pygame.display.update()
	clock = pygame.time.Clock()
	finished = False
	moment_of_start = pygame.time.get_ticks()
	while not finished:
		clock.tick(FPS)
		pos = pygame.mouse.get_pos()
		time = pygame.time.get_ticks() - moment_of_start
		screen.fill(BLACK)
		grov_new_food(Food, time, number_of_foods, period_of_spawn_food)
		grov_new_herbivor(herbivore, time, number_of_herb, period_of_spawn_herb)
		grov_new_smart_predator(Pacman_smart, time, number_of_smart_predator, period_of_spawn_smart_predator)
		grov_new_direct_predator(Pacman_direct, time, number_of_direct_predator, period_of_spawn_direct_predator)
		move_and_draw_all_object(time, time_to_die_herbivore, time_to_die_predator)
		groving_up_check()
		write_data_for_graphic(time)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				finished = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				fill_list_of_herbivore(herbivore, time, time_to_die_herbivore)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_DOWN]:
			fill_list_of_pacmans(Pacman_smart, time, time_to_die_predator)
		elif keys[pygame.K_UP]:
			fill_list_of_pacmans_direct(Pacman_direct, time, time_to_die_predator)
		elif keys[pygame.K_w]:
			added_new_food(Food, pos[0], pos[1])
		elif keys[pygame.K_s]:
			print('')
			added_new_wall(Walls, pos[0], pos[1], 1)
		elif keys[pygame.K_a]:
			added_new_wall(Walls, pos[0], pos[1], -1)
		elif keys[pygame.K_z]:
			added_new_predator(Pacman_smart, time, pos[0], pos[1], time_to_die_predator, list_of_pacmans)
		elif keys[pygame.K_x]:
			added_new_predator(Pacman_direct, time, pos[0], pos[1], time_to_die_predator, list_of_pacmans_direct)
		elif keys[pygame.K_q]:
			added_new_herbivore(herbivore, time, pos[0], pos[1], time_to_die_herbivore)
		if time // 1000 == time_draw_graphic:
			draw_graphic(number_of_foods)
		pygame.display.update()
	pygame.quit()

window = Tk()
window.title("MENU")
window.geometry('300x200')
btn1 = Button(text="Start",
			 background="#555",
			 foreground="#ccc",
			 padx="20",
			 pady="8",
			 font="16",
			 command=start
			 )
btn2 = Button(text="Settings",
			 background="#555",
			 foreground="#ccc",
			 padx="20",
			 pady="8",
			 font="16",
			 command=settings
			 )
btn4 = Button(text="Free mode",
			 background="#555",
			 foreground="#ccc",
			 padx="20",
			 pady="8",
			 font="16",
			 command=free_mode
			 )
btn3 = Button(text="Quit",
			 background="#555",
			 foreground="#ccc",
			 padx="20",
			 pady="8",
			 font="16",
			 command=window.quit
			 )
btn1.pack()
btn2.pack()
btn4.pack()
btn3.pack()

window.mainloop()







