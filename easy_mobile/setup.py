from .sprite import *
from .camera import *
from kivy.config import Config

WIN_WIDTH, WIN_HEIGHT = 320, 240
LEVEL_WIDTH, LEVEL_HEIGHT = 320, 240

def setup(**kwargs):
    global LEVEL_WIDTH, LEVEL_HEIGHT, WIN_WIDTH, WIN_HEIGHT
    if "level_width" not in kwargs:
        LEVEL_WIDTH = kwargs["win_width"]
    else:
        LEVEL_WIDTH = kwargs["level_width"]

    if "level_height" not in kwargs:
        LEVEL_HEIGHT = kwargs["win_height"]
    else:
        LEVEL_HEIGHT = kwargs["level_height"]

    if "full_screen" not in kwargs:
        FS = False
    else:
        FS = True

    WIN_WIDTH = kwargs["win_width"]
    WIN_HEIGHT = kwargs["win_height"]

    DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
    DEPTH = 32
    FLAGS = 0
    CAMERA_SLACK = 1000

    Config.set('graphics', 'width', str(WIN_WIDTH))
    Config.set('graphics', 'height', str(WIN_HEIGHT))


    return Screen(WIN_WIDTH, WIN_HEIGHT, Camera(complex_camera, LEVEL_WIDTH, LEVEL_HEIGHT, WIN_WIDTH, WIN_HEIGHT), FS)

# def setup()
