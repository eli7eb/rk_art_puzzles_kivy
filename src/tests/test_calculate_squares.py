import sys
import os, os.path
import random

import pygame

from pathlib import Path
from pygame.math import Vector2

from pygame.locals import *
import math
from PIL import Image

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
# spacer between tiles
SCREEN_SPACER_SIZE = 2
# frame around the display edges
OUTER_BORDER_SIZE = 20
# space between grid dashboard and grid scroller
INNER_BORDER_SIZE = 4
levels = {
  "beginner" : {
    "width" : 440,
    "height" : 660,
    "num_tiles": 24
  },
  "intermid" : {
    "width" : 450,
    "height" : 630,
    "num_tiles": 35
  },
   "inter_1": {
     "width": 420,
     "height": 630,
     "num_tiles": 63
   },
   "inter_2": {
      "width": 450,
      "height": 630,
      "num_tiles": 35
   },
    "master" : {
    "width" : 450,
    "height" : 650,
    "num_tiles": 117
  }
}
level = levels['intermid']
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('test transparent')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False

def show_image(im):
    gameDisplay.blit(im, (OUTER_BORDER_SIZE/2, OUTER_BORDER_SIZE/2))

# resize based on level
# width needs to accomodate the scroller
# height needs to accomodate the dashboard
# validate that the size is divided by tile_size
def image_resize(im):
    grid_size_percent = 85
    original_width = SCREEN_WIDTH - OUTER_BORDER_SIZE * 2 + INNER_BORDER_SIZE
    original_height = SCREEN_HEIGHT - OUTER_BORDER_SIZE * 2 + INNER_BORDER_SIZE
    # make the grid 80%


    im_width = level['width'] #  int(original_width * (grid_size_percent / 100))
    im_height = level['height'] # int(original_height * (grid_size_percent / 100))
    im = im.resize((im_width, im_height), Image.LANCZOS)
    return im

# the squares need to be exactly the size to fit in the array
# we need to decide which comes first the image size or the tiles size
# on a beginner level I have 4 - 6
# then 5 - 7
# then 7 - 9
def fit_squares(im, num_tiles):
    print('fit_squares')
    width = im.width
    height = im.height

    px = math.ceil(math.sqrt(num_tiles * width / height))
    if math.floor(px * height / width) * px < num_tiles:
        sx = height / math.ceil(px * height / width)
    else:
        sx = width / px
    py = math.ceil(math.sqrt(num_tiles * height / width))
    if math.floor(py * width / height) * py < num_tiles:
        sy = width / math.ceil((width * py / height))
    else:
        sy = height / py
    # TODO get the number of cols and rows by deviding the width/size and height/size
    # return all as tuple
    size = int(max(sx, sy))
    num_cols = int(width / size)
    num_rows = int(height / size)
    return size, num_cols, num_rows


