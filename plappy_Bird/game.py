from turtle import Tbuffer

import pygame, sys, random
from pygame import MOUSEBUTTONDOWN


#tạo hàm cho trò chơi
def draw_flow():#tạo cho sàn lặp lại
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))
def create_pipe(): # tạo ống lặp lại
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = ong.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = ong.get_rect(midtop=(500, random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):#ống lặp lại
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes
#vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(ong, pipe)
        else:
            flip_pipe = pygame.transform.flip(ong,False,True)
            screen.blit(flip_pipe, pipe)
#xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <=75 or bird_rect.bottom > 750:
        hit_sound.play()
        return False
    return True
#xoay chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird
#hiển thị điểm
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True,(0,0,0))
        score_rect = score_surface.get_rect(center = (216,100))
        screen .blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)
#cập nhật điểm
def update_score(score , high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((432,768))#tạo ra của số file game màu đen
clock = pygame.time.Clock() # Tốc độ game mong muốn
game_font = pygame.font.Font('04B_19.TTF',40)
#tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
passed_pipes = [] #danh sách luu ống đã đi qu a
#chèn background
bg = pygame.image.load('Hinh/background-night.png').convert()#làm nhanh hơn
bg = pygame.transform.scale2x(bg)# tăng khung hình
#chèn sàn
floor = pygame.image.load('Hinh/floor.png').convert()#chèn hình ảnh
floor = pygame.transform.scale2x(floor)# tăng khung hình
floor_x_pos = 0 #di chuyển sàn
#chèn chim
bird = pygame.image.load('Hinh/yellowbird-upflap.png').convert_alpha()#chèn hình ảnh
bird = pygame.transform.scale2x(bird)# tăng khung hình
bird_rect = bird.get_rect(center =(100,384))
#tạo ống
ong = pygame.image.load('Hinh/pipe-green.png').convert()
ong = pygame.transform.scale2x(ong)
pipe_list = []
#tạo timer
spawntipe = pygame.USEREVENT
pygame.time.set_timer(spawntipe, 1800)
pipe_height = [400,250,350,300]
#tạo màn hình kết thích cho trò chơi
game_over_surface = pygame.image.load('Hinh/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (216,384))
#chèm âm thanh
flap_sound = pygame.mixer.Sound('nhac/5_Flappy_Bird_sound_sfx_wing.wav')
hit_sound = pygame.mixer.Sound('nhac/5_Flappy_Bird_sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('nhac/5_Flappy_Bird_sound_sfx_point.wav')
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Nhấn Space để chim bay lên
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -8
                flap_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_active == False:
            game_active = True
            pipe_list.clear()
            bird_rect.center = (100,384)
            bird_movement = 0
            score = 0
        if event.type == spawntipe:
            pipe_list.extend(create_pipe())

    screen.blit(bg,(0,0))
    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        if game_active:
            # Kiểm tra khi chim qua ống
            last_score = 0
            for pipe in pipe_list:
                if pipe.centerx < bird_rect.centerx and pipe not in passed_pipes:
                    score += 0.5
                    passed_pipes.append(pipe)
            if score > last_score:
                score_sound.play()
                last_score = score

            pass_pipes = [pipe for pipe in passed_pipes if pipe.centerx > -50]
        score_display('main_game')
        score_sound_countdown -= 1
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score , high_score)
        score_display('game_over')


    #sàn
    floor_x_pos -=1
    draw_flow()
    if floor_x_pos <= -432: # tạo cho sàn lặp lại
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(100)

