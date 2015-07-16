# Game Controller Displayer

## Requirements:
Python 2.x (tested on 2.7.9)
pygame (tested on 1.9.2a0)

## Usage

### Scripts
define_controller.py:
This script walks the user through
defining a controller.
By default, settings are saved
under ./controller_defs/
in JSON format.

display_controller.py:
The user passes the desired controller name
as a commandline argument,
and the controller is displayed.
If the controller is not present,
the static controller base image is displayed
for testing purposes.

### Images
A base image (base.png) should be made for each controller
with no transparency.
Highlighted button images should be made for each button,
transparent everywhere except the location of the button.
See Examples.

## Bugs/Todo
These scripts only work
for controllers that have directional buttons
mapped as buttons; hats are not polled.
Polling for hat buttons will be added.

Only PNG image files are expected by the scripts.

## Examples
See the examples/ directory
for a Sega Genesis-like demo.