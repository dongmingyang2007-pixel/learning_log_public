############import packages############
import pygame

##########The class of Hinanawi Tenshi##########
class HinanawiTenshi:
    def __init__(x,tht_game):
        x.screen = tht_game.screen
        x.screen_rect = tht_game.screen.get_rect()
        x.frames = [pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/hinanawi_tenshi/frame_{i}.png").convert_alpha() for i in range(0,30)]
        x.frame_index = 0


    def blitme(x):
        x.screen.blit((pygame.transform.scale(x.frames[x.frame_index].convert_alpha(), (200, 160))), (500, 640))
        x.frame_index = (x.frame_index + 1) % len(x.frames)