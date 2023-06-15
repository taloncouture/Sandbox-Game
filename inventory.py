import pygame
import config
import items

class Inventory(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.transform.scale(pygame.image.load('Textures/inventory.png'), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.toolbar_image = pygame.transform.scale(pygame.image.load('Textures/toolbar.png'), (config.TILE_WIDTH * 3, config.TILE_WIDTH))
        self.selector_image = pygame.transform.scale(pygame.image.load('Textures/selector.png'), (config.TILE_WIDTH, config.TILE_WIDTH))

        self.rect.x = self.x
        self.rect.y = self.y

        self.screen = screen

        self.selected_item = 'none'
        self.last_slot = 'none'

        self.toolbar_selected_slot = 0

        self.slots = [
            [items.hoe, items.shovel, 'empty'],
            ['empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty']
        ]

    def update(self, x, y):
        self.rect.x = x + config.TILE_WIDTH * 2
        self.rect.y = y - config.TILE_WIDTH

        self.draw_items()
        self.toolbar()

        # Fix this so 'shovel' is not being hardcoded
        if self.selected_item != 'none':
            self.screen.blit(self.selected_item, (self.mouse_x - config.ITEM_WIDTH / 2, self.mouse_y - config.ITEM_WIDTH / 2))

    # Same here with the hardcoding
    def draw_items(self):
        for y in range(len(self.slots)):
            for x in range(len(self.slots[y])):
                if self.slots[y][x] != 'empty':
                    self.screen.blit(self.slots[y][x], (self.rect.x + x * config.TILE_WIDTH + config.ITEM_OFFSET, self.rect.y + y * config.TILE_WIDTH + config.ITEM_OFFSET))

    def in_bounds(self, mouse_x, mouse_y):
         if mouse_x >= self.rect.x and mouse_x <= self.rect.x + self.width and mouse_y >= self.rect.y and mouse_y <= self.rect.y + self.height:
                self.slot_x = int((mouse_x - self.rect.x) / config.TILE_WIDTH)
                self.slot_y = int((mouse_y - self.rect.y) / config.TILE_WIDTH)

                return True

    # Probably could be condensed
    def mouse_update(self, mouse_x, mouse_y, state):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        if state == 'pressed' and self.in_bounds(mouse_x, mouse_y):

                if self.slots[self.slot_y][self.slot_x] != 'empty':
                    self.selected_item = self.slots[self.slot_y][self.slot_x]
                    self.slots[self.slot_y][self.slot_x] = 'empty'
                    self.last_slot = self.slot_x, self.slot_y

        if state == 'released':
            if self.in_bounds(mouse_x, mouse_y):
                self.slots[self.slot_y][self.slot_x] = self.selected_item
            elif self.selected_item != 'none':
                self.slots[self.last_slot[1]][self.last_slot[0]] = self.selected_item
            
            self.selected_item = 'none'

    def key_input(self, key):
        self.toolbar_selected_slot = key - 1

    def toolbar(self):
        # Hardcoding issue again
        self.toolbar_x = (config.SCREEN_WIDTH / 2) - config.TILE_WIDTH - (config.TILE_WIDTH / 2)
        self.toolbar_y = config.SCREEN_HEIGHT - config.TILE_WIDTH
        self.screen.blit(self.toolbar_image, (self.toolbar_x, self.toolbar_y))
        self.screen.blit(self.selector_image, (self.toolbar_x + self.toolbar_selected_slot * config.TILE_WIDTH, self.toolbar_y))

        for x in range(len(self.slots[3])):
            if self.slots[3][x] != 'empty':
                self.screen.blit(self.slots[3][x], (self.toolbar_x + x * config.TILE_WIDTH + config.ITEM_OFFSET, self.toolbar_y + config.ITEM_OFFSET))


