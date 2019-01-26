#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math

class GameBall:
    def __init__(self,img):
        self.speed = [0,0]
        self.gamenum = 0
        self.bitmap = pygame.image.load(img)
        self.bitmap.set_colorkey((0,0,0))

    def reset(self, player):
        if player.getX() < 320:
            self.x = 12
        else:
            self.x = 618
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

    def increaseGameNum(self):
        self.gamenum += 1

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

    def getServicePl1(self):
        if self.gamenum == 0:
            return True
        else:
            if math.ceil((self.gamenum + 1) / 2) % 2:
                return False
            else:
                return True

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

class Score:
    def __init__(self, goal):
        self.pnt = [0, 0]
        self.goal = goal
        self.font = pygame.font.Font('img/slkscr.ttf', 20)

    def displayScore(self, screen):
        textscore = str(' - ').join([str(s) for s  in self.pnt])
        score_text = self.font.render(textscore, True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.centerx = 320
        score_rect.y = 5
        screen.blit(score_text, score_rect)
        pygame.display.update(score_rect)
    
    def setScore(self, player):
        return_state = 0
        self.pnt[player.getId()] += 1
        if self.pnt[player.getId()] >= self.goal:
            return_state = 2
        return return_state

    def displayWinner(self, screen):
        text_win = ""
        if self.pnt[0] == self.goal:
            text_win = 'vince la partita  Player 1'
        elif self.pnt[1] == self.goal:
            text_win = 'vince la partita Player 2'

        if text_win != '':
            winner_text = self.font.render(text_win, True, (255, 255, 255))
            winner_rect = winner_text.get_rect()
            winner_rect.centerx = 320
            winner_rect.y = 200
            screen.blit(winner_text, winner_rect)
            pygame.display.update(winner_rect)

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
    player2 = Paddle(628, 292, 'img/paddle_vert.png', 1)

    ball = GameBall('img/ball_base.png')
    ball.reset(player1)
    score = Score(2)
    score.displayScore(screen)
    
    quit = 0
    gamestate = 0

    while quit == 0:
        screen.blit(backdrop, (0,0))

        for ourevent in pygame.event.get():
            if ourevent.type == pygame.QUIT:
                quit = 1
            if ourevent.type == pygame.KEYDOWN:

                # Player 1 controls
                if ourevent.key == pygame.K_z and gamestate < 2:
                    player1.addY(5)
                    if gamestate == 0 and ball.getServicePl1():
                        if ball.getY() < 445:
                            ball.addY(5)
                
                if ourevent.key == pygame.K_a and gamestate < 2:
                    player1.addY(-5)
                    if gamestate == 0 and ball.getServicePl1():
                        if ball.getY() > 63:
                            ball.addY(-5)
                
                if ourevent.key == pygame.K_s and gamestate < 2:
                    if gamestate == 0 and ball.getServicePl1():
                        ball.start(3, 3)
                        gamestate = 1
                
                # Player 2 controls
                if ourevent.key == pygame.K_l and gamestate < 2:
                    player2.addY(5)
                    if gamestate == 0 and not ball.getServicePl1():
                        if ball.getY() < 445:
                            ball.addY(5)
                
                if ourevent.key == pygame.K_p and gamestate < 2:
                    player2.addY(-5)
                    if gamestate == 0 and not ball.getServicePl1():
                        if ball.getY() > 63:
                            ball.addY(-5)
                
                if ourevent.key == pygame.K_o and gamestate < 2:
                    if gamestate == 0 and not ball.getServicePl1():
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
                ball.increaseGameNum()
                gamestate = score.setScore(player2)
                if gamestate < 2:
                    pygame.time.delay(500)
                    if ball.getServicePl1():
                        ball.reset(player1)
                    else:
                        ball.reset(player2)
                else:
                    ball.reset(player2)
        elif ball.getX() >= 619:
            diff_pl2_x, diff_pl2_y = player2.diffPos(ball)
            if diff_pl2_x < 10 and (diff_pl2_y < 40 and diff_pl2_y > -10):
                ball.setSpeedX(-ball.speedX())
                if (ball.speedY() * player2.dirY()) < 0:
                    ball.setSpeedY(-ball.speedY())
            else:
                # palla persa da player2
                ball.increaseGameNum()
                gamestate = score.setScore(player1)
                if gamestate < 2:
                    pygame.time.delay(500)
                    if ball.getServicePl1():
                        ball.reset(player1)
                    else:
                        ball.reset(player2)
                else:
                    ball.reset(player1)

        if ball.getX() >= 629:
            ball.setSpeedX(-ball.speedX())
        
        player1.render(screen)
        player2.render(screen)
        ball.render(screen)
        score.displayScore(screen)
        if gamestate == 2:
            winplayer = score.displayWinner(screen)

        pygame.display.update()
        pygame.time.delay(2)

    return 0

# --------------------------------------------------------------
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))





