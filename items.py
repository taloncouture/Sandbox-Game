import pygame
import config

shovel = {"name": 'Shovel', "image": pygame.transform.scale(pygame.image.load('Textures/items/shovel2.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
hoe = {"name": 'Hoe', "image": pygame.transform.scale(pygame.image.load('Textures/items/hoe.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
axe = {"name": 'Axe', "image": pygame.transform.scale(pygame.image.load('Textures/items/axe.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}