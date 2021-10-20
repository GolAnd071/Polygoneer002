import pygame
import math

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

phi, color = 0, BLUE

balls, periodBall = [], 0

lDown, rDown = False, False

pygame.init()

screenWidth, screenHeight = 1280, 960
FPS = 60
screen = pygame.display.set_mode((screenWidth, screenHeight))


class Ball:
    ''' Represents a player's shot '''

    def __init__(self, x, y, vx, vy, color):
        ''' Creates a Ball
            x, y    - coordinates of the Ball 
            vx, vy  - speed of the Ball 
            color   - color of the Ball '''

        self.x, self.y, self.vx, self.vy, self.color = x, y, vx, vy, color

    def updateBall(self):
        ''' Updates the conditions of the Ball '''

        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)


def updatePlayer():
    ''' Updates the conditions of the player '''

    player = pygame.Surface((300, 300))
    pygame.draw.polygon(
        player,
        color,
        [
            (50, 150),
            (100, 150 - 50 * 3 ** 0.5),
            (200, 150 - 50 * 3 ** 0.5),
            (225, 150 - 25 * 3 ** 0.5),
            (275, 150 - 25 * 3 ** 0.5),
            (275, 150 + 25 * 3 ** 0.5),
            (225, 150 + 25 * 3 ** 0.5),
            (200, 150 + 50 * 3 ** 0.5),
            (100, 150 + 50 * 3 ** 0.5),
        ],
        10,
    )
    player = pygame.transform.rotate(player, phi)
    screen.blit(
        player,
        (
            (
                screenWidth
                - 300
                * (abs(math.sin(math.radians(phi))) + abs(math.cos(math.radians(phi))))
            )
            / 2,
            (
                screenHeight
                - 300
                * (abs(math.sin(math.radians(phi))) + abs(math.cos(math.radians(phi))))
            )
            / 2,
        ),
    )


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while finished != True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lDown = True
            if event.key == pygame.K_RIGHT:
                rDown = True
            if event.key == pygame.K_z:
                color = GREEN
                if periodBall == 0:
                    balls.append(
                        Ball(
                            screenWidth / 2 + 150 * math.cos(math.radians(phi)),
                            screenHeight / 2 - 150 * math.sin(math.radians(phi)),
                            10 * math.cos(math.radians(phi)),
                            -10 * math.sin(math.radians(phi)),
                            GREEN,
                        )
                    )
                    periodBall = 30
            if event.key == pygame.K_x:
                color = BLUE
                if periodBall == 0:
                    balls.append(
                        Ball(
                            screenWidth / 2 + 150 * math.cos(math.radians(phi)),
                            screenHeight / 2 - 150 * math.sin(math.radians(phi)),
                            10 * math.cos(math.radians(phi)),
                            -10 * math.sin(math.radians(phi)),
                            BLUE,
                        )
                    )
                    periodBall = 30
            if event.key == pygame.K_c:
                color = RED
                if periodBall == 0:
                    balls.append(
                        Ball(
                            screenWidth / 2 + 150 * math.cos(math.radians(phi)),
                            screenHeight / 2 - 150 * math.sin(math.radians(phi)),
                            10 * math.cos(math.radians(phi)),
                            -10 * math.sin(math.radians(phi)),
                            RED,
                        )
                    )
                    periodBall = 30
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                lDown = False
            if event.key == pygame.K_RIGHT:
                rDown = False

    if lDown == True:
        phi += 2
    if rDown == True:
        phi -= 2
    if periodBall > 0:
        periodBall -= 1
    updatePlayer()
    for ball in balls:
        if ball.x < 0 or ball.x > screenWidth or ball.y < 0 or ball.y > screenHeight:
            balls.remove(ball)
        ball.updateBall()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
