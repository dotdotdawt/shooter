import pygame
import sys
import random

SCREEN_SIZE = 600
BASIC_WAVE = {
    'eye': 7,
    'grunt': 0,
    'speedy': 0
    }
TERTIARY_WAVE = {
    'eye': 4,
    'grunt': 1,
    'speedy': 1
    }
GRUNT_WAVE = {
    'eye': 0,
    'grunt': 5,
    'speedy': 0
    }
INVASION_WAVE = {
    'eye': 15,
    'grunt': 0,
    'speedy': 2
    }
SPEEDY_WAVE = {
    'eye': 3,
    'grunt': 0,
    'speedy': 10
    }
WAVES = {
    'basic': BASIC_WAVE,
    'tert': TERTIARY_WAVE,
    'grunt': GRUNT_WAVE,
    'invasion': INVASION_WAVE,
    'speedy': SPEEDY_WAVE
    }
    

pygame.init()


class Game(object):
    def __init__(self):
        self.playing = True
        self.screen_width = 750
        self.screen_height = 700
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.wave_interval = 150
        self.wave_time = 0
        self.waves = WAVES
        self.wave_types = [ 'basic', 'tert', 'grunt', 'invasion', 'speedy' ]
        self.bullets = []
        self.enemies = []
        self.text_objects = []
        self.powerup_thresholds = []
        self.powerup_amount = 0
        for i in range(0, 500):
            self.powerup_thresholds.append(50 * i)

game = Game()
        

class Enemy(object):
    def __init__(self):
        self.image = pygame.image.load("Enemy_Eyeball.png")
        self.rect = self.image.get_rect()
        self.y = 0
        self.x = random.randint(0,SCREEN_SIZE)
        self.starting_x = self.x
        self.dead = False
        self.damage_cooldown = False
        self.reverse = True
        self.damage_cd = 0

    def invulnerability(self):
        if self.damage_cooldown == True:
            self.damage_cd += 1
        if self.damage_cd >= self.damage_wait:
            self.damage_cooldown = False
            self.damage_cd = 0        

