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

        # self.label = 'none'
        # self.label_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.toolbar_selected_slot = 0

        self.slots = [
            [items.hoe, items.shovel, items.axe],
            ['empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty'],
            ['empty', 'empty', 'empty']
        ]

        self.inventory_font = pygame.font.Font('Textures/Fonts/8bitOperatorPlus8-Regular.ttf', 20)

    def update(self, player_x, player_y):
        self.rect.x = player_x + config.TILE_WIDTH * 2
        self.rect.y = player_y - config.TILE_WIDTH

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT

        self.draw_items()
        #self.toolbar()

        # Fix this so 'shovel' is not being hardcoded
        if self.selected_item != 'none':
            self.screen.blit(self.selected_item.get("image"), (self.mouse_x - config.ITEM_WIDTH / 2, self.mouse_y - config.ITEM_WIDTH / 2))

        self.draw_label(self.mouse_x, self.mouse_y)

    # Same here with the hardcoding
    def draw_items(self):
        for y in range(len(self.slots)):
            for x in range(len(self.slots[y])):
                if self.slots[y][x] != 'empty':
                    self.screen.blit(self.slots[y][x].get("image"), (self.rect.x + x * config.TILE_WIDTH + config.ITEM_OFFSET, self.rect.y + y * config.TILE_WIDTH + config.ITEM_OFFSET))

    def get_slots(self, mouse_x, mouse_y):
        slot_x = int((mouse_x - self.rect.x) / config.TILE_WIDTH)
        slot_y = int((mouse_y - self.rect.y) / config.TILE_WIDTH)

        return slot_x, slot_y
    
    def in_bounds(self, mouse_x, mouse_y):
         if mouse_x >= self.rect.x and mouse_x < self.rect.x + self.width and mouse_y >= self.rect.y and mouse_y < self.rect.y + self.height:
                self.slot_x = int((mouse_x - self.rect.x) / config.TILE_WIDTH)
                self.slot_y = int((mouse_y - self.rect.y) / config.TILE_WIDTH)

                return True
    
    def draw_label(self, mouse_x, mouse_y):
        if self.in_bounds(mouse_x, mouse_y):

            slot_x, slot_y = self.get_slots(mouse_x, mouse_y)

            if self.slots[slot_y][slot_x] != 'empty':
                    self.label = self.inventory_font.render(self.slots[self.slot_y][self.slot_x].get("name"), False, (255, 255, 255))
                    self.label_rect = self.label.get_rect(midbottom = (self.rect.x + (self.slot_x * config.TILE_WIDTH) + config.ITEM_OFFSET + (config.ITEM_WIDTH / 2), self.rect.y + (self.slot_y * config.TILE_WIDTH) + config.ITEM_OFFSET))
                    #self.label_rect = self.label.get_rect(topleft = (0, 0))
                    self.screen.blit(self.label, self.label_rect)

    # Probably could be condensed
    def mouse_update(self, mouse_x, mouse_y, state):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        if state == 'pressed' and self.in_bounds(mouse_x, mouse_y) and self.selected_item == 'none':

                if self.slots[self.slot_y][self.slot_x] != 'empty':
                    self.selected_item = self.slots[self.slot_y][self.slot_x]
                    self.slots[self.slot_y][self.slot_x] = 'empty'
                    self.last_slot = self.slot_x, self.slot_y

        #if state == 'movement' and self.in_bounds(mouse_x, mouse_y):
            
                #print(self.slots[self.slot_y][self.slot_x].get("name"))

        if state == 'released':
            if self.in_bounds(mouse_x, mouse_y) and self.slots[self.slot_y][self.slot_x] == 'empty':
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
                self.screen.blit(self.slots[3][x].get("image"), (self.toolbar_x + x * config.TILE_WIDTH + config.ITEM_OFFSET, self.toolbar_y + config.ITEM_OFFSET))


