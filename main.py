import pygame
import numpy as np
from noise import pnoise2
import time
import random

pygame.init()
largura = 1800
altura = 1000
window = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Seed Generator")
background_color = (10, 10, 10)
window.fill(background_color)

white = (255, 255, 255)
black = (0, 0, 0)

grid_columns = (1800, 1000)
pixel_size = (5, 5)

pixels_info = []

terrain_noise_map = None
temperature_noise_map = None
humidity_noise_map = None

seed = 275692 #334806
seed_terrain = 0
seed_temperature = 0
seed_humidity = 0

def make_grid():
    starter_point = ((largura - (grid_columns[0] * pixel_size[0])) / 2, (altura - (grid_columns[1] * pixel_size[1])) / 2)
    
    for x in range(0, grid_columns[0]):
        for y in range(0, grid_columns[1]):
            pixels_info.append({"Cords": (starter_point[0] + (pixel_size[1] * x), starter_point[1] + (pixel_size[0] * y)), "Color": white})
            
make_grid()
        
def update_grid():
    starter_point = ((largura - (grid_columns[0] * pixel_size[0])) / 2, (altura - (grid_columns[1] * pixel_size[1])) / 2)
    
    for pixel in pixels_info:
        pygame.draw.rect(window, pixel["Color"], (pixel["Cords"][0], pixel["Cords"][1], pixel_size[0], pixel_size[1]))
        
    '''for x in range(grid_columns[0] + 1):
        pygame.draw.line(window, black, (starter_point[0] + (pixel_size[0] * x), starter_point[1]), (starter_point[0] + (pixel_size[0] * x), starter_point[1] + (grid_columns[1] * pixel_size[1])))
    for y in range(grid_columns[1] + 1):
        pygame.draw.line(window, black, (starter_point[0], starter_point[1] + (pixel_size[1] * y)), (starter_point[0] + (grid_columns[0] * pixel_size[0]), starter_point[1]  + (pixel_size[1] * y)))'''
        
def treat_seed():
    global seed_terrain, seed_temperature, seed_humidity
    
    np.random.seed(seed)
    
    seed_terrain = int(np.random.uniform(0, 999999))
    seed_temperature = int(np.random.uniform(0, 999999))
    seed_humidity = int(np.random.uniform(0, 999999))
        
def generate_terrain_perlin_noise_map():
    global terrain_noise_map
    
    np.random.seed(seed_terrain)
    
    # Frequency and scale
    frequency = np.random.uniform(0.5, 0.75)  # Modifica a frequência com base na seed
    scale = np.random.uniform(50, 70) * frequency # Modifica a escala com base na seed
    octaves = 4  # controls the number of detail layers
    persistence = 0.5  # controls the smoothness between layers
    lacunarity = 2.5  # controls the gap between layers
    x_offset = np.random.uniform(0, 1000)
    y_offset = np.random.uniform(0, 1000)
    
    frequency2 = np.random.uniform(0.01, 0.1)  # Modifica a frequência com base na seed
    scale2 = np.random.uniform(35, 65) # Modifica a escala com base na seed
    octaves2 = 2  # controls the number of detail layers
    persistence2 = np.random.uniform(0.01, 0.8)  # controls the smoothness between layers
    lacunarity2 = np.random.uniform(0.01, 0.8)  # controls the gap between layers
    x_offset2 = np.random.uniform(0, 1000)
    y_offset2 = np.random.uniform(0, 1000)

    terrain_noise_layer1 = np.zeros((grid_columns[0], grid_columns[1]))
    terrain_noise_layer2 = np.zeros((grid_columns[0], grid_columns[1]))

    for y in range(grid_columns[1]):
        for x in range(grid_columns[0]):
            terrain_noise_layer1[x, y] = pnoise2((x  + x_offset) / scale, (y + y_offset) / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            terrain_noise_layer2[x, y] = pnoise2((x + x_offset2) / scale2, (y + y_offset2) / scale2, octaves=octaves2, persistence=persistence2, lacunarity=lacunarity2)
    
    for collumn in range(0, len(terrain_noise_layer2)):
        for element in terrain_noise_layer2[collumn]:
            if element > 0.5:
                element = 0
            else:
                element = 1- element
    
    terrain_noise_map = terrain_noise_layer1 + terrain_noise_layer2
    
    terrain_noise_map = (terrain_noise_map - np.min(terrain_noise_map)) / (np.max(terrain_noise_map) - np.min(terrain_noise_map))
    
    print("1:", frequency, scale, octaves, persistence, lacunarity, x_offset, y_offset, "2:", frequency2, scale2, octaves2, persistence2, lacunarity2, x_offset2, y_offset2)
    
def generate_temperature_perlin_noise():
    global temperature_noise_map
    
    np.random.seed(seed_temperature)
    
    # Frequency and scale
    #frequency = np.random.uniform(0.04, 0.06)  # frequência do noise
    scale = np.random.uniform(30, 50)  # escala do noise
    octaves = 2
    persistence = np.random.uniform(0.01, 0.2)
    lacunarity = np.random.uniform(0.01, 0.2)

    temperature_noise_map = np.zeros((grid_columns[0], grid_columns[1]))

    for y in range(grid_columns[1]):
        for x in range(grid_columns[0]):
            noise_val = pnoise2(x / scale, y / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            temperature_noise_map[x, y] = noise_val

    temperature_noise_map = (temperature_noise_map - np.min(temperature_noise_map)) / (np.max(temperature_noise_map) - np.min(temperature_noise_map))

def create_terrain(): 
    generate_terrain_perlin_noise_map()
    generate_temperature_perlin_noise()
    
    for collumn in range(0, grid_columns[0]):
        for element in range(0, grid_columns[1]):
            element_terrain_value = terrain_noise_map[collumn][element]
            element_temperature_value = temperature_noise_map[collumn][element]
            if 1 - element_terrain_value < 0.5:
                if element_temperature_value < 0.1:
                    pixels_info[collumn * grid_columns[1] + element]["Color"] = (180, 200, 240)
                else:
                    pixels_info[collumn * grid_columns[1] + element]["Color"] = (80 * (1 - element_terrain_value), 150 * (1 - element_terrain_value), 240 * (1 - element_terrain_value))
            elif 1 - element_terrain_value >= 0.5 and 1 - element_terrain_value < 0.525:
                pixels_info[collumn * grid_columns[1] + element]["Color"] = (105 * ((1 - element_terrain_value) * 1.5), 255 * ((1 - element_terrain_value) * 1.5), 95 * ((1 - element_terrain_value) * 1.5))
            elif 1 - element_terrain_value > 0.80:
                pixels_info[collumn * grid_columns[1] + element]["Color"] = (205 * (1 - element_terrain_value), 210 * (1 - element_terrain_value), 200 * (1 - element_terrain_value))
            else:
                pixels_info[collumn * grid_columns[1] + element]["Color"] = (0, 255 * (1 - element_terrain_value), 0)

treat_seed()                
create_terrain()
update_grid()
now_time = time.time()
window_open = True
while window_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
            
    pygame.display.flip()  
    if time.time() - now_time >= 1:
        now_time = time.time()
        seed = random.randint(0, 999999)
        print(seed)
        treat_seed()
        create_terrain()
        update_grid()
        