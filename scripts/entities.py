import pygame

class PhysicsEntity:
                      #the entity itself, referencing the game, position, size of the entity
    def __init__(self, game, e_type,pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

   
    def update(self, tilemap, movement=(0, 0)):
        # Calculate the movement for this frame based on velocity and input
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # X-axis position update
        self.pos[0] += frame_movement[0]

        #  collision detection
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): 
                if frame_movement[0] > 0:  # Moving right
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:  # Moving left
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x

        # Y-axis position update
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        on_ground = False

        
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # Moving downward
                    entity_rect.bottom = rect.top
                    on_ground = True
                if frame_movement[1] < 0:  # Moving upward
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y

        # adjust velocity based on whether on ground
        if not on_ground:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)
        else:
            self.velocity[1] = 0


    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)