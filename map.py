import pygame
import config
import terrain

overworld_chunks = [
    ['a1', 'a2', 'a3'],
    ['b1', 'b2', 'b3'],
    ['c1', 'c2', 'c3']
]

overworld = [['0' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]
overworld_layer_1 = [[' ' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]


overworld_2 = [['0' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]
overworld2_layer_1 = [[' ' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]

underground = [['+' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]

overworld2_layer_1[10][10] = 'p'
overworld_2[4][4] = 'f'

overworld2_layers = [overworld_2, overworld2_layer_1, False]

def create_boundary(area, id):
    new_area = area
    
    for x in range(len(area[0])):
        new_area[0][x] = id
        new_area[len(area[0]) - 1][x] = id
    for y in range(len(area)):
        new_area[y][0] = id
        new_area[y][len(area) - 1] = id

    return new_area

overworld_layer_1 = create_boundary(overworld_layer_1, 'h')
overworld2_layer_1 = create_boundary(overworld2_layer_1, 'h')


overworld_layer_1[3][2] = 'p'
overworld_layer_1[0][5] = 'H'
overworld_layer_1[5][5] = 's'
overworld2_layer_1[99][5] = 'H'

overworld_layers = [overworld, overworld_layer_1, False]

def generate_underground_layer():
    return terrain.create_terrain(config.MAP_WIDTH, config.MAP_HEIGHT, 10000)

underground_1 = generate_underground_layer()
underground_1 = create_boundary(underground_1, '#')

# for y in range(len(underground_1)):
#     row = ''
#     for x in range(len(underground_1[y])):
#         row += underground_1[y][x]

#     print(row)
underground_1[50][50] = 'p'
underground_layers = [underground, underground_1, True]

def get_level(level):
    if level == 'overworld':
        return overworld_layers
    
current_area = overworld_layers