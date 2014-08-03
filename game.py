import pygame
import sys
import random
import wave_template as wave_temp

ENEMY_TYPES = [
    'eye', 'grunt', 'speedy'
    ]
WAVE_LEVEL_FACTOR = [
    1.0, 1.1, 1.25, 1.50, 1.75, 2.0, 2.33, 2.66, 3.00, 3.5, 4.0, 5.0, 7.5, 10.0
    ]
WAVE_CONSTANT = 0.80
WAVES_TO_LEVEL_UP = 6
WAVE_INTERVAL = 150 # In frames
DEAD_BULLET_SPEED_FACTOR = 12 # Probably obsolete but keep it around just in case
OFFSCREEN_THRESHOLD = 100

pygame.init()

def create_enemy(enemy_type):
    if enemy_type == 'eye':
        return Eye()
    elif enemy_type == 'grunt':
        return Grunt()
    elif enemy_type == 'speedy':
        return Speedy()
    else:
        print '| INVALID INPUT | Could not create enemy: %s' % enemy_type

class Game(object):
    def __init__(self):
        self.playing = True
        self.initialize_displays()
        self.initialize_waves()
        self.initialize_powerups()

    def initialize_displays(self):
        self.screen_size = (800, 800)
        self.bg_color = (50, 20, 50)
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.fps = 60
        self.text_objects = []

    def initialize_waves(self):
        self.waves = {}
        self.wave_types = [ 'basic', 'tert', 'grunt', 'invasion', 'speedy' ]
        self.enemy_types = [ 'eye', 'grunt', 'speedy' ]
        self.waves['basic'] = wave_temp.Wave('basic', (11, 0, 2))
        self.waves['tert'] = wave_temp.Wave('tert', (6, 2, 2))
        self.waves['grunt'] = wave_temp.Wave('grunt', (0, 8, 1))
        self.waves['invasion'] = wave_temp.Wave('invasion', (25, 0, 10))
        self.waves['speedy'] = wave_temp.Wave('speedy', (5, 1, 15))
        # Random easter egg that turns background red when chaos is on
        for wave_type in self.wave_types:
            if self.waves[wave_type].chaos:
                prev_bg = self.bg_color
                self.bg_color = (prev_bg[0]+100, prev_bg[1], prev_bg[2])
        self.wave_level = 0
        self.waves_passed = 0
        self.wave_time = 0
        self.wave_level_up_threshold = []
        for i in range(0, len(WAVE_LEVEL_FACTOR)):
            self.wave_level_up_threshold.append(i*WAVES_TO_LEVEL_UP)
        self.bullets = []
        self.explosions = []
        self.enemies = []
        self.enemies_leaked = 0

    def initialize_powerups(self):
        self.powerup_thresholds = []
        self.powerup_amount = 0
        for i in range(0, 500):
            self.powerup_thresholds.append(50 * i)

    def debug(self):
        bullets = len(self.bullets)
        enemies = len(self.enemies)
        explosions = len(self.explosions)
        print '| Showing living objects at wave %i with level %i | bullets = %i | enemies = %i | explosions = %i |' % (
            self.waves_passed, self.wave_level, bullets, enemies, explosions)

    def create_wave(self, wave_type):
        self.debug()
        self.waves_passed += 1
        self.wave_time = 0
        wave_multiply_factor = WAVE_LEVEL_FACTOR[self.wave_level] * WAVE_CONSTANT
        current_wave = self.waves[wave_type]
        for enemy_type in self.enemy_types:
            for i in range(0, int(current_wave.enemy_amounts[enemy_type] * wave_multiply_factor)):
                self.enemies.append(create_enemy(enemy_type))
        self.debug()

    def handle_waves(self):
        self.wave_time += 1
        if self.waves_passed >= int(self.wave_level_up_threshold[self.wave_level]):
            self.wave_level += 1
        if self.wave_time >= WAVE_INTERVAL:
            random_wave = random.randint(0, len(self.wave_types)-1)
            wave_type = self.wave_types[random_wave]
            self.create_wave(wave_type)

    def update_text(self):
        # CLEAN UP !
        #
        #
        for i in range(0, len(self.text_objects)):
            self.text_objects[i].rect.topleft = (self.text_objects[i].x, self.text_objects[i].y)
            if game.text_objects[i].text_type == 'powerup':
                game.text_objects[i].string = " Powerups: %i " % player.powerups
            elif game.text_objects[i].text_type == 'info':
                game.text_objects[i].string = " | Press 1 to activate powerup | Spacebar to shoot basic gun | Q to shoot explosive gun | "
            elif game.text_objects[i].text_type == 'score':
                game.text_objects[i].string = " | Level: %i | Score: %i | Enemies leaked: %i | " % (game.wave_level, player.score, game.enemies_leaked)
            game.text_objects[i].surf = game.text_objects[i].font.render(
                game.text_objects[i].string, game.text_objects[i].aa, game.text_objects[i].color, game.text_objects[i].bg_color)
            game.screen.blit(game.text_objects[i].surf, game.text_objects[i].rect)

    def update_bullets(self):
        # update_bullets is run every frame of the game so we must use a try/except to prevent getting
        # an error. This is because game.bullets will be empty before any bullets are shot.
        try:
            for bullet in game.bullets:
                # If the bullet has exploded on an enemy, we set alive to False so that it will no
                # longer show on the screen. Then, we create an Explosion object so that the bullet
                # can apply AOE damage if possible or simply look cool.
                if bullet.exploded:
                    bullet.alive = False
                    game.explosions.append(Explosion(bullet.bullet_id))
                # OFFSCREEN_THRESHOLD is a global constant for how many pixels off screen an object
                # must be before we consider it gone. It is multiplied by -1 to make it a negative
                # value since it is going off the screen at the top.
                if bullet.y >= (OFFSCREEN_THRESHOLD * -1):
                    if bullet.alive:
                        game.screen.blit(bullet.image, bullet.rect)
                else:
                    bullet.alive = False
                bullet.y -= bullet.speed
                bullet.rect.topleft = (bullet.x, bullet.y)
                
                # We are already running a for loop that checks each bullet. Now we are running
                # another loop on top of that that checks each enemy. This is important to note
                # because we just multiplied the processing needed by a factor of 2. For each
                # bullet, we check each enemy. Bullets on the screen usually never reach more
                # than 6 or so, but enemies can get up to around 60. 6*60 = 360, which is a lot
                # of objects for python/pygame it would seem.
                #
                # If the game begins to get laggy, it is probably because of this.
                for enemy in game.enemies:
                    if bullet.rect.colliderect(enemy.rect) and bullet not in enemy.damaged_by:
                        self.bullet_collision(bullet, enemy)

            # The most important line in the whole dang program.
            #
            # This changes the bullets that we apply logic to to a smaller amount based on
            # whether or not the bullet is alive. We use the alive flag because we can't
            # delete the bullet directly, we just stop referencing it. If no one talks about
            # it for long enough, it ceases to exist and our RAM rejoices. Seemingly the only
            # way I can think of this failing to work out is if the enemy.damaged_by list is
            # never emptied. That WILL contain a reference to a dead bullet no matter what.
            game.bullets[:] = [bullet for bullet in game.bullets if bullet.alive]
            
        except NameError: # If the list is empty, nothing happens.
            pass

    def update_enemies(self):
        # update_enemies is run every frame of the game so we must use a try/except to prevent getting
        # an error. This is because game.enemies will be empty before a wave spawns or the player kills
        # all enemies.
        try:
            for enemy in game.enemies:
                if not enemy.dead:
                    if enemy.y >= game.screen_size[1] + OFFSCREEN_THRESHOLD:
                        self.enemies_leaked += 1
                        self.kill_target(enemy) # Clears all references this enemy has to objects
                    enemy.update_position()
                    player.check_collision(enemy)

            # game.enemies references all the enemy objects so we gotta keep that as small
            # as possible. We cannot waste processing power.
            # This reduces game.enemies to the previous list of game.enemies minus every
            # reference to a dead enemy.
            # Very, very, very important.
            game.enemies[:] = [enemy for enemy in game.enemies if enemy.dead == False]

            # Now show all of the ones that exist.
            for enemy in game.enemies:
                self.screen.blit(enemy.image, enemy.rect)
                
        except NameError:
            pass

    def update_explosions(self):
        # Need list comprehension like the others.
        self.explosions = self.explosions

    def update(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(player.image, player.rect)
        self.update_enemies()
        self.update_bullets()
        self.update_text()

    def bullet_collision(self, bullet, target):
        # Bullet collision detects the death of target! Very important!
        bullet.exploded = True
        bullet.speed = (bullet.speed / DEAD_BULLET_SPEED_FACTOR)
        target.damaged_by.append(bullet)
        target.health -= 1
        target.damage_cooldown = True
        # CHECK DEAD SCRIPT!
        if target.health <= 0:
            player.score += 1
            self.kill_target(target)

    def kill_target(self, target):
        target.dead = True
        # Trying to clear the references to a dead bullet object.
        # If lag occurs, this is a possible source.
        try:
            del target.damaged_by[:]
        except NameError:
            pass

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
        self.x = random.randint(0, game.screen_size[0]-32)
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
        self.damaged_by = []
        self.reverse = True

    def get_movement(self):
        # Not doing this yet.
        return 0

    def update_position(self):
        self.y += self.speed
        self.x += self.get_movement()
        self.rect.topleft = (self.x, self.y)

class Eye(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.speed = random.randint(5, 20)/5
        self.health = 1
        self.damage_wait = 15
        self.movement_factor = 2
        self.movement_x = 5
        self.movement_destination = (self.x + self.movement_x)

class Grunt(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.speed = 0.60
        self.health = 3
        self.damage_wait = 25
        self.movement_factor = 1
        self.movement_x = 1
        self.movement_destination = (self.x + self.movement_x)

class Speedy(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.speed = random.randint(20, 40)/5
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

    def check_collision(self, enemy):
        # PLAYER HEALTH DOESNT MATTER YET
        # NEED TO EXPAND
        if self.rect.colliderect(enemy.rect) and enemy.dead == False and self.damage_cooldown == False:
            self.health -= 1
            self.damage_cooldown = True

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

class Explosion(object):
    def __init__(self, bullet_id):
        self.explosion_id = bullet_id

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
    (5, 0), " | Powerups: %i | " % player.powerups, 24, (244, 212, 244), (10, 10, 10), 'powerup')
                         )
game.text_objects.append(Text(
    (130, 0), "  |  Press 1 to activate powerup  |  Spacebar to shoot basic gun  |  Q to shoot explosive gun  |  ", 18, (212, 212, 244), (10, 10, 10), 'info')
                         )
game.text_objects.append(Text(
    (5, 18), " | Level: %i | Score: %i | Enemies leaked: %i | " % (game.wave_level, player.score, game.enemies_leaked), 24, (240, 180, 192), (10, 10, 10), 'score'
    ))


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
