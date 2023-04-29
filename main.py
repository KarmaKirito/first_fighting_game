import pygame
import sys
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 440
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption('Parralax test')
bg_images = []
scroll = 0
scroll_limit = False
ground_img = pygame.image.load('ground.png').convert_alpha()
ground_width = ground_img.get_width()
ground_height = ground_img.get_height()
for i in range(1, 6):
    bg_image = pygame.image.load('plx-{}.png'.format(i)).convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


class Player:
    def __init__(self, x, y, player, color):
        self.rect = pygame.Rect(x, y, 50, 100)
        self.player = player
        self.vel_y = 0
        self.vel_x = 0
        self.bullet_speed = 0
        self.ultimate_y_speed, self.ultimate_x_speed = 0, 0
        self.color = color
        self.jumped = False
        self.ultimate_available = False
        self.left = False
        self.has_attacked = False
        self.attacking = False
        self.moving = False
        self.sprint_limit = False
        self.attack_cooldown = 0
        self.attack_type = 0
        self.mana = 100
        self.health = 500

    def move(self, surface, target):
        if self.mana < 100:
            self.mana += 0.2
        speed = 10
        dx = 0
        dy = 0
        gravity = 2
        self.vel_x = 0
        self.vel_y += gravity
        self.moving = False
        dy += self.vel_y
        keys = pygame.key.get_pressed()
        if not self.attacking:
            if self.player == 1:
                if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                    if keys[pygame.K_a] and self.rect.left > 0:
                        dx -= speed
                        self.left = True
                    if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
                        dx += speed
                        self.left = False
                    if keys[pygame.K_w] and not self.jumped:
                        self.rect.height = 100
                        self.vel_y = -25
                        dy += self.vel_y
                        self.jumped = True
                    self.moving = True
                    if keys[pygame.K_s]:
                        self.vel_y = 10
                        dy += self.vel_y
                        self.rect.height = 50
                if not self.sprint_limit and self.moving and self.mana > 1:
                    if keys[pygame.K_y] and not self.left:
                        self.vel_x = 10
                        if self.mana > 1:
                            self.mana -= 1
                        if self.mana == 1:
                            self.sprint_limit = True
                    if keys[pygame.K_y] and self.left:
                        self.vel_x = -10
                        if self.mana > 1:
                            self.mana -= 1
                        if self.mana == 1:
                            self.sprint_limit = True
                if keys[pygame.K_r] or keys[pygame.K_t] or keys[pygame.K_q]:
                    self.attack(surface, target)
                    if keys[pygame.K_r]:
                        self.attack_type = 1
                    if keys[pygame.K_t]:
                        self.attack_type = 2
                        if self.mana > 0:
                            self.mana -= 0.5
                    if keys[pygame.K_q]:
                        if self.mana < 1:
                            self.ultimate_available = False
                        else:
                            self.ultimate_available = True
                        if self.ultimate_available:
                            self.attack_type = 3
                            if self.mana > 0:
                                self.mana -= 3
                        else:
                            self.attack_type = 0
            if self.player == 2:
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    if keys[pygame.K_LEFT] and self.rect.left > 0:
                        dx -= speed
                        self.left = True
                    if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                        dx += speed
                        self.left = False
                    if keys[pygame.K_UP] and not self.jumped:
                        self.rect.height = 100
                        self.vel_y = -25
                        dy += self.vel_y
                        self.jumped = True
                    self.moving = True
                    if keys[pygame.K_DOWN]:
                        self.vel_y = 10
                        dy += self.vel_y
                        self.rect.height = 50
                if not self.sprint_limit and self.moving and self.mana > 1:
                    if keys[pygame.K_KP3] and not self.left:
                        self.vel_x = 10
                        if self.mana > 1:
                            self.mana -= 1
                        if self.mana == 1:
                            self.sprint_limit = True
                    if keys[pygame.K_KP3] and self.left:
                        self.vel_x = -10
                        if self.mana > 1:
                            self.mana -= 1
                        if self.mana == 1:
                            self.sprint_limit = True
                if keys[pygame.K_KP1] or keys[pygame.K_KP2] or keys[pygame.K_KP5]:
                    self.attack(surface, target)
                    if keys[pygame.K_KP1]:
                        self.attack_type = 1
                    if keys[pygame.K_KP2]:
                        self.attack_type = 2
                    if keys[pygame.K_KP5]:
                        if self.mana == 100:
                            if self.ultimate_available:
                                self.attack_type = 3
                            self.mana -= 20
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - ground_height/3:
            self.vel_y = 0
            dy = SCREEN_HEIGHT - ground_height/3 - self.rect.bottom
            self.jumped = False
        dx += self.vel_x
        self.rect.x += dx
        self.rect.y += dy

    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.has_attacked = False

    def attack(self, surface, target):
        if not self.left:
            side = self.rect.centerx
            bullet_side = self.rect.right
            angle = -40
        else:
            side = self.rect.centerx - 2 * self.rect.width
            bullet_side = self.rect.left - 30
            angle = 40
        bullet_speed = self.bullet_speed
        if self.ultimate_y_speed <= 405:
            self.ultimate_y_speed += 15
            if self.ultimate_y_speed == 405:
                self.ultimate_y_speed = 0
        if self.left:
            if self.bullet_speed >= -200:
                self.bullet_speed -= 5
                if self.bullet_speed == -200:
                    self.bullet_speed = 0
            if self.ultimate_x_speed >= -300:
                self.ultimate_x_speed -= 10
                if self.ultimate_x_speed == -300:
                    self.ultimate_x_speed = 0
        else:
            if self.bullet_speed <= 200:
                self.bullet_speed += 5
                if self.bullet_speed == 200:
                    self.bullet_speed = 0
            if self.ultimate_x_speed <= 300:
                self.ultimate_x_speed += 10
                if self.ultimate_x_speed == 300:
                    self.ultimate_x_speed = 0
        sword_rect = pygame.Rect(side, self.rect.centery - 10, self.rect.width * 2, 20)
        bullet_rect = pygame.Rect(bullet_side + bullet_speed, self.rect.centery - 10, 30, 10)
        ultimate = pygame.image.load('ultimate.png').convert_alpha()
        ultimate1 = pygame.transform.rotate(ultimate, angle)
        ultimate_rect = ultimate1.get_rect(center=(self.rect.centerx + self.ultimate_x_speed,
                                                   self.rect.centery + self.ultimate_y_speed - 500))
        attack_rect = pygame.Rect(side, self.rect.y, self.rect.width * 1.5, self.rect.height)
        if self.attack_type == 1:
            attack_rect = sword_rect
            pygame.draw.rect(surface, (0, 0, 0), sword_rect)
        if self.attack_type == 2:
            pygame.draw.rect(surface, (0, 0, 0), bullet_rect)
            attack_rect = bullet_rect
        if self.attack_type == 3:
            screen.blit(ultimate1, ultimate_rect)
            attack_rect = ultimate_rect
        if attack_rect.colliderect(target.rect) and not self.has_attacked:
            if target.health >= 0:
                if self.attack_type == 1:
                    target.health -= 10
                if self.attack_type == 2:
                    target.health -= 5
                if self.attack_type == 3:
                    target.health -= 30
            self.has_attacked = True
            self.attack_cooldown = 10

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


