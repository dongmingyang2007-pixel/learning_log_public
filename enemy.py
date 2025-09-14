import pygame
from random import randint
from pygame.sprite import Sprite
from settings import Settings
from time import sleep

class Dog_1(Sprite):
    def __init__(x, tht_game):
        super().__init__()
        x.screen = tht_game.screen
        x.world  = tht_game.world         

        x.settings = tht_game.settings 
        x.frames_dog_1_idle_right = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/dog_1_idle/frame_{i}.png"),(300, 150)),True,False) for i in range(0,3)]      
        x.frames_dog_1_idle_left = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/dog_1_idle/frame_{i}.png"),(300, 150)) for i in range(0,3)]      
        x.rects_dog_1_idle_left = [frame.get_rect(x = 0 ,y = 500) for frame in x.frames_dog_1_idle_left]
        x.rects_dog_1_idle_right = [frame.get_rect(x = 0 ,y = 500) for frame in x.frames_dog_1_idle_right]
        x.frames_dog_1_walk_left = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/dog_1_walk/frame_{i}.png"),(300, 150)) for i in range(0,3)]  
        x.frames_dog_1_walk_right = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/dog_1_walk/frame_{i}.png"),(300, 150)),True,False) for i in range(0,3)]  
        x.rects_dog_1_walk_left = [frame.get_rect(x = 0 ,y = 500) for frame in x.frames_dog_1_walk_left]
        x.rects_dog_1_walk_right = [frame.get_rect(x = 0 ,y = 500) for frame in x.frames_dog_1_walk_right]
        x.frames_dog_1_die = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/dog_1_die/frame_{i}.png"),(300, 150)) for i in range(0,13)] 
        x.frames_dog_1_attack = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/dog_1_attack/frame_{i}.png"),(300, 150)) for i in range(0,2)] 
        x.sx, x.sy = 0, 0
        x.rect = x.frames_dog_1_idle_left[0].get_rect()
        x.mask = pygame.mask.from_surface(x.frames_dog_1_idle_left[0].convert_alpha())
        x.state = "alive"
        x.flag = None
        x.rect.topleft = (x.sx, x.sy)
        x.damage = None

        x.wx = randint(0,1000)
        x.wy = randint(150,200)
        x.sx = 0
        x.sy = 0

        x.frame_dog_1_idle_index = 0
        x.frame_dog_1_walk_index = 0
        x.frame_dog_1_die_index = 0
        x.frame_dog_1_attack_index = 0
    
        x.dog_1_hp = 5
        x.hurt = None
    
    def update_dog_1_die_right(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        idx = min(x.frame_dog_1_die_index, len(x.frames_dog_1_die) - 1)
        frame = pygame.transform.flip(x.frames_dog_1_die[idx], True, False).convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        if x.frame_dog_1_die_index < len(x.frames_dog_1_die) - 1:
            x.frame_dog_1_die_index += 1

    def update_dog_1_die_left(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        idx = min(x.frame_dog_1_die_index, len(x.frames_dog_1_die) - 1)
        frame = x.frames_dog_1_die[idx].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        if x.frame_dog_1_die_index < len(x.frames_dog_1_die) - 1:
            x.frame_dog_1_die_index += 1

    def _to_screen(x, wx, wy, parallax=1.0):
        sw, sh = x.screen.get_size()
        cam_lx = (x.world.cam_x - sw * 0.5) * parallax
        cam_ly = (x.world.cam_y - sh * 0.5) * parallax
        return int(wx - cam_lx), int(wy - cam_ly)

    def update_dog_1_idle_left(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        frame = x.frames_dog_1_idle_left[x.frame_dog_1_idle_index].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.frame_dog_1_idle_index = (x.frame_dog_1_idle_index + 1) % len(x.frames_dog_1_idle_left)
        x.sx, x.sy = sx, sy

    def update_dog_1_idle_right(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        frame = x.frames_dog_1_idle_right[x.frame_dog_1_idle_index].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.frame_dog_1_idle_index = (x.frame_dog_1_idle_index + 1) % len(x.frames_dog_1_idle_right)
        x.sx, x.sy = sx, sy
    
    def update_dog_1_walk_left(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        frame = x.frames_dog_1_walk_left[x.frame_dog_1_walk_index].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.frame_dog_1_walk_index = (x.frame_dog_1_walk_index + 1) % len(x.frames_dog_1_walk_left)
        x.wx = x.wx - x.settings.dog_1_walk_speed
        x.sx, x.sy = sx, sy


    def update_dog_1_walk_right(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        frame = x.frames_dog_1_walk_right[x.frame_dog_1_walk_index].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.frame_dog_1_walk_index = (x.frame_dog_1_walk_index + 1) % len(x.frames_dog_1_walk_right)
        x.wx = x.wx + x.settings.dog_1_walk_speed
        x.sx, x.sy = sx, sy
    
    def update_dog_1_hurt_right(x):
        x.wx = x.wx - 150
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        idx = min(x.frame_dog_1_die_index, 11)
        frame = pygame.transform.flip(x.frames_dog_1_die[idx], True, False).convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.sx, x.sy = sx, sy
        if x.frame_dog_1_die_index < 11:
            x.frame_dog_1_die_index += 1

    def update_dog_1_hurt_left(x):
        x.wx = x.wx + 150
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        idx = min(x.frame_dog_1_die_index, 11)
        frame = x.frames_dog_1_die[idx].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.sx, x.sy = sx, sy
        if x.frame_dog_1_die_index < 11:
            x.frame_dog_1_die_index += 1

    def update_dog_1_threaten_right(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        idx = 0
        frame = pygame.transform.flip(x.frames_dog_1_attack[1], True, False).convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.sx, x.sy = sx, sy

    def update_dog_1_threaten_left(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        idx = 0
        frame = x.frames_dog_1_attack[1].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.sx, x.sy = sx, sy

    def update_dog_1_attack_left(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        frame = x.frames_dog_1_attack[0].convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.frame_dog_1_attack_index = (x.frame_dog_1_attack_index + 1) % len(x.frames_dog_1_attack)
        x.wx = x.wx - 50
        x.sx, x.sy = sx, sy
    
    def update_dog_1_attack_right(x):
        sx, sy = x._to_screen(x.wx, x.wy, 1.0)
        frame = pygame.transform.flip(x.frames_dog_1_attack[0],True,False).convert_alpha()
        x.image = frame
        x.rect  = x.image.get_rect(topleft=(sx, sy))
        x.mask  = pygame.mask.from_surface(x.image)
        x.screen.blit(x.image, x.rect)
        x.frame_dog_1_attack_index = (x.frame_dog_1_attack_index + 1) % len(x.frames_dog_1_attack)
        x.wx = x.wx + 50
        x.sx, x.sy = sx, sy
