import pygame
from pygame import mixer
import random
import math
from threading import Thread
from time import sleep
import pickle

pygame.init()
score = 0
highscore = 0
WIDTH = 800
HEIGHT = 600
playerX = 400
playerY = 300
xv = 0
yv = 0
angle = 0
left = False
right = False
up = False
down = False
beamstate = 0
beaming = False
needast = True
running = True
alive = True
started = False
clock = pygame.time.Clock()
velocityvalues = [-1, 0, 1]
playerimg = pygame.image.load('assets\\ufo.png')
playerrect = pygame.Rect((1, 1), (1, 1))
beamrect = pygame.Rect((1, 1), (1, 1))
tractorimgs = [pygame.image.load('assets\\tractor beam0.png'), pygame.image.load('assets\\tractor beam1.png'),
               pygame.image.load('assets\\tractor beam2.png')]
tractorsound = mixer.Sound('assets\\tractor beam sound.wav')
exploder = mixer.Sound('assets\\explosion.wav')
pointsounds = [mixer.Sound('assets\\pop0.wav'), mixer.Sound('assets\\pop1.wav'), mixer.Sound('assets\\pop2.wav')]
bg = pygame.image.load('assets\\background.jpg')
asteroidimg = pygame.image.load('assets\\asteroid.png')
asteroids = []
alienimgs = [pygame.image.load('assets\\alien0.png'), pygame.image.load('assets\\alien1.png'), pygame.image.load('assets\\alien2.png')]
aliens = []
gofont = pygame.font.SysFont('Calibri', 48)
scorefont = pygame.font.SysFont('Times New Roman', 50)
icon = pygame.image.load('assets\\stars.png')
mixer.music.load('assets\\background.mp3')
mixer.music.play(-1)


def saveshs():
    global highscore
    filename = 'assets\\highscore.pk'
    with open(filename, 'wb') as file:
        try:
            pickle.dump(highscore, file)
        except Exception as e:
            print(e)
            highscore = 0


def loadhs():
    global highscore
    filename = 'assets\\highscore.pk'
    with open(filename, 'rb') as fi:
        try:
            highscore = pickle.load(fi)
        except Exception as e:
            print(e)
            highscore = 0


