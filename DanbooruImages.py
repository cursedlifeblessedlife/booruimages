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

#Fetches Random Danbooru Posts in JSON
random_posts = client.post_list(limit=100, random=True)

post_ids = []
image_widths = []
image_heights = []
image_urls= []

for items in random_posts:
    for item in items:
        if re.search('^file_url$', item):
            post_ids.append(items['id'])
            image_widths.append(items['image_width'])
            image_heights.append(items['image_height'])
            image_urls.append(items['file_url'])

#Initializes Pygame
pygame.init()

#Requests Random Danbooru Image from URLs
list_limit = 0 
for i in image_urls:
    list_limit += 1

random_index = random.randint(0, list_limit-1)
print(f'https://danbooru.donmai.us/posts/{post_ids[random_index]} has an original width of {image_widths[random_index]} and height of {image_heights[random_index]}. Default Scaled Dimensions are in 720p (1280x720).')

Req = Request(
    url=image_urls[random_index],
    headers={'User-Agent': 'Chrome/121.0.0.0'}
) 

#Image Manipulation
image_STR = urlopen(Req).read()
image_FILE = io.BytesIO(image_STR)

#Screen Manipulation
white = (255, 255, 255)
screen_resolution = (1280, 720) # 720p

screen = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)
screen.fill(white)
window = screen.get_rect()

#Default Image Scaling
image_width = image_widths[random_index]
image_height = image_heights[random_index]
screen_width = screen_resolution[0]
screen_height = screen_resolution[1]
image_SCALE = ()

if image_width > screen_width:
    image_SCALE_WIDTH = (screen_width,)
else:
    image_SCALE_WIDTH = (image_width,)
image_SCALE += image_SCALE_WIDTH

if image_height > screen_height:
    image_SCALE_HEIGHT = (screen_height,)
else:
    image_SCALE_HEIGHT = (image_height,)
image_SCALE += image_SCALE_HEIGHT

#Displays Image
image_LOAD = pygame.transform.scale(pygame.image.load(image_FILE), image_SCALE)
screen.blit(image_LOAD, image_LOAD.get_rect(center=window.center))
pygame.display.flip()

#Screen Caption & Icon Manipulation
pygame.display.set_caption('Danbooru')
pygame.display.set_icon(image_LOAD)

#Program Run Loop
running = True

while running:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Handles Run Loop Break
            running = False

        if event.type == pygame.VIDEORESIZE: # Handles Window Resizing
            screen.fill(white)
            window = screen.get_rect()

            image_SCALE_TEMPORARY = ()

            if image_width > event.w:
                image_SCALE_WIDTH = (event.w,)
            else:
                image_SCALE_WIDTH = (image_width,)
            image_SCALE_TEMPORARY += image_SCALE_WIDTH

            if image_height > event.h:
                image_SCALE_HEIGHT = (event.h,)
            else:
                image_SCALE_HEIGHT = (image_height,)
            image_SCALE_TEMPORARY += image_SCALE_HEIGHT
            
            image_LOAD = pygame.transform.scale(image_LOAD, image_SCALE_TEMPORARY)
            screen.blit(image_LOAD, image_LOAD.get_rect(center=window.center))
            pygame.display.flip()
            
        if event.type == pygame.VIDEOEXPOSE:  # Handles Window Minimising/Maximising
            screen.fill(white)
            window = screen.get_rect()
            screen.blit(image_LOAD, image_LOAD.get_rect(center=window.center))
            pygame.display.flip()

#Program Exit
def exit():
    print('Exiting...')
    pygame.quit()
    raise SystemExit()
exit()
