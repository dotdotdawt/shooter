import pygame
import sys
import random

SCREEN_SIZE = 600
BASIC_WAVE = {
    'eye': 11,
    'grunt': 0,
    'speedy': 2
    }
TERTIARY_WAVE = {
    'eye': 6,
    'grunt': 2,
    'speedy': 2
    }
GRUNT_WAVE = {
    'eye': 0,
    'grunt': 8,
    'speedy': 1
    }
INVASION_WAVE = {
    'eye': 25,
    'grunt': 0,
    'speedy': 5
    }
SPEEDY_WAVE = {
    'eye': 5,
    'grunt': 1,
    'speedy': 15
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
        self.screen_size = (800, 800)
        self.bg_color = (50, 20, 50)
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.wave_interval = 150
        self.fps = 60
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

    def handle_waves(self):
        game.wave_time += 1
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

    def update_text(self):
        for i in range(0, len(game.text_objects)):
            game.text_objects[i].rect.topleft = (game.text_objects[i].x, game.text_objects[i].y)
            if game.text_objects[i].text_type == 'powerup':
                game.text_objects[i].string = " Powerups: %i " % player.powerups
            elif game.text_objects[i].text_type == 'info':
                game.text_objects[i].string = " | Press 1 to activate powerup | Spacebar to shoot basic gun | Q to shoot explosive gun | "
            game.text_objects[i].surf = game.text_objects[i].font.render(
                game.text_objects[i].string, game.text_objects[i].aa, game.text_objects[i].color, game.text_objects[i].bg_color)
            game.screen.blit(game.text_objects[i].surf, game.text_objects[i].rect)
        

    def update_bullets(self):
        try:
            for i in range(0, len(game.bullets)):
                if game.bullets[i].y >= -200:
                    if game.bullets[i].exploded:
                        if game.bullets[i].explosion_timer >= game.bullets[i].explosion_duration:
                            game.bullets[i].alive = False
                        # This is where individual gun type explosions happen. Fix this later.
                        """
                        if game.bullets[i].alive and game.bullets[i].bullet_id == 2:
                            game.screen.blit(game.bullets[i].explosion, game.bullets[i].rect)
                        else:
                            game.screen.blit(game.bullets[i].explosion, game.bullets[i].rect)
                        """
                        if game.bullets[i].alive:
                            game.screen.blit(game.bullets[i].explosion, game.bullets[i].rect)
                        game.bullets[i].explosion_timer += 1
                        
                    else:
                        if game.bullets[i].alive:
                            game.screen.blit(game.bullets[i].image, game.bullets[i].rect)
                    
                    game.bullets[i].alive = True
                else:
                    game.bullets[i].alive = False
                game.bullets[i].y -= game.bullets[i].speed
                game.bullets[i].rect.topleft = (game.bullets[i].x, game.bullets[i].y)
                for x in range(0, len(game.enemies)):
                    if game.bullets[i].rect.colliderect(game.enemies[x].rect) and (
                        game.enemies[x].damage_cooldown == False):
                        game.bullets[i].exploded = True
                        game.bullets[i].speed = (game.bullets[i].speed / 12)
                        game.bullets[i].x -= 32
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

    def update_enemies(self):
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

    def update(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(player.image, player.rect)
        self.update_enemies()
        self.update_bullets()
        self.update_text()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.playing = False
                if event.key == pygame.K_1:
                    if player.powerups >= 1:
                        player.powerup = True
                        player.powerups -= 1
                        player.powerup_timer = 0

game = Game()
        

class Enemy(object):
    def __init__(self):
        self.image = pygame.image.load("Enemy_Eyeball.png")
        self.rect = self.image.get_rect()
        self.y = 30
        self.x = random.randint(0, SCREEN_SIZE)
        self.rect.topleft = (self.x, self.y)
        # Trying to make the enemies never spawn on top of each... Figure this out later.
        """
        for i in range(0, len(enemies)):
            if enemies[i].rect.colliderect(self.rect):
                print("WARNING!")
                self.image = pygame.image.load("missile01.png")
        """
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
            self.damage_cd = 1        

class Eye(Enemy):
    def __init__(self):
        Enemy.__init__(self)
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
        self.x = game.screen_size[0]/2 + 16
        self.y = game.screen_size[1] - self.size[1]
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

    def check_left(self, location):
        if location < 0:
            return player.speed
        if location >= game.screen_size[0]:
            return player.speed
        else:
            return -player.speed

    def check_right(self, location):
        if location < 0:
            return -player.speed
        if location >= game.screen_size[0]-player.size[0]:
            return -player.speed
        else:
            return player.speed

    def handle_powerups(self):
        # If powerup active
        if player.powerup == True:
            player.powerup_timer += 1
        # If powerup over
        if player.powerup_timer >= player.powerup_duration:
            player.powerup = False
            player.powerup_timer = 0
        # If player should get a new powerup
        if player.score >= game.powerup_thresholds[game.powerup_amount]:
            game.powerup_amount += 1
            player.powerups += 1

    def handle_guns(self, keys_pressed):
        if (keys_pressed[pygame.K_SPACE]):
            if player.powerup and player.guns['laser']['cooldown'] == False:
                game.bullets.append(player.get_new_bullet('laser'))
            elif player.powerup == False and player.guns['basic']['cooldown'] == False:
                game.bullets.append(player.get_new_bullet('basic'))

        if (keys_pressed[pygame.K_q]) and player.guns['shot_gun']['cooldown'] == False:
            game.bullets.append(player.get_new_bullet('shot_gun'))

    def handle_movement(self, keys_pressed):
        xMove = 0
        tempMove = 0
        if keys_pressed[pygame.K_RIGHT]:
            xMove += player.speed
            tempMove = player.check_right((player.x + xMove))
            player.x += (xMove + tempMove)
        if keys_pressed[pygame.K_LEFT]:
            xMove -= player.speed
            tempMove = player.check_left((player.x + xMove))
            player.x += (xMove + tempMove)
            
        player.rect.topleft = (player.x, player.y)

    def update_from_input(self, keys_pressed):
        self.handle_guns(keys_pressed)
        self.handle_movement(keys_pressed)
        
    def weapon_cooldowns(self):
        for weapon in self.guns:   
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
        if weapon == 'basic':
            bullet_id = 3
        elif weapon == 'laser':
            bullet_id = 2
        elif weapon == 'shot_gun':
            bullet_id = 1
        new_bullet = Bullet(player.rect.topleft, speed, bullet_id)
        
        return new_bullet

class Bullet(object):
    def __init__(self, location, speed, bullet_id):
        self.x, self.y = location
        self.bullet_id = bullet_id
        self.speed = speed
        self.alive = True
        self.exploded = False
        self.explosion_duration = 30
        self.explosion_timer = 0
        file_name = "missile0%i.png" % bullet_id
        self.image = pygame.image.load(file_name)
        self.explosion = pygame.image.load("explosion.png")
        pygame.transform.scale(self.explosion, (800, 800))
        self.explosion_rect = self.explosion.get_rect()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.explosion_rect.topleft = (self.x, self.y)

class Text(object):
    def __init__(self, location, string, size, color, bg_color, text_type):
        self.x, self.y = location
        self.string = string
        self.aa = True
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.text_type = text_type
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

# Create all menu text objects.
game.text_objects.append(Text(
    (5, 0), " Powerups: %i " % player.powerups, 24, (244, 212, 244), (10, 10, 10), 'powerup')
                         )
game.text_objects.append(Text(
    (130, 0), "  |  Press 1 to activate powerup  |  Spacebar to shoot basic gun  |  Q to shoot explosive gun  |  ", 18, (212, 212, 244), (10, 10, 10), 'info')
                         )


while game.playing:
    player.weapon_cooldowns()
    player.invulnerability()
    player.handle_powerups()
    game.handle_waves()
    game.handle_events()
    keys_pressed = pygame.key.get_pressed()
    player.update_from_input(keys_pressed)
    game.update()        
    pygame.display.flip()
    game.fps_clock.tick(game.fps)

pygame.quit()
sys.exit(0)
