import pygame
import config

overworld_chunks = [
    ['a1', 'a2', 'a3'],
    ['b1', 'b2', 'b3'],
    ['c1', 'c2', 'c3']
]

overworld = [['0' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]
overworld_layer_1 = [[' ' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]


overworld_2 = [['0' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]
overworld2_layer_1 = [[' ' for x in range(config.MAP_WIDTH)] for y in range(config.MAP_HEIGHT)]

overworld2_layer_1[10][10] = 'p'
overworld_2[4][4] = 'f'

overworld2_layers = [overworld_2, overworld2_layer_1, False]


for x in range(len(overworld_layer_1[0])):
    overworld_layer_1[0][x] = 'h'
    overworld_layer_1[len(overworld_layer_1[0]) - 1][x] = 'h'
for y in range(len(overworld_layer_1)):
    overworld_layer_1[y][0] = 'h'
    overworld_layer_1[y][len(overworld_layer_1) - 1] = 'h'

for x in range(len(overworld2_layer_1[0])):
    overworld2_layer_1[0][x] = 'h'
    overworld2_layer_1[len(overworld2_layer_1[0]) - 1][x] = 'h'
for y in range(len(overworld_layer_1)):
    overworld2_layer_1[y][0] = 'h'
    overworld2_layer_1[y][len(overworld2_layer_1) - 1] = 'h'

overworld_layer_1[3][2] = 'p'
overworld_layer_1[0][5] = 'H'
overworld2_layer_1[99][5] = 'H'

overworld_layers = [overworld, overworld_layer_1, False]

def get_level(level):
    if level == 'overworld':
        return overworld_layers
    
current_area = overworld_layers