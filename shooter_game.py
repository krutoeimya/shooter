from pygame import *
from random import *
from time import time as timer
win_width = 700
win_hight = 500
bck = 'galaxy.jpg'
pl = "bullet.png"
en = 'rocket.png'
bul = 'asteroid.png'
ast = 'ufo.png'
font.init()
font1 = font.SysFont('Arial', 70)
win = font1.render('YOU WIN!',True,(255,215,0))
lose = font1.render('YOU LOSE!',True,(180,0,0))
font2 = font.SysFont('Arial',36)
lost = 0
score = 0
goal = 20
max_lost = 3
life = 3
display.set_caption('Стрелялка')
window = display.set_mode((win_width, win_hight))
bg = transform.scale(image.load(bck),(win_width, win_hight))

class GameSprite(sprite.Sprite):
    def __init__ (self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -=self.speed
        if keys_pressed[K_d] and self.rect.x < win_width-80:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet(bul, self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost = lost +1
class Enemyy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(en,randint(80,win_width-80,),-40,80,50,randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemyy(ast,randint(30,win_width-30,),-40,80,50,randint(1,7))
    asteroids.add(asteroid)
bullets = sprite.Group()
ship = Player(pl,5,win_hight - 100,80,100,10)
finish = False
run = True
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<10 and rel_time == False:
                    num_fire += 1
                    print(num_fire)
                    ship.fire()
                if num_fire>=10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(bg,(0,0))
        if score >=goal:
            finish = True
            window.blit(win,(200,200))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        asteroids.update()
        monsters.draw(window)
        bullets.draw(window) 
        asteroids.draw(window)
        if rel_time ==True:
            now_time = timer( )
            if now_time -last_time<2:
                reload = font2.render('Падажде, барашка домой зашёл',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets,True,True)
        for c in collides:
            score = score +1
            monster = Enemy(en,randint(80,win_width-80,),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
                sprite.spritecollide(ship,monsters,True)
                sprite.spritecollide(ship,asteroids,True)
                life = life -1
        if life ==0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        text = font2.render('Счёт:'+str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lost = font2.render('Пропущено:'+str(lost),1,(255,255,255))
        window.blit(text_lost,(10,50))
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (0,0,150)
        if life == 1:
            life_color = (150,0,0)
        text_life = font1.render(str(life),1,life_color)
        window.blit(text_life,(650,10))
        display.update()
    time.delay(40)
