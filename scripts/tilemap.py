import pygame

NAABER_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (1, 0), (1, 1)]
PHYSICS_TILES = {'grass'}


class Tilemap():
        def __init__(self, game, tile_size = 16):
                self.game = game
                self.tile_size = tile_size
                self.tilemap = {}
                self.offgrid_tiles = []

                #filling tilemap
                for i in range(10):
                        self.tilemap[str(3 + i) + ';10'] = {'type' : 'grass', 'variant' : '1', 'pos': (3 + i, 10)}
                        #self.tilemap[';10' + str(5 + i)] = {'type' : 'grass', 'variant' : '1', 'pos': (1, 5 + i)}
                        self.tilemap[str(1) + ';' + str(5 + i)] = {'type': 'grass', 'variant': '1', 'pos': (1, 5 + i)}


        def tiles_around(self, pos):
                tiles = []
                tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
                for offset in NAABER_OFFSET:
                                check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
                                if check_loc in self.tilemap:
                                        tiles.append(self.tilemap[check_loc])
                return tiles
        
        def physics_rects_around(self, pos, offset = (0, 0)):
                rects = []
                for tile in self.tiles_around(pos):
                        if tile['type'] in PHYSICS_TILES:
                                tile_x = tile['pos'][0] * self.tile_size - offset[0]
                                tile_y = tile['pos'][1] * self.tile_size - offset[1]
                                rects.append(pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size))
                return rects                      
        
        def render(self, surf, offset = (0, 0)):
                
                for tile in self.offgrid_tiles:
                        surf.blit(self.game.assets[tile['type']][int(tile['variant'])], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))


                for loc in self.tilemap:
                        tile = self.tilemap[loc]
                                        
                        
                        surf.blit(
                            self.game.assets[tile['type']][int(tile['variant'])],
                            (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1])
                            )