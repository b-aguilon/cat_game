import pygame
import sys
from scripts.asset import load_assets, tiles, assets
from scripts.tilemap import Tilemap

FPS = 60

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption('editor')
        self.dimensions = (640, 360)
        self.display = pygame.Surface(self.dimensions)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.render_scale = 3
        self.clock = pygame.time.Clock()
        load_assets()
        self.tilemap = Tilemap(self, 32)
        self.path = 'map.json'

        self.tile_selection = False
        self.scroll = [0, 0]
        self.movement = [0, 0, 0, 0]

        self.type = 0
        self.var = 0
        self.ramp = 'none'
        self.offgrid = False
        self.tile_buttons = []
        self.set_buttons()
        self.hovering_tile = None

        self.clicks = (0, 0, 0)

    def main(self):
        while True:            
            self.update()
            self.draw()
    
    def set_buttons(self):
        j = 0
        for i in range(0, len(tiles)):
            if ((i+1) - (j*i)) * self.tilemap.tile_size > self.dimensions[0]:
                j += 1
            self.tile_buttons.append(pygame.Rect((i - (j*(self.dimensions[0] // self.tilemap.tile_size)))*self.tilemap.tile_size, j*self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size))
    
    def get_mpos(self):
        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0] / self.render_scale, mpos[1] / self.render_scale)
        return mpos
    
    def get_tile_pos(self):
        pos = self.get_mpos()
        return (int((pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((pos[1] + self.scroll[1]) // self.tilemap.tile_size))
    
    def button_presses(self, clicks):
        if not self.tile_selection:
            return
        for i in range(len(self.tile_buttons)):
            if not self.tile_buttons[i].collidepoint(self.get_mpos()):
                self.hovering_tile = None
                continue
            self.hovering_tile = assets[tiles[i]][0]
            if clicks[0] == 1:
                self.type = i
                self.var = 0
            return

    def update(self):
        self.movement = [0, 0, 0, 0]
        held = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()
        last_clicks = self.clicks
        self.clicks = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if held[pygame.K_w]:
            self.movement[0] = 1
        if held[pygame.K_s]:
            self.movement[1] = 1
        if held[pygame.K_a]:
            self.movement[2] = 1
        if held[pygame.K_d]:
            self.movement[3] = 1

        if just_pressed[pygame.K_LEFT] and tiles[self.type] == 'ramp': 
            self.ramp = 'left'
        elif just_pressed[pygame.K_RIGHT] and tiles[self.type] == 'ramp':
            self.ramp = 'right'
        
        if just_pressed[pygame.K_r]:
            self.offgrid = not self.offgrid
        if just_pressed[pygame.K_p]:
            self.tilemap.save(self.path)
        if just_pressed[pygame.K_TAB]:
            self.tile_selection = not self.tile_selection
        if just_pressed[pygame.K_DOWN]:
            self.var = (self.var - 1) % len(assets[tiles[self.type]])
        elif just_pressed[pygame.K_UP]:
            self.var = (self.var + 1) % len(assets[tiles[self.type]])

        mpos = self.get_mpos()
        mpos = (int(mpos[0] + self.scroll[0]), int(mpos[1] + self.scroll[1]))
        pos = self.get_tile_pos()
        if self.clicks[0] == 1 and self.hovering_tile == None:
            ramp = self.ramp if tiles[self.type] == 'ramp' else 'none'
            if not self.offgrid:
                str_pos = str(pos[0]) + ';' + str(pos[1])
                self.tilemap.tilemap[str_pos] = {'type' : tiles[self.type], 'variant' : self.var, 'ramp' : ramp, 'pos' : pos}
            elif self.offgrid and last_clicks[0] == 0:
                str_mpos = str(mpos[0]) + ';' + str(mpos[1])
                self.tilemap.offgrid[str_mpos] = {'type' : tiles[self.type], 'variant' : self.var, 'ramp' : ramp, 'pos' : mpos}
        if self.clicks[2] == 1 and self.hovering_tile == None:
            if not self.offgrid:
                str_pos = str(pos[0]) + ';' + str(pos[1])
                if str_pos in self.tilemap.tilemap:
                    del self.tilemap.tilemap[str_pos]
            else:
                for key in self.tilemap.offgrid.copy():
                    tile = self.tilemap.offgrid[key]
                    img = assets[tile['type']][tile['variant']]
                    rect = pygame.Rect(tile['pos'][0], tile['pos'][1], img.get_width(), img.get_height())
                    if rect.collidepoint(mpos):
                        del self.tilemap.offgrid[key]

        self.button_presses(self.clicks)

        self.scroll = [self.scroll[0] + (self.movement[3] - self.movement[2])*2, self.scroll[1] + (self.movement[1] - self.movement[0])*2]

        self.clock.tick(FPS)

    def draw_ui(self):
        tile_img = assets[tiles[self.type]][self.var].copy()
        if self.hovering_tile == None:
            tile_img.set_alpha(150)
            tile_img = pygame.transform.flip(tile_img, True, False) if self.ramp == 'right' and tiles[self.type] == 'ramp' else tile_img
            if not self.offgrid:
                self.display.blit(tile_img, (self.get_tile_pos()[0] * self.tilemap.tile_size - self.scroll[0], self.get_tile_pos()[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(tile_img, self.get_mpos())
        if not self.tile_selection:
            self.display.blit(tile_img, (0, 0))
            return
        for i in range(len(self.tile_buttons)):
            img = assets[tiles[i]][self.var].copy() if assets[tiles[i]] == assets[tiles[self.type]] else assets[tiles[i]][0].copy()
            if tiles[i] == 'ramp' and self.ramp == 'right':
                img = pygame.transform.flip(img, True, False)
            if self.hovering_tile != assets[tiles[i]][0]:
                img.set_alpha(150)
            self.display.blit(img, self.tile_buttons[i].topleft)

    def draw(self):
        self.display.fill((0, 0, 0))
        draw_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.tilemap.draw(self.display, draw_scroll)
        self.draw_ui()

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    Editor().main()