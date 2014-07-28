import pygame
import sys

pygame.init()
explosions = []

class Game(object):
    def __init__(self):
        self.playing = True
        self.screen_size = (400, 400)
        self.bg_color = (30, 0, 0)
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.fps = 60

class Explosion(object):
    def __init__(self):
        self.frames = []
        self.frame_pos = []
        self.frame_index = 0
        self.size = 118
        self.sprite_sheet = pygame.image.load('Explosion-Sprite-Sheet.png')
        self.setup_frames()

    def get_image(self, coords, size):
        width, height = size
        x, y = coords
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        #image = pygame.transfrom.scale(image,
        #                               (int(rect.width*2.0),
        #                                int(rect.height*2.0)))

        return image

    def setup_frames(self):
        for i in range(0, 4):
            self.frame_pos.append((i*self.size, 0, self.size, self.size))
        for i in range(0, len(self.frame_pos)):
            self.frames.append(self.get_image(
                (self.frame_pos[i][0], self.frame_pos[i][1]),
                (self.size, self.size)
                ))
        
game = Game()
explosions.append(Explosion())

while game.playing:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                game.playing = False
            if event.key == pygame.K_q:
                if explosions[0].frame_index <= len(explosions[0].frames)-2:
                    explosions[0].frame_index += 1
                    print len(explosions[0].frames)
                else:
                    explosions[0].frame_index = 0
    game.screen.fill(game.bg_color)
    for i in range(0, len(explosions)):
        explosions[i].x = 30
        explosions[i].y = 30
        explosions[i].image = explosions[i].frames[explosions[i].frame_index]
        explosions[i].rect = explosions[i].image.get_rect()
        explosions[i].rect.topleft = (explosions[i].x, explosions[i].y)
        game.screen.blit(explosions[i].image, explosions[i].rect)
    pygame.display.flip()
    game.fps_clock.tick(game.fps)

pygame.quit()
sys.exit(0)
