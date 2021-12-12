from evolution_variables import *
from evolution_classes import *
from evolution_functions import *
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
pygame.init()
fill_list_of_walls_separate(Walls)
pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
	clock.tick(FPS)
	pos = pygame.mouse.get_pos()
	time = pygame.time.get_ticks()
	screen.fill(BLACK)
	grov_new_food(Food, time)
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
