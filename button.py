import pygame.font

class Button:
    def __init__(x,tht_game,msg):
        x.screen = tht_game.screen
        x.screen_rect = x.screen.get_rect()
        x.w, x.h = 200,50
        x.button_color = (0, 135, 0)
        x.text_color = (255, 255, 255)
        x.font = pygame.font.SysFont(None, 48)

        x.rect = pygame.Rect(0, 0, x.w, x.h)

        x.rect.center = x.screen_rect.center

        x._prep_msg(msg)
    
    def _prep_msg(x, msg):
        x.msg_image = x.font.render(msg, True, x.text_color, x.button_color)
        x.msg_image_rect = x.msg_image.get_rect()
        x.msg_image_rect.center = x.rect.center
    
    def draw_button(x):
        x.screen.fill(x.button_color, x.rect)
        x.screen.blit(x.msg_image, x.msg_image_rect)