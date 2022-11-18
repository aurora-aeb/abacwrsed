import pygame, numpy
import math

WIDTH = 1920
HEIGHT = 1080
BACKGROUND = (55, 110, 100)

SQUARE_ROOT_OF_TWO = math.sqrt(2)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def event(self, **kwargs):
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

        self.speed = 8
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
        onground = self.check_collision(0, 1, grounds=boxes)
        # check keys
        keys = pygame.key.get_pressed()

        hsp = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        vsp = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        # MOVEMENT ANIMATION DISABLED FOR SIMPLIFIED TESTING [1]
        
        #if hsp < 0:
        #    self.facing_left = True
        #   self.walk_animation()

        #else:
        #    self.facing_right = True
        #    self.walk_animation()

        # END OF DISABLE [1]

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
        if collide:
            collide.event(player=self)

        self.rect.move_ip([-x, -y])
        return collide


class Wall_H(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_H.png", startx, starty)

class Wall_V(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_V.png", startx, starty)

class Wall_H_JD(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_H_JD.png", startx, starty)

class Wall_VE_JU(Sprite):
    def __init__(self, startx, starty):
        super().__init__("TempWall_VE_JU.png", startx, starty)

class Barrier(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Barrier.png", startx, starty)

class SadBarrier(Barrier):
    def event(self, player):
        player.stand_image = pygame.image.load("p1_front_cry.png")

class HappyBarrier(Barrier):
    def event(self, player):
        player.stand_image = pygame.image.load("p1_front.png")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 900)          #Player start location [WIDTH / 2, HEIGHT / 2]
    
    boxes = pygame.sprite.Group()

    for bx in range(0, 2000, 70):
        boxes.add(Wall_H(bx, 100))                              #Wall horizontal top row
        boxes.add(Wall_H(bx, 1035))                             #Wall horizontal bottom row

    for bx in range(5):
        for by in range(170, 660, 70):
            boxes.add(Wall_V(bx * 490, by))                     #Wall vertical
            boxes.add(Wall_VE_JU(bx * 490, 730))                #Wall vertical end blocks
            boxes.add(Wall_H_JD(bx * 490, 100))                 #Wall horizontal top junctions
        for i in range(3):
            boxes.add(Wall_H(((i - 1) * 70) + (bx * 490), 660)) #Wall horizontal middle chunks
        for i in range(3):
            boxes.add(Barrier((i * 70) + 630, 660))             #Barrier blocking access to one room

        boxes.add(SadBarrier((3 * 70) + 630, 800))
        boxes.add(HappyBarrier((6 * 70) + 630, 800))

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
