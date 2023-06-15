import pygame
import config
import map
import tiles
import items

class Player(pygame.sprite.Sprite):
    
    # Check if there are any unnecessary lines in here
    def __init__(self, x, y, width, height, screen, obstacle_sprites):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.offset_x = 0
        self.offset_y = 0

        self.speed = 3

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

        self.rect.x = self.x
        self.rect.y = self.y

        self.hitbox = self.rect.inflate(0, -20)

        self.screen = screen

        self.center_x = config.SCREEN_WIDTH / 2
        self.center_y = config.SCREEN_HEIGHT / 2

        self.outline = pygame.transform.scale(pygame.image.load('Textures/outline.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
        self.highlighted_tile_x = 0
        self.highlighted_tile_y = 0

        self.direction = 'none'
        self.facing = 'down'

        self.dig_animation_index = 0
        dig_0 = pygame.transform.scale(pygame.image.load('Textures/dig_states/dig_0.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
        dig_1 = pygame.transform.scale(pygame.image.load('Textures/dig_states/dig_1.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
        self.dig_frames = [dig_0, dig_1]

        self.obstacle_sprites = obstacle_sprites

    def get_offset_x(self):
        return self.offset_x
    def get_offset_y(self):
        return self.offset_y
    
    def highlight_tile(self, x_diff, y_diff):
        tile_x = int((self.x + self.width / 2 ) / config.TILE_WIDTH)
        tile_y = int((self.y + self.height / 2) / config.TILE_WIDTH)
        
        self.screen.blit(self.outline, ((tile_x + x_diff) * config.TILE_WIDTH - self.offset_x, (tile_y + y_diff) * config.TILE_WIDTH - self.offset_y))

    def update(self, selected_object):
        self.selected_object = selected_object
        # if self.selected_object == 'shovel':
        #     if self.facing == 'down':
        #         self.highlight_tile(0, 1)
        #     if self.facing == 'up':
        #         self.highlight_tile(0, -1)
        #     if self.facing == 'right':
        #         self.highlight_tile(1, 0)
        #     if self.facing == 'left':
        #         self.highlight_tile(-1, 0)
        if self.selected_object == items.shovel:
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
                        if self.direction == 'right':
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction == 'left':
                            self.hitbox.left = sprite.hitbox.right
                        self.direction = 'none'
                        return True
                for sprite in tiles.tile_collisions_group:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction == 'right':
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction == 'left':
                            self.hitbox.left = sprite.hitbox.right
                        self.direction = 'none'
                        return True
            elif direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction == 'up':
                            self.hitbox.top = sprite.hitbox.bottom
                        if self.direction == 'down':
                            self.hitbox.bottom = sprite.hitbox.top
                        self.direction = 'none'
                        return True
                for sprite in tiles.tile_collisions_group:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction == 'up':
                            self.hitbox.top = sprite.hitbox.bottom
                        if self.direction == 'down':
                            self.hitbox.bottom = sprite.hitbox.top
                        self.direction = 'none'
                        return True

            return False

    # Make a more condensed movement system that isn't a bunch of if statements
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_p] and self.selected_object == items.shovel:
            self.create_path()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 'left'
            self.facing = 'left'
            #self.hitbox = self.rect.inflate(-20, -20)
            self.animation(self.left_frames)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 'right'
            self.facing = 'right'
            #self.hitbox = self.rect.inflate(-20, -20)
            self.animation(self.right_frames)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = 'up'
            self.facing = 'up'
            #self.hitbox = self.rect.inflate(0, -20)
            self.animation(self.up_frames)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = 'down'
            self.facing = 'down'
            #self.hitbox = self.rect.inflate(0, -20)
            self.animation(self.down_frames)
        else:
            self.direction = 'none'

    # Animates by cycling through an array of frames
    def animation(self, frames):
        self.animation_index += 0.05
        if self.animation_index >= len(frames):
            self.animation_index = 0
        self.image = frames[int(self.animation_index)]

    # Maybe this could merge with the regular animation
    def dig_animation(self, x, y):
        self.dig_animation_index += 0.1
        if self.dig_animation_index > 1.5:
            self.dig_animation_index = 0
            map.overworld[y][x] = '1'
        else:
            self.screen.blit(self.dig_frames[int(self.dig_animation_index)], (x * config.TILE_WIDTH - self.offset_x, y * config.TILE_WIDTH - self.offset_y))
            #map.overworld[y][x] = self.frames[int(self.animation_index)]

    # Check if there are any repetitive parts in here
    def create_path(self):
        tile_x = int((self.x + self.width / 2) / config.TILE_WIDTH) + self.highlighted_tile_x
        tile_y = int((self.y + self.height / 2) / config.TILE_WIDTH) + self.highlighted_tile_y

        if tile_x >= 0 and tile_x < len(map.overworld[0]) - 1 and tile_y >= 0 and tile_y < len(map.overworld) - 1:

            if map.overworld[tile_y][tile_x] == '0':
                self.dig_animation(tile_x, tile_y)
                if self.facing == 'right': self.animation(self.shovel_right_frames)
                #map.overworld[tile_y][tile_x] = '1'

    def move(self):

        # Probably could be condensed -- ALSO THERE ARE STILL SOME COLLISION GLITCHES
        if self.direction == 'left':
            if self.offset_x >= 0 and self.rect.x <= self.center_x - self.width / 2:
                self.offset_x -= 3
                #self.x -= 3
            elif self.rect.x >= 0:
                self.hitbox.x -= 3
                #self.x -= 3

            self.collision('horizontal')

        if self.direction == 'right':
            if self.offset_x <= config.SCREEN_WIDTH and self.rect.x >= self.center_x - self.width / 2:
                self.offset_x += 3
                #self.x += 3
            elif self.rect.x + self.width <= config.SCREEN_WIDTH:
                self.hitbox.x += 3 
                #self.x += 3

            self.collision('horizontal')

        if self.direction == 'up':
            if self.offset_y >= 0 and self.rect.y <= self.center_y - self.height / 2: 
                self.offset_y -= 3
                #self.y -= 3
            elif self.rect.y >= 0:
                self.hitbox.y -= 3
                #self.y -= 3

            self.collision('vertical')

        if self.direction == 'down':
            if self.offset_y <= config.SCREEN_HEIGHT and self.rect.y >= self.center_y - self.height / 2:
                self.offset_y += 3
                #self.y += 3
            elif self.rect.y + self.height <= config.SCREEN_HEIGHT:
                self.hitbox.y += 3
                #self.y += 3

            self.collision('vertical')
        
        self.rect.center = self.hitbox.center
        self.x = self.rect.x + self.offset_x
        self.y = self.rect.y + self.offset_y
        

        
