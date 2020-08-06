import pygame
import math
from PIL import Image

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('test transparent')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False

def show_image(x, y):
    im = pygame.transform.scale(pygame.image.load("rk_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    gameDisplay.blit(im, (x, y))

def fit_squares(im, num_tiles):
    print()

    n = num_tiles

    im = im.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
    width = im.width
    height = im.height
    px = math.ceil(math.sqrt(n*width/height))
    if math.floor(px*height/width)*px < n:
        sx = height/math.ceil(px*height/width)
    else:
        sx = width/px
    py = math.ceil(math.sqrt(n*height/width))
    if math.floor(py * width / height) * py < n:
        sy = width / math.ceil((width*py/height))
    else:
        sy = height/py
    # TODO get the number of cols and rows by deviding the width/size and height/size
    # return all as tuple
    size = max(sx,sy)
    num_cols = int(width/size)
    num_rows = int(height/size)
    return math.max(sx,sy)

def show_image_resize(x,y):
    desired_size = 468
    im_pth = "rk_background.png"
    # img = Image.open("rk_background.png")
    im = Image.open(im_pth)
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
    img = Image.open("rk_background.png")
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
    print("box {}".format(box))
    # find the middle point
    x = box[0] + tile_size/2
    y = box[1] + tile_size/2
    x_index = int(x/tile_size)
    y_index = int(y/tile_size)
    return y_index, x_index

def crop_image_to_array(self, image,tiles_hor,tiles_ver):
    self.image = image

    # TODO 4 tiles across depends on level
    w = tiles_hor
    # floor division
    h = tiles_ver
    int(SCREEN_HEIGHT // self.tile_size)
    # build matrix for tiles
    width = int(self.image.width)
    height = int(self.image.height)
    chopsize = int(self.tile_size)

    w_index = int(math.ceil(width/chopsize))
    h_index = int(math.ceil(height/chopsize))
    tile_matrix = [[1] * w_index for n in range(h_index)]
    w_counter = 0
    h_counter = 0
    counter = 0
    infile = 'in.jpg'
    for x0 in range(0, width, chopsize):
        for y0 in range(0, height, chopsize):
            box = (x0, y0,
                   x0 + chopsize if x0 + chopsize < width else width - 1,
                   y0 + chopsize if y0 + chopsize < height else height - 1)
            print('box {}'.format(box))

            cropped = image.crop(box)
            mode = cropped.mode
            size = cropped.size
            data = cropped.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)

            # PIL for transparant copy
            pil_image_rgba = cropped.copy()
            # test to save tiles
            # cropped.save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))

            pil_image_rgba = pil_image_rgba.convert('RGBA')
            #pil_image_rgba = pil_image_rgba.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
            data = pil_image_rgba.getdata()  # you'll get a list of tuples
            newData = []
            for a in data:
                a = a[:3]  # you'll get your tuple shorten to RGB
                a = a + (128,)  # change the 100 to any transparency number you like between (0,255)
                newData.append(a)
            pil_image_rgba.putdata(newData)  # you'll get your new img ready
            mode_t = pil_image_rgba.mode
            size_t = pil_image_rgba.size
            data_t = pil_image_rgba.tobytes()
            py_image_t = pygame.image.fromstring(data_t, size_t, mode_t)
            # position is set in game view when the tile is displayed
            counter += 1
            coords = getXYCoordinatesFromBox(box, self.tile_size)

            tile_matrix[coords[0]][coords[1]] = py_image
            # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))

    return tile_matrix


gameDisplay.fill(white)
im_pth = "rk_background.png"
# img = Image.open("rk_background.png")
im = Image.open(im_pth)
num_tiles = 24
tile_size = fit_squares(im, num_tiles)
# crop to tiles and show
matrix = crop_image_to_array(im,num_tiles,tile_size)
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True


    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()