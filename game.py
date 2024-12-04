import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image
from scripts.utils import load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        

        pygame.init()

        pygame.display.set_caption('Forest Chasm')

        #ekraan pikslites
        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))

        #ограниченное колво кадров
        self.clock = pygame.time.Clock()

        
        self.movement = [False, False]

            #всё норм
        self.assets = {
            'player': load_image('entities/player/idle/idle1.png'), #for now!!!!!!!
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'background': load_image('background.png')
        }


        
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))


        
        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

        

   

    def run(self):

        #mängutsükkel
        while True:

            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15

            



            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            

            self.display.blit(self.assets['background'], (0, 0))
         

            self.tilemap.render(self.display, offset = render_scroll)

                #pole muutusi y teljel
            horisontaal = (self.movement[1] - self.movement[0]) * 2
            self.player.update(self.tilemap, (horisontaal, 0))

            self.player.render(self.display, offset = render_scroll)




            for event in pygame.event.get():   #event on igasugune sisend vms
                #exiting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    #klahv on vajutatud
                if event.type == pygame.KEYDOWN:
                    #up
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        #down
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
 
                   #klahv pole vajutatud  
                if event.type == pygame.KEYUP:
                    #stop up and down
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()   #lihtsalt must ekraan ilma selleta
            self.clock.tick(60)
#kutsun initsializeeritud objecti(siin Game)
Game().run()



