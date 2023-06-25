import pygame
import sys
import tiles
import config
import player
import map
import inventory
import sprites
import items
import animations

# TO ADD:
# Tall Grass -- ability to get seeds which can then be planted
# Farmland must be near water
# Wheat
# How to get rid of unwanted items
# Chests -- for storing items similar GUI to the inventory
# Crafting menu in both the inventory and in crafting benches


pygame.init()
clock = pygame.time.Clock()

x_tiles = int(config.SCREEN_WIDTH / config.TILE_WIDTH)
y_tiles = int(config.SCREEN_HEIGHT / config.TILE_WIDTH)

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Sandbox Game")

#inventory_image = pygame.transform.scale(pygame.image.load('Textures/inventory.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 3))
inventory_opened = False

player_object = player.Player(64, 64, screen)
player_group = pygame.sprite.GroupSingle()
player_group.add(player_object)

transition = animations.Darkness()

sprites.visible_sprites.add(player_object)

paused = False

# Calls the create_objects function which making objects like trees -- can be improved with the passing of the sprite groups in as arguments

def initalize_level(area):
    for sprite in sprites.obstacle_sprites:
        if sprite.name != 'player':
            sprite.kill()
    for sprite in sprites.visible_sprites:
        if sprite.name != 'player':
            sprite.kill()

    if area[2] == False:
        tiles.create_level(area)
        tiles.create_objects_random(area, 'tree', 300)
    if area == map.overworld:
        for y in range(len(area[1])):
            for x in range(len(area[1][y])):
                if area[1][y][x] == 'p':
                    player_object.set_location(x * config.TILE_WIDTH, y * config.TILE_WIDTH)
    else:
        if player_object.facing_direction[1] == -1:
            player_object.hitbox.bottom = (config.MAP_HEIGHT * config.TILE_WIDTH) - (config.TILE_WIDTH * 2)
        if player_object.facing_direction[1] == 1:
            player_object.hitbox.top = config.TILE_WIDTH * 2
    area[2] = True


initalize_level(map.current_area)

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
                    paused = False
                else: 
                    inventory_opened = True
                    paused = True

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

    screen.fill((0, 0, 0))

    # The loop that draws the tiles on the screen each frame -- has a lot of arguments that may be unnecessary
    for m in range(len(map.current_area) - 1):
        for y in range(int((config.SCREEN_HEIGHT + y_offset) / config.TILE_WIDTH) + 1):
            for x in range(int((config.SCREEN_WIDTH + x_offset) / config.TILE_WIDTH) + 1):
                if (x + 2) * config.TILE_WIDTH > x_offset and (x) * config.TILE_WIDTH < x_offset + config.SCREEN_WIDTH:
                    if (y + 2) * config.TILE_WIDTH > y_offset and (y) * config.TILE_WIDTH < y_offset + config.SCREEN_HEIGHT:
                        if m == 0:
                            screen.blit(tiles.TileID(map.current_area[m][y][x], x, y, map.current_area[m], screen, x_offset, y_offset), ((x * config.TILE_WIDTH) - x_offset, (y * config.TILE_WIDTH) - y_offset))
                        if m > 0:
                            tiles.TileID(map.current_area[m][y][x], x, y, map.current_area[m], screen, x_offset, y_offset)

                
    #tiles.update_groups(map.overworld_layers, x_offset, y_offset)
    #print(len(sprites.obstacle_sprites))


    if paused == True:
         inventory.update(player_object.rect.x, player_object.rect.y, screen)
    else:
        player_group.update(inventory.slots[3][items.toolbar_selected_slot])

    sprites.visible_sprites.draw(screen, player_object)
       

    if inventory_opened == False: 
        inventory.toolbar(screen)
    else:
        inventory.update(player_object.rect.x, player_object.rect.y, screen)


    #pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_object.hitbox.x - x_offset, player_object.hitbox.y - y_offset, player_object.hitbox.width, player_object.hitbox.height), 2)
    for sprite in sprites.obstacle_sprites:
            #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sprite.rect.x - x_offset, sprite.rect.y - y_offset, sprite.width, sprite.height), 2)
        if sprite.name != 'player' and sprite.name != 'dropped_item':
            sprite.kill()
    for sprite in sprites.visible_sprites:
        if sprite.name != 'player' and sprite.name != 'dropped_item':
            sprite.kill()

    if map.current_area != player_object.current_area:
        transition.fade()
        if transition.alpha_index < 0:
            map.current_area = player_object.current_area
            initalize_level(map.current_area)


    transition.display()

    #pygame.display.update()
    pygame.display.flip()
    clock.tick(60)



