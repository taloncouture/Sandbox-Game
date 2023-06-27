import pygame
import config
import map
import tiles
import items
import animations
import sprites
import pygame
import inventory

class Player(pygame.sprite.Sprite):
    
    # Check if there are any unnecessary lines in here
    def __init__(self, width, height, screen):
        super().__init__()
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

        self.name = 'player'

        # self.offset_x = int((config.SCREEN_WIDTH / 2) - self.x)
        # self.offset_y = int((config.SCREEN_HEIGHT / 2) - self.y)
        self.offset_x = 0
        self.offset_y = 0

        self.current_chunk_x = 0
        self.current_chunk_y = 0

        self.starting_x = 0
        self.starting_y = 0

        self.speed = 5

        self.image = pygame.transform.scale(pygame.image.load('Textures/player_states/front_0.png'), (self.width, self.height))
        self.rect = self.image.get_rect()

        down_0 = pygame.transform.scale(pygame.image.load('Textures/player_states/front_0.png'), (self.width, self.height))
        down_1 = pygame.transform.scale(pygame.image.load('Textures/player_states/front_1.png'), (self.width, self.height))
        up_0 = pygame.transform.scale(pygame.image.load('Textures/player_states/back_0.png'), (self.width, self.height))
        up_1 = pygame.transform.scale(pygame.image.load('Textures/player_states/back_1.png'), (self.width, self.height))
        right_0 = pygame.transform.scale(pygame.image.load('Textures/player_states/right_0.png'), (self.width, self.height))
        right_1 = pygame.transform.scale(pygame.image.load('Textures/player_states/right_1.png'), (self.width, self.height))
        left_0 = pygame.transform.scale(pygame.image.load('Textures/player_states/left_0.png'), (self.width, self.height))
        left_1 = pygame.transform.scale(pygame.image.load('Textures/player_states/left_1.png'), (self.width, self.height))
        shovel_right_0 = pygame.transform.scale(pygame.image.load('Textures/shovel_animation/shovel_0.png'), (self.width * 2, self.height))
        shovel_right_1 = pygame.transform.scale(pygame.image.load('Textures/shovel_animation/shovel_1.png'), (self.width * 2, self.height))

        self.down_frames = [down_0, down_1]
        self.up_frames = [up_0, up_1]
        self.right_frames = [right_0, right_1]
        self.left_frames = [left_0, left_1]
        self.shovel_right_frames = [shovel_right_0, shovel_right_1]
        self.animation_index = 0
        self.fade_animation_index = 0

        self.rect.centerx = config.SCREEN_WIDTH / 2
        self.rect.centery = config.SCREEN_HEIGHT / 2

        self.hitbox = self.rect.inflate(-6, -32)
        self.move_direction = [0, 0]

        self.screen = screen

        self.center_x = config.SCREEN_WIDTH / 2
        self.center_y = config.SCREEN_HEIGHT / 2

        self.outline = pygame.transform.scale(pygame.image.load('Textures/outline.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
        self.highlighted_tile_x = 0
        self.highlighted_tile_y = 0

        self.facing_tile_x = 0
        self.facing_tile_y = 0

        self.direction = 'none'
        self.facing = 'down'
        self.facing_direction = [0, 0]

        self.dig_animation_index = 0
        self.break_animation_index = 0
        self.path_dig_frames = animations.path_dig_frames
        self.farmland_dig_frames = animations.farmland_dig_frames

        self.obstacle_sprites = sprites.obstacle_sprites
        self.visible_sprites = sprites.visible_sprites

        self.key_pressed_index = 0

        self.current_area = map.overworld_layers

    def get_offset_x(self):
        return self.offset_x
    def get_offset_y(self):
        return self.offset_y
    
    def set_location(self, x, y):
        self.hitbox.x = x
        self.hitbox.y = y
        self.starting_x = x
        self.starting_y = y

    
    def highlight_tile(self, x_diff, y_diff):
        tile_x = int((self.x + self.width / 2 ) / config.TILE_WIDTH)
        tile_y = int((self.y + self.height / 2) / config.TILE_WIDTH)
        
        self.screen.blit(self.outline, ((tile_x + x_diff) * config.TILE_WIDTH - self.offset_x, (tile_y + y_diff) * config.TILE_WIDTH - self.offset_y))

    def update(self, selected_item):

        self.facing_tile_x = int((self.x + self.width / 2) / config.TILE_WIDTH) + self.facing_direction[0]
        self.facing_tile_y = int((self.y + self.height / 2) / config.TILE_WIDTH) + self.facing_direction[1]

        self.tile_x = int((self.x + self.width / 2) / config.TILE_WIDTH) + self.highlighted_tile_x
        self.tile_y = int((self.y + self.height / 2) / config.TILE_WIDTH) + self.highlighted_tile_y

        #print(self.tile_x, self.tile_y)

        self.x = self.rect.x
        self.y = self.rect.y

        #print(self.tile_x, self.tile_y)

        self.selected_object = selected_item
        
        # if self.selected_object == 'shovel':
        #     if self.facing == 'down':
        #         self.highlight_tile(0, 1)
        #     if self.facing == 'up':
        #         self.highlight_tile(0, -1)
        #     if self.facing == 'right':
        #         self.highlight_tile(1, 0)
        #     if self.facing == 'left':
        #         self.highlight_tile(-1, 0)
        if self.selected_object != 'empty':
            if self.selected_object == items.shovel or self.selected_object == items.hoe or self.selected_object == items.axe or self.selected_object.get("type") == 'block':
                if self.facing == 'down':
                    self.highlighted_tile_y = 1
                    self.highlighted_tile_x = 0
                if self.facing == 'up':
                    self.highlighted_tile_y = -1
                    self.highlighted_tile_x = 0
                if self.facing == 'right':
                    self.highlighted_tile_x = 1
                    self.highlighted_tile_y = 0
                if self.facing == 'left':
                    self.highlighted_tile_x = -1
                    self.highlighted_tile_y = 0
                self.highlight_tile(self.highlighted_tile_x, self.highlighted_tile_y)

        self.input()
        self.move()

    def collision(self, direction):
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if sprite.name == 'dropped_item':
                            # items.new_item = sprite.item_type
                            # if inventory.is_full == False: sprite.kill()
                            inventory.add_item(sprite.item_type, sprite)
                        else:
                            if self.move_direction[0] == 1:
                                self.hitbox.right = sprite.hitbox.left
                            if self.move_direction[0] == -1:
                                self.hitbox.left = sprite.hitbox.right
                            self.direction = 'none'
                        return True
                for sprite in tiles.tile_collisions_group:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.move_direction[0] == 1:
                            self.hitbox.right = sprite.hitbox.left
                        if self.move_direction[0] == -1:
                            self.hitbox.left = sprite.hitbox.right
                        self.direction = 'none'
                        return True
            
            if direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if sprite.name == 'dropped_item':
                            # items.new_item = sprite.item_type
                            # if inventory.is_full == False: sprite.kill()
                            inventory.add_item(sprite.item_type, sprite)
                        else:
                            if self.move_direction[1] == -1:
                                self.hitbox.top = sprite.hitbox.bottom
                            if self.move_direction[1] == 1:
                                self.hitbox.bottom = sprite.hitbox.top
                            self.direction = 'none'
                        return True
                for sprite in tiles.tile_collisions_group:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.move_direction[1] == -1:
                            self.hitbox.top = sprite.hitbox.bottom
                        if self.move_direction[1] == 1:
                            self.hitbox.bottom = sprite.hitbox.top
                        self.direction = 'none'
                        return True

            return False

    # Make a more condensed movement system that isn't a bunch of if statements
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.selected_object == items.shovel:
            self.create_path()
        if keys[pygame.K_SPACE] and self.selected_object == items.hoe:
            self.create_farmland()
        if keys[pygame.K_SPACE] and self.selected_object == items.axe:
            self.key_pressed_index += 0.05
            if self.key_pressed_index > 1:
                self.chop_tree()
                self.key_pressed_index = 0
        if self.selected_object != 'empty':
            if keys[pygame.K_SPACE] and self.selected_object.get("type") == 'block':
                self.place_block()
        if keys[pygame.K_LSHIFT]:
            # Temporary Code -- will have better world navigation system in place eventually
            if self.current_area[1][self.facing_tile_y][self.facing_tile_x] != ' ' and self.current_area[1][self.facing_tile_y][self.facing_tile_x] != 'p':
                if tiles.BlockID(self.current_area[1][self.facing_tile_y][self.facing_tile_x]).get("type") == 'door':
                    if tiles.BlockID(self.current_area[1][self.facing_tile_y][self.facing_tile_x]).get("name") == 'down_stair':
                        self.current_area = map.underground_layers
                    if tiles.BlockID(self.current_area[1][self.facing_tile_y][self.facing_tile_x]).get("name") == 'hedge_door':
                        if self.current_area == map.overworld_layers:
                            self.current_area = map.overworld2_layers
                        else:
                            self.current_area = map.overworld_layers
        if keys[pygame.K_b]:
            self.current_area = map.overworld_layers

        if self.key_pressed_index > 0:
            self.key_pressed_index -= 0.01
        else: self.key_pressed_index = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 'left'
            self.facing = 'left'
            self.move_direction[0] = -1
            self.facing_direction[0] = -1
            self.facing_direction[1] = 0
            #self.hitbox = self.rect.inflate(-20, -20)
            self.animation(self.left_frames)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 'right'
            self.facing = 'right'
            self.move_direction[0] = 1
            self.facing_direction[0] = 1
            self.facing_direction[1] = 0
            #self.hitbox = self.rect.inflate(-20, -20)
            self.animation(self.right_frames)
        else:
            self.move_direction[0] = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = 'up'
            self.facing = 'up'
            self.move_direction[1] = -1
            self.facing_direction[1] = -1
            self.facing_direction[0] = 0
            #self.hitbox = self.rect.inflate(0, -20)
            self.animation(self.up_frames)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = 'down'
            self.facing = 'down'
            self.move_direction[1] = 1
            self.facing_direction[1] = 1
            self.facing_direction[0] = 0
            #self.hitbox = self.rect.inflate(0, -20)
            self.animation(self.down_frames)
        else:
            self.direction = 'none'
            self.move_direction[1] = 0

    # Animates by cycling through an array of frames
    def animation(self, frames):
        self.animation_index += 0.05
        if self.animation_index >= len(frames):
            self.animation_index = 0
        self.image = frames[int(self.animation_index)]

    def break_animation(self, x, y, result, area):
        self.break_animation_index += 0.1
        if self.break_animation_index > len(animations.break_frames):
            self.break_animation_index = 0
            area[y][x] = result
        else:
            self.screen.blit(animations.break_frames[int(self.break_animation_index)], (x * config.TILE_WIDTH - self.offset_x, y * config.TILE_WIDTH - self.offset_y))

    def fade_animation(self):
        self.fade_animation_index += 1
        self.screen.set_alpha(self.fade_animation_index)


    # Maybe this could merge with the regular animation
    def dig_animation(self, x, y, frames, result):
        self.dig_animation_index += 0.1
        if self.dig_animation_index > 2:
            self.dig_animation_index = 0
            map.overworld[y][x] = result
        else:
            self.screen.blit(frames[int(self.dig_animation_index)], (x * config.TILE_WIDTH - self.offset_x, y * config.TILE_WIDTH - self.offset_y))
            #map.overworld[y][x] = self.frames[int(self.animation_index)]

    def chop_tree(self):
        if self.tile_x >= 0 and self.tile_x < len(self.current_area[0]) - 1 and self.tile_y >= 0 and self.tile_y < len(self.current_area[0]) - 1:
            if self.current_area[1][self.tile_y][self.tile_x] == 't':
                #self.break_animation(self.tile_x, self.tile_y, '0', map.get_level(self.current_level)[1])
                self.current_area[1][self.tile_y][self.tile_x] = '0'
                # for sprite in sprites.obstacle_sprites:
                #     if sprite.name == 'tree':
                #         sprite.kill()
                # for sprite in sprites.visible_sprites:
                #     if sprite.name == 'tree':
                #         sprite.kill()
                        
                #tiles.create_objects()
                drop = items.dropped_item(self.tile_x, self.tile_y, items.wood)

                sprites.obstacle_sprites.add(drop)
                sprites.visible_sprites.add(drop)

    # Check if there are any repetitive parts in here
    def create_path(self):

        if self.tile_x >= 0 and self.tile_x < len(map.overworld[0]) - 1 and self.tile_y >= 0 and self.tile_y < len(map.overworld) - 1:

            if self.current_area[0][self.tile_y][self.tile_x] == '0':
                #self.dig_animation(self.tile_x, self.tile_y, self.path_dig_frames, '1')
                self.break_animation(self.tile_x, self.tile_y, '1', self.current_area[0])
                if self.facing == 'right': self.animation(self.shovel_right_frames)
                #map.overworld[tile_y][tile_x] = '1'

    def create_farmland(self):

        if self.tile_x >= 0 and self.tile_x < len(map.overworld[0]) - 1 and self.tile_y >= 0 and self.tile_y < len(map.overworld) - 1:
            if self.current_area[0][self.tile_y][self.tile_x] == '0':
                self.break_animation(self.tile_x, self.tile_y, 'f',self.current_area[0])

    def place_block(self):
        if self.tile_x >= 0 and self.tile_x < len(map.overworld[0]) - 1 and self.tile_y >= 0 and self.tile_y < len(map.overworld) - 1:
            if tiles.is_placeable(self.tile_x, self.tile_y, self.current_area):
                self.current_area[1][self.tile_y][self.tile_x] = 'c'
                inventory.remove_item()

    def move(self):
        # if self.move_direction[0] == -1:
        #     self.hitbox.x -= self.speed
        #     self.collision('horizontal')
        # if self.move_direction[0] == 1:
        #     self.hitbox.x += self.speed
        #     self.collision('horizontal')
        multiplier = 1
        if self.move_direction[0] != 0 and self.move_direction[1] != 0:
            multiplier = 1.414

        self.hitbox.x += self.move_direction[0] * self.speed / multiplier
        self.collision('horizontal')
        self.hitbox.y += self.move_direction[1] * self.speed / multiplier
        self.collision('vertical')
       

        # if self.offset_x < 0:
        #     self.offset_x = 0
        # if self.offset_x > (config.MAP_WIDTH * config.TILE_WIDTH) - (config.SCREEN_WIDTH):
        #     self.offset_x = (config.MAP_WIDTH * config.TILE_WIDTH) - (config.SCREEN_WIDTH)
        # if self.offset_y < 0:
        #     self.offset_y = 0
        # if self.offset_y > (config.MAP_HEIGHT * config.TILE_WIDTH) - config.SCREEN_HEIGHT:
        #     self.offset_y = (config.MAP_HEIGHT * config.TILE_WIDTH) - config.SCREEN_HEIGHT

        self.rect.center = self.hitbox.center
        self.offset_x = self.rect.centerx - (config.SCREEN_WIDTH / 2)
        self.offset_y = self.rect.centery - (config.SCREEN_HEIGHT / 2)

        if self.offset_x < 0:
            self.offset_x = 0
        if self.offset_y < 0:
            self.offset_y = 0
        if self.offset_x > (config.MAP_WIDTH * config.TILE_WIDTH) - config.SCREEN_WIDTH:
            self.offset_x = (config.MAP_WIDTH * config.TILE_WIDTH) - config.SCREEN_WIDTH
        if self.offset_y > (config.MAP_WIDTH * config.TILE_WIDTH) - config.SCREEN_HEIGHT:
            self.offset_y = (config.MAP_WIDTH * config.TILE_WIDTH) - config.SCREEN_HEIGHT


       
       

        
