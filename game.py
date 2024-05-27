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
        self.held_inputmap = {pygame.K_a : 'left', pygame.K_d : 'right', pygame.K_w : 'up', pygame.K_s : 'down'}
        self.just_pressed_inputmap = {pygame.K_SPACE : 'jump', pygame.K_RETURN : 'select', pygame.K_ESCAPE : 'back', pygame.K_LSHIFT : 'dodge'}

    def main(self):
        while True:            
            self.state.update(self.input())
            self.state.draw()
    
    def input(self):
        inputs = []
        just_pressed = pygame.key.get_just_pressed()
        held = pygame.key.get_pressed()

        for key in self.held_inputmap:
            if held[key]:
                inputs.append(self.held_inputmap[key])
        for key in self.just_pressed_inputmap:
            if just_pressed[key]:
                inputs.append(self.just_pressed_inputmap[key])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        return inputs

    def change_state(self, state):
        self.state = state

if __name__ == '__main__':
    Game().main()