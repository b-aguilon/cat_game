import pygame

class Collider:
    def __init__(self, _type, game, pos, size):
        self.type = _type
        self.game = game
        self.pos = list(pos)
        self.size = size

    def rect(self): return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap):
        pass
    