import pygame
import ctypes
from scripts.asset import assets
from scripts.tilemap import Tilemap
from scripts.entities import Collider

FPS = 60

class State:
    def __init__(self, game):
        self.game = game
        self.dimensions = (320, 180)
        self.render_dimensions = (1280, 720)
        self.fullscreen = False
        self.display = pygame.Surface(self.dimensions)
        self.screen = pygame.display.set_mode(self.render_dimensions)
        self.clock = pygame.time.Clock()

    def update(self, inputs=[]):
        pass

    def draw(self):
        bounds = self.display_bounds()
        self.screen.blit(pygame.transform.scale(self.display, (bounds.width, bounds.height)), (bounds.x, bounds.y))
        pygame.display.update()
    
    def change_state(self, state):
        self.game.change_state(state)
    
    def monitor_size(self):
        user32 = ctypes.windll.user32
        return (user32.GetSystemMetrics(78), user32.GetSystemMetrics(79))

    def display_bounds(self):
        xy = [0, 0]
        wh = [0, 0]
        aspect_ratio = self.dimensions[0] / self.dimensions[1]
        render_aspect_ratio = self.render_dimensions[0] / self.render_dimensions[1]
        if aspect_ratio > render_aspect_ratio:
            wh[0] = self.render_dimensions[0]
            wh[1] = wh[0] / aspect_ratio
            xy[1] = (self.render_dimensions[1] - wh[1]) / 2
        else:
            wh[1] = self.render_dimensions[1]
            wh[0] = wh[1] * aspect_ratio
            xy[0] = (self.render_dimensions[0] - wh[0]) / 2

        return pygame.Rect(xy[0], xy[1], wh[0], wh[1])

    def change_resolution(self, render_dimensions):
        self.render_dimensions = render_dimensions
        if render_dimensions != self.monitor_size():
            self.fullscreen = False
            self.screen = pygame.display.set_mode(self.render_dimensions)
        else:
            if self.fullscreen:
                self.screen = pygame.display.set_mode(self.render_dimensions, pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(self.render_dimensions)
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.render_dimensions = self.monitor_size()
            self.screen = pygame.display.set_mode(self.render_dimensions, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.render_dimensions)

class Gameplay(State):
    def __init__(self, game):
        super().__init__(game)
        self.tilemap = Tilemap(self)
        self.tilemap.load('map.json')

        self.scroll = [0, 0]
        self.movement = [0, 0, 0, 0]
        self.player = Collider('player', self, (100, 100), (16, 16))

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
        
        self.player.update(self.tilemap, [(self.movement[3] - self.movement[2]) / 2, (self.movement[1] - self.movement[0]) / 2])
        self.cam_follow(self.player.pos, 5, (self.player.rect().width / 2, self.player.rect().height / 2))

        self.clock.tick(FPS)

    def draw(self):
        self.display.fill((100, 100, 125))
        
        draw_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.tilemap.draw(self.display, draw_scroll)
        self.player.draw(self.display, draw_scroll)
        super().draw()
    
    def cam_follow(self, pos, lag=1, offset=(0,0)):
        self.scroll[0] += ((pos[0] - self.scroll[0]) - (self.dimensions[0] / 2 - offset[0])) / lag
        self.scroll[1] += ((pos[1] - self.scroll[1]) - (self.dimensions[1] / 2 - offset[1])) / lag

class Test(State):
    def __init__(self, game):
        super().__init__(game)
    
    def update(self, inputs):
        print('state change')
        self.clock.tick(FPS)

    def draw(self):
        super().draw()