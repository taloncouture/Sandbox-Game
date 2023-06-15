import pygame
import config
import tree
import map

# Put in the x and y width and height (0 is not included) and this goes from left to right and then top to bottom (like reading a book)
def crop(surface, num_x, num_y):
    images = []
    for y in range(num_y):
        for x in range(num_x):
            images.append(surface.subsurface(x * config.TILE_WIDTH, y * config.TILE_WIDTH, config.TILE_WIDTH, config.TILE_WIDTH))
    return images

    #return [surface.subsurface(0, 0, config.TILE_WIDTH, config.TILE_WIDTH), surface.subsurface(config.TILE_WIDTH, 0, config.TILE_WIDTH, config.TILE_WIDTH), surface.subsurface(0, config.TILE_WIDTH, config.TILE_WIDTH, config.TILE_WIDTH), surface.subsurface(config.TILE_WIDTH, config.TILE_WIDTH, config.TILE_WIDTH, config.TILE_WIDTH)]

path_center = pygame.transform.scale(pygame.image.load('Textures/path/path_center.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
path_corner = pygame.transform.scale(pygame.image.load('Textures/path/path_corners.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
path_corners = crop(path_corner, 2, 2)
path_one_sided_overall = pygame.transform.scale(pygame.image.load('Textures/path/path_one_sided.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
path_one_sided = crop(path_one_sided_overall, 2, 2)
path_two_sided_overall = pygame.transform.scale(pygame.image.load('Textures/path/path_two_sided.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH))
path_two_sided = crop(path_two_sided_overall, 2, 1)
path_three_sided_overall = pygame.transform.scale(pygame.image.load('Textures/path/path_three_sided.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 4))
path_three_sided = crop(path_three_sided_overall, 4, 4)
path_four_sided_overall = pygame.transform.scale(pygame.image.load('Textures/path/path_four_sided.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 4))
path_four_sided = crop(path_four_sided_overall, 4, 4)

water_center = pygame.transform.scale(pygame.image.load('Textures/water/water_center.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
water_corner = pygame.transform.scale(pygame.image.load('Textures/water/water_corners.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
water_corners = crop(water_corner, 2, 2)
water_one_sided_overall = pygame.transform.scale(pygame.image.load('Textures/water/water_one_sided.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
water_one_sided = crop(water_one_sided_overall, 2, 2)
water_two_sided_overall = pygame.transform.scale(pygame.image.load('Textures/water/water_two_sided.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH))
water_two_sided = crop(water_two_sided_overall, 2, 1)
water_three_sided_overall = pygame.transform.scale(pygame.image.load('Textures/water/water_three_sided.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 4))
water_three_sided = crop(water_three_sided_overall, 4, 4)
water_four_sided_overall = pygame.transform.scale(pygame.image.load('Textures/water/water_four_sided.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 4))
water_four_sided = crop(water_four_sided_overall, 4, 4)

farmland_center = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_center.png'), (config.TILE_WIDTH, config.TILE_WIDTH))
farmland_corner = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_corners.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
farmland_corner_solid = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_corners_solid.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
farmland_corners = crop(farmland_corner, 2, 2)
farmland_corners_solid = crop(farmland_corner_solid, 2, 2)
farmland_one_sided_overall = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_one_sided.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH * 2))
farmland_one_sided = crop(farmland_one_sided_overall, 2, 2)
farmland_two_sided_overall = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_two_sided.png'), (config.TILE_WIDTH * 2, config.TILE_WIDTH))
farmland_two_sided = crop(farmland_two_sided_overall, 2, 1)
farmland_three_sided_overall = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_three_sided_2.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 4))
farmland_three_sided = crop(farmland_three_sided_overall, 4, 4)
farmland_four_sided_overall = pygame.transform.scale(pygame.image.load('Textures/farmland/farmland_four_sided.png'), (config.TILE_WIDTH * 4, config.TILE_WIDTH * 4))
farmland_four_sided = crop(farmland_four_sided_overall, 4, 4)


path_images = [path_center, path_corners, path_corners, path_one_sided, path_two_sided, path_three_sided, path_four_sided]
water_images = [water_center, water_corners, water_corners, water_one_sided, water_two_sided, water_three_sided, water_four_sided]
farmland_images = [farmland_center, farmland_corners, farmland_corners_solid, farmland_one_sided, farmland_two_sided, farmland_three_sided, farmland_four_sided]

# Handles all the collisions with tiles that need it by making hitboxes -- maybe too many arguments here
class Tile_Collisions(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, surface, x_offset, y_offset):
        super().__init__()
        self.x = x * config.TILE_WIDTH
        self.y = y * config.TILE_WIDTH
        self.width = width
        self.height = height

        self.hitbox = pygame.Rect(self.x - x_offset + (self.width / 3), self.y - y_offset, self.width / 2, self.height / 2)

tile_collisions_group = pygame.sprite.Group()

# Creates objects like trees by scanning through the overworld map -- arguments could be improved and also change the map so that it could be a variable
def create_objects(obstacle_sprites, visible_sprites):
    for y in range(len(map.overworld)):
        for x in range(len(map.overworld[y])):
            if map.overworld[y][x] == 't':
                tree_object = tree.Tree(x, y, config.TILE_WIDTH, config.TILE_WIDTH * 2)
                obstacle_sprites.add(tree_object)
                visible_sprites.add(tree_object)

# This gets the tile id and returns the tile image which is drawn in main.py
def TileID(id, x, y, area, surface, x_offset, y_offset, obstacle_sprites):
    if id == '0': return grass
    if id == '1': return create_path(id, x, y, area, path_images)
    if id == 'w': 
        water_collisions = Tile_Collisions(x, y, config.TILE_WIDTH, config.TILE_WIDTH, surface, x_offset, y_offset)
        tile_collisions_group.add(water_collisions)
        return create_path(id, x, y, area, water_images)
    if id == 't':
        # tree_object = tree.Tree(x, y, config.TILE_WIDTH, config.TILE_WIDTH * 2)
        # obstacle_sprites.add(tree_object)
        return grass
    if id == 'f':
        return create_path(id, x, y, area, farmland_images)

# This checks if there are any tiles next to it so that it can change the texture of the tile for design purposed
def create_path(id, x, y, area, images):
    path_matrix = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]

    corners = [
        [0, 0],
        [0, 0]
    ]

    if area[y][x - 1] == id:
        path_matrix[1][0] = 1
    if area[y][x + 1] == id:
        path_matrix[1][2] = 1
    if area[y - 1][x] == id:
        path_matrix[0][1] = 1
    if area[y + 1][x] == id:
        path_matrix[2][1] = 1

    if area[y - 1][x - 1] == id:
        corners[0][0] = 1
    if area[y - 1][x + 1] == id:
        corners[0][1] = 1
    if area[y + 1][x - 1] == id:
        corners[1][0] = 1
    if area[y + 1][x + 1] == id:
        corners[1][1] = 1

    if path_matrix == [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]:
        return images[3][2]
    
    if path_matrix == [
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]:
        return images[3][3]
    
    if path_matrix == [
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]:
        return images[3][0]
    
    if path_matrix == [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]:
        return images[3][1]

    if path_matrix == [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]:
        if corners[1][0] == 1:
            return images[2][1]
        else:
            return images[1][1]
    
    if path_matrix == [
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 0]
    ]:
        if corners[1][1] == 1:
            return images[2][0]
        else:
            return images[1][0]
    
    if path_matrix == [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]:
        if corners[0][0] == 1:
            return images[2][3]
        else:
            return images[1][3]
    
    if path_matrix == [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]:
        if corners[0][1] == 1:
            return images[2][2]
        else:
            return images[1][2]
    
    if path_matrix == [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]:
        return images[4][1]
    
    if path_matrix == [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]:
        return images[4][0]
    
    if path_matrix == [
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 0]
    ]:
        if corners[0][1] == 0 and corners[1][1] == 0:
            return images[5][2]
        elif corners[0][1] == 0:
            return images[5][0]
        elif corners[1][1] == 0:
            return images[5][1]
        else:
            return images[5][3]
    
    if path_matrix == [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]:
        if corners[0][0] == 0 and corners[0][1] == 0:
            return images[5][10]
        elif corners[0][0] == 0:
            return images[5][8]
        elif corners[0][1] == 0:
            return images[5][9]
        else:
            return images[5][11]
    
    if path_matrix == [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]:
        if corners[0][0] == 0 and corners[1][0] == 0:
            return images[5][6]
        elif corners[0][0] == 0:
            return images[5][4]
        elif corners[1][0] == 0:
            return images[5][5]
        else:
            return images[5][7]
    
    if path_matrix == [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]:
        if corners[1][0] == 0 and corners[1][1] == 0:
            return images[5][14]
        elif corners[1][0] == 0:
            return images[5][12]
        elif corners[1][1] == 0:
            return images[5][13]
        else:
            return images[5][15]
    
    if path_matrix == [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]:
        if corners[0][0] == 1 and corners[0][1] == 1 and corners[1][0] == 1 and corners[1][1] == 1:
            return images[6][10]
        elif corners[0][0] == 0 and corners[0][1] == 0 and corners[1][0] == 0 and corners[1][1] == 0:
            return images[6][11]
        elif corners[0][0] == 0 and corners[1][1] == 0 and corners[1][0] == 1 and corners[0][1] == 1:
            return images[6][8]
        elif corners[0][1] == 0 and corners[1][0] == 0 and corners[0][0] == 1 and corners[1][1] == 1:
            return images[6][9]
        elif corners[0][0] == 0 and corners[1][0] == 0 and corners[0][1] == 1 and corners[1][1] == 1:
            return images[6][12]
        elif corners[0][0] == 0 and corners[0][1] == 0 and corners[1][0] == 1 and corners[1][1] == 1:
            return images[6][13]
        elif corners[0][1] == 0 and corners[1][1] == 0 and corners[1][0] == 1 and corners[0][0] == 1:
            return images[6][15]
        elif corners[1][0] == 0 and corners[1][1] == 0 and corners[0][0] == 1 and corners[0][1] == 1:
            return images[6][14]
        
        elif corners[0][1] == 0 and corners[1][0] == 0 and corners[1][1] == 0:
            return images[6][4]
        elif corners[0][0] == 0 and corners[1][0] == 0 and corners[1][1] == 0:
            return images[6][5]
        elif corners[0][0] == 0 and corners[0][1] == 0 and corners[1][1] == 0:
            return images[6][6]
        elif corners[0][0] == 0 and corners[0][1] == 0 and corners[1][0] == 0:
            return images[6][7]
        elif corners[0][0] == 0:
            return images[6][0]
        elif corners[0][1] == 0:
            return images[6][1]
        elif corners[1][0] == 0:
            return images[6][2]
        elif corners[1][1] == 0:
            return images[6][3]

    return images[0]




grass = pygame.transform.scale(pygame.image.load('Textures/grass.png'), (config.TILE_WIDTH, config.TILE_WIDTH))