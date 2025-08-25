############import packages############
import sys
import pygame
image_1 = pygame.image.load("/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/g_1.jpg")




############set the classes############
class TouhouHinanawiTenshi:
    """"The class which manages the resources and the behaviour"""
    def __init__(x):
        pygame.init()
        x.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Touhou Hinanawi Invasion")

    def run_game(x):
        """Beginning the main circulation of the game"""
        while True:
            """Suspect the action of mouse and keyboard"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            """Making the screen can be seen"""
            pygame.display.flip()

###########Producing the game and lunch it###########
if __name__ == '__main__':
    ai = TouhouHinanawiTenshi()
    ai.run_game()
