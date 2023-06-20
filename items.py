import pygame
import config
import sprites

shovel = {"name": 'Shovel', "type": 'tool', "image": pygame.transform.scale(pygame.image.load('Textures/items/shovel2.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
hoe = {"name": 'Hoe', "type": 'tool', "image": pygame.transform.scale(pygame.image.load('Textures/items/hoe.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
axe = {"name": 'Axe', "type": 'tool', "image": pygame.transform.scale(pygame.image.load('Textures/items/axe.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
wood = {"name": 'Wood', "type": 'item', "amount_min": 3, "amount_max": 5, "image": pygame.transform.scale(pygame.image.load('Textures/items/wood.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}

new_item = 'none'
selected_item = 'none'
last_slot = 'none'
toolbar_selected_slot = 0

class dropped_item(pygame.sprite.Sprite):
    def __init__(self, x, y, item):
        super().__init__()

        self.x = x
        self.y = y

        self.name = 'dropped_item'
        self.item_type = item
        self.image = item.get("image")
        self.rect = self.image.get_rect()
        self.rect.x = x * config.TILE_WIDTH + config.ITEM_OFFSET
        self.rect.y = y * config.TILE_WIDTH + config.ITEM_OFFSET

        self.hitbox = self.rect.inflate(-10, -10)

        sprites.visible_sprites.add(self)
        sprites.obstacle_sprites.add(self)


    # Find a better way to do this
    def update(self, x_offset, y_offset):
        self.rect.x = (self.x * config.TILE_WIDTH + config.ITEM_OFFSET) - x_offset
        self.rect.y = (self.y * config.TILE_WIDTH + config.ITEM_OFFSET) - y_offset
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

