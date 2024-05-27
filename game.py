import pygame
import json
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
        self.held_inputmap = {}
        self.just_pressed_inputmap = {}
        self.inputmap_path = 'json/inputmap.json'
        self.load_inputmap()

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
    
    def save_inputmap(self):
        f = open(self.inputmap_path, 'w')
        json.dump({'held' : self.held_inputmap, 'just_pressed' : self.just_pressed_inputmap}, f)
        f.close()

    def load_inputmap(self):
        f = open(self.inputmap_path, 'r')
        data = json.load(f)
        self.held_inputmap = data['held']
        self.just_pressed_inputmap = data['just_pressed']

        for key in self.held_inputmap.copy():
            new_key = int(key)
            self.held_inputmap[new_key] = self.held_inputmap[key]
            del self.held_inputmap[key]
        for key in self.just_pressed_inputmap.copy():
            new_key = int(key)
            self.just_pressed_inputmap[new_key] = self.just_pressed_inputmap[key]
            del self.just_pressed_inputmap[key]

    def change_state(self, state):
        self.state = state

if __name__ == '__main__':
    Game().main()