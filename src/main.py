import pygame, numpy
import math

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)

SQUARE_ROOT_OF_TWO = math.sqrt(2)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")

        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,12)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 0
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        """
        TODO Document this method.
        """
        hsp = 0
        vsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        keys = pygame.key.get_pressed()

        hsp = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        vsp = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        if hsp < 0:
            self.facing_left = True
            self.walk_animation()

        else:
            self.facing_right = True
            self.walk_animation()


        if hsp * vsp != 0:
            hsp /= SQUARE_ROOT_OF_TWO
            vsp /= SQUARE_ROOT_OF_TWO
        if hsp == vsp == 0:
            self.image = self.stand_image

        # TODO This is a relic, should be removed if we do not use jumping.
        if self.prev_key[pygame.K_UP] and not keys[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = keys

        # movement
        self.move(hsp, vsp, boxes)

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide


class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)

    boxes = pygame.sprite.Group()
    for bx in range(0, 400, 70):
        boxes.add(Box(bx, 300))

    boxes.add(Box(330, 230))
    boxes.add(Box(100, 70))

    while True:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()