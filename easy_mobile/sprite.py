import sys
import time
from .setup import *
from .tools import *
from .camera import *
from .camera import Rect
from collections import deque
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.input.providers.mouse import MouseMotionEvent

keyDown = lambda event, key: False
keyUp = lambda event, key: False
TheScreen = None


class Sprite(Image):
    rect = Rect(0, 0, 0, 0)
    def __init__(self, x, y, **kwargs):
        super(Sprite, self).__init__()
        self.static = False
        self.touch_up = True
        self.touch = MouseMotionEvent(0, 0, (x, y))
        self.touch.pos = (x, y)
        self.pos = (0, 0)
        self.source = os.path.abspath(kwargs["image"])
        self.texture = CoreImage(self.source).texture
        self.rect = Rect(x, y, self.texture.width, self.texture.height)
        self.width = self.texture.width
        self.height = self.texture.height
        self.allow_stretch = True

    def draw(self, camera):
        if self.static:
            self.pos = (self.rect.x, self.rect.y)
        else:
            self.pos = camera.apply(self)

    def setStaticPosition(self, static):
        self.static = static

    def getImage(self):
        return self.source

    def setImage(self, image):
        self.source = image
        self.texture = CoreImage(self.source).texture
        self.rect = Rect(self.rect.x, self.rect.y, self.texture.width, self.texture.height)
        self.width = self.texture.width
        self.height = self.texture.height

    def update(self, entities):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getX(self): return self.rect.x

    def getY(self): return self.rect.y

    def getWidth(self): return self.rect.w

    def getHeight(self): return self.rect.h

    def getPos(self):
        return self.getX(), self.getY()

    def getDistance(self, sprite):
        return ((self.getX() - sprite.getX())**2  +  (self.getY() - sprite.getY())**2)**0.5

    def collide(self, sprite):
        if (self.rect.x > sprite.rect.x and self.rect.x < (sprite.rect.x + sprite.rect.w)) or (self.rect.x + self.rect.w > sprite.rect.x and self.rect.x + self.rect.w < (sprite.rect.x + sprite.rect.w)):
            if (self.rect.y > sprite.rect.y and self.rect.y < sprite.rect.y + sprite.rect.h) or (self.rect.y+self.rect.h > sprite.rect.y and self.rect.y+self.rect.h < sprite.rect.y + sprite.rect.h):
                return True
        return False

    def getTouch(self):
        return self.touch

    def getTouchDown(self):
        return not self.touch_up

    def getTouchUp(self):
        return self.touch_up

    def __str__(self):
        return "<Sprite at: x={}, y={}>".format(self.rect.x, self.rect.y)


class Surface(Widget):
    def __init__(self, sprites):
        super(Surface, self).__init__()
        self.sprites = sprites

    def update(self, screen):
        pass

    def pop(self):
        try:
            self.remove_widget(self.sprites.pop())
        except:
            pass

    def append(self, sprite):
        self.sprites.append(sprite)
        self.add_widget(sprite)

    def remove(self, sprite):
        try:
            self.sprites.remove(sprite)
            self.remove_widget(sprite)
        except:
            pass


class Joystick(Sprite):
    def __init__(self, x, y, image=""):
        super(Joystick, self).__init__(x, y, image=image)
        self.x_val = 0
        self.y_val = 0
        self.setStaticPosition(True)

    def update(self, screen):
        if not self.getTouchUp():
            self.x_val = 5 * min(max((self.getTouch().pos[0] - self.getX() - self.getWidth()/2) / (96), -10), 10)
            self.y_val = 5 * min(max((self.getTouch().pos[1] - self.getY() - self.getHeight()/2) / (96), -10), 10)
        else:
            self.x_val = 0
            self.y_val = 0

    def getDirection(self):
        return self.x_val, self.y_val


class ButtonSprite(Sprite):
    def __init__(self, x, y, image=""):
        super(ButtonSprite, self).__init__(x, y, image=image)
        self.setStaticPosition(True)

    def update(self, screen):
        pass

    def getPressed(self):
        return self.getTouchDown()


class Gif(object):
    """A class to simplify the act of adding animations to sprites."""
    def __init__(self, frames, fps, loops=-1):
        """
        The argument frames is a list of frames in the correct order;
        fps is the frames per second of the animation;
        loops is the number of times the animation will loop (a value of -1
        will loop indefinitely).
        """
        self.frames = frames
        self.fps = fps
        self.frame = 0
        self.timer = time.time()
        self.loops = loops
        self.loop_count = 0
        self.done = False

    def getFrame(self):
        if time.time()-self.timer > 1/self.fps:
            self.frame += 1
            self.timer = time.time()
            if self.frame >= len(self.frames):
                self.frame = 0

        return self.frames[self.frame]

    def reset(self):
        """Set frame, timer, and loop status back to the initialized state."""
        self.frame = 0
        self.timer = None
        self.loop_count = 0
        self.done = False


