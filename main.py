from easy_mobile.setup import *
from easy_mobile.tools import *
from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite
from entities.joystick import Joystick

screen = setup(win_width=2220,
               win_height=1080,
               level_width=4440,
               level_height=2160,
               full_screen=False)

screen.append(Sprite(2220, 1080, image="png/brick.png"))

j = Joystick(100, 100)
a = ButtonSprite(2220-(200+260), 300, image="png/a.png")
b = ButtonSprite(2220-(200), 300, image="png/b.png")
player = Sprite(0, 0, image="png/fatbot.png")

screen.append(player)
screen.append(j)
screen.append(a)
screen.append(b)

wav = Sound("wav/theme.wav")
wav.play()

def f():
    x, y = j.getDirection()
    player.move(2*x, 2*y)
    screen.focus(player)

screen.run(f)