adventurer_1 = Player(50, 340, 1, (255, 0, 0))
adventurer_2 = Player(600, 340, 2, (0, 0, 255))


def draw_mana(mana, x, y):
    ratio = mana / 100
    pygame.draw.rect(screen, (255, 255, 0), (x - 5, y - 3, 110, 26))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 20))
    pygame.draw.rect(screen, (150, 25, 78), (x, y, 100 * ratio, 20))


def draw_health_bar(health, x, y):
    ratio = health / 500
    pygame.draw.rect(screen, (255, 255, 255), (x - 5, y - 3, 210, 36))
    pygame.draw.rect(screen, (119, 252, 3), (x, y, 200, 30))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200 * ratio, 30))


def draw_bg():
    for x in range(15):
        speed = 1
        for t in bg_images:
            screen.blit(t, ((x * bg_width) - scroll * speed, 0))
            speed += 0.1


def draw_ground():
    for x in range(15):
        screen.blit(ground_img, ((x * ground_width) - scroll * 2, SCREEN_HEIGHT - ground_height/2))


while True:
    clock.tick(FPS)
    draw_bg()
    draw_ground()
    adventurer_1.draw(screen)
    adventurer_2.draw(screen)
    adventurer_1.move(screen, adventurer_2)
    adventurer_2.move(screen, adventurer_1)
    adventurer_1.update_cooldown()
    adventurer_2.update_cooldown()
    draw_health_bar(adventurer_1.health, 20, 20)
    draw_health_bar(adventurer_2.health, 580, 20)
    draw_mana(adventurer_1.mana, 20, 55)
    draw_mana(adventurer_2.mana, 680, 55)
    key = pygame.key.get_pressed()
    if 0 <= scroll < 5000 and not scroll_limit:
        scroll += 5
        if scroll >= 4955:
            scroll_limit = True
    if scroll_limit:
        scroll -= 5
        if scroll <= 0:
            scroll_limit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    pygame.display.update()
