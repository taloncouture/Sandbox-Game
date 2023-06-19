import pygame
import config
import items
import random


slots = [
    [items.hoe, items.shovel, items.axe],
    [items.wood, 'empty', 'empty'],
    ['empty', items.wood, items.wood],
    ['empty', 'empty', 'empty']
]

slots_amounts = [
    [0, 0, 0],
    [2, 0, 0],
    [0, 5, 1],
    [0, 0, 0]
]

def is_full(name):
    full = True
    for y in range(len(slots)):
        for x in range(len(slots[y])):
            if slots[y][x] == 'empty':
                full = False
            elif slots[y][x].get('name') == name:
                full = False
    return full

mouse_x = 0
mouse_y = 0


x = 352 + config.TILE_WIDTH
y = 352 - config.TILE_WIDTH
width = 3 * config.TILE_WIDTH
height = 4 * config.TILE_WIDTH

image = pygame.transform.scale(pygame.image.load('Textures/inventory.png'), (width, height))
rect = image.get_rect()

toolbar_image = pygame.transform.scale(pygame.image.load('Textures/toolbar.png'), (config.TILE_WIDTH * 3, config.TILE_WIDTH))
selector_image = pygame.transform.scale(pygame.image.load('Textures/selector.png'), (config.TILE_WIDTH, config.TILE_WIDTH))

rect.x = x
rect.y = y


pygame.font.init()
inventory_font = pygame.font.Font('Textures/Fonts/8bitOperatorPlus8-Regular.ttf', 24)

def update(player_x, player_y, screen):

    rect.x = player_x + config.TILE_WIDTH * 2
    rect.y = player_y - config.TILE_WIDTH

    if rect.y < 0:
        rect.y = 0
    if rect.bottom > config.SCREEN_HEIGHT:
        rect.bottom = config.SCREEN_HEIGHT

    screen.blit(image, (rect.x, rect.y))
    draw_items(screen)

    if items.selected_item != 'none':
        screen.blit(items.selected_item.get("image"), (mouse_x - config.ITEM_WIDTH / 2, mouse_y - config.ITEM_WIDTH / 2))

    draw_label(screen)

    for y in range(len(slots)):
        for x in range(len(slots[y])):

            if slots[y][x] == 'empty' and items.selected_item == 'none': 
                slots_amounts[y][x] = 0
            draw_amounts(x, y, screen)

def add_item(item, sprite):
    if is_full(item.get('name')) == False:

        item_amount = random.randint(item.get('amount_min'), item.get('amount_max'))

        for y in range(len(slots)):
            for x in range(len(slots[y])):
                if slots[y][x] != 'empty':
                    if slots[y][x].get('name') == item.get('name'):
                        slots_amounts[y][x] += item_amount
                        print('adding item')
                        items.new_item = 'none'
                        sprite.kill()
                        return
        for y in range(len(slots)):
            for x in range(len(slots[y])):
                if slots[y][x] == 'empty':
                    slots[y][x] = item
                    slots_amounts[y][x] = item_amount
                    items.new_item = 'none'
                    sprite.kill()
                    return


def draw_items(screen):
    for y in range(len(slots)):
        for x in range(len(slots[y])):
            if slots[y][x] != 'empty':
                screen.blit(slots[y][x].get("image"), (rect.x + x * config.TILE_WIDTH + config.ITEM_OFFSET, rect.y + y * config.TILE_WIDTH + config.ITEM_OFFSET))

def get_slots():
    slot_x = int((mouse_x - rect.x) / config.TILE_WIDTH)
    slot_y = int((mouse_y - rect.y) / config.TILE_WIDTH)

    return slot_x, slot_y

def in_bounds():
        if mouse_x >= rect.x and mouse_x < rect.x + width and mouse_y >= rect.y and mouse_y < rect.y + height:
            return True
        else:
            return False
        
def draw_amounts(x, y, screen):
    if slots_amounts[y][x] > 0 and slots[y][x] != 'empty':
        amount_txt = inventory_font.render(str(slots_amounts[y][x]), False, (255, 255, 255))
        amount_txt_rect = amount_txt.get_rect(bottomright = (rect.x + x * config.TILE_WIDTH + config.TILE_WIDTH - config.ITEM_OFFSET, rect.y + y * config.TILE_WIDTH + config.TILE_WIDTH - config.ITEM_OFFSET))
        screen.blit(amount_txt, amount_txt_rect)

def draw_label(screen):
    if in_bounds():

        slot_x, slot_y = get_slots()

        if slots[slot_y][slot_x] != 'empty':
                label = inventory_font.render(slots[slot_y][slot_x].get("name"), False, (255, 255, 255))
                label_rect = label.get_rect(midbottom = (rect.x + (slot_x * config.TILE_WIDTH) + config.ITEM_OFFSET + (config.ITEM_WIDTH / 2), rect.y + (slot_y * config.TILE_WIDTH) + config.ITEM_OFFSET))
                screen.blit(label, label_rect)

# Probably could be condensed
def mouse_update(state):

    slot_x, slot_y = get_slots()

    if state == 'pressed' and in_bounds() and items.selected_item == 'none':

            if slots[slot_y][slot_x] != 'empty':
                items.selected_item = slots[slot_y][slot_x]
                slots[slot_y][slot_x] = 'empty'
                items.last_slot = slot_x, slot_y

    if state == 'released':
        if in_bounds() and slots[slot_y][slot_x] == 'empty':
            slots[slot_y][slot_x] = items.selected_item
            slots_amounts[slot_y][slot_x] = slots_amounts[items.last_slot[1]][items.last_slot[0]]
            slots_amounts[items.last_slot[1]][items.last_slot[0]] = 0
        elif in_bounds() and slots[slot_y][slot_x].get('name') == items.selected_item.get('name'):
            slots_amounts[slot_y][slot_x] += slots_amounts[items.last_slot[1]][items.last_slot[0]]
        elif items.selected_item != 'none':
            slots[items.last_slot[1]][items.last_slot[0]] = items.selected_item
        
        items.selected_item = 'none'

def key_input(key):
    items.toolbar_selected_slot = key - 1

def toolbar(screen):
    toolbar_x = (config.SCREEN_WIDTH / 2) - config.TILE_WIDTH - (config.TILE_WIDTH / 2)
    toolbar_y = config.SCREEN_HEIGHT - config.TILE_WIDTH
    screen.blit(toolbar_image, (toolbar_x, toolbar_y))
    screen.blit(selector_image, (toolbar_x + items.toolbar_selected_slot * config.TILE_WIDTH, toolbar_y))

    for x in range(len(slots[3])):
        if slots[3][x] != 'empty':
            screen.blit(slots[3][x].get("image"), (toolbar_x + x * config.TILE_WIDTH + config.ITEM_OFFSET, toolbar_y + config.ITEM_OFFSET))


