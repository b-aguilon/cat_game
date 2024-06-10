import pygame
import math
from scripts.asset import assets
from enum import Enum

class Collider:
    def __init__(self, _type, game, pos, size):
        self.type = _type
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        self.flip = False
        self.on_ramp = False

    def update(self, tilemap, movement=(0,0), friction=0.2):
        for key in self.collisions:
            self.collisions[key] = False  
        self.velocity = [self.velocity[0] + movement[0], self.velocity[1] + movement[1]]
        self.velocity[1] += 0.25
        self.velocity[1] = min(self.velocity[1], 8)
        friction = friction * 1.3 if self.on_ramp else friction
        self.velocity[0] = pygame.math.lerp(self.velocity[0], 0, friction)
        self.on_ramp = False
        if self.velocity[0] > 0:
            self.flip = False
        elif self.velocity[0] < 0:
            self.flip = True
        self.rect_collisions(tilemap)
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.ramp_collisions(tilemap)

    def rect(self): return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def touching_right(self, other):
        bounds = self.rect()
        return bounds.left + self.velocity[0] < other.right and bounds.bottom > other.top and bounds.top < other.bottom and bounds.left > other.left
    
    def touching_top(self, other):
        bounds = self.rect()
        return bounds.bottom + self.velocity[1] > other.top and bounds.left < other.right and bounds.right > other.left and bounds.top < other.top

    def touching_bottom(self, other):
        bounds = self.rect()
        return bounds.top + self.velocity[1] < other.bottom and bounds.left < other.right and bounds.right > other.left and bounds.bottom > other.bottom
    
    def touching_left(self, other):
        bounds = self.rect()
        return bounds.right + self.velocity[0] > other.left and bounds.top < other.bottom and bounds.bottom > other.top and bounds.right < other.right
    
    def ramp_collisions(self, tilemap):
        erect = self.rect()
        for ramp in tilemap.near_ramps(self.pos):
            if not erect.colliderect(ramp.bounds) or (self.velocity[0] == 0 and self.velocity[1] < 0):
                continue
            if erect.bottom >= ramp.top_at(self.pos[0] + self.size[0])[1] and ramp.face == 'left':
                erect.bottom = ramp.top_at(self.pos[0] + self.size[0])[1]
                self.velocity[1] = -self.velocity[0] if self.velocity[0] < 0 else 0
            elif erect.bottom >= ramp.top_at(self.pos[0])[1] and ramp.face == 'right':
                erect.bottom = ramp.top_at(self.pos[0])[1]
                self.velocity[1] = self.velocity[0] if self.velocity[0] > 0 else 0
            self.on_ramp = True
            self.collisions['down'] = True
            self.pos[1] = erect.y

    def rect_collisions(self, tilemap):
        for rect in tilemap.near_rects(self.pos):
            if self.touching_top(rect):
                self.collisions['down'] = True
                self.pos[1] = rect.top - self.rect().height
                self.velocity[1] = 0
            if self.touching_bottom(rect):
                self.collisions['up'] = True
                self.pos[1] = rect.bottom
                self.velocity[1] = 0
            if self.touching_right(rect):
                self.collisions['left'] = True
                self.pos[0] = rect.right
                self.velocity[0] = 0
            if self.touching_left(rect):
                self.collisions['right'] = True
                self.pos[0] = rect.left - self.rect().width
                self.velocity[0] = 0
        
    def draw(self, surf, scroll=(0,0)):
        pass

class Cat(Collider):
    def __init__(self, game, pos, size):
        super().__init__('cat', game, pos, size)
        self.air_time = 0
        self.jumps = 1
        self.dodge_speed = 16
    
    def update(self, tilemap, movement=(0,0), friction=0.12):
        super().update(tilemap, movement, friction)
        self.jumps = 1
        self.air_time += 1
        if self.air_time > 6:
            self.jumps = 0
        if self.collisions['down']:
            self.jumps = 1
            self.air_time = 0

    def jump(self):
        if self.jumps > 0:
            self.velocity[1] = -5
            self.jumps = max(0, self.jumps - 1)
    
    def dodge(self):
        if self.jumps > 0:
            self.velocity[0] = self.dodge_speed if not self.flip else -self.dodge_speed

    def draw(self, surf, scroll=(0,0)):
        img = assets['cat']
        if not self.flip:
            surf.blit(img, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))
        else:
            surf.blit(pygame.transform.flip(img, True, False), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))

class EnemyState(Enum):
    WANDER = 0
    PURSUIT = 1
    COMBAT = 2 

class Enemy(Collider):
    def __init__(self, game, pos, size):
        super().__init__('enemy', game, pos, size)
        self.curr_state = EnemyState.WANDER

    def update(self, tilemap, movement=(0,0), friction=0.2):
        super().update(tilemap, movement, friction)

        match self.curr_state:
            case EnemyState.WANDER:
                self.wander()
            case EnemyState.PURSUIT:
                self.pursuit()
            case EnemyState.COMBAT:
                self.combat()       
    
    def wander(self):
        pass

    def pursuit(self):
        pass

    def combat(self):
        pass

    def draw(self, surf, scroll=(0,0)):
        img = assets['cat']
        if not self.flip:
            surf.blit(img, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))
        else:
            surf.blit(pygame.transform.flip(img, True, False), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))

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