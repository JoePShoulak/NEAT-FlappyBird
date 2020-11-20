import pygame

from Config import C_ANIMATION_TIME, C_ROT_VEL, C_MAX_ROTATION, C_JUMP_VEL, C_BASE_HEIGHT
from Helper import load_image

BIRD_IMGS = [load_image("bird1.png"), load_image("bird2.png"), load_image("bird3.png")]


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = C_MAX_ROTATION
    ROT_VEL = C_ROT_VEL
    ANIMATION_TIME = C_ANIMATION_TIME

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = C_JUMP_VEL
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:  # Terminal velocity
            d = 16

        if d < 0:  # Extra boost on jump
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def hit_ground(self):
        return self.y + self.img.get_height() >= C_BASE_HEIGHT

    def passed(self, pipe):
        return not pipe.passed and pipe.x < self.x

    def too_high(self):
        return self.y < 0

    def draw(self, win):
        self.img_count += 1

        adjusted_indices = [0, 1, 2, 1, 0]

        self.img = self.IMGS[adjusted_indices[self.img_count % self.ANIMATION_TIME]]

        if self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
