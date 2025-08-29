############import packages############
import pygame

##########The class of Hinanawi Tenshi##########
class HinanawiTenshi:
    def __init__(x,tht_game):
        x.screen = tht_game.screen
        x.screen_rect = tht_game.screen.get_rect()
        x.settings = tht_game.settings
        x.frames_idle = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/hinanawi_tenshi_idle/frame_{i}.png"),(x.settings.tenshi_size_x, x.settings.tenshi_size_y)) for i in range(0,5)]
        x.frames_walk = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/hinanawi_tenshi_walk/frame_{i}.png"),(x.settings.tenshi_size_x, x.settings.tenshi_size_y)) for i in range(0,8)]
        x.frames_hinanawi_tenshi_dash_forward_air_A = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/hinanawi_tenshi_dash_forward_air_A/frame_{i}.png"),(x.settings.tenshi_size_x, x.settings.tenshi_size_y)) for i in range(0,8)]
        x.frames_hinanawi_tenshi_dash_forward_air_B = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/hinanawi_tenshi_dash_forward_air_B/frame_{i}.png"),(400, x.settings.tenshi_size_y)) for i in range(0,13)]
        x.frames_hinanawi_tenshi_sit = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/hinanawi_tenshi_sit/frame_{i}.png"),(x.settings.tenshi_size_x, x.settings.tenshi_size_y)) for i in range(0,12)]
        x.frames_hinanawi_tenshi_sit_down = x.frames_hinanawi_tenshi_sit[0:6]
        x.frame_hinanawi_tenshi_sitting = x.frames_hinanawi_tenshi_sit[6]
        x.frames_hinanawi_tenshi_stand_up = x.frames_hinanawi_tenshi_sit[7:12]
        x.frame_idle_index = 0
        x.frame_walk_index = 0
        x.frame_hinanawi_tenshi_dash_forward_air_A_index = 0
        x.frame_hinanawi_tenshi_dash_forward_air_B_index = 0
        x.frame_hinanawi_tenshi_sit_index = 0
        x.frame_hinanawi_tenshi_stand_index = 0
        x.rects_idle = [frame.get_rect(x = 865, y = 540) for frame in x.frames_idle]
        x.rects_walk = [frame.get_rect(x = 865, y = 540) for frame in x.frames_walk]
        x.rects_hinanawi_tenshi_dash_forward_air_A = [frame.get_rect(x = 865, y = 540) for frame in x.frames_hinanawi_tenshi_dash_forward_air_A]
        x.rects_hinanawi_tenshi_dash_forward_air_B = [frame.get_rect(x = 865, y = 540) for frame in x.frames_hinanawi_tenshi_dash_forward_air_B]        
        x.rects_hinanawi_tenshi_sit = [frame.get_rect(x = 865, y = 540) for frame in x.frames_hinanawi_tenshi_sit]
        x.rects_hinanawi_tenshi_sit_down = x.rects_hinanawi_tenshi_sit[0:6]
        x.rect_hinanawi_tenshi_sitting = x.rects_hinanawi_tenshi_sit[6]
        x.rects_hinanawi_tenshi_sit_up = x.rects_hinanawi_tenshi_sit[7:12]
        x.moving_right = False
        x.moving_left = False
        x.moving_up = False
        x.moving_down = False
        x.moving_fast = False
        x.dash_forward_air_A = False
        x.dash_forward_air_B = False
        x.sit_down = False
        x.stand_up = False
        x.sit_phase = "idle"

    def blitme_right(x):
        x.screen.blit(x.frames_idle[x.frame_idle_index].convert_alpha(), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        x.frame_idle_index = (x.frame_idle_index + 1) % len(x.frames_idle)

    def blitme_left(x):
        x.screen.blit(pygame.transform.flip(x.frames_idle[x.frame_idle_index].convert_alpha(), flip_x = True , flip_y = False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        x.frame_idle_index = (x.frame_idle_index + 1) % len(x.frames_idle)

    def update(x):
        if x.moving_right:
            if x.moving_fast:
                for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                    x.x = float(x.rect.x)
                    x.x += 2 * x.settings.hinanawi_tenshi_walk_speed
                    x.rect.x = x.x
                x.screen.blit(x.frames_walk[x.frame_walk_index].convert_alpha(), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
            if x.moving_fast == False:
                for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                    x.x = float(x.rect.x)
                    x.x += x.settings.hinanawi_tenshi_walk_speed
                    x.rect.x = x.x
                x.screen.blit(x.frames_walk[x.frame_walk_index].convert_alpha(), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        x.flag = "right"

        if x.moving_left:
            if x.moving_fast:
                for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                    x.x = float(x.rect.x)
                    x.x -= 2 * x.settings.hinanawi_tenshi_walk_speed
                    x.rect.x = x.x
                x.screen.blit(pygame.transform.flip(x.frames_walk[x.frame_walk_index].convert_alpha(), flip_x = True , flip_y = False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
            if x.moving_fast == False:
                for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                    x.x = float(x.rect.x)
                    x.x -= x.settings.hinanawi_tenshi_walk_speed
                    x.rect.x = x.x
                x.screen.blit(pygame.transform.flip(x.frames_walk[x.frame_walk_index].convert_alpha(), flip_x = True , flip_y = False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        x.frame_walk_index = (x.frame_walk_index + 1) % len(x.frames_walk)
        x.flag = "left"

    def function_dash_forward_air_A_right(x):
        if x.dash_forward_air_A and x.moving_right:
            for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                x.x = float(x.rect.x)
                x.x += 6 * x.settings.hinanawi_tenshi_walk_speed
                x.rect.x = x.x
            x.screen.blit(x.frames_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index], x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        if x.frame_hinanawi_tenshi_dash_forward_air_A_index == 7:
            x.dash_forward_air_A = False
        x.frame_hinanawi_tenshi_dash_forward_air_A_index = (x.frame_hinanawi_tenshi_dash_forward_air_A_index + 1) % len(x.frames_hinanawi_tenshi_dash_forward_air_A)

    def function_dash_forward_air_A_left(x):
        if x.dash_forward_air_A and x.moving_left:
            for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                x.x = float(x.rect.x)
                x.x -= 6 * x.settings.hinanawi_tenshi_walk_speed
                x.rect.x = x.x
            x.screen.blit(pygame.transform.flip(x.frames_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index].convert_alpha(), flip_x = True , flip_y = False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        if x.frame_hinanawi_tenshi_dash_forward_air_A_index == 7:
            x.dash_forward_air_A = False
        x.frame_hinanawi_tenshi_dash_forward_air_A_index = (x.frame_hinanawi_tenshi_dash_forward_air_A_index + 1) % len(x.frames_hinanawi_tenshi_dash_forward_air_A)

    def function_sit_down_left(x):
        if x.sit_down and x.sit_phase == "idle":
            x.sit_phase = "sit_down"
        if x.sit_down and x.sit_phase == "sit_down":
            if 0 <= x.frame_hinanawi_tenshi_sit_index < 6:
                x.screen.blit(pygame.transform.flip(x.frames_hinanawi_tenshi_sit_down[x.frame_hinanawi_tenshi_sit_index].convert_alpha(), True, False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
                if x.frame_hinanawi_tenshi_sit_index < 5:
                    x.frame_hinanawi_tenshi_sit_index += 1
                else:
                    x.sit_phase = "sitting"
            else:
                x.sit_phase = "sitting"
        elif x.sit_phase == "sitting":
            x.screen.blit(pygame.transform.flip(x.frame_hinanawi_tenshi_sitting.convert_alpha(), True, False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
            if (not x.sit_down) and (not x.stand_up):
                x.stand_up = True
                x.sit_phase = "stand_up"

    def function_sit_down_right(x):
        if x.sit_down and x.sit_phase == "idle":
            x.sit_phase = "sit_down"
        if x.sit_down and x.sit_phase == "sit_down":
            if 0 <= x.frame_hinanawi_tenshi_sit_index < 6:
                x.screen.blit(x.frames_hinanawi_tenshi_sit_down[x.frame_hinanawi_tenshi_sit_index].convert_alpha(), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
                if x.frame_hinanawi_tenshi_sit_index < 5:
                    x.frame_hinanawi_tenshi_sit_index += 1
                else:
                    x.sit_phase = "sitting"
            else:
                x.sit_phase = "sitting"
        elif x.sit_phase == "sitting":
            x.screen.blit(x.frame_hinanawi_tenshi_sitting.convert_alpha(), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
            if (not x.sit_down) and (not x.stand_up):
                x.stand_up = True
                x.sit_phase = "stand_up"

    def function_stand_up_left(x):
        if x.sit_phase == "stand_up" or x.stand_up == True:
            if x.stand_up and x.sit_phase != "stand_up":
                x.sit_phase = "stand_up"
            if 0 <= x.frame_hinanawi_tenshi_stand_index < 5:
                x.screen.blit(pygame.transform.flip(x.frames_hinanawi_tenshi_stand_up[x.frame_hinanawi_tenshi_stand_index].convert_alpha(), True, False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
                if 0 <= x.frame_hinanawi_tenshi_stand_index < 4:
                    x.frame_hinanawi_tenshi_stand_index += 1
                else:
                    x.sit_phase = "idle" 
                    x.stand_up = False
                    x.frame_hinanawi_tenshi_stand_index = 0

    def function_stand_up_right(x):
        if x.sit_phase == "stand_up" or x.stand_up == True:
            if x.stand_up and x.sit_phase != "stand_up":
                x.sit_phase = "stand_up"
            if 0 <= x.frame_hinanawi_tenshi_stand_index < 5:
                x.screen.blit(x.frames_hinanawi_tenshi_stand_up[x.frame_hinanawi_tenshi_stand_index].convert_alpha(), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
                if 0 <= x.frame_hinanawi_tenshi_stand_index < 4:
                    x.frame_hinanawi_tenshi_stand_index += 1
                else:
                    x.sit_phase = "idle" 
                    x.stand_up = False    
                    x.frame_hinanawi_tenshi_stand_index = 0

    def function_dash_forward_air_B_right(x):
        if x.dash_forward_air_B and x.moving_right:
            for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                x.x = float(x.rect.x)
                x.x += 6 * x.settings.hinanawi_tenshi_walk_speed
                x.rect.x = x.x
            x.screen.blit(x.frames_hinanawi_tenshi_dash_forward_air_B[x.frame_hinanawi_tenshi_dash_forward_air_B_index], x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        if x.frame_hinanawi_tenshi_dash_forward_air_B_index == 12:
            x.dash_forward_air_B = False
        x.frame_hinanawi_tenshi_dash_forward_air_B_index = (x.frame_hinanawi_tenshi_dash_forward_air_B_index + 1) % len(x.frames_hinanawi_tenshi_dash_forward_air_B)

    def function_dash_forward_air_B_left(x):
        if x.dash_forward_air_B and x.moving_left:
            for x.rect in x.rects_hinanawi_tenshi_dash_forward_air_A:
                x.x = float(x.rect.x)
                x.x -= 6 * x.settings.hinanawi_tenshi_walk_speed
                x.rect.x = x.x
            x.screen.blit(pygame.transform.flip(x.frames_hinanawi_tenshi_dash_forward_air_B[x.frame_hinanawi_tenshi_dash_forward_air_B_index].convert_alpha(), flip_x = True , flip_y = False), x.rects_hinanawi_tenshi_dash_forward_air_A[x.frame_hinanawi_tenshi_dash_forward_air_A_index])
        if x.frame_hinanawi_tenshi_dash_forward_air_B_index == 12:
            x.dash_forward_air_B = False
        x.frame_hinanawi_tenshi_dash_forward_air_B_index = (x.frame_hinanawi_tenshi_dash_forward_air_B_index + 1) % len(x.frames_hinanawi_tenshi_dash_forward_air_B)