class AnimatedSprite(Sprite):
    def __init__(self, x, y, **kwargs):
        image_paths = kwargs["images"]
        if "frequency" in kwargs:
            frequency = kwargs["frequency"]
        else:
            frequency = 1

        self.frame = 0
        self.frames = list(map(lambda i: pygame.image.load(path(i)), image_paths))
        Screen.getScreen().addAction(TimedAction(frequency, self.changeFrame))
        super(AnimatedSprite, self).__init__(x, y, image=image_paths[0])

    def changeFrame(self, screen):
        self.setImage(self.getFrame())

    def getFrame(self):
        if self.frame == len(self.frames):
            self.frame = 0
        frame = self.frames[self.frame]
        self.frame += 1
        return frame


class ScreenWidget(Widget):
    def __init__(self, w, h, camera, fs=False):
        super(ScreenWidget, self).__init__()
        global TheScreen
        self.sprites = []
        self.surfaces = []
        self.background = False

        self.camera = camera
        self.actions = []

        self.run = None

        self.width = w
        self.height = h
        TheScreen = self

        self.touch = None
        self.touch_up = None

    def __len__(self):
        return len(self.sprites)

    def __getitem__(self, i):
        return self.sprites[i]

    def getScreen():
        return TheScreen

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setBackground(self, sprite):
        self.background = sprite
        self.add_widget(sprite)

    def append(self, sprite):
        self.sprites.append(sprite)
        self.add_widget(sprite)

    def remove(self, sprite):
        try:
            self.sprites.remove(sprite)
            self.remove_widget(sprite)
        except:
            pass

    def add(self, sprites):
        self.sprites.extend(sprites)
        list(map(self.add_widget, sprites))

    def addAction(self, action):
        self.actions.append(action)

    def addSurface(self, surface):
        self.surfaces.append(surface)
        self.add_widget(surface)

    def fill(self, color):
        pass

    def focus(self, sprite):
        self.camera.update(sprite)

    def update(self, dt):
        self.fill((0, 0, 0))

        if self.background:
            self.background.draw(self.camera)

        for sprite in self.sprites:
            sprite.draw(self.camera)
            sprite.update(self)

        list(map(lambda a: a.update(self), self.actions))
        list(map(lambda s: s.update(self), self.surfaces))

        self.run()

    def on_touch_move(self, touch):
        for item in self:
            if item.collide_point(*touch.pos):
                item.touch = touch
                item.touch_up = False
            else:
                if item.touch == touch:
                    item.touch_up = True                    
        return True
        
    def on_touch_down(self, touch):
        for item in self:
            if item.collide_point(*touch.pos):
                item.touch_up = False
                item.touch = touch
        return True
        
    def on_touch_up(self, touch):
        for item in self:
            if touch == item.touch:
                item.touch_up = True
                item.touch = touch
        return True

    # def getTouch(self):
    #     return self.touch

    # def getTouchDown(self):
    #     return not self.touch_up

    # def getTouchUp(self):
    #     return self.touch_up


class Screen(App):
    def __init__(self, *args):
        super(Screen, self).__init__()
        self.s = ScreenWidget(*args)

    def build(self):
        Clock.schedule_interval(self.s.update, 1.0 / 60.0)
        return self.s

    def on_pause(self):
        return True

    def on_resume(self):
        return True

    @staticmethod
    def getScreen():
        return TheScreen

    def getWidth(self):
        return self.s.width

    def getHeight(self):
        return self.s.height

    def setBackground(self, sprite):
        sprite.setStaticPosition(True)
        self.s.setBackground(sprite)

    def append(self, sprite):
        self.s.append(sprite)

    def remove(self, sprite):
        self.s.remove(sprite)

    def add(self, sprites):
        self.s.add(sprites)

    def addAction(self, action):
        self.s.addAction(action)

    def addSurface(self, surface):
        self.s.addSurface(surface)

    def fill(self, color):
        pass

    def focus(self, sprite):
        self.s.focus(sprite)

    def getTouch(self):
        return self.s.getTouch()

    def getTouchDown(self):
        return self.s.getTouchDown()

    def getTouchUp(self):
        return self.s.getTouchUp()

    def run(self, f):
        self.s.run = f
        super(Screen, self).run()

    def __len__(self):
        return self.s.__len__()

    def __getitem__(self, i):
        return self.s.__getitem__(i)
    
        
if __name__ == "__main__":
    pygame.init()
    pygame.mouse.set_visible(False)
    s = Screen(WIN_WIDTH, WIN_HEIGHT)
    # s = Screen(640, 480)
    s.fill((0, 0, 0))
    spr = Boomerang(0,120)
    s.append(spr)
    while True:
        # s.blit(pygame.image.load("/Users/kiwi/Desktop/old-desktop/desktop/py/b4/library/resources/weapon/boomerang1.png"), (0, 0))
        s.update()
        print(s[0])
