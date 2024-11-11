import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image
from scripts.utils import load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        

        pygame.init()

        pygame.display.set_caption('ты приёмный')

        #window resolution in pixels
        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))

        #restricting framerate
        self.clock = pygame.time.Clock()

        '''self.img = pygame.image.load(r'data\img\large_decor\large_decor2.png')
        self.img.set_colorkey((0, 0, 0))  #color black is transparent
        self.img_pos = [160, 260]'''
        
        self.movement = [False, False]



        self.assets = {
            'player': load_image('large_decor/large_decor2.png'), #for now!!!!!!!
            'decor': load_images('decor'),
            'grass': load_images('grass'),
            'large_decor': load_images('large_decor')
        }
        
        self.player = PhysicsEntity(self, 'player', (50, 160 - 15), (8, 15))


        
        self.tilemap = Tilemap(self, tile_size=16)

   

    def run(self):

        #gameloop
        while True:

            self.display.fill((50, 100, 90))

            self.tilemap.render(self.display)

                #no change on y axis
            horisontaal = (self.movement[1] - self.movement[0]) * 5
            self.player.update(self.tilemap, (horisontaal, 0))

            self.player.render(self.display)




            for event in pygame.event.get():   #event is any input and similar stuff
                #exiting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    #jey is pressed down
                if event.type == pygame.KEYDOWN:
                    #moving up
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        #moving down
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
 
                   #key is released  
                if event.type == pygame.KEYUP:
                    #stop moving up and down
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()   #just a black screen wo it
            self.clock.tick(60)
#calling initialized object(here Game)
Game().run()