def show_image_resize(x,y):
    desired_size = 468

    # img = Image.open("milkmaid.png")
    im = getLoadedImage()
    old_size = im.size  # old_size[0] is in (width, height) format
    # I    have    the    final    image: 2    considerations:
    # need to resize and keep aspect ratio - i have a maximum of size I can use
    # the width is setting the size of the resizing
    # the height sets the number and size of each tile
    # need to resize so that tile size is going to fit
    wpercent = (im.width / float(im.size[0]))
    mywidth = 468
    hsize = int((float(im.size[1]) * float(wpercent)))
    img = im.resize((mywidth, hsize), Image.ANTIALIAS)
    img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
    grid_image = im.resize((int(im.width), hsize), Image.LANCZOS)
    mode = grid_image.mode
    size = grid_image.size
    data = grid_image.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    # use thumbnail() or resize() method to resize the input image

    # thumbnail is a in-place operation

    # im.thumbnail(new_size, Image.ANTIALIAS)

    im = im.resize(new_size, Image.ANTIALIAS)

    # create a new image and paste the resized on it

    new_im = Image.new("RGB", (desired_size, desired_size))
    new_im.paste(im, ((desired_size - new_size[0]) // 2,
                      (desired_size - new_size[1]) // 2))
    mode = new_im.mode
    size = new_im.size
    data = new_im.tobytes()
    py_image = pygame.image.fromstring(data, size, mode)
    gameDisplay.blit(py_image, (0, 0))
    #new_im.show()
# first convert pygame image to PIL
# then change alpha
# then display
def show_image_transparant(x, y):
    img = getLoadedImage()
    img = img.convert('RGBA')
    img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
    data = img.getdata()  # you'll get a list of tuples
    newData = []
    for a in data:
        a = a[:3]  # you'll get your tuple shorten to RGB
        a = a + (100,)  # change the 100 to any transparency number you like between (0,255)
        newData.append(a)
    img.putdata(newData)  # you'll get your new img ready
    img.save("bg_trans.png")
    mode = img.mode
    size = img.size
    data = img.tobytes()
    py_image = pygame.image.fromstring(data, size, mode)
    gameDisplay.blit(py_image, (x, y))

def getXYCoordinatesFromBox(box, tile_size):
    #print("box {}".format(box))
    x = box[0] + tile_size / 2
    y = box[1] + tile_size / 2
    x_index = int(x / tile_size)
    y_index = int(y / tile_size)
    return y_index,x_index

def validate_crop_size(image):
    w = abs(image.width - tile_size)
    h = abs(image.height - tile_size)
    if w > 5 or h > 5:
        return False
    return True


def crop_image_to_array():
    # TODO 4 tiles across depends on level
    # build matrix for tiles
    width = int(im.width)
    height = int(im.height)
    chopsize = tile_tuple[0]

    tile_matrix = [[1] * num_cols for n in range(num_rows)]
    #tile_matrix = [[1] * w_index for n in range(h_index)]
    counter = 0

    for x0 in range(0, width, chopsize):
        for y0 in range(0, height, chopsize):
            box = (x0, y0,
                   x0 + chopsize if x0 + chopsize < width else width - 1,
                   y0 + chopsize if y0 + chopsize < height else height - 1)
            print('box {}'.format(box))

            cropped = im.crop(box)
            if validate_crop_size(cropped):
                mode = cropped.mode
                size = cropped.size
                data = cropped.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)

                # position is set in game view when the tile is displayed
                counter += 1
                coords = getXYCoordinatesFromBox(box, chopsize)
                print("coords {}".format(str(coords)))

                tile_matrix[coords[0]][coords[1]] = py_image
                # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))
            else:
                print ('error on crop')

    return tile_matrix

# from counter calculate the x y position
#
def get_xy_from_counter(tiles_grid,counter):
    # divide counter by size to get the col and row
    row = 0
    col = 0

    rows = len(tiles_grid)
    cols = len(tiles_grid[0])
    total = rows*cols

    row,col = divmod(counter,cols)

    return row*tile_tuple[0]+OUTER_BORDER_SIZE/2,col*tile_tuple[0]+OUTER_BORDER_SIZE/2


def generate_random_color():
    start = 0
    stop = 255

    red = random.randint(start, stop)
    green = random.randint(start, stop)
    blue = random.randint(start, stop)
    return pygame.Color(red, green, blue)

def draw_border():
    print('draw_border')
    top_x = 0
    top_y = 0
    btm_x = SCREEN_WIDTH
    btm_y = SCREEN_HEIGHT
    border_color = generate_random_color()
    rect = pygame.Rect(top_x, top_y, btm_x, btm_y)
    # self.logger.info("y {} x {} ".format(str(y_pos),str(x_pos)))
    pygame.draw.rect(gameDisplay, border_color, rect, OUTER_BORDER_SIZE)

# draw grid of rects for the tiles to display
# calculate like
def draw_grid_of_rects():
    print('draw_grid_of_rects')
    width = im.width
    height = im.height

    grid_color = generate_random_color()
    # self.logger.info("draw_grid width {} height {}".format(str(width),str(height)))

    for y in range(num_rows):
        for x in range(num_cols):
            row_spacer = OUTER_BORDER_SIZE/2 + SCREEN_SPACER_SIZE * y
            col_spacer = OUTER_BORDER_SIZE/2 + SCREEN_SPACER_SIZE * x
            # print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))

            x_pos = int(x * tile_size + col_spacer)
            y_pos = int(y * tile_size + row_spacer)
            print('x_pos {} y_pos {}'.format(str(x_pos), str(y_pos)))
            locations_matrix[y][x] = (x_pos,y_pos)
            rect = pygame.Rect(x_pos, y_pos, tile_size, tile_size)
            # self.logger.info("y {} x {} ".format(str(y_pos),str(x_pos)))
            pygame.draw.rect(gameDisplay, grid_color, rect, SCREEN_SPACER_SIZE)
    print('end')

def display_tiles(tiles_grid):
    # check for grid tiles
    counter = 0

    counter_col = 0
    counter_row = 0
    # row is y col is x
    x = 0
    y = 0

    x_counter = 0
    y_counter = 0
    print('display_tile')
    for row in tiles_grid:
        for col in row:
            # row_index is screen spacer and tile size times row
            #print('counter {} coords[0] {} coords[1] {}'.format(str(counter), str(col.coords[0]),
            #                                                 str(col.coords[1])))

            #print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))

            loc_tuple = locations_matrix[x_counter][y_counter]

            y = int(loc_tuple[0])
            x = int(loc_tuple[1])
            # # TODO set the Tile object state
            # tile.y = y
            # tile.state = TILE_ON_BOARD_TEST
            print('y {} x {}'.format(str(y), str(x)))
            py_image = col
            gameDisplay.blit(py_image, (y, x))
            # self.tiles_grid[col.y_index][col.x_index] = tile
            y_counter += 1
            if y_counter > num_cols-1:
                y_counter = 0
        x_counter += 1

def getLoadedImage():
    im_pth = "milkmaid.png"
    base_path = Path(__file__).parent.resolve()
    file_path = (base_path / im_pth).resolve()

    # show_image()
    # img = Image.open("milkmaid.png")
    im = Image.open(file_path)
    return im

# return the tile where the mouse is on
def return_tile_at_pos(x_pos,y_pos):
    print ('return_tile_at_pos')
    x_counter = 0
    y_counter = 0
    found = False
    print('display_tile')
    for row in matrix:
        for col in row:
            # row_index is screen spacer and tile size times row
            # print('counter {} coords[0] {} coords[1] {}'.format(str(counter), str(col.coords[0]),
            #                                                 str(col.coords[1])))

            # print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))

            loc_tuple = locations_matrix[x_counter][y_counter]

            x = int(loc_tuple[0])
            y = int(loc_tuple[1])
            # # TODO set the Tile object state
            # tile.y = y
            # tile.state = TILE_ON_BOARD_TEST
            print('event pos x {} y {} tile pos y {} x {}'.format(str(mouse_x),str(mouse_y),str(y), str(x)))
            if mouse_x > x and mouse_x < x+tile_size and mouse_y > y and mouse_y < y + tile_size:
                found = True
                return col
            else:
                y_counter += 1
                if y_counter > num_cols - 1:
                    y_counter = 0
        x_counter += 1
    print ("I shoule never get here and there must be a better way to do that !!")

def init_graphics():
    draw_border()
    draw_grid_of_rects()

def redraw_graphics():
    gameDisplay.fill(white)
    init_graphics()

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('test transparent')
gameDisplay.fill(white)

im = getLoadedImage()
num_tiles = level['num_tiles']
im = image_resize(im)
tile_tuple = fit_squares(im, num_tiles)
#size,num_cols,num_rows
# crop to tiles and show
tile_size = tile_tuple[0]
num_cols = tile_tuple[1]
num_rows = tile_tuple[2]
locations_matrix = [[1] * num_cols for n in range(num_rows)]
init_graphics()
matrix = crop_image_to_array()
display_tiles(matrix)
clock = pygame.time.Clock()
running = True
mouse_pressed = False
selected_tile = None
while running:

    for event in pygame.event.get():
        print ('event type {}'.format(str(event.type)))
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_tile = return_tile_at_pos(mouse_x, mouse_y)
                print('mouse MOUSEBUTTONDOWN ' + str(selected_tile))
                mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected_tile = None
                mouse_pressed = False
                print('mouse MOUSEBUTTONUP ' + str(selected_tile))
        elif event.type == pygame.MOUSEMOTION and mouse_pressed:
            print('pygame.MOUSEMOTION ' + str(selected_tile))
            if selected_tile:
                print ('mouse motion ' + str(event.rel))
                delta_x = event.rel[0]
                delta_y = event.rel[1]
                pos_x = event.pos[0]
                pos_y = event.pos[1]
                redraw_graphics()
                display_tiles(matrix)
                gameDisplay.blit(selected_tile, (pos_x, pos_y))
                pygame.display.flip()
    clock.tick(30)
    pygame.display.flip()

pygame.quit()
sys.exit()
