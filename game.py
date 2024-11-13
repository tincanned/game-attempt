import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image
from scripts.utils import load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        

        pygame.init()

        pygame.display.set_caption('mänguprojekt')

        #aken pikslites
        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))

        #ограниченное колво кадров
        self.clock = pygame.time.Clock()

        
        self.movement = [False, False]

        self.assets = {
            'player': load_image('player/idle1.png'), 
            'decor': load_images('decor'),
            'grass': load_images('grass'),
            'large_decor': load_images('large_decor')
        }
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (16, 16))


        
        self.tilemap = Tilemap(self, tile_size=16)
        

   

    def run(self):

        #gametsükkel
        while True:

            self.display.fill((50, 100, 90))

            self.tilemap.render(self.display)

                
            horisontaal = (self.movement[1] - self.movement[0]) * 1
            self.player.update(self.tilemap, (horisontaal, 0))

            self.player.render(self.display)




            for event in pygame.event.get():   #event is any input and similar stuff
                #exiting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    #klahv on vajutatud
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
 
                   #klahv pole vajutatu d 
                if event.type == pygame.KEYUP:
                    #stop up, down
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()   #must ekraan ilma selleta
            self.clock.tick(60)
#kutsun initializeeritud objecti(siin Game)
Game().run()



