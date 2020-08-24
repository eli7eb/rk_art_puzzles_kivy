# Gain access to the pygame library
import os
import pygame

pygame.init()

# Improting Image class from PIL module
from PIL import Image

# Opens a image in RGB mode

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
#  os.path.join("assets",
im = pygame.transform.scale(pygame.image.load("milkmaid.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.blit(im, (0, 0))
# Setting the points for cropped image
left = 10
top = 20
right = 100
bottom = 200

# Cropped image of above dimension
# (It will not change orginal image)
im1 = im.crop((left, top, right, bottom))

# Shows the image in image viewer
im1.show()
