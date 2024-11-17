class Sprite:
    sprite_list = []

    def __init__(self, name, image_bank, x, y, u, v, w, h, colkey, speed):
        self.sprite_list.append(self)
        self.name = name
        self.image_bank = image_bank
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.speed = speed
        self.show = True
        self.rotation = 0
        self.scale = 1
        self.direction = ""
        self.timer = 0

    #    draft move function...
    def move(self, direction, speed=None, rotation=None, flip_v=None, flip_h=None):
        if speed:
            self.speed = speed
        if rotation:
            self.rotation = rotation
        else:
            self.rotation = 0
        if flip_v:
            self.w = -abs(self.w)
        else:
            self.w = abs(self.w)
        if flip_h:
            self.h = -abs(self.h)
        else:
            self.h = abs(self.h)

        match direction:
            case "right":
                self.x += self.speed
            case "left":
                self.x -= self.speed
            case "down":
                self.y += self.speed
            case "up":
                self.y -= self.speed

    def move_right(self, speed=None, rotation=None):
        if speed:
            self.speed = speed
        if rotation:
            self.rotation = rotation
        else:
            self.rotation = 0
        # abs returns the absolute (postive) of an integer, converts to positive
        # this will
        self.w = abs(self.w)
        self.x += self.speed

    def move_left(self, rotation=0):
        self.rotation = rotation
        # -abs retuns the positive but with a - sign! so a negative...
        self.w = -abs(self.w)
        self.x -= self.speed

    def move_down(self, rotation=0):
        self.rotation = rotation
        self.y += self.speed

    def move_up(self, rotation=0):
        self.rotation = rotation
        self.y -= self.speed

    def change_costume(self, costume):
        self.u = costume * 8
        # if costume == 0:
        #    self.u = 0
        # elif costume == 1:
        #    self.u = 8
        # elif costume == 2:
        #    self.u == 16
