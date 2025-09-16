import pygame
##########The class of all settings in the game##########
class Settings:
    def __init__(x):
        x.screen_width = 1730
        x.screen_height = 980
        x.hinanawi_tenshi_walk_speed = 20
        x.life_limit = 100


        x.tenshi_size_x = 260
        x.tenshi_size_y = 440
        x.attack_B_1_damage = 1
        x.attack_bullet_ga_damage = 5


        x.bullet_ga_speed = 100
        x.bullet_ga_size_x = 488
        x.bullet_ga_size_y = 120
        x.frames_bullet_ga_right = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/bullet_ga/frame_{i}.png"),(x.bullet_ga_size_x, x.bullet_ga_size_y)) for i in range(0,4)]        
        x.frames_bullet_ga_left = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/bullet_ga/frame_{i}.png"),(x.bullet_ga_size_x, x.bullet_ga_size_y)),True,False) for i in range(0,4)]      


        x.dog_1_walk_speed = 50