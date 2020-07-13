import pygame
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2
TEXT_COLOR = pygame.Color(255, 255, 255)
SCREEN_SPACER_SIZE = 5
# how many spacers vertical and horizontal
SCREEN_SPACER_NUMBER_VER = 3
SCREEN_SPACER_NUMBER_HOR = 2


class GameUtils:

    def __init__(self):
        self.done = False
        self.image = None

    # tile needs to fit in the screen 5 times in the horizontal directions with overheads
    # at least 5 tiles across: 4 grid and one to drag
    def calculateTileSize(self):
        self.tile_size = (SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE) / 5
        print("tile size " + str(self.tile_size))
        return self.tile_size

    def calculateGridSize(self):
        self.grid_width = SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE - self.tile_size
        self.grid_height = SCREEN_HEIGHT - SCREEN_SPACER_NUMBER_VER * SCREEN_SPACER_SIZE
        return (self.grid_width,self.grid_height)

    # crop function
    # Set the cropping area with box=(left, upper, right, lower).
    # an_array = [[1, 2], [3, 4]]
    # rows = len(an_array) Find row and column length.
    # columns = len(an_array[0])
    # total_length = rows * columns. Compute total length.
    # print(total_length)
    def crop_image_to_array(self,image):
        self.image = image

        # TODO 4 tiles across depends on level
        w = 4
        # floor division
        h = int(SCREEN_HEIGHT // self.tile_size)

        tile_matrix = [[0 for x in range(w)] for y in range(h)]
        print('array rows %s cols %s', str(len(tile_matrix)), str(len(tile_matrix[0])))
        for i in range(len(tile_matrix)):
            for j in range(len(tile_matrix[i])):
                print('i %s j %s', str(i), str(j))
                top = SCREEN_SPACER_SIZE + i*self.tile_size
                upper = SCREEN_SPACER_SIZE + j*self.tile_size
                right = SCREEN_SPACER_SIZE + i * self.tile_size + self.tile_size
                lower = SCREEN_SPACER_SIZE + j * self.tile_size + self.tile_size
                print('i %s j %s top % upper % right % lower %', str(i), str(j), str(top), str(upper), str(right),
                      str(lower))
                cropped = self.image.crop((top, upper, right, lower))
                # TODO generate tile class image, x,y, state : found, in pos
                tile_matrix[i][j] = cropped

        return tile_matrix

