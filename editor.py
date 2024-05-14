import pygame
import sys
from scripts.asset import load_assets, tiles, assets
from scripts.tilemap import Tilemap

FPS = 60

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption('game')
        self.DIMENSIONS = (320, 180)
        self.display = pygame.Surface(self.DIMENSIONS)
        self.screen = pygame.display.set_mode((1280, 720))
        self.render_scale = 4
        self.clock = pygame.time.Clock()
        load_assets()
        self.tilemap = Tilemap(self)

        self.tile_selection = False
        self.scroll = [0, 0]
        self.movement = [0, 0, 0, 0]

        self.type = 0
        self.var = 0
        self.tile_buttons = []
        self.set_buttons()
        self.hovering_tile = None

    def main(self):
        while True:            
            self.update()
            self.draw()
    
    def set_buttons(self):
        j = 0
        for i in range(0, len(tiles)):
            if ((i+1) - (j*i)) * self.tilemap.tile_size > self.DIMENSIONS[0]:
                j += 1
            self.tile_buttons.append(pygame.Rect((i - (j*(self.DIMENSIONS[0] // self.tilemap.tile_size)))*self.tilemap.tile_size, j*self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size))
    
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
        clicks = pygame.mouse.get_pressed()

        if held[pygame.K_w]:
            self.movement[0] = 1
        if held[pygame.K_s]:
            self.movement[1] = 1
        if held[pygame.K_a]:
            self.movement[2] = 1
        if held[pygame.K_d]:
            self.movement[3] = 1

        if just_pressed[pygame.K_TAB]:
            self.tile_selection = not self.tile_selection
        if just_pressed[pygame.K_DOWN]:
            self.var = (self.var - 1) % len(assets[tiles[self.type]])
        elif just_pressed[pygame.K_UP]:
            self.var = (self.var + 1) % len(assets[tiles[self.type]])

        if clicks[0] == 1 and self.hovering_tile == None:
            pos = self.get_tile_pos()
            str_pos = str(pos[0]) + ';' + str(pos[1])
            self.tilemap.tilemap[str_pos] = {'type' : tiles[self.type], 'variant' : self.var, 'pos' : pos}
        if clicks[2] == 1 and self.hovering_tile == None:
            pos = self.get_tile_pos()
            str_pos = str(pos[0]) + ';' + str(pos[1])
            if str_pos in self.tilemap.tilemap:
                del self.tilemap.tilemap[str_pos]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.button_presses(clicks)

        self.scroll = [self.scroll[0] + (self.movement[3] - self.movement[2])*2, self.scroll[1] + (self.movement[1] - self.movement[0])*2]

        self.clock.tick(FPS)

    def draw_ui(self):
        tile_img = assets[tiles[self.type]][self.var].copy()
        if self.hovering_tile == None:
            tile_img.set_alpha(150)
            self.display.blit(tile_img, (self.get_tile_pos()[0] * self.tilemap.tile_size - self.scroll[0], self.get_tile_pos()[1] * self.tilemap.tile_size - self.scroll[1]))
        if not self.tile_selection:
            self.display.blit(tile_img, (0, 0))
            return
        for i in range(len(self.tile_buttons)):
            img = assets[tiles[i]][self.var].copy() if assets[tiles[i]] == assets[tiles[self.type]] else assets[tiles[i]][0].copy()
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