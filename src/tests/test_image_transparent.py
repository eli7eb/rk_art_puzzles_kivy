import pygame
from PIL import Image

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('test transparent')

black = (0, 0, 0)
white = (255, 255, 255)
x = 0 #(display_width * 0.45)
y = 0 #(display_height * 0.8)

clock = pygame.time.Clock()
crashed = False

def show_image(x, y):
    im = pygame.transform.scale(pygame.image.load("milkmaid.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    gameDisplay.blit(im, (x, y))

def show_image_resize(x,y):
    desired_size = 468
    im_pth = "milkmaid.png"
    # img = Image.open("milkmaid.png")
    im = Image.open(im_pth)
    old_size = im.size  # old_size[0] is in (width, height) format

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
    img = Image.open("milkmaid.png")
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

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    show_image_resize(x, y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()