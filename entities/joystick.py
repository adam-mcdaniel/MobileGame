from easy_mobile.sprite import Joystick as BaseJoystick



# class Joystick(Sprite):
#     def __init__(self, x, y, image=""):
#         super(Joystick, self).__init__(x, y, image=image)
#         self.x_val = 0
#         self.y_val = 0
#         self.setStaticPosition(True)

#     def update(self, screen):
#         if not self.getTouchUp():
#             self.x_val = 5 * min(max((self.getTouch().pos[0] - self.getX() - self.getWidth()/2) / (96), -10), 10)
#             self.y_val = 5 * min(max((self.getTouch().pos[1] - self.getY() - self.getHeight()/2) / (96), -10), 10)
#         else:
#             self.x_val = 0
#             self.y_val = 0

#     def getDirection(self):
#         return self.x_val, 0


class Joystick(BaseJoystick):
    def __init__(self, x, y):
        super(Joystick, self).__init__(x, y, "png/joystick/00.png")

    def update(self, screen):
        super(Joystick, self).update(screen)
        if self.x_val > 2 and self.y_val > 2:
            self.setImage("png/joystick/11.png")
        elif self.x_val < -2 and self.y_val > 2:
            self.setImage("png/joystick/-11.png")
        elif self.x_val > 2 and self.y_val < -2:
            self.setImage("png/joystick/1-1.png")
        elif self.x_val < -2 and self.y_val < -2:
            self.setImage("png/joystick/-1-1.png")
        elif self.x_val < 2 and self.x_val > -2  and self.y_val > 2:
            self.setImage("png/joystick/01.png")
        elif self.x_val < 2 and self.x_val > -2  and self.y_val < -2:
            self.setImage("png/joystick/0-1.png")
        elif self.x_val < -2 and self.y_val < 2 and self.y_val > -2:
            self.setImage("png/joystick/-10.png")
        elif self.x_val > 2 and self.y_val < 2 and self.y_val > -2:
            self.setImage("png/joystick/10.png")
        else:
            self.setImage("png/joystick/00.png")
            