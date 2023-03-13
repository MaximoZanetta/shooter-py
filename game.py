import pygame, random


#setting of width, height and colors
WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)


#initializing pygame, screen , clock and music
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

#function for draw text on the screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)



#function for draw the shield bar on the top left
def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)
 

#class of the player with function update(for the movement) and shoot(for shoot lasers...)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10 
        self.speed_x = 0
        self.shield = 100
        
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites_list.add(bullet)
        bullets.add(bullet)
        laser_sound.play()


#class meteor with function udpate(create random meteors in random positions)
class Meteor(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__() 
        self.image = random.choice(meteor_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speed_y = random.randrange(1, 10)
        self.speed_x = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speed_y = random.randrange(1, 10)


#class bullet, centering the laser with the player center
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.bottom < 0:
            self.kill()


#class explosion for create the differents explosion when a laser hit the meteor
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


#function of game over screen
def show_go_screen():
    screen.blit(background, [0,0])
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instructions", 27, WIDTH // 2, HEIGHT //2)
    draw_text(screen, "Press key to start...", 20, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True 
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#differents meteor images
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert_alpha())


#for lop for the explosion images
explosion_anim = []
for i in range(9):
    file = f"assets/regularExplosion0{i}.png"
    img = pygame.image.load(file).convert_alpha()
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

#setting the background image
background = pygame.image.load("assets/background.png").convert_alpha()

#laser sound, explosion sound and music
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/assets_explosion.wav")
pygame.mixer.music.load("assets/assets_music.ogg")
pygame.mixer.music.set_volume(0.2)


pygame.mixer.music.play(loops=-1)
game_over = True
running = True

#main loop
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites_list = pygame.sprite.Group() 
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites_list.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites_list.add(meteor) 
            meteor_list.add(meteor)

        score = 0



    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites_list.update()

    #laser-meteor collide
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 1
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites_list.add(explosion)
        meteor = Meteor()
        all_sprites_list.add(meteor)
        meteor_list.add(meteor)

    # player-meteoro collide
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    if hits:
        player.shield -= 25
        print(player.shield)
        if player.shield == 0:
            game_over = True

    
    screen.blit(background, [0,0])

    all_sprites_list.draw(screen)

    draw_text(screen, str(score), 25, WIDTH // 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
  
    pygame.display.flip()
 
pygame.quit()