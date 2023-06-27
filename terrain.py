import random


def create_terrain(width, height, n):
    WIDTH = width
    HEIGHT = height

    countdown = n

    current_x = int(WIDTH / 2)
    current_y = int(HEIGHT / 2)

    map = [['#' for x in range(WIDTH)] for y in range(HEIGHT)]

    map[current_y][current_x] = ' '

    while countdown >= 0:
        
        direction = random.randint(1, 4)

        if direction == 1 and current_y > 0:
            current_y -= 1
        if direction == 2 and current_y < HEIGHT - 1:
            current_y += 1
        if direction == 3 and current_x > 0:
            current_x -= 1
        if direction == 4 and current_x < WIDTH - 1:
            current_x += 1
        
        map[current_y][current_x] = ' '
        
        countdown -= 1

    return map
   