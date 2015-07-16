output_dir = 'controller_defs/' # directory for saved definitions
img_dir = 'controller_imgs/' # directory for image files

from collections import OrderedDict
dpad = ['up', 'down', 'left', 'right'] # directional pad will always be defined
dpad_corners = False # option for corner buttons
button_map = OrderedDict() # definitions will be stored in an ordered dict then output to JSON

yes = ['', 'yes', 'y', 'Y', '1'] # input responses to be interpreted as "yes"

# initialize pygame, joysticks, and get number of joysticks
import pygame
pygame.init()
pygame.joystick.init()
njoy = pygame.joystick.get_count()

# exit script if there are no joysticks
from sys import exit
if not njoy:
    pygame.quit()
    exit('No controllers found')

# internal functions
def get_controller(njoy):
    
    '''
    Polls all joysticks until a button is pressed,
    then returns the id of the used joystick.
    
    Inputs
    ----
    njoy: number of joysticks [int]
    
    Outputs
    ----
    id of chosen joystick [int]
    '''
    
    done = False
    while done == False:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # loop over joysticks
        for ijoy in range(njoy):
            joy = pygame.joystick.Joystick(ijoy)
            joy.init()
        
            # loop over butttons
            nbtn = joy.get_numbuttons()
            for ibtn in range(nbtn):
                pressed = joy.get_button(ibtn)
                
                # stop when a button is pressed
                if pressed:
                    controller = ijoy
                    done = True

    return controller
    
def get_button(ijoy):

    '''
    Polls given joysticks until a button is pressed,
    then returns the id of the used button.
    
    Inputs
    ----
    ijoy: id of joysticks [int]
    
    Outputs
    ----
    id of chosen button [int]
    '''
    
    done = False
    while done == False:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        joy = pygame.joystick.Joystick(ijoy)
        joy.init()
        
        # loop over butttons
        nbtn = joy.get_numbuttons()
        for ibtn in range(nbtn):
            pressed = joy.get_button(ibtn)
            
            # stop when a button is pressed
            if pressed:
                button = ibtn
                done = True

    return button
    
# prompt user for name
console = raw_input('Name this controller (e.g. NES, SNES, Genesis, Xbox): ')
print

# get joystick user wishes to define
ok = 'n'
while not (ok in yes):
    print 'Hit any button on the controller you wish to set up'
    ijoy = get_controller(njoy)
    print 'Controller %d' % (ijoy)
    ok = raw_input('ok? [enter for yes]: ')
print

# get directional pad buttons
# TODO: also accept hat input
print 'Binding d-pad buttons...'
for button_name in dpad:
    ok = 'n'
    while not (ok in yes):
        print 'Hit button mapped to %s:' % (button_name),
        button = get_button(ijoy)
        print 'Button %d' % button,
        ok = raw_input('ok? [enter for yes]: ')
    button_map[button_name] = button
print

# prompt user for whether or not corners should be used
dpad_corners = raw_input('Separate images for corners? [enter for yes]: ') in yes
print

# get additional buttons defined by the user
print 'Binding other buttons, enter "done" when finished...'
print
button_name = ''
while button_name != 'done':
    button_name = raw_input('Button: ')
    if(button_name == 'done'): continue
    if(button_name == ''): continue
    
    ok = 'n'
    while not (ok in yes):
        print 'Hit button mapped to %s:' % (button_name),
        button = get_button(ijoy)
        print 'Button %d' % button,
        ok = raw_input('ok? [enter for yes]: ')
    button_map[button_name] = button
    print

pygame.quit()
    
# build dictionary to be output to JSON file
controller_map = OrderedDict()
controller_map['console'] = console
controller_map['joystick'] = ijoy
controller_map['buttons'] = button_map
controller_map['corners'] = dpad_corners

# make the controller name more filesystem friendly
console_str = '_'.join(console.split()).lower()

# save the controller definition to disk
import json
fname = output_dir + '%s.json' % (console_str)
json.dump(controller_map, open(fname, 'w'), indent = 4)
    
# inform user of files to be created
print 'Configuration saved in ./%s' % (fname)
print
print 'You should have/create image files:'
print './controllers/%s/' % (console_str)
print '\tbase.png'
for button_name in button_map:
    print '\t%s.png' % (button_name)
if dpad_corners:
    print '\tur.png (up-right)'
    print '\tul.png (up-left)'
    print '\tdr.png (down-right)'
    print '\tdl.png (down-left)'

