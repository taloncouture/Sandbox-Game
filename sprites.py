import pygame

obstacle_sprites = pygame.sprite.Group()

# Class that sorts the sprites into an order based on y position for drawing overlaps
class YAwareGroup(pygame.sprite.Group):
    def by_y(self, sprite):
        result = sprite.rect.y
        if sprite.name == 'dropped_item':
            result -= 1000000
        return result
    def draw(self, surface):
        sprites = self.sprites()
        for sprite in sorted(sprites, key=self.by_y):
            self.spritedict[sprite] = surface.blit(sprite.image, sprite.rect)

# Initalizing the visible sprites group
visible_sprites = YAwareGroup()