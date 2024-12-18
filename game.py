import pygame
import sys
import os
import math

import random

from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utils import load_image, Animation
from scripts.utils import load_images
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.spark import Spark

class Game:
    def __init__(self):
        

        pygame.init()

        pygame.display.set_caption('Forest Chasm')

        #ekraan pikslites
        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)

        self.display_2 = pygame.Surface((320, 240))

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
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=3),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=6),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur = 5),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur = 5),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur = 5),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'spawners': load_images('tiles/spawners'),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('sfx/jump.wav'),
            'dash': pygame.mixer.Sound('sfx/dash.wav'),
            'hit': pygame.mixer.Sound('sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('sfx/ambience.wav'),
        }
        #фиксит громкость звука
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)



        self.player = Player(self, (50, 50), (8, 15))


        
        self.tilemap = Tilemap(self, tile_size=16)

        self.level = 0
        self.load_level(self.level)
        #self.tilemap.load('map.json')

        self.screenshake = 0
        

    def load_level(self, map_id):
        self.tilemap.load('andmed/maps/' + str(map_id) + '.json') #load everything from map 'maps'

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        print(self.leaf_spawners)

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.player.pos = [50, 50] #спамниться на спавне а не бегает как сумашедшая при смерти внизу

        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

   

    def run(self):

        pygame.mixer.music.load('andmed/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sfx['ambience'].play(-1)

        #mängutsükkel
        while True:
            self.display.fill((0, 0, 0, 0))

            self.display_2.blit(self.assets['background'], (0, 0))
            self.screenshake = max(0, self.screenshake - 1)

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('andmed/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1


            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))


            
            self.tilemap.render(self.display, offset = render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                #pole muutusi y teljel
            #horisontaal = (self.movement[1] - self.movement[0]) * 2

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset = render_scroll)

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random()- 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))


            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)            


            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # smoother pattern for falling leafs
                if kill:
                    self.particles.remove(particle)

            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset) # тут короче можно менять колическо теней


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
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
 
                   #klahv pole vajutatud  
                if event.type == pygame.KEYUP:
                    #stop up and down
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                #рисует черный круг с центра
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
                    
            self.display_2.blit(self.display, (0, 0))
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0, 0))
            pygame.display.update()   #lihtsalt must ekraan ilma selleta
            self.clock.tick(60)
#kutsun initsializeeritud objecti(siin Game)
Game().run()