import pygame
import sys

class Game:
    def __init__(self):
        

        pygame.init()

        pygame.display.set_caption('ты приёмный')

        #window resolution in pixels
        self.screen = pygame.display.set_mode((640, 480))

        #restricting framerate
        self.clock = pygame.time.Clock()

        self.img = pygame.image.load(r'game-attempt\data\img\large_decor\large_decor2.png')
        self.img_pos = [160, 260]
        self.movement = [False, False]

    def run(self):

        #gameloop
        while True:

            self.img_pos[1] += self.movement[1] - self.movement[0] * 5
            self.screen.fill((0, 0, 0))
            #where we place the image
            self.screen.blit(self.img, self.img_pos)
            for event in pygame.event.get():   #event is any input and similar stuff
                #exiting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    #jey is pressed down
                if event.type == pygame.KEYDOWN:
                    #moving up
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                        #moving down
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
 
                   #key is released  
                    if event.key == pygame.KEYUP:
                    #stop moving up and down
                        if event.key == pygame.K_UP:
                            self.movement[0] = False
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = False
                    



            pygame.display.update()   #just a black screen wo it
            self.clock.tick(60)
#calling initialized object(here Game)
Game().run()

