import pygame
import sys
from scripts.asset import load_assets
from scripts.tilemap import Tilemap

FPS = 60

class Game:
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

        self.scroll = [0, 0]
        self.movement = [0, 0, 0, 0]

    def main(self):
        while True:            
            self.update(self.input())
            self.draw()

    def update(self, inputs):
        self.movement = [0, 0, 0, 0]

        if 'up' in inputs:
            self.movement[0] = 1
        if 'down' in inputs:
            self.movement[1] = 1
        if 'left' in inputs:
            self.movement[2] = 1
        if 'right' in inputs:
            self.movement[3] = 1

        self.scroll = [self.scroll[0] + (self.movement[3] - self.movement[2])*2, self.scroll[1] + (self.movement[1] - self.movement[0])*2]

        self.clock.tick(FPS)

    def draw(self):
        self.display.fill((100, 100, 125))
        
        draw_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.tilemap.draw(self.display, draw_scroll)

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()
    
    def input(self):
        inputs = []
        just_pressed = pygame.key.get_just_pressed()
        held = pygame.key.get_pressed()

        if held[pygame.K_w]:
            inputs.append('up')
        if held[pygame.K_s]:
            inputs.append('down')
        if held[pygame.K_a]:
            inputs.append('left')
        if held[pygame.K_d]:
            inputs.append('right')
        if just_pressed[pygame.K_RETURN]:
            inputs.append('select')
        if just_pressed[pygame.K_ESCAPE]:
            inputs.append('back')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        return inputs

if __name__ == '__main__':
    Game().main()