import pygame
import config

obstacle_sprites = pygame.sprite.Group()

# Class that sorts the sprites into an order based on y position for drawing overlaps
class YAwareGroup(pygame.sprite.Group):
    def by_y(self, sprite):
        result = sprite.hitbox.y
        # if sprite.name == 'dropped_item':
        #     result -= 1000000
        return result
    def draw(self, surface, player):
        x_offset = player.offset_x
        y_offset = player.offset_y

        sprites = self.sprites()
        for sprite in sorted(sprites, key=self.by_y):
            if sprite.rect.x >= x_offset - sprite.width and sprite.rect.x <= x_offset + config.SCREEN_WIDTH and sprite.rect.y >= y_offset - sprite.height and sprite.rect.y <= y_offset + config.SCREEN_HEIGHT:
                self.spritedict[sprite] = surface.blit(sprite.image, pygame.Rect(sprite.rect.x - x_offset, sprite.rect.y - y_offset, sprite.width, sprite.height))

# Initalizing the visible sprites group
visible_sprites = YAwareGroup()


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
