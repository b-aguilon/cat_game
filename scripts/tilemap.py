import json
from scripts.asset import assets

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid = {}
    
    def draw(self, surf, scroll=(0, 0)):
        dim = self.game.DIMENSIONS

        for tile in self.offgrid:
            img = assets[tile['type']][tile['variant']]
            surf.blit(img, (tile['pos'][0], tile['pos'][1]))

        for x in range(scroll[0] // self.tile_size, (dim[0] + scroll[0]) // self.tile_size + 1):
            for y in range(scroll[1] // self.tile_size, (dim[1] + scroll[1]) // self.tile_size + 1):
                pos = str(x) + ';' + str(y)
                if not pos in self.tilemap: 
                    continue
                tile = self.tilemap[pos]
                img = assets[tile['type']][tile['variant']]
                surf.blit(img, (tile['pos'][0] * self.tile_size - scroll[0], tile['pos'][1] * self.tile_size - scroll[1]))