import pygame
import sys
import math
import random
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, Animation
from scripts.utils import load_images
from scripts.tilemap import Tilemap
from scripts.particle import Particle

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
            'background': load_image('background.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur = 5),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur = 5),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur = 5),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'spawners': load_images('tiles/spawners'),
        }


        
        self.player = Player(self, (50, 50), (10, 24))


        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('game-attempt/map.json')
        

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        print(self.leaf_spawners)

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners',1 )]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                print(spawner['pos'], 'enemy')


        self.particles = []
        self.scroll = [0, 0]

   

    def run(self):

        #mängutsükkel
        while True:

            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))


            
            self.tilemap.render(self.display, offset = render_scroll)

                #pole muutusi y teljel
            horisontaal = (self.movement[1] - self.movement[0]) * 2

            self.player.update(self.tilemap, (horisontaal, 0))
            self.player.render(self.display, offset = render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # smoother pattern for falling leafs
                if kill:
                    self.particles.remove(particle)



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
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
 
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