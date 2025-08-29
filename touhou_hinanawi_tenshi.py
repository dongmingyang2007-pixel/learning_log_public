import sys
import pygame
from settings import Settings
from hinanawi_tenshi import HinanawiTenshi
image_1 = pygame.image.load("/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/g_1.jpg")
image_2 = pygame.image.load("/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/g_2.jpg")


class TouhouHinanawiTenshi:
    def __init__(x):
        pygame.init()
        x.clock = pygame.time.Clock()
        x.settings = Settings()
        x.screen = pygame.display.set_mode((x.settings.screen_width,x.settings.screen_height))
        pygame.display.set_caption("Touhou Hinanawi Tenshi")
        x.hinanawi_tenshi = HinanawiTenshi(x)
        x.screen.fill((255, 255, 255))
        x.last_key = None
        x.left_down = False
        x.right_down = False
        x.flag = None

    def _check_events(x):
        for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                x.hinanawi_tenshi.moving_right = True
                                x.last_key = pygame.K_RIGHT
                                x.right_down = True
                            if event.key == pygame.K_LEFT:
                                x.hinanawi_tenshi.moving_left = True
                                x.last_key = pygame.K_LEFT
                                x.left_down = True
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.moving_down = True
                            if event.key == pygame.K_UP:
                                x.hinanawi_tenshi.moving_up = True
                            if event.key == pygame.K_LSHIFT:
                                x.hinanawi_tenshi.moving_fast = True
                            if event.key == pygame.K_z:
                                x.hinanawi_tenshi.dash_forward_air_A = True
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.sit_down = True
                                x.hinanawi_tenshi.stand_up = False
                                x.hinanawi_tenshi.frame_hinanawi_tenshi_sit_index = 0
                                x.hinanawi_tenshi.frame_hinanawi_tenshi_stand_index = 0
                                try:
                                    x.hinanawi_tenshi.sit_phase = "sit_down"
                                except Exception:
                                    pass
                            

                        elif event.type == pygame.KEYUP:
                            if event.key == pygame.K_RIGHT:
                                x.hinanawi_tenshi.moving_right = False  
                                x.right_down = False   
                            if event.key == pygame.K_LEFT:
                                x.hinanawi_tenshi.moving_left = False
                                x.left_down = False
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.moving_down = False
                            if event.key == pygame.K_UP:
                                x.hinanawi_tenshi.moving_up = False   
                            if event.key == pygame.K_LSHIFT:
                                x.hinanawi_tenshi.moving_fast = False 
                            if event.key == pygame.K_z:
                                x.hinanawi_tenshi.dash_forward_air_A = False
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.sit_down = False
                                x.hinanawi_tenshi.stand_up = True


        if x.left_down and x.right_down:
            if x.last_key == pygame.K_RIGHT:
                  x.hinanawi_tenshi.moving_left = False
            if x.last_key == pygame.K_LEFT:
                  x.hinanawi_tenshi.moving_right = False

    def _check_screen(x):
            if x.last_key == None:
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_right()
                x.flag = "right"
            elif x.last_key == pygame.K_LEFT:
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_left()
                x.flag = "left"
            elif x.last_key == pygame.K_RIGHT:
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_right()
                x.flag = "right"
            elif x.flag == "right":
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_right()
                x.flag = "right"
            elif x.flag == "left":
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_left()
                x.flag = "left"

                 

    def run_game(x):
        while True:
            x._check_events()
            image_2_1 = pygame.transform.scale(image_2.convert(), (x.settings.screen_width, x.settings.screen_height))
            x.screen.blit(image_2_1,(0,0))
            if x.hinanawi_tenshi.dash_forward_air_A and x.hinanawi_tenshi.moving_right:
                x.hinanawi_tenshi.function_dash_forward_air_A_right()
                x.clock.tick(8)

            elif x.hinanawi_tenshi.dash_forward_air_A and x.hinanawi_tenshi.moving_left:
                x.hinanawi_tenshi.function_dash_forward_air_A_left()
                x.clock.tick(8)

            elif x.hinanawi_tenshi.sit_down:
                if x.flag == "right":
                    x.hinanawi_tenshi.function_sit_down_right()
                    x.clock.tick(8)
                elif x.flag == "left":
                    x.hinanawi_tenshi.function_sit_down_left()
                    x.clock.tick(8)

            elif x.hinanawi_tenshi.stand_up and x.flag == "right":
                x.hinanawi_tenshi.function_stand_up_right()
                x.clock.tick(8)
                
            elif x.hinanawi_tenshi.stand_up and x.flag == "left":
                x.hinanawi_tenshi.function_stand_up_left()
                x.clock.tick(8)
            
            elif x.hinanawi_tenshi.moving_right or x.hinanawi_tenshi.moving_left or x.hinanawi_tenshi.moving_up or x.hinanawi_tenshi.moving_down:
                x.hinanawi_tenshi.update()
                x.clock.tick(10)

            else:
                x._check_screen()
                x.clock.tick(8)
            pygame.display.flip()

if __name__ == '__main__':
    tht = TouhouHinanawiTenshi()
    tht.run_game()