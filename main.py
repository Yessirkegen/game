import datetime
import os
import random
import pygame

pygame.init()
pygame.mixer.init()


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("run")
coin_sound = pygame.mixer.Sound("mus/mixkit-bonus-earned-in-video-game-2058.wav")
death_sound = pygame.mixer.Sound("mus/mixkit-boxer-getting-hit-2055.wav")
Ico = pygame.image.load("assets/Tile.png")
pygame.display.set_icon(Ico)

pygame.mixer.music.load("mus/cruising-down-8bit-lane-159615.mp3")
pygame.mixer.music.set_volume(1.0)

width = 75
height = 75

RUNNING = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Run__00{}.png".format(i))), (width, height)) for i in range(10)]
JUMPING = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Jump__006.png")), (width, height))
DUCKING = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Slide__007.png")), (width, height))]
SMALL_CACTUS = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "DeadBush.png")), (width, height))]
LARGE_CACTUS = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Tree.png")), (width, height))]
BIRD = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Skeleton.png")), (100, 50))]
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
COIN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "COIN.png")), (30, 30))
FONT_COLOR = (0, 0, 0)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        self.index += 1
        if self.index >= 9:
            self.index = 0


class Coin:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 200)
        self.image = pygame.transform.scale(COIN, (50, 50))
        self.rect = self.image.get_rect()
        self.coin_sound = coin_sound

    def update(self):
        self.x -= game_speed
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x < -self.rect.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
            self.coin_sound.play()


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, coins
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()

    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    coins = []
    death_count = 0
    pause = False


    pygame.mixer.music.play(-1)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]
            if not score_ints:
                highscore = 0
            else:
                highscore = max(score_ints)
            if points > highscore:
                highscore = points
            text = font.render(
                "High Score: " + str(highscore) + "  Points: " + str(points) + "  Speed: " + str(game_speed),
                True,
                FONT_COLOR,
            )
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def unpause():
        nonlocal pause, run
        pause = False
        run = True
        pygame.mixer.music.unpause()

    def paused():
        nonlocal pause
        pause = True
        pygame.mixer.music.pause()
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render(
            "Game Paused, Press 'u' to Unpause", True, FONT_COLOR
        )
        arrow_text = font.render(
            "Use UP arrow key or SPACE to jump", True, FONT_COLOR
        )
        duck_text = font.render(
            "Use DOWN arrow key to duck", True, FONT_COLOR
        )


        pause_text = font.render(
            "Press 'p' to Pause/Resume", True, FONT_COLOR
        )


        info_text1 = font.render(
            "Additional instruction line 1", True, FONT_COLOR
        )
        info_text2 = font.render(
            "Additional instruction line 2", True, FONT_COLOR
        )

        textRect = text.get_rect()
        arrow_rect = arrow_text.get_rect()
        duck_rect = duck_text.get_rect()

        pause_rect = pause_text.get_rect()

        info_rect1 = info_text1.get_rect()
        info_rect2 = info_text2.get_rect()

        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        arrow_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        duck_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

        pause_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)

        info_rect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)
        info_rect2.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        unpause()
                    elif event.key == pygame.K_p:
                        unpause()
                        return

            SCREEN.blit(text, textRect)
            SCREEN.blit(arrow_text, arrow_rect)
            SCREEN.blit(duck_text, duck_rect)
            SCREEN.blit(pause_text, pause_rect)
            SCREEN.blit(info_text1, info_rect1)
            SCREEN.blit(info_text2, info_rect2)
            pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        current_time = datetime.datetime.now().hour
        # if 7 < current_time < 19:
        #     SCREEN.fill((255, 255, 255))
        # else:
        SCREEN.fill((0, 0, 0))

        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + SCREEN_WIDTH, y_pos_bg))

        x_pos_bg -= game_speed
        if x_pos_bg <= -SCREEN_WIDTH:
            x_pos_bg = 0

        pygame.draw.rect(SCREEN, (139, 69, 19), (0, 400, SCREEN_WIDTH, 200))
        pygame.draw.rect(SCREEN, (139, 69, 19), (0, 0, SCREEN_WIDTH, 50))

        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS[0]))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS[0]))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD[0]))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        if len(coins) == 0:
            coins.append(Coin())

        for coin in coins:
            coin.draw(SCREEN)
            coin.update()
            if player.dino_rect.colliderect(coin.rect):
                coins.remove(coin)
                points += 10

        score()

        clock.tick(30)
        pygame.display.update()

    pygame.mixer.music.stop()

def menu(death_count):
    global points
    global FONT_COLOR
    run = True


    menu_bg = pygame.image.load(
            "assets/hint3.png")
    menu_bg = pygame.transform.scale(menu_bg, (300, 150))

    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR = (0, 0, 0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR = (255, 255, 255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font(pygame.font.get_default_font(), 30)

        SCREEN.blit(menu_bg, (0, 0))

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render(
                "Press any Key to Restart", True, FONT_COLOR
            )
            score = font.render(
                "Your Score: " + str(points), True, FONT_COLOR
            )
            scoreRect = score.get_rect()
            scoreRect.center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50,
            )
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = f.read()
                score_ints = [int(x) for x in score.split()]
            highscore = max(score_ints) if score_ints else 0
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 100,
            )
            SCREEN.blit(hs_score_text, hs_score_rect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(
            RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140)
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                death_sound.play()
                run = False
                # death_sound.play()

                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

menu(0)
