import pygame
import config

path_dig_0 = pygame.transform.scale(pygame.image.load('Textures/dig_states/dig_0.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
path_dig_1 = pygame.transform.scale(pygame.image.load('Textures/dig_states/dig_1.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
path_dig_frames = [path_dig_0, path_dig_1]

farmland_dig_0 = pygame.transform.scale(pygame.image.load('Textures/farmland/dig_states/dig_0.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
farmland_dig_1 = pygame.transform.scale(pygame.image.load('Textures/farmland/dig_states/dig_1.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
farmland_dig_frames = [farmland_dig_0, farmland_dig_1]