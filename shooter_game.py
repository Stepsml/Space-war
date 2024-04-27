#Создай собственный Шутер!
from time import time as timer
from random import randint
from pygame import *
win_width = 1000
win_height = 700
window = display.set_mode((win_width,win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))
img_enemy = 'StarDestroer.png'
img_bullet = 'cat.png'
img_asteroid = 'asteroid.png'

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (10,255,100))
lose = font1.render('YOU LOSE!', True,(255,100,100))

score = 0
goal = 10
lost = 0
max_lost = 3
life = 3

game = True
finish = False
clock = time.Clock()
FPS = 60


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed     
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top,50,70,-10)
        Bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            

    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player("rocket.png", 5 , win_height - 100, 80, 100, 5)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

Asteroids = sprite.Group() 
for i in range(1,3):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1,7))
    Asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('Sound_16300.mp3')

font.init()
font2 = font.SysFont('Arial', 36)

space = mixer.Sound('fire.ogg')

Bullets = sprite.Group()

finish = False

rel_time = False
num_fire = 0

game = True


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                    if num_fire >= 5 and rel_time == False:

                        last_time = timer()
                        rel_time = True

     
    if not finish:
        window.blit(background,(0,0))

        text = font2.render('Счёт:'+ str(score),1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        ship.update()
        ship.reset()

        monsters.draw(window)
        monsters.update()

        Asteroids.draw(window)
        Asteroids.update()

        Bullets.update()
        Bullets.draw(window)
        
        collides = sprite.groupcollide(monsters, Bullets , True, True)
        for i in collides:
            score = score +1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50,randint(1,3))
            monsters.add(monster)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time <3:
                reload = font2.render('Wait, reload...',1,(150,0,0))
                window.blit(reload,(400,650))
            else:
                num_fire = 0
                rel_time = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship,Asteroids, False):
            sprite.spritecollide(ship, monsters,True)
            sprite.spritecollide(ship,Asteroids,True)
            life = life -1

            finish = True
            window.blit(lose,(200,200))

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        if life == 3:
            life_color = (70,250,70)
        if life == 2:
            life_color = (170,0,20)
        if life == 1:
            life_color = (250,40,40)

        text_life = font1.render(str(life),1, life_color)
        window.blit(text_life,(650,10))


    display.update()
    clock.tick(FPS)







#pygame.sprite.Sprite.add()




















































































































































