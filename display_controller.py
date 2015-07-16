input_dir = 'controller_defs/' # directory for saved definitions
img_dir = 'controller_imgs/' # directory for image files
fps = 30 # set update rate (frames per second)

# get controller name from command line argument(s)
from sys import argv, exit
console_str = '_'.join(argv[1:]).lower()
if(not console_str):
    exit('Usage: display_controller.py [controller name]')

# load controller definition file
import json
fname = input_dir + console_str + '.json'
controller_map = json.load(open(fname))

# partition controller definition dict to vars
console = controller_map['console']
joystick = controller_map['joystick']
buttons = controller_map['buttons']
corners = controller_map['corners']

# define corner buttons from coordinate pairs
if(corners):
    corners = {
        'ur': (buttons['up'], buttons['right']),
        'ul': (buttons['up'], buttons['left']),
        'dr': (buttons['down'], buttons['right']),
        'dl': (buttons['down'], buttons['left'])
        }

# set window name
caption = '%s controller' % (console)

# initialize pygame
import pygame
pygame.init()

# initialize display window
bg_img = pygame.image.load(img_dir + console_str + '/base.png')
img_size = bg_img.get_rect().size
screen = pygame.display.set_mode(img_size)
pygame.display.set_caption(caption)

# initialize clock
clock = pygame.time.Clock()

# initialize the joysticks
pygame.joystick.init()

# select joystick
joystick_count = pygame.joystick.get_count()
if joystick_count > joystick: # only initialize if joystick is plugged in
    joy = pygame.joystick.Joystick(joystick)
    joy.init()

# load button images
fg_imgs = {}
for b in buttons:
    fg_imgs[buttons[b]] = pygame.image.load(img_dir + console_str + '/%s.png' % (b))
if corners:
    for c in corners:
        fg_imgs[c] = pygame.image.load(img_dir + console_str + '/%s.png' % (c))

# loop until user clicks the close button
done = False
while done == False:

    # start event capture and check for close
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            done = True
        
    # print the background image
    screen.blit(bg_img, [0, 0])
    
    # ignore rest of loop if joystick not plugged in
    if not (joystick_count > joystick):
        pygame.display.flip()
        clock.tick(30)
        continue

    # get pressed buttons on joystick
    pressed = {}
    for b in buttons:
        pressed[buttons[b]] = bool(joy.get_button(buttons[b])) 

    # handle corner images if they are being used
    if corners:
        for c in corners:
            # print corner button images if corresponding cardinal directions are pressed
            if pressed[corners[c][0]] and pressed[corners[c][1]]:
                screen.blit(fg_imgs[c], [0, 0])
                
                # the cardinal directions are now "unpressed"
                pressed[corners[c][0]] = False
                pressed[corners[c][1]] = False

    # print remaining pressed buttons
    for b in pressed:
        if pressed[b]:
            screen.blit(fg_imgs[b], [0, 0])
                
       
    # update the screen
    pygame.display.flip()

    # limit to update rate
    clock.tick(fps)
    
# close the window and quit
pygame.quit()


