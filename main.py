import pygame
import sys
import tiles
import config
import player
import map
import inventory
import tree

# TO ADD:
# Diagonal Movement
# Tall Grass -- ability to get seeds which can then be planted
# Hoe for making farmland -- farmland must be near water
# Wheat
# Textures that look 3D -- The tile at the bottom with be like the trees but the tiles above it will just be the top -- this will be similar to the paths
# Should items be dropped or picked up by the player
# How to get rid of unwanted items
# Chests -- for storing items similar GUI to the inventory
# Axes for cutting down trees -- wood will be dropped on the floor which is picked up by the player
# Placeable blocks like crafting benches
# Crafting menu in both the inventory and in crafting benches


pygame.init()
clock = pygame.time.Clock()

x_tiles = int(config.SCREEN_WIDTH / config.TILE_WIDTH)
y_tiles = int(config.SCREEN_HEIGHT / config.TILE_WIDTH)

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Sandbox Game")

# tree_object = tree.Tree(2, 2, 64, 128)
obstacle_sprites = pygame.sprite.Group()
# obstacle_sprites.add(tree_object)

player_object = player.Player(352, 352, 64, 64, screen, obstacle_sprites)
player_group = pygame.sprite.GroupSingle()
player_group.add(player_object)

inventory_object = inventory.Inventory(352 + config.TILE_WIDTH, 352 - config.TILE_WIDTH, 3 * config.TILE_WIDTH, 4 * config.TILE_WIDTH, screen)
inventory_group = pygame.sprite.GroupSingle()
inventory_group.add(inventory_object)

#inventory_image = pygame.transform.scale(pygame.image.load('Textures/inventory.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 3))
inventory_opened = False

# Class that sorts the sprites into an order based on y position for drawing overlaps
class YAwareGroup(pygame.sprite.Group):
    def by_y(self, sprite):
        return sprite.rect.y
    def draw(self, surface):
        sprites = self.sprites()
        for sprite in sorted(sprites, key=self.by_y):
            self.spritedict[sprite] = surface.blit(sprite.image, sprite.rect)

# Initalizing the visible sprites group
visible_sprites = YAwareGroup()
visible_sprites.add(player_object)

# Calls the create_objects function which making objects like trees -- can be improved with the passing of the sprite groups in as arguments
tiles.create_objects(obstacle_sprites, visible_sprites)

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
                inventory_object.key_input(1)
            if event.key == pygame.K_2:
                inventory_object.key_input(2)
            if event.key == pygame.K_3:
                inventory_object.key_input(3)

        # Handling mouse input and passes it along to the player class -- maybe could be improved upon?
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and inventory_opened:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            inventory_object.mouse_update(mouse_x, mouse_y, 'pressed')

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            inventory_object.mouse_update(mouse_x, mouse_y, 'movement')

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                inventory_object.mouse_update(mouse_x, mouse_y, 'released')

    # Getting the x and y offsets which is used by basically all of the objects in the game, so there might be a better way to pass this along to other classes rather than in the arguments
    x_offset = player_object.get_offset_x()
    y_offset = player_object.get_offset_y()

    # The loop that draws the tiles on the screen each frame -- has a lot of arguments that may be unnecessary
    for y in range(len(map.overworld)):
        for x in range(len(map.overworld[y])):
            screen.blit(tiles.TileID(map.overworld[y][x], x, y, map.overworld, screen, x_offset, y_offset, obstacle_sprites), ((x * config.TILE_WIDTH) - x_offset, (y * config.TILE_WIDTH) - y_offset))

    # Reorganize this a bit -- seems to be repetitive
    if inventory_opened == False:

        player_group.update(inventory_object.slots[3][inventory_object.toolbar_selected_slot])
        obstacle_sprites.update(x_offset, y_offset)
        #print(len(obstacle_sprites), len(visible_sprites))
        #inventory_object.toolbar()
        tiles.tile_collisions_group.empty()

    else:
        inventory_group.update(player_object.rect.x, player_object.rect.y)
        inventory_group.draw(screen)
        inventory_group.update(player_object.rect.x, player_object.rect.y)
    
    visible_sprites.draw(screen)
    if inventory_opened: 
        inventory_group.draw(screen)
        inventory_group.update(player_object.rect.x, player_object.rect.y)
    else:
        inventory_object.toolbar()
    # player_group.draw(screen)
    # obstacle_sprites.draw(screen)
    # for sprite in visible_sprites:
    #         pygame.draw.rect(screen, 'red', sprite.hitbox, 3)
    pygame.display.update()
    clock.tick(60)



