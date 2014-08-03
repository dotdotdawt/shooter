import pygame

# Text globals
TEXT_POINTS = {
    'powerup': (5, 18),
    'info': (5, 0),
    'score': (110, 18)
    }
TEXT_COLORS = {
    'powerup': (240, 180, 192),
    'info': (220, 212, 244),
    'score': (240, 180, 192)
    }
TEXT_SIZES = {
    'powerup': 24,
    'info': 18,
    'score': 24
    }
TEXT_BG = (10, 10, 10)

class Text(object):

    
    def __init__(self, text_type):
        self.x, self.y = TEXT_POINTS[text_type]
        self.size = TEXT_SIZES[text_type]
        self.color = TEXT_COLORS[text_type]
        self.bg_color = TEXT_BG
        self.text_type = text_type
        self.initialize_pygame_object()

    def initialize_pygame_object(self):
        self.string = "" # Set it to empty for now, it gets updated
        self.aa = True
        self.type = 'freesansbold.tff'
        self.font = pygame.font.SysFont(self.type, self.size)
        self.surf = self.font.render(self.string, self.aa, self.color, self.bg_color)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (self.x, self.y)
