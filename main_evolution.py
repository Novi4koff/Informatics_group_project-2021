import pygame.time
from evolution_constants import *
from evolution_classes import *
from evolution_functions import *
from tkinter import *

"""
При запуске программы появляется number_of_walls стен. Раз в period_of_spawn_food единиц времени появляется 
number_of_foods зеленых шариков (еды) в случайном месте на экране. 
При нажатии на левую кнопку мыши появляются синие шарики (травоядные), которые движутся до ближайшей еды и 
едят ее. При нажатии на клавиатуре на нижнюю стрелку появляется желтый шар (хищник), преследующий травоядных,
если он догоняет их, то ест. Оба вида шариков не могут пройти через стены. Через time_draw_graphic спустя
запуска программы рисуется график зависимости числа особей (хищников и травоядных) от времени.
При нажатии на w создает еду там, где находится курсор мыши. Аналогично для a (вертикальная стена) и s (горизонтальная
стена)
"""

'''Начальные условия (настройки по умолчанию)'''
FPS = 45
number_of_walls = 50
number_of_foods = 30
period_of_spawn_food = 1
time_draw_graphic = 50

def submit(opt1, opt2, opt3, opt4):
	global number_of_walls, number_of_foods, period_of_spawn_food, time_draw_graphic
	number_of_walls = int(opt1)
	number_of_foods = int(opt2)
	period_of_spawn_food = int(opt3)
	time_draw_graphic = int(opt4)

def settings():
	def clicked():
		submit(txt1.get(), txt2.get(), txt3.get(), txt4.get())
		options.destroy()
	options = Tk()
	options.title("Settings")
	options.geometry('400x400')
	lbl1 = Label(options, text="number of walls")
	lbl2 = Label(options, text="number of foods")
	lbl3 = Label(options, text="period of spawn food")
	lbl4 = Label(options, text="time draw graphic")
	txt1 = Entry(options, width=10)
	txt2 = Entry(options, width=10)
	txt3 = Entry(options, width=10)
	txt4 = Entry(options, width=10)
	lbl1.grid(column=0, row=0)
	lbl2.grid(column=0, row=1)
	lbl3.grid(column=0, row=2)
	lbl4.grid(column=0, row=3)
	txt1.grid(column=1, row=0)
	txt2.grid(column=1, row=1)
	txt3.grid(column=1, row=2)
	txt4.grid(column=1, row=3)
	btn4 = Button(options,
				  text="Submit",
				  background="#555",
				  foreground="#ccc",
				  padx="20",
				  pady="8",
				  font="16",
				  command=clicked
				  )
	btn4.grid(column=1, row=4)

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
		move_and_draw_all_object(time)
		groving_up_check()
		write_data_for_graphic(time)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				finished = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				fill_list_of_herbivore(herbivore, time)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_DOWN]:
			fill_list_of_pacmans(Pacman_smart, time)
		elif keys[pygame.K_w]:
			added_new_food(Food, pos[0], pos[1])
		elif keys[pygame.K_s]:
			added_new_wall(Walls, pos[0], pos[1], 1)
		elif keys[pygame.K_a]:
			added_new_wall(Walls, pos[0], pos[1], -1)
		if time // 1000 == time_draw_graphic:
			draw_graphic()
		pygame.display.update()
	pygame.quit()

window = Tk()
window.title("MENU")
window.geometry('600x600')
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
btn3.pack()

window.mainloop()