class Eye(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        print "Eye created."
        self.speed = 0.8
        self.health = 1
        self.damage_wait = 15
        self.movement_factor = 2
        self.movement_x = 5
        self.movement_destination = (self.x + self.movement_x)

class Grunt(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.speed = 0.45
        self.health = 3
        self.damage_wait = 25
        self.movement_factor = 1
        self.movement_x = 1
        self.movement_destination = (self.x + self.movement_x)

class Speedy(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.speed = random.randint(20, 40)/10
        self.health = 1
        self.damage_wait = 0
        self.movement_factor = 4
        self.movement_x = 10
        self.movement_destination = (self.x + self.movement_x)

class Player(object):
    def __init__(self):
        self.speed = 9.56
        self.health = 500
        self.size = (32, 32)
        self.image = pygame.image.load("GameCat3.png")
        self.rect = self.image.get_rect()
        self.x = game.screen_width/2 + 16
        self.y = game.screen_height - self.size[1]
        self.damage_cooldown = False
        self.damage_wait = 15
        self.damage_cd = 0
        self.score = 0
        self.powerup = False
        self.powerups = 2
        self.powerup_duration = 240
        self.powerup_timer = 0
        
        self.shot_gun = {
            'cd': 0,
            'cooldown': False,
            'wait': 40,
            'damage': 1,
            'speed': 23
            }
        self.laser_gun = {
            'cd': 0,
            'cooldown': False,
            'wait': 4,
            'damage': 0.5,
            'speed': 45
            }
        self.basic_gun = {
            'cd': 0,
            'cooldown': False,
            'wait': 15,
            'damage': 5,
            'speed': 13
            }
        self.guns = {
            'basic': self.basic_gun,
            'shot_gun': self.shot_gun,
            'laser': self.laser_gun
            }
        
    def weapon_cooldown(self, weapon):
        if self.guns[weapon]['cooldown'] == True:
            self.guns[weapon]['cd'] += 1
        if self.guns[weapon]['cd'] >= self.guns[weapon]['wait']:
            self.guns[weapon]['cooldown'] = False
            self.guns[weapon]['cd'] = 0
            
    def invulnerability(self):
        if self.damage_cooldown == True:
            self.damage_cd += 1
        if self.damage_cd >= self.damage_wait:
            self.damage_cooldown = False
            self.damage_cd = 0

    def get_new_bullet(self, weapon):
        speed = self.guns[weapon]['speed']
        self.guns[weapon]['cooldown'] = True
        new_bullet = Bullet(player.rect.topleft, speed)
        
        return new_bullet

class Bullet(object):
    def __init__(self, location, speed):
        self.x, self.y = location
        self.speed = speed
        self.alive = True
        self.image = pygame.image.load("Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class Text(object):
    def __init__(self, location, string, size, color, bg_color):
        self.x, self.y = location
        self.string = string
        self.aa = True
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.type = 'freesansbold.tff'
        self.font = pygame.font.SysFont(self.type, self.size)
        self.surf = self.font.render(self.string, self.aa, self.color, self.bg_color)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (self.x, self.y)        
        
bullets = []
remaining_bullets = []
enemies = []
SPEED = 1.5
spawn_amount = 8
player = Player()
game.text_objects.append(Text((20, game.screen_height-50), "Powerups: %i" % player.powerups, 24, (244, 244, 244), (10, 10, 10)))


while game.playing:
    game.wave_time += 1
    player.weapon_cooldown('basic')
    player.weapon_cooldown('shot_gun')
    player.weapon_cooldown('laser')
    player.invulnerability()

    if player.powerup == True:
        player.powerup_timer += 1

    if player.powerup_timer >= player.powerup_duration:
        player.powerup = False
        player.powerup_timer = 0
    
    if game.wave_time >= game.wave_interval:
        game.wave_time = 0
        random_wave = random.randint(0, len(WAVES)-1)
        wave_type = game.wave_types[random_wave]
        
        for i in range (0, game.waves[wave_type]['eye']):
            game.enemies.append(Eye())
            game.enemies[i].rect.topleft = (game.enemies[i].x, game.enemies[i].y)
        for i in range (0, game.waves[wave_type]['grunt']):
            game.enemies.append(Grunt())
            game.enemies[i].rect.topleft = (game.enemies[i].x, game.enemies[i].y)
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.playing = False
            if event.key == pygame.K_1:
                if player.powerups >= 1:
                    player.powerup = True
                    player.powerups -= 1

    keys_pressed = pygame.key.get_pressed()
    xMove = 0
    yMove = 0
    if (keys_pressed[pygame.K_LEFT]):
        xMove -= player.speed
    if (keys_pressed[pygame.K_RIGHT]):
        xMove += player.speed
        
    if (keys_pressed[pygame.K_SPACE]):
        if player.powerup and player.guns['laser']['cooldown'] == False:
            game.bullets.append(player.get_new_bullet('laser'))
        elif player.powerup == False and player.guns['basic']['cooldown'] == False:
            game.bullets.append(player.get_new_bullet('basic'))

    if (keys_pressed[pygame.K_q]) and player.guns['shot_gun']['cooldown'] == False:
        game.bullets.append(player.get_new_bullet('shot_gun'))
        
    if (player.rect.x + player.rect.width + xMove) > game.screen_width:
        xMove = 0
        
    player.x += xMove
    player.y += yMove
    player.rect.topleft = (player.x, player.y)
    game.screen.fill((0,0,0))
    rect = game.screen.blit(player.image, player.rect)
    
    try:
        for i in range(0, len(game.enemies)):
            if game.enemies[i].dead == False:
                game.enemies[i].invulnerability()
                game.screen.blit(game.enemies[i].image, game.enemies[i].rect)
            game.enemies[i].y += game.enemies[i].speed
            """
            if game.enemies[i].x >= game.enemies[i].movement_destination:
                game.enemies[i].movement_destination = (game.enemies[i].starting_x - game.enemies[i].movement_x)
                if game.enemies[i].reverse:
                    game.enemies[i].reverse = False
                else:
                    game.enemies[i].reverse = True
            else:
                if game.enemies[i].reverse:
                    game.enemies[i].x += (game.enemies[x].movement_factor * -1)
                else:
                    game.enemies[i].x += game.enemies[x].movement_factor
            print game.enemies[i].movement_destination
            """
            game.enemies[i].rect.topleft = (game.enemies[i].x, game.enemies[i].y)
            if player.rect.colliderect(game.enemies[i].rect) and game.enemies[i].dead == False and player.damage_cooldown == False:
                player.health -= 1
                player.damage_cooldown = True
            
    except NameError:
        pass

    try:
        for i in range(0, len(game.bullets)):
            if game.bullets[i].y >= -200:
                game.screen.blit(game.bullets[i].image, game.bullets[i].rect)
                game.bullets[i].alive = True
            else:
                game.bullets[i].alive = False
            game.bullets[i].y -= game.bullets[i].speed
            game.bullets[i].rect.topleft = (game.bullets[i].x, game.bullets[i].y)
            for x in range(0, len(game.enemies)):
                if game.bullets[i].rect.colliderect(game.enemies[x].rect) and game.enemies[x].damage_cooldown == False:
                    game.enemies[x].health -= 1
                    game.enemies[x].damage_cooldown = True
                    print(game.enemies[x].health)
                    if game.enemies[x].health <= 0:
                        player.score += 1
                        game.enemies[x].dead = True
                        print player.score

        game.bullets = [bullet for bullet in game.bullets if bullet.alive]
        #game.enemies = [enemy for enemy in game.enemies if not enemy.dead]
        #print len(game.bullets)
            
    except NameError:
        pass

    for i in range(0, len(game.text_objects)):
        game.text_objects[i].rect.topleft = (game.text_objects[i].x, game.text_objects[i].y)
        game.text_objects[i].string = "Powerups: %i" % player.powerups
        game.text_objects[i].surf = game.text_objects[i].font.render(
            game.text_objects[i].string, game.text_objects[i].aa, game.text_objects[i].color, game.text_objects[i].bg_color)
        game.screen.blit(game.text_objects[i].surf, game.text_objects[i].rect)
                   

    if player.score >= game.powerup_thresholds[game.powerup_amount]:
        game.powerup_amount += 1
        player.powerups += 1
    if player.health <= 0:
        pygame.quit()
        sys.exit(0)
        
    pygame.display.flip()
    game.fps_clock.tick(60)

pygame.quit()
sys.exit(0)
