import random
import os
import pygame 
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from pygame import mixer

#K_DOWN is an int that stands for down-button index in array of indexes of all buttons on the keyboard

pygame.init()

def start_game():

    FPS = pygame.time.Clock()

    HEIGHT = 700
    WIDTH = 1200

    COLOUR_WHITE = (255,255,255)
    COLOUR_BLACK = (0,0,0)
    CLOUR_BLUE = (0, 0, 255)
    COLOUR_1 = (255,253,155)
    COLOUR_2 = (255, 79, 108)
    COLOUR_3 = (158,255, 166)


    # Создание окна
    main_display = pygame.display.set_mode((WIDTH,HEIGHT))   #Surface object
    pygame.display.set_caption("Shooting Star")
    icon_image = pygame.image.load("icon.png")
    pygame.display.set_icon(icon_image)

    # Background sound
    mixer.music.load('Curious Critters (Extended Version) 1.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)

    # Создание фона

    bg_image1=pygame.transform.scale(pygame.image.load("pictures/background/parallax-1.png").convert_alpha(), (WIDTH,HEIGHT))
    bg_image2=pygame.transform.scale(pygame.image.load("pictures/background/parallax-2.png").convert_alpha(), (1500, 120))
    bg_image3=pygame.transform.scale(pygame.image.load("pictures/background/parallax-3.png").convert_alpha(), (1400, 170))

    bg1_move = 0.7
    bg2_move = 0.5
    bg3_move = 0.3
    bg1_X1, bg2_X1, bg3_X1  = 0, 0, 0
    bg1_X2 = bg_image1.get_width()
    bg2_X2 = bg_image2.get_width()
    bg3_X2 = bg_image3.get_width()  - 0

    Images = [bg_image1, bg_image2, bg_image3]
    Moves = [bg1_move,bg2_move, bg3_move]
    Xes = [[bg1_X1, bg1_X2], [bg2_X1, bg2_X2], [bg3_X1, bg3_X2]]

    def draw_bg():

        main_display.blit(bg_image1, (Xes[0][0], 0))
        main_display.blit(bg_image1, (Xes[0][1], 0))

        main_display.blit(bg_image2, (Xes[1][0],HEIGHT-bg_image2.get_height()))
        main_display.blit(bg_image2, (Xes[1][1],HEIGHT-bg_image2.get_height()))

        main_display.blit(bg_image3, (Xes[2][0],HEIGHT-bg_image3.get_height()))
        main_display.blit(bg_image3, (Xes[2][1],HEIGHT-bg_image3.get_height()))


    # Создание player score
    score_count = 0 
    score_font = pygame.font.Font("Eirian.ttf", 25)


    # Создание player 
    IMAGE_PATH = "pictures/ufo"
    PLAYER_IMAGES = os.listdir(IMAGE_PATH)
    image_index = 0

    player = pygame.image.load('player.png').convert_alpha()
    player_rect = player.get_rect()   #Rect object,  player position, is the bounding rectangle of the image(player)
    player_size = (player.get_width(), player.get_height())
    player_move_down = [0, 2]
    player_move_up = [0, -2]
    player_move_right = [2, 0]
    player_move_left = [-2, 0]

    player_rect.y = HEIGHT/2 - player_size[1]  # Чтобы игрок появлялся в левом центре экрана 

    CHANGE_IMAGE = pygame.USEREVENT + 2
    pygame.time.set_timer(CHANGE_IMAGE, 100)


    # Создание enemy 
    def create_enemy():
        enemy = pygame.transform.scale(pygame.image.load("arrow.png").convert_alpha(), (180, 30))
        enemy_size = (enemy.get_width(), enemy.get_height())
        enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT- enemy_size[1]), *enemy_size)
        enemy_move = [random.randint(-6, -2), 0]                           # [-1, 0]
        
        return [enemy, enemy_rect, enemy_move]   #повертає list, елементи потім можна змінити
    # return enemy, enemy_rect, enemy_move    #повертає tuple, елементи потім не можна змінити

    CREATE_ENEMY = pygame.USEREVENT + 0           # ID of this event. Event ID's from 24 to 32 are available. Other are pre-defined. The pygame.USEREVENT has a value of 24
    pygame.time.set_timer(CREATE_ENEMY, 1500)     #1000 миллисек = 1 сек

    enemies = []


    # Создание bonus
    def create_bonus():
        bonus =pygame.transform.scale(pygame.image.load("shooting_star.png").convert_alpha(), (100,100))
        bonus = pygame.transform.rotate(bonus, 3)
        bonus_size = (bonus.get_width(), bonus.get_height())
        bonus_rect = pygame.Rect(random.randint(100,WIDTH-bonus_size[0]-200), 0, *bonus_size) # где появляется
        bonus_move = [2, random.uniform(2, 4)]                           
        #bonus_move = [0, random.randint(1,2)] 

        return [bonus, bonus_rect, bonus_move]   

    CREATE_BONUS = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_BONUS, 1500) 

    bonuses = []


    # Создание healthbar
    BAR_IMAGE_PATH = "pictures/health_bars"
    BAR_IMAGES = os.listdir(BAR_IMAGE_PATH)
    bar_image_index = 0
    CHANGE_BAR_IMAGE = pygame.USEREVENT + 3
    CHANGE_BAR_IMAGE_EVENT = pygame.event.Event(CHANGE_BAR_IMAGE)

    health_bar = pygame.image.load("bar-1.png")
    health_bar_size = (health_bar.get_width(), health_bar.get_height())
    health_bar_rect = pygame.Rect(WIDTH -350,20, *health_bar_size)

    health = 6

    #pygame.time.set_timer(CHANGE_BAR_IMAGE, 1000) 

    # Основной цикл программы --------------------------------------------------------------------------------------------------

    playing=True
    while playing:
        FPS.tick(240)                     # Щоб не так швидко оновлювалося 
        # Обработка событий
        for event in pygame.event.get():  #"event" is pygame.event.Event object. These objects are in the event queue
            if event.type == QUIT:
                playing = False
                mixer.music.load('WereWasI.ogg')
                mixer.music.play(-1)
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])), (200, 115))
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0
            if event.type == CHANGE_BAR_IMAGE:
                health_bar = pygame.transform.scale(pygame.image.load(os.path.join(BAR_IMAGE_PATH, BAR_IMAGES[bar_image_index])),(150,35))
                bar_image_index +=1
                if bar_image_index >=len(BAR_IMAGES):
                    bar_image_index = 4

        #main_display.fill(COLOUR_BLACK) 
        #main_display.blit(bg, (0,0)) 
        # bg отрисовывается первым, чтобы не закрывать след. объекты

        for i in range(3):
            Xes[i][0] -= Moves[i]
            Xes[i][1] -= Moves[i]
            if Xes[i][0] < -Images[i].get_width():
                Xes[i][0] = Images[i].get_width()
            if Xes[i][1] < -Images[i].get_width():
                Xes[i][1] = Images[i].get_width()

        draw_bg()


        keys = pygame.key.get_pressed()
        # Rect.move() меняет координаты 'x' 'y' у объекта Rect ('x' 'y' - атрибуты класса)
        # Поэтому мы пишем Rect = Rect.move()
        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)
        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        # enemy_rect = enemy_rect.move(enemy_move)
        # main_display.blit(enemy, enemy_rect)
        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                health  -= 1
                enemies.pop(enemies.index(enemy))
                pygame.event.post(CHANGE_BAR_IMAGE_EVENT)

                hit_sound = mixer.Sound('impactMetal_medium_003.ogg')
                hit_sound.set_volume(0.7)
                hit_sound.play()
                if health == 0:
                    playing = False
                    mixer.music.load('WereWasI.ogg')
                    mixer.music.play(-1)

        
        for bonus in bonuses:
            bonus[1] =bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score_count += 1
                bonuses.pop(bonuses.index(bonus))

                star_sound = mixer.Sound('sd_0.wav')
                star_sound.set_volume(0.9)
                star_sound.play()


        score = score_font.render("Score:"+" "+str(score_count) , True , COLOUR_WHITE)  #Surface obj. Должен быть в цикле, так как count обновляется и нкжнл переписать текст, что передается

        main_display.blit(health_bar, health_bar_rect)
        main_display.blit(score,(WIDTH-150, 20))
        main_display.blit(player, player_rect)          #put Surface obj in the coorditanes
        # player_rect = player_rect.move(player_speed)

        pygame.display.flip()              #Update the full display Surface to the screen

        #Delete enemies afterwards
        for enemy in enemies:
            if enemy[1].right < 0:
                enemies.pop(enemies.index(enemy))
        
        #Delete bonuses afterwards
        for bonus in bonuses:
            if bonus[1].top > HEIGHT:
                bonuses.pop(bonuses.index(bonus))


# Quit Pygame
pygame.quit()

