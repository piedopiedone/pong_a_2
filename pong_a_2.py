#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

class GameBall:
    def __init__(self,img):
        self.speed = [0,0]
        self.bitmap = pygame.image.load(img)
        self.bitmap.set_colorkey((0,0,0))

    def reset(self, player):
        self.x = 12
        self.y = player.getY() + 15
        self.speed = [0,0]

    def start(self, speedX, speedY):
        self.speed = [speedX, speedY]

    def addX(self, val):
        new_x = self.x + val
        if new_x < 640 and new_x > 0:
            self.x += val
        else:
            if new_x < 0:
                diff = abs(new_x)
                self.x = diff
            else:
                diff = new_x - 629
                self.x = 629 - diff
            self.setSpeedX(-self.speedX())

    def addY(self, val):
        new_y = self.y + val
        if new_y <= 466 and new_y >= 42:
            self.y += val
        else:
            if new_y < 42:
                diff = 42 - new_y
                self.y = 42 + diff
            else:
                diff = new_y - 466
                self.y = 466 - diff
            self.setSpeedY(-self.speedY())

    def makeStep(self):
        self.addX(self.speed[0])
        self.addY(self.speed[1])

    def setSpeedX(self, val):
        self.speed[0] = val

    def speedX(self):
        return self.speed[0]

    def setSpeedY(self, val):
        self.speed[1] = val

    def speedY(self):
        return self.speed[1]

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def render(self, screen):
        self.makeStep()
        screen.blit(self.bitmap, (self.x, self.y))

class Paddle:
    def __init__(self, xpos, ypos, img, pl_id):
        self.x = xpos
        self.y = ypos
        self.oldy = ypos
        self.bitmap = pygame.image.load(img)
        self.bitmap.set_colorkey((0,0,0))
        self.pl_id = pl_id

    def getId(self):
        return self.pl_id
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def addY(self, val):
        if (self.y + val) < 435 and (self.y + val) > 43:
            self.oldy = self.y
            self.y += val
    def dirY(self):
        return self.y -self.oldy
    def diffPos(self, ball):
        diff_posx = abs(ball.getX() - self.x)
        diff_posy = ball.getY() - self.y
        return (diff_posx, diff_posy)
    def render(self, screen):
        screen.blit(self.bitmap, (self.x, self.y))


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
def main(args):
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.key.set_repeat(1,1)
    pygame.display.set_caption("python pong")
    backdrop = pygame.image.load('img/pong_a_2.bmp')

    player1 = Paddle(0, 292, 'img/paddle_vert.png', 0)

    ball = GameBall('img/ball_base.png')
    ball.reset(player1)
    
    quit = 0
    gamestate = 0

    while quit == 0:
        screen.blit(backdrop, (0,0))

        for ourevent in pygame.event.get():
            if ourevent.type == pygame.QUIT:
                quit = 1
            if ourevent.type == pygame.KEYDOWN:

                if ourevent.key == pygame.K_z:
                    player1.addY(5)
                    if (gamestate == 0):
                        if ball.getY() < 445:
                            ball.addY(5)
                
                if ourevent.key == pygame.K_a:
                    player1.addY(-5)
                    if (gamestate == 0):
                        if ball.getY() > 63:
                            ball.addY(-5)
                
                if ourevent.key == pygame.K_s:
                    if (gamestate == 0):
                        ball.start(3, 3)
                        gamestate = 1
                
                if ourevent.key == pygame.K_ESCAPE:
                    quit = 1

        if ball.getX() <= 9:
            diff_pl1_x, diff_pl1_y = player1.diffPos(ball)
            if diff_pl1_x < 10 and (diff_pl1_y < 40 and diff_pl1_y > -10):
                ball.setSpeedX(-ball.speedX())
                if (ball.speedY() * player1.dirY()) < 0:
                    ball.setSpeedY(-ball.speedY())
            else:
                # palla persa da player1
                gamestate = 0
                ball.reset(player1)

        if ball.getX() >= 629:
            ball.setSpeedX(-ball.speedX())
        
        player1.render(screen)
        ball.render(screen)
        pygame.display.update()
        pygame.time.delay(2)

    return 0

# --------------------------------------------------------------
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))





