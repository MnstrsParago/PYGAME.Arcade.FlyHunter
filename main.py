import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

score = 0

def menu(screen):
    start = pygame.font.Font(None, 36)
    textStart = start.render('Start', True, (255, 255, 255))
    text_rect = textStart.get_rect(center=(WIDTH//2,HEIGHT//2))
    screen.blit(textStart, text_rect)
    pygame.display.update()
    # button start
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    return
            elif event.type == pygame.MOUSEMOTION:
                if text_rect.collidepoint(pygame.mouse.get_pos()):
                    textStart = start.render('Start', True, (255,0,0))
                    screen.blit(textStart, text_rect)
                    pygame.display.update()
                else:
                    textStart = start.render('Start', True, (255,255,255))
                    screen.blit(textStart, text_rect)
                    pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONUP:
                if text_rect.collidepoint(pygame.mouse.get_pos()):
                    textStart = start.render('Start', True, (0,0,255))
                    screen.blit(textStart, text_rect)
                    pygame.display.update()
                else:
                    textStart = start.render('Start', True, (255,255,255))
                    screen.blit(textStart, text_rect)
                    pygame.display.update()
            elif event.type == pygame.KEYUP:
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    return

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.direction = "right"

        self.left = [
            pygame.image.load('left/1.png'),
            pygame.image.load('left/2.png'),
            pygame.image.load('left/3.png'),
            pygame.image.load('left/4.png'),
            pygame.image.load('left/5.png'),
        ]
        self.lC = 0
        self.right = []
        self.rC = 0
        for bird in self.left:
            self.right.append(pygame.transform.flip(bird, True, False))
        self.prev_x = self.rect.centerx

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

        # Сравниваем текущую позицию с предыдущей
        if self.rect.centerx > self.prev_x:
            self.direction = "right"
        else:
            self.direction = "left"
        self.prev_x = self.rect.centerx

        # Обновляем анимацию только при смене направления
        if self.direction == "right":
            if self.rC == 4:
                self.rC = 0
            else:
                self.image = self.right[self.rC]
                self.rC += 1
        else:
            if self.lC == 4:
                self.lC = 0
            else:
                self.image = self.left[self.lC]
                self.lC += 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('fly.png'), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.dx = random.choice([-1, 1]) * random.randint(1, 3)
        self.dy = random.choice([-1, 1]) * random.randint(1, 3)
        self.alive = True

    def update(self):
        if self.alive:
            self.rect.x += self.dx
            self.rect.y += self.dy

            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.dx *= -1
            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.dy *= -1
        else:
                self.rect.x = 10000
                self.rect.y = 10000




all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


menu(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.direction = "left"
            elif event.key == pygame.K_RIGHT:
                player.direction = "right"


    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, enemies, False)
    for hit in hits:
        print("Player collided with enemy!")
        score += 1
        hit.alive = False

    screen.blit(pygame.transform.scale(pygame.image.load('backGoundAbda1.jpg'),(WIDTH,HEIGHT)),(0,0))
    all_sprites.draw(screen)
    font = pygame.font.Font(None, 36)
    scoreText = font.render(f"your score - {score}", True, (0, 0, 0))
    screen.blit(scoreText, (40, 40))
    pygame.display.flip()
    pygame.time.Clock().tick(240)
pygame.quit()
