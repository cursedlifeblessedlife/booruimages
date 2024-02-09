#Hides pygame Welcome Message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from pybooru import Danbooru
from urllib.request import Request, urlopen
import pygame
import io
import random
import re


#Danbooru Client
client = Danbooru(
    'danbooru'
)

#Fetches Random Danbooru Image URL
Random_Posts = client.post_list(limit=100, random=True)

Post_ID = []
Image_WIDTH = []
Image_HEIGHT = []
Image_URL = []

for items in Random_Posts:
    for item in items:
        if re.search('^file_url$', item):
            Post_ID.append(items['id'])
            Image_WIDTH.append(items['image_width'])
            Image_HEIGHT.append(items['image_height'])
            Image_URL.append(items['file_url'])

#Initializes Pygame
pygame.init()

#Requests Random Danbooru Image URL
list_limit = 0 
for i in Image_URL:
    list_limit += 1

Random_Index = random.randint(0, list_limit-1)
print(f'https://danbooru.donmai.us/posts/{Post_ID[Random_Index]} has an original width of {Image_WIDTH[Random_Index]} and height of {Image_HEIGHT[Random_Index]}. Default Scaled Dimensions are in 720p (1280x720).')

Req = Request(
    url=Image_URL[Random_Index],
    headers={'User-Agent': 'Chrome/121.0.0.0'}
) 

#Image Manipulation
Image_STR = urlopen(Req).read()
Image_FILE = io.BytesIO(Image_STR)

#Screen Manipulation
white = (255, 255, 255)
screen_resolution = (1280, 720) # 720p

screen = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)
screen.fill(white)
window = screen.get_rect()

#Default Image Scaling
screen_width = screen_resolution[0]
screen_height = screen_resolution[1]
image_width = Image_WIDTH[Random_Index]
image_height = Image_HEIGHT[Random_Index]
Image_SCALE = ()

if image_width > screen_width:
    Image_SCALE_WIDTH = (screen_width,)
else:
    Image_SCALE_WIDTH = (image_width,)
Image_SCALE += Image_SCALE_WIDTH

if image_height > screen_height:
    Image_SCALE_HEIGHT = (screen_height,)
else:
    Image_SCALE_HEIGHT = (image_height,)
Image_SCALE += Image_SCALE_HEIGHT

#Displays Image
Image_LOAD = pygame.transform.scale(pygame.image.load(Image_FILE), Image_SCALE)
screen.blit(Image_LOAD, Image_LOAD.get_rect(center=window.center))
pygame.display.flip()

#Screen Caption & Icon Manipulation
pygame.display.set_caption('Danbooru')
pygame.display.set_icon(Image_LOAD)

#Program Run Loop
running = True

while running:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Handles Run Loop Break
            running = False

        if event.type == pygame.VIDEORESIZE: # Handles Window Resizing
            screen.fill(white)
            window = screen.get_rect()

            Image_SCALE_TEMPORARY = ()

            if image_width > event.w:
                Image_SCALE_WIDTH = (event.w,)
            else:
                Image_SCALE_WIDTH = (image_width,)
            Image_SCALE_TEMPORARY += Image_SCALE_WIDTH

            if image_height > event.h:
                Image_SCALE_HEIGHT = (event.h,)
            else:
                Image_SCALE_HEIGHT = (image_height,)
            Image_SCALE_TEMPORARY += Image_SCALE_HEIGHT
            
            Image_LOAD = pygame.transform.scale(Image_LOAD, Image_SCALE_TEMPORARY)
            screen.blit(Image_LOAD, Image_LOAD.get_rect(center=window.center))
            pygame.display.flip()
            
        if event.type == pygame.VIDEOEXPOSE:  # Handles Window Minimising/Maximising
            screen.fill(white)
            window = screen.get_rect()
            screen.blit(Image_LOAD, Image_LOAD.get_rect(center=window.center))
            pygame.display.flip()

#Program Exit
def exit():
    print('Exiting...')
    pygame.quit()
    raise SystemExit()
exit()
