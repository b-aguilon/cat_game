import pygame
from scripts.asset import assets

class Collider:
    def __init__(self, _type, game, pos, size):
        self.type = _type
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def rect(self): return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0,0), friction=0.2):   
        self.velocity = [self.velocity[0] + movement[0], self.velocity[1] + movement[1]]
        self.velocity[1] += 0.25
        self.velocity[1] = min(self.velocity[1], 7)
        self.velocity[0] = pygame.math.lerp(self.velocity[0], 0, friction)
        self.collisions(tilemap)

    def collisions(self, tilemap):
        self.pos[0] += self.velocity[0] 
        erect = self.rect()
        for rect in tilemap.near_rects(self.pos):
            if erect.colliderect(rect):
                if self.velocity[0] > 0:
                    erect.right = rect.left
                if self.velocity[0] < 0:
                    erect.left = rect.right
                self.velocity[0] = 0
                self.pos[0] = erect.x

        self.pos[1] += self.velocity[1] 
        erect = self.rect()
        for rect in tilemap.near_rects(self.pos):
            if erect.colliderect(rect):
                if self.velocity[1] > 0:
                    erect.bottom = rect.top
                if self.velocity[1] < 0:
                    erect.top = rect.bottom
                self.velocity[1] = 0
                self.pos[1] = erect.y
        #I AM SO FUCKING
        erect = self.rect()
        for ramp in tilemap.near_ramps(self.pos):
            if not erect.colliderect(ramp.bounds) or self.velocity[1] < 0:
                continue
            if erect.bottom >= ramp.top_at(self.pos[0] + self.size[0])[1] and ramp.face == 'left':
                erect.bottom = ramp.top_at(self.pos[0] + self.size[0])[1]
                self.velocity[1] = 0
            elif erect.bottom >= ramp.top_at(self.pos[0])[1] and ramp.face == 'right':
                erect.bottom = ramp.top_at(self.pos[0])[1]
                self.velocity[1] = 0
            
            self.pos[1] = erect.y
        
    def draw(self, surf, scroll=(0,0)):
        surf.blit(assets['dirt'][0], (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))

class Ramp:
    def __init__(self, pos, size, face):
        self.pos = list(pos)
        self.size = size
        self.face = face
        self.bounds = pygame.Rect(pos[0], pos[1], size, size)

    def bottom(self):
        return self.pos[1] + self.size
    
    def top(self):
        return self.pos[1]
    
    def top_at(self, x):
        pos = [x, 0]
        if self.face == 'left':
            pos[1] = -x + self.bottom() + self.top() - (self.pos[1] - self.pos[0])
        elif self.face == 'right':
            pos[1] = self.size + x - self.bottom() + self.top() + (self.pos[1] - self.pos[0])
        else:
            raise Exception('left or right, not' + self.face)
        pos[1] = pygame.math.clamp(pos[1], self.pos[1], self.pos[1] + self.size)

        return pos
    
    def left(self):
        return self.pos[0]
    
    def right(self):
        return self.pos[0] + self.size