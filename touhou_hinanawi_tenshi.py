############import packages############
import sys
import pygame
from settings import Settings
from hinanawi_tenshi import HinanawiTenshi
image_1 = pygame.image.load("/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/g_1.jpg")
image_2 = pygame.image.load("/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/g_2.jpg")

############set the classes############
class TouhouHinanawiTenshi:
    def __init__(x):
        pygame.init()
        x.clock = pygame.time.Clock()
        x.settings = Settings()
        x.screen = pygame.display.set_mode((x.settings.screen_width,x.settings.screen_height))
        pygame.display.set_caption("Touhou Hinanawi Invasion")
        x.hinanawi_tenshi = HinanawiTenshi(x)
        x.screen.fill((255, 255, 255))
        
    def run_game(x):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            image_2_1 = pygame.transform.scale(image_2.convert(), (x.settings.screen_width, x.settings.screen_height))
            x.screen.blit(image_2_1,(0,0))
            x.hinanawi_tenshi.blitme()

            pygame.display.flip()
            x.clock.tick(60)

###########Producing the game and lunch it###########
if __name__ == '__main__':
    tht = TouhouHinanawiTenshi()
    tht.run_game()