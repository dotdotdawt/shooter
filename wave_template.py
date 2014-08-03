import random

class Wave(object):
    # Simply holds the data for a wave type
    # Give a list in order to create wave. game constant ENEMY_TYPES has the order
    def __init__(self, name, enemy_amounts):
        self.name = name
        self.enemy_types = [
            'eye', 'grunt', 'speedy'
        ]
        self.enemy_amounts = {}
        for i in range(0, len(self.enemy_types)):
            self.enemy_amounts[self.enemy_types[i]] = enemy_amounts[i]
        self.chaos_wave()    

    def chaos_wave(self):
        self.chaos = False
        is_chaos = random.randint(0, 100)
        if is_chaos == 1:
            self.eye += random.randint(0, int(self.enemy_amounts['eye']))
            self.grunt += random.randint(0, int(self.enemy_amounts['grunt']))
            self.speedy += random.randint(0, int(self.enemy_amounts['speedy']))
            print '| This game has generated a chaos wave for %i ' % self.name
            self.chaos = True
