import pygame
import sys
from scripts.asset import load_assets
from scripts.states import Gameplay

FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption('cat')
        self.state = Gameplay(self)
        load_assets()

    def main(self):
        while True:            
            self.state.update(self.input())
            self.state.draw()
    
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

    def change_state(self, state):
        self.state = state

if __name__ == '__main__':
    Game().main()