def gameover():
    tractorsound.stop()
    exploder.play()
    global running
    global alive
    global highscore
    global aliens
    alive = False
    gotext = gofont.render('Game Over!', True, (255, 255, 255))
    ngtext = gofont.render('press space to continue', False, (255, 255, 255))
    asteroids.clear()
    aliens.clear()
    pygame.display.flip()
    while not alive:
        setscore()
        window.blit(gotext, (300, 300))
        window.blit(ngtext, (230, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveshs()
                running = False
                alive = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global playerY
                    global playerX
                    global xv
                    global yv
                    global angle
                    global left
                    global right
                    global up
                    global down
                    global beamstate
                    global beaming
                    global score
                    playerX = 400
                    playerY = 300
                    xv = 0
                    yv = 0
                    angle = 0
                    left = False
                    right = False
                    up = False
                    down = False
                    beamstate = 0
                    beaming = False
                    alive = True
                    score = 0


def addast():
    global asteroids
    asteroids.append(asteroid(834,
                              random.randint(100, 500),
                              random.randint(3, 7) / -2,
                              random.choice(velocityvalues) / 3))


def setscore():
    global score
    global highscore
    scoretext = scorefont.render(f'Score: {score}', False, 'white')
    if score > highscore:
        highscore = score
    highscoretext = scorefont.render(f'Highscore: {highscore}', False, 'white')
    window.blit(scoretext, (5, 0))
    window.blit(highscoretext, (5, 50))


def addasteroids():
    num = 1
    while running:
        if alive:
            addast()
            num += 1
            aps = round(1 / math.log(num) * 2, 4)  # longer game = more asteroids
            sleep(aps)
        else:
            num = 1


def beam(x, y):
    global beamstate
    global beamrect
    beamrect = pygame.Rect((x + 5, y - 15), (50, 80))
    # pygame.draw.rect(window,'green',beamrect)
    if beamstate <= 0:
        window.blit(tractorimgs[0], (x, y))
    elif beamstate <= 75:
        window.blit(tractorimgs[1], (x, y))
    elif beamstate <= 150:
        window.blit(tractorimgs[2], (x, y))
    else:
        beamstate = -75


def collisiondetection(astX, astY, playersX, playersY):
    distance = math.sqrt((math.pow(astX - playersX, 2)) +
                         (math.pow(astY - playersY, 2)))
    if distance < 64:
        return True


def alienhitast(astX, astY, alienX, alienY):
    distance = math.sqrt((math.pow(astX - alienX, 2)) +
                         (math.pow(astY - alienY, 2)))
    if distance < 48:
        return True


class asteroid:

    def rotate(self):  # spin
        if self.x >= -100:
            self.newimg = pygame.transform.rotate(self.image, self.angle)
            self.angle += 0.1
            window.blit(self.newimg, (self.x, self.y))

    def move(self):
        if self.x >= -100:
            self.x += self.vx
            self.y += self.vy
            self.offset += 0.05
            self.rect = pygame.Rect((self.x + self.offset, self.y + self.offset / 3), (64, 64))
            # pygame.draw.rect(window, 'red', self.rect)  # draw hitbox
            window.blit(self.newimg, (self.x, self.y))

    def __init__(self, x, y, vx, vy):
        self.image = asteroidimg
        self.angle = 0
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.rect = pygame.Rect((self.x, self.y), (64, 64))
        self.offset = 0
        self.newimg = None


def player(x, y):
    global playerrect
    playerrect = pygame.Rect((x, y + 10), (64, 40))
    # pygame.draw.rect(window, 'red', playerrect)  # draw hitbox
    window.blit(playerimg, (x, y))


class alien:
    def move(self):
        if self.x >= -50:
            if self.x > 768 or self.x < 0:
                self.vx *= -1
            if self.y > 568 or self.y < 0:
                self.vy *= -1
            self.x += self.vx
            self.y += self.vy
            self.rect = pygame.Rect((self.x, self.y), (32, 32))
            # pygame.draw.rect(window, 'red', self.rect)  # draw hitbox
            window.blit(self.img, (self.x, self.y))

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.vx = random.choice(velocityvalues)
        self.vy = random.choice(velocityvalues)
        self.img = img
        self.rect = pygame.Rect((self.x, self.y), (32, 32))


def suckalien(alienX, alienY, beamX, beamY):
    distancex = math.sqrt((math.pow(beamX - alienX, 2)))
    distancey = math.sqrt((math.pow(beamY - alienY, 2)))
    if distancex < 40 and distancey < 80:
        if distancex < 5 and distancey < 15:
            return 2
        elif distancex < 5:
            return 1.1
        else:
            return 1
    else:
        return 0


def addaliens():
    global aliens
    while running:
        if alive:
            aliens.append(alien(random.randint(50, 750), random.randint(50, 550), random.choice(alienimgs)))
            sleep(2)


if __name__ == '__main__':
    loadhs()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Space")
    startfont = pygame.font.SysFont('Arial', 50)
    starttext = startfont.render('Press Any Key to Start', True, 'white')
    how2playtext1 = pygame.font.SysFont('Arial', 30).render('Press space to activate tractor beam', True, 'white')
    how2playtext2 = pygame.font.SysFont('Arial', 30).render('save the aliens from flying meteors!', True, 'white')
    window.blit(bg, (0, 0))
    window.blit(starttext, (200, 270))
    window.blit(how2playtext1, (210, 330))
    window.blit(how2playtext2, (215, 370))
    pygame.display.flip()
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveshs()
                started = True
                running = False
            if event.type == pygame.KEYDOWN:
                started = True
    Thread(target=addasteroids, daemon=True).start()  # start spawning asteroids
    Thread(target=addaliens, daemon=True).start()

    while running:
        window.fill((0, 0, 0))
        window.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveshs()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down = True
                if event.key == pygame.K_SPACE:
                    beaming = True
                    tractorsound.play(-1, 0, 200)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down = False
                if event.key == pygame.K_SPACE:
                    beaming = False
                    beamrect = pygame.Rect((1, 1), (-50, 0))
                    tractorsound.stop()
        if left:
            xv = -3
        if right:
            xv = 3
            if left:
                xv = 0
        if up:
            yv = -3
        if down:
            yv = 3
            if up:
                yv = 0
        if not left:
            if not right:
                xv = 0
        if not up:
            if not down:
                yv = 0
        playerX += xv
        playerY += yv
        if playerX >= 736:
            playerX = 736
        if playerX <= 0:
            playerX = 0
        if playerY >= 536:
            playerY = 536
        if playerY <= 0:
            playerY = 0
        for i, ast in enumerate(asteroids):
            if ast.x >= -64:
                ast.rotate()
                ast.move()
                if collisiondetection(ast.rect.centerx,
                                      ast.rect.centery,
                                      playerrect.centerx,
                                      playerrect.centery):
                    gameover()
                for index, al in enumerate(aliens):
                    if alienhitast(ast.rect.centerx,
                                   ast.rect.centery,
                                   al.rect.centerx,
                                   al.rect.centery):
                        aliens.pop(index)

            else:
                asteroids.pop(i)
                # print(len(asteroids))
        for ind, a in enumerate(aliens):
            a.move()
            grav = suckalien(a.rect.centerx, a.rect.centery, beamrect.centerx, beamrect.centery)
            if grav == 0:
                pass
            elif grav == 1:
                try:
                    a.vx += 2 / (beamrect.centerx - a.rect.centerx)
                    a.vy += 3 / (beamrect.centery - a.rect.centery)
                except ZeroDivisionError:
                    pass
            elif grav == 1.1:
                a.vx = (beamrect.centerx - a.rect.centerx)
                a.vy = (beamrect.centery - a.rect.centery) / 10
            elif grav == 2:
                aliens.pop(ind)
                random.choice(pointsounds).play()
                score += 1

        beamstate += 1
        if beaming:
            beam(playerX, playerY + 18)
        player(playerX, playerY)
        setscore()
        pygame.display.flip()
        clock.tick(144)
