import pygame
import config


# There might be some unnecessary lines in here
class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.name = 'tree'
        
        self.image = pygame.transform.scale(pygame.image.load('Textures/tree.png'), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x * config.TILE_WIDTH
        self.rect.y = y * config.TILE_WIDTH
        self.width = width
        self.height = height

        self.hitbox = pygame.Rect(0, 0, width, height / 2)
        self.hitbox.bottomright = (self.rect.x + width, self.rect.y + height - 20)
        

        self.x = x
        self.y = y

    def update(self, x_offset, y_offset):
        self.rect.x = (self.x * config.TILE_WIDTH) - x_offset
        self.rect.y = (self.y * config.TILE_WIDTH) - y_offset
        self.hitbox.bottomright = (self.rect.x + self.width, self.rect.y + self.height - 20)
