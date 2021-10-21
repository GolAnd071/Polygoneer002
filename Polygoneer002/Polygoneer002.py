import pygame
import math
import random

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

phi, color = 0, BLUE

points = 0

balls, periodBall = [], 0
enemies, periodEnemy = [], 0
colors = [RED, GREEN, BLUE]

lDown, rDown = False, False

pygame.init()

screenWidth, screenHeight = 1280, 960
FPS = 60
screen = pygame.display.set_mode((screenWidth, screenHeight))

text = pygame.font.Font(pygame.font.get_default_font(), 25)


class Enemy:
    """Represents an enemy polygon"""

    def __init__(self, x, y, vx, vy, color, nSides):
        """Creates an Enemy
        x, y    - coordinates of the Enemy
        vx, vy  - speed of the Enemy
        color   - color of the Enemy
        nSides  - number of polygon sides"""

        self.x, self.y, self.vx, self.vy, self.color, self.nSides, self.a = (
            x,
            y,
            vx,
            vy,
            color,
            nSides,
            0,
        )

    def updateEnemy(self):
        """Updates the conditions of the Enemy"""

        self.x += self.vx
        self.y += self.vy
        self.a += 5
        enemy = pygame.Surface((100, 100), pygame.SRCALPHA)
        enemy.fill((0, 0, 0, 0))
        if self.nSides == 3:
            pygame.draw.polygon(
                enemy,
                self.color,
                [(50 - 25 * 3 ** 0.5, 75), (50, 0), (50 + 25 * 3 ** 0.5, 75)],
                5,
            )
        if self.nSides == 4:
            pygame.draw.polygon(
                enemy, self.color, [(0, 50), (50, 0), (100, 50), (50, 100)], 5
            )
        if self.nSides == 5:
            pygame.draw.polygon(
                enemy,
                self.color,
                [
                    (50, 0),
                    (
                        50 + 6.25 * (1 + 5 ** 0.5) * (10 - 2 * 5 ** 0.5) ** 0.5,
                        (125 - 25 * 5 ** 0.5) / 2,
                    ),
                    (
                        50 + 50 * (5 / 8 - 5 ** 0.5 / 8) ** 0.5,
                        50 + 12.5 * (1 + 5 ** 0.5),
                    ),
                    (
                        50 - 50 * (5 / 8 - 5 ** 0.5 / 8) ** 0.5,
                        50 + 12.5 * (1 + 5 ** 0.5),
                    ),
                    (
                        50 - 6.25 * (1 + 5 ** 0.5) * (10 - 2 * 5 ** 0.5) ** 0.5,
                        (125 - 25 * 5 ** 0.5) / 2,
                    ),
                ],
                5,
            )
        if self.nSides == 6:
            pygame.draw.polygon(
                enemy,
                self.color,
                [
                    (50, 0),
                    (50 + 25 * 3 ** 0.5, 25),
                    (50 + 25 * 3 ** 0.5, 75),
                    (50, 100),
                    (50 - 25 * 3 ** 0.5, 75),
                    (50 - 25 * 3 ** 0.5, 25),
                ],
                5,
            )
        enemy = pygame.transform.rotate(enemy, self.a)
        screen.blit(
            enemy,
            (
                (
                    2 * self.x
                    - 100
                    * (
                        abs(math.sin(math.radians(self.a)))
                        + abs(math.cos(math.radians(self.a)))
                    )
                )
                / 2,
                (
                    2 * self.y
                    - 100
                    * (
                        abs(math.sin(math.radians(self.a)))
                        + abs(math.cos(math.radians(self.a)))
                    )
                )
                / 2,
            ),
        )


class Ball:
    """Represents a player's shot"""

    def __init__(self, x, y, vx, vy, color):
        """Creates a Ball
        x, y    - coordinates of the Ball
        vx, vy  - speed of the Ball
        color   - color of the Ball"""

        self.x, self.y, self.vx, self.vy, self.color = x, y, vx, vy, color

    def updateBall(self):
        """Updates the conditions of the Ball"""

        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)


def updatePlayer():
    """Updates the conditions of the player"""

    player = pygame.Surface((150, 150))
    pygame.draw.polygon(
        player,
        color,
        [
            (25, 75),
            (50, 75 - 25 * 3 ** 0.5),
            (100, 75 - 25 * 3 ** 0.5),
            (112.5, 75 - 12.5 * 3 ** 0.5),
            (137.5, 75 - 12.5 * 3 ** 0.5),
            (137.5, 75 + 12.5 * 3 ** 0.5),
            (112.5, 75 + 12.5 * 3 ** 0.5),
            (100, 75 + 25 * 3 ** 0.5),
            (50, 75 + 25 * 3 ** 0.5),
        ],
        5,
    )
    player = pygame.transform.rotate(player, phi)
    screen.blit(
        player,
        (
            (
                screenWidth
                - 150
                * (abs(math.sin(math.radians(phi))) + abs(math.cos(math.radians(phi))))
            )
            / 2,
            (
                screenHeight
                - 150
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
                            screenWidth / 2 + 75 * math.cos(math.radians(phi)),
                            screenHeight / 2 - 75 * math.sin(math.radians(phi)),
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
                            screenWidth / 2 + 75 * math.cos(math.radians(phi)),
                            screenHeight / 2 - 75 * math.sin(math.radians(phi)),
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
                            screenWidth / 2 + 75 * math.cos(math.radians(phi)),
                            screenHeight / 2 - 75 * math.sin(math.radians(phi)),
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
        phi += 5
    if rDown == True:
        phi -= 5
    if periodBall > 0:
        periodBall -= 1
    if periodEnemy > 0:
        periodEnemy -= 1
    if periodEnemy == 0:
        b = random.randint(0, 359)
        enemies.append(
            Enemy(
                screenWidth / 2 + 1000 * math.cos(math.radians(b)),
                screenHeight / 2 - 1000 * math.sin(math.radians(b)),
                -5 * math.cos(math.radians(b)),
                5 * math.sin(math.radians(b)),
                colors[random.randint(0, 2)],
                random.randint(3, 6),
            )
        )
        periodEnemy = random.randint(60, 120)
    updatePlayer()
    for ball in balls:
        for enemy in enemies:
            if (ball.x - enemy.x) ** 2 + (
                ball.y - enemy.y
            ) ** 2 < 50 ** 2 and ball.color == enemy.color:
                balls.remove(ball)
                enemies.remove(enemy)
                points += 100
    for ball in balls:
        if ball.x < 0 or ball.x > screenWidth or ball.y < 0 or ball.y > screenHeight:
            balls.remove(ball)
            points -= 10
        ball.updateBall()
    for enemy in enemies:
        if (enemy.x - screenWidth / 2) ** 2 + (
            enemy.y - screenHeight / 2
        ) ** 2 < 75 ** 2:
            enemies.remove(enemy)
            points -= 200
        enemy.updateEnemy()
    if points < 0:
        finished = True
    screen.blit(text.render(str(points), 0, WHITE), (10, 10))
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
