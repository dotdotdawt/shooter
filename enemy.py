import pygame
import random

TOP_SCREEN_SPAWN_OFFSET = 30

class Enemy(object):

    
    def __init__(self, enemy_type, image_path):
        self.type = enemy_type
        self.damaged_by = []
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.y = TOP_SCREEN_SPAWN_OFFSET
        self.x = 0
        self.dead = False
        self.reverse = True

    def get_movement(self):
        # Not doing this yet.
        return 0

    def update_position(self, moved=False):
        if moved:
            self.y += self.speed
            self.x += self.get_movement()
        self.rect.topleft = (self.x, self.y)

class Eye(Enemy):

    
    def __init__(self, image_path):
        Enemy.__init__(self, 'eye', image_path)
        self.speed = random.randint(5, 20)/5
        self.health = 1
        self.damage_wait = 15
        self.movement_factor = 2
        self.movement_x = 5
        self.movement_destination = (self.x + self.movement_x)
        self.size = (64,64)

class Grunt(Enemy):

    
    def __init__(self, image_path):
        Enemy.__init__(self, 'grunt', image_path)
        self.speed = 0.60
        self.health = 3
        self.damage_wait = 25
        self.movement_factor = 1
        self.movement_x = 1
        self.movement_destination = (self.x + self.movement_x)
        self.size = (64,64)

class Speedy(Enemy):

    
    def __init__(self, image_path):
        Enemy.__init__(self, 'speedy', image_path)
        self.speed = random.randint(20, 40)/5
        self.health = 1
        self.damage_wait = 0
        self.movement_factor = 4
        self.movement_x = 10
        self.movement_destination = (self.x + self.movement_x)
        self.size = (32,32)
