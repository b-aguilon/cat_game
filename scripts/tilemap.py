import json
import pygame
from scripts.asset import assets
from scripts.entities import Ramp

PHYS_TILE_RECTS = {'road', 'stone'}
NEAR_TILES = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1),
              (-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2), (0, 0)]

class Tilemap:
    def __init__(self, state, tile_size=16):
        self.state = state
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid = {}
    
    def draw(self, surf, scroll=(0, 0)):
        dim = self.state.dimensions

        for key in self.offgrid:
            tile = self.offgrid[key]
            draw_offset = 32
            outside_x = tile['pos'][0] > dim[0] + scroll[0] or tile['pos'][0] < scroll[0] - draw_offset
            outside_y = tile['pos'][1] > dim[1] + scroll[1] or tile['pos'][1] < scroll[1] - draw_offset
            if outside_x or outside_y:
                continue
            img = assets[tile['type']][tile['variant']]
            flip = True if tile['ramp'] == 'right' else False
            if not flip:
                surf.blit(img, (tile['pos'][0] - scroll[0], tile['pos'][1] - scroll[1]))
            else:
                surf.blit(pygame.transform.flip(img, True, False), (tile['pos'][0] - scroll[0], tile['pos'][1] - scroll[1]))

        for x in range(scroll[0] // self.tile_size, (dim[0] + scroll[0]) // self.tile_size + 1):
            for y in range(scroll[1] // self.tile_size, (dim[1] + scroll[1]) // self.tile_size + 1):
                pos = str(x) + ';' + str(y)
                if not pos in self.tilemap: 
                    continue
                tile = self.tilemap[pos]
                img = assets[tile['type']][tile['variant']]
                flip = True if tile['ramp'] == 'right' else False
                if not flip:
                    surf.blit(img, (tile['pos'][0] * self.tile_size - scroll[0], tile['pos'][1] * self.tile_size - scroll[1]))
                else:
                    surf.blit(pygame.transform.flip(img, True, False), (tile['pos'][0] * self.tile_size - scroll[0], tile['pos'][1] * self.tile_size - scroll[1]))
    
    def extract(self, idPairs, keep=False):
        matches = []
        for tile in self.offgridTiles.copy():
            if (tile['type'], tile['variant']) in idPairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgridTiles.remove(tile)
        
        for pos in self.tilemap.copy():
            tile = self.tilemap[pos]
            if (tile['type'], tile['variant']) in idPairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tileSize
                matches[-1]['pos'][1] *= self.tileSize
                if not keep: 
                    del self.tilemap[pos]

    def near_tiles(self, pos):
        tiles = []
        loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEAR_TILES:
            key = str(loc[0] + offset[0]) + ';' + str(loc[1] + offset[1])
            if key in self.tilemap:
                tiles.append(self.tilemap[key])
        return tiles
    
    def near_rects(self, pos):
        rects = []
        for tile in self.near_tiles(pos):
            if tile['type'] in PHYS_TILE_RECTS:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        
        return rects
    
    def near_ramps(self, pos):
        ramps = []
        for tile in self.near_tiles(pos):
            if tile['type'] == 'ramp':
                ramps.append(Ramp((tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size), self.tile_size, tile['ramp']))
        
        return ramps

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap' : self.tilemap, 'tile_size' : self.tile_size, 'offgrid' : self.offgrid}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        data = json.load(f)
        self.tilemap = data['tilemap']
        self.tile_size = data['tile_size']
        self.offgrid = data['offgrid']
