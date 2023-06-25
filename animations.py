import pygame
import config

path_dig_0 = pygame.transform.scale(pygame.image.load('Textures/dig_states/dig_0.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
path_dig_1 = pygame.transform.scale(pygame.image.load('Textures/dig_states/dig_1.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
path_dig_frames = [path_dig_0, path_dig_1]

farmland_dig_0 = pygame.transform.scale(pygame.image.load('Textures/farmland/dig_states/dig_0.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
farmland_dig_1 = pygame.transform.scale(pygame.image.load('Textures/farmland/dig_states/dig_1.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
farmland_dig_frames = [farmland_dig_0, farmland_dig_1]

tree_chop_0 = pygame.transform.scale(pygame.image.load('Textures/animations/tree_chop_states/chop_0.png'), (config.TILE_WIDTH / 4, config.TILE_WIDTH / 8))
tree_chop_1 = pygame.transform.scale(pygame.image.load('Textures/animations/tree_chop_states/chop_1.png'), (config.TILE_WIDTH / 4, config.TILE_WIDTH / 8))
tree_chop_2 = pygame.transform.scale(pygame.image.load('Textures/animations/tree_chop_states/chop_2.png'), (config.TILE_WIDTH / 4, config.TILE_WIDTH / 8))
tree_chop_3 = pygame.transform.scale(pygame.image.load('Textures/animations/tree_chop_states/chop_3.png'), (config.TILE_WIDTH / 4, config.TILE_WIDTH / 8))
tree_chop_frames = [tree_chop_0, tree_chop_1, tree_chop_2, tree_chop_3]

break_0 = pygame.transform.scale(pygame.image.load('Textures/animations/break_states/0.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
break_1 = pygame.transform.scale(pygame.image.load('Textures/animations/break_states/1.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
break_2 = pygame.transform.scale(pygame.image.load('Textures/animations/break_states/2.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
break_frames = [break_0, break_1, break_2]

class Darkness:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.black_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        self.alpha_index = 255
        self.fading = False

    def fade(self):
        if self.fading == False:
            self.fading = True

    def display(self):
        if self.fading == True:
            self.alpha_index -= 5
        if self.alpha_index <= -255:
            self.alpha_index = 255
            self.fading = False
       

        self.black_surface.fill((0, 0, 0, 255 - abs(self.alpha_index)))
        self.display_surface.blit(self.black_surface, (0, 0))
