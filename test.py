class Bullet(object):
    def __init__(self, alive):
        self.alive = alive
bullets = []
for i in range(0, 4):
    bullets.append(Bullet(True))
    bullets.append(Bullet(False))

for i in range(0, len(bullets)):
    print bullets[i].alive
bullets = [bullet for bullet in bullets if bullet.alive == False]
for i in range(0, len(bullets)):
    print bullets[i].alive
