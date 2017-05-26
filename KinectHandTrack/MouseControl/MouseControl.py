"""
MouseControl module allows to control mouse location and button actions,
based on the centroid coordinates and contour shape, got from DepthContours module
"""
from Xlib import X
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest
from KinectHandTrack.constants import DISPLAY


def move_mouse(x, y):
    """
    Moves the mouse to point witn (x,y) coordinates
    :param x: x coordinate of present point 
    :type x: integer
    :param y: y coordinate of present point
    :type y: integer
    """
    screen = DISPLAY.screen()
    root = screen.root
    root.warp_pointer(x, y)
    DISPLAY.sync()


def click_down(button):
    """
    Simulates a down click
    :param button: Number of mouse button command
    :type button: integer
    """
    Xlib.ext.xtest.fake_input(DISPLAY, X.ButtonPress, button)
    DISPLAY.sync()


def click_up(button):
    """
    Simulates an up click
    :param button: Number of mouse button command
    :type button: integer
    """
    Xlib.ext.xtest.fake_input(DISPLAY, X.ButtonRelease, button)
    DISPLAY.sync()

