import pygame

class PhysicsEntity:
                      #the entity itself, referencing the game, position, size of the entity
    def __init__(self, game, e_type,pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, 'right': False, 'left' : False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

   
    def update(self, tilemap, movement=(0, 0), offset = (0, 0)):
        self.collisions = {'up' : False, 'down' : False, 'right': False, 'left' : False}

        # Calculate the movement for this frame based on velocity and input
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # X-axis position update
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.pos, offset = offset):
            if entity_rect.colliderect(rect): 
                if frame_movement[0] > 0:  # Moving right
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:  # Moving left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # Y-axis position update
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        on_ground = False

        
        for rect in tilemap.physics_rects_around(self.pos, offset = offset):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # Moving downward
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    on_ground = True
                if frame_movement[1] < 0:  # Moving upward
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

            # adjust velocity based on whether on ground
        if not on_ground:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)
        else:
            self.velocity[1] = 0
            #if self.collisions['down'] or self.collisions['up']:
            #   self.velocity[1] = 0 


    def render(self, surf, offset = (0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))