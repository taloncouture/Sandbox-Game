import pygame
import config
import sprites

shovel = {"name": 'Shovel', "type": 'tool', "image": pygame.transform.scale(pygame.image.load('Textures/items/shovel2.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
hoe = {"name": 'Hoe', "type": 'tool', "image": pygame.transform.scale(pygame.image.load('Textures/items/hoe.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
axe = {"name": 'Axe', "type": 'tool', "image": pygame.transform.scale(pygame.image.load('Textures/items/axe.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
wood = {"name": 'Wood', "type": 'item', "amount_min": 3, "amount_max": 5, "image": pygame.transform.scale(pygame.image.load('Textures/items/wood.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}
crafting_bench = {"name": 'Crafting Bench', "type": 'block', "image": pygame.transform.scale(pygame.image.load('Textures/crafting_bench.png'), (config.ITEM_WIDTH, config.ITEM_WIDTH))}

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

        self.width = config.ITEM_WIDTH
        self.height = config.ITEM_WIDTH

        self.hitbox = self.rect.inflate(-10, -10)


