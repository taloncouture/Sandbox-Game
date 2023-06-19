import pygame
import sys
import tiles
import config
import player
import map
import inventory
import tree
import sprites
import items

# TO ADD:
# Diagonal Movement
# Tall Grass -- ability to get seeds which can then be planted
# Farmland must be near water
# Wheat
# Textures that look 3D -- The tile at the bottom with be like the trees but the tiles above it will just be the top -- this will be similar to the paths
# How to get rid of unwanted items
# Chests -- for storing items similar GUI to the inventory
# Placeable blocks like crafting benches
# Crafting menu in both the inventory and in crafting benches


pygame.init()
clock = pygame.time.Clock()

x_tiles = int(config.SCREEN_WIDTH / config.TILE_WIDTH)
y_tiles = int(config.SCREEN_HEIGHT / config.TILE_WIDTH)

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Sandbox Game")

#inventory_image = pygame.transform.scale(pygame.image.load('Textures/inventory.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 3))
inventory_opened = False

player_object = player.Player(352, 352, 64, 64, screen)
player_group = pygame.sprite.GroupSingle()
player_group.add(player_object)

sprites.visible_sprites.add(player_object)

# Calls the create_objects function which making objects like trees -- can be improved with the passing of the sprite groups in as arguments
tiles.create_objects()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handling keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if inventory_opened == True:
                    inventory_opened = False
                else: inventory_opened = True

            if event.key == pygame.K_1:
                inventory.key_input(1)
            if event.key == pygame.K_2:
                inventory.key_input(2)
            if event.key == pygame.K_3:
                inventory.key_input(3)

        # Handling mouse input and passes it along to the player class -- maybe could be improved upon?
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and inventory_opened:
            inventory.mouse_x, inventory.mouse_y = pygame.mouse.get_pos()
            inventory.mouse_update('pressed')

        if event.type == pygame.MOUSEMOTION:
            inventory.mouse_x, inventory.mouse_y = pygame.mouse.get_pos()
            inventory.mouse_update('movement')

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                inventory.mouse_x, inventory.mouse_y = pygame.mouse.get_pos()
                inventory.mouse_update('released')

    # Getting the x and y offsets which is used by basically all of the objects in the game, so there might be a better way to pass this along to other classes rather than in the arguments
    x_offset = player_object.get_offset_x()
    y_offset = player_object.get_offset_y()

    # The loop that draws the tiles on the screen each frame -- has a lot of arguments that may be unnecessary
    for y in range(len(map.overworld)):
        for x in range(len(map.overworld[y])):
            screen.blit(tiles.TileID(map.overworld[y][x], x, y, map.overworld, screen, x_offset, y_offset), ((x * config.TILE_WIDTH) - x_offset, (y * config.TILE_WIDTH) - y_offset))

    # Reorganize this a bit -- seems to be repetitive
    if inventory_opened == False:

        player_group.update(inventory.slots[3][items.toolbar_selected_slot])
        sprites.obstacle_sprites.update(x_offset, y_offset)
        tiles.tile_collisions_group.empty()

    else:
        inventory.update(player_object.rect.x, player_object.rect.y, screen)
    
    sprites.visible_sprites.draw(screen)
    if inventory_opened: 
        inventory.update(player_object.rect.x, player_object.rect.y, screen)
    else:
        #inventory_group.update(player_object.rect.x, player_object.rect.y)
        inventory.toolbar(screen)

    pygame.display.update()
    clock.tick(60)



