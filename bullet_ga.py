import pygame
from pygame.sprite import Sprite

class BulletGa(Sprite):
    def __init__(x, tht_game):
        super().__init__()
        x.screen = tht_game.screen
        x.settings = tht_game.settings
        x.frames_bullet_ga_right = tht_game.settings.frames_bullet_ga_right
        x.frames_bullet_ga_left = tht_game.settings.frames_bullet_ga_left
        x.hinanawi_tenshi = tht_game.hinanawi_tenshi
        x.rects_bullet_ga_right = [frame.get_rect(x = x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x + 100, y = x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].y + 180) for frame in x.frames_bullet_ga_right]
        x.rects_bullet_ga_left = [frame.get_rect(x = x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - 200, y = x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].y + 150) for frame in x.frames_bullet_ga_left]
        x.frame_bullet_ga_index = 0
        x.shot = False
        x.rect = x.rects_bullet_ga_right[0].copy()
        x.mask = pygame.mask.from_surface(x.frames_bullet_ga_left[0])


    def update_right(x):
        for rect in x.rects_bullet_ga_right:
            x.x = float(rect.x)
            x.x += x.settings.bullet_ga_speed
            rect.x = x.x
            x.rect = rect
        for frame in x.frames_bullet_ga_right:
            frame = frame.convert_alpha()
            x.mask = pygame.mask.from_surface(frame)
    
    def draw_bullet_right(x):
        x.screen.blit(x.frames_bullet_ga_right[x.frame_bullet_ga_index], x.rect)
        x.frame_bullet_ga_index = (x.frame_bullet_ga_index + 1) % len(x.frames_bullet_ga_right)


    def update_left(x):
        for rect in x.rects_bullet_ga_left:
            x.x = float(rect.x)
            x.x -= x.settings.bullet_ga_speed
            rect.x = x.x
            x.rect =rect
        for frame in x.frames_bullet_ga_right:
            frame = frame.convert_alpha()
            x.mask = pygame.mask.from_surface(frame)


    def draw_bullet_left(x):
        x.screen.blit(x.frames_bullet_ga_left[x.frame_bullet_ga_index], x.rect)
        x.frame_bullet_ga_index = (x.frame_bullet_ga_index + 1) % len(x.frames_bullet_ga_left